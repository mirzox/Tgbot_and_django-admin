from telegram import ChatAction

from .models import TgUser, Order, FoodType, Food
from . import messages as msg
from . import markups as mrk
from .messages import translates
from .utils import request


def start(update, context):
    user_id = update.message.chat.id
    firstname = update.message.chat.first_name
    username = update.message.chat.username
    user, created = TgUser.objects.get_or_create(
        chat_id=user_id,
    )
    if created:
        user.firstname = firstname
        user.username = username
        user.stage = 1
        user.save()
        context.bot.send_message(
            chat_id=user_id,
            text=msg.start_msg,
            reply_markup=mrk.choose_lang()
        )
    else:
        print(user)


def language_chosen(update, context):
    user_id = update.callback_query.message.chat.id
    msg_id = update.callback_query.message.message_id
    data = update.callback_query.data
    user = TgUser.objects.get(chat_id=user_id)
    user.language = data
    user.save()
    context.bot.edit_message_text(
        chat_id=user_id,
        message_id=msg_id,
        text=translates[data]['lang_chosen'],
        reply_markup=None
    )
    if user.stage == 1:
        user.stage = 2
        user.save()
        context.bot.send_message(
            chat_id=user_id,
            text=translates[data]['send_contact'],
            reply_markup=mrk.send_contact(data)
        )


def take_contact(update, context):
    user_id = update.message.chat.id
    phone_num = update.message.contact.phone_number
    if len(phone_num) == 13:
        phone_num = phone_num[1:]
    user = TgUser.objects.get(chat_id=user_id)
    user.phone = phone_num
    user.save()
    if user.stage == 2:
        user.stage = 3
        user.save()
        send_food_type(update, context)


def send_food_type(update, context):
    user_id = update.message.chat.id
    user = TgUser.objects.get(chat_id=user_id)
    order = Order(chat_id=user)
    order.save()
    user.stage = 4
    user.save()
    context.bot.send_message(
        chat_id=user_id,
        text=translates[user.language]['contact_chosen'],
        reply_markup=mrk.generate_food_type()
    )


def food_type_chosen(update, context):
    user_id = update.callback_query.message.chat.id
    msg_id = update.callback_query.message.message_id
    data = update.callback_query.data
    user = TgUser.objects.get(chat_id=user_id)
    user.stage = 5
    user.save()
    foodtype = FoodType.objects.get(calldata=data)
    order = Order.objects.filter(chat_id=user_id, status='in progress').update(
        type=foodtype
    )
    context.bot.edit_message_text(
        chat_id=user_id,
        message_id=msg_id,
        text=f"{translates[user.language]['food_type_chosen']}{data}",
        reply_markup=mrk.generate_food(data)
    )


def food_chosen(update, context):
    user_id = update.callback_query.message.chat.id
    msg_id = update.callback_query.message.message_id
    user = TgUser.objects.get(chat_id=user_id)
    data = update.callback_query.data
    food = Food.objects.get(calldata=data)
    order = Order.objects.get(chat_id=user, status='in progress')
    order.food = food
    user.stage = 6
    order.save()
    user.save()
    context.bot.edit_message_text(
        chat_id=user_id,
        message_id=msg_id,
        text=translates[user.language]['food_chosen'],
        reply_markup=mrk.quantity_for_food()
    )


def back_button(update, context):
    user_id = update.callback_query.message.chat.id
    msg_id = update.callback_query.message.message_id
    user = TgUser.objects.get(chat_id=user_id)
    if user.stage == 5:
        context.bot.edit_message_text(
            chat_id=user_id,
            message_id=msg_id,
            text=translates[user.language]['contact_chosen'],
            reply_markup=mrk.generate_food_type()
        )
    elif user.stage == 6:
        order = Order.objects.get(chat_id=user_id, status='in progress')
        user.stage = 5
        user.save()
        context.bot.edit_message_text(
            chat_id=user_id,
            message_id=msg_id,
            text=translates[user.language]['food_type_chosen'],
            reply_markup=mrk.generate_food(order.type)
        )


def quantity_chosen(update, context):
    user_id = update.callback_query.message.chat.id
    msg_id = update.callback_query.message.message_id
    data = update.callback_query.data
    user = TgUser.objects.get(chat_id=user_id)
    order = Order.objects.get(chat_id=user_id, status='in progress')
    order.quantity = int(data)
    order.save()
    user.stage = 7
    user.save()
    context.bot.edit_message_text(
        chat_id=user_id,
        message_id=msg_id,
        text=translates[user.language]['quantity_chosen'],
        reply_markup=mrk.quantity_chosen_mrk(user.language)
    )


def continue_order(update, context):
    user_id = update.callback_query.message.chat.id
    msg_id = update.callback_query.message.message_id
    user = TgUser.objects.get(chat_id=user_id)
    order = Order.objects.get(chat_id=user_id, status='in progress')
    order.status = 'in cart'
    order.save()
    order = Order(chat_id=user)
    order.save()
    user.stage = 4
    user.save()
    context.bot.edit_message_text(
        chat_id=user_id,
        message_id=msg_id,
        text=translates[user.language]['contact_chosen'],
        reply_markup=mrk.generate_food_type()
    )


def finish_order(update, context):
    user_id = update.callback_query.message.chat.id
    msg_id = update.callback_query.message.message_id
    user = TgUser.objects.get(chat_id=user_id)
    order = Order.objects.get(chat_id=user_id, status='in progress')
    order.status = 'in cart'
    order.save()
    order = Order.objects.filter(chat_id=user_id, status='in cart')
    text = '\n\n'.join([f"{i.food.text} - {i.quantity} - {i.cost}" for i in order])
    user.stage = 8
    user.save()
    context.bot.edit_message_text(
        chat_id=user_id,
        message_id=msg_id,
        text=f"Корзина:\n{text}",
        reply_markup=mrk.delete_cart_items(order)
    )


def delete_item_from_cart(update, context):
    user_id = update.callback_query.message.chat.id
    msg_id = update.callback_query.message.message_id
    data = update.callback_query.data.replace('delete_', '', 1)
    del_order = Order.objects.get(chat_id=user_id, food__calldata=data, status='in cart')
    del_order.delete()
    order = Order.objects.filter(chat_id=user_id, status='in cart')
    user = TgUser.objects.get(chat_id=user_id)
    if order.count() == 0:
        user.stage = 4
        text = translates[user.language]['contact_chosen']
        new_order = Order(chat_id=user)
        new_order.save()
    else:
        user.stage = 9
        TgUser.objects.filter(chat_id=user_id).update(stage=9)
        temp = '\n\n'.join([f'{i.food.text} - {i.quantity} - {i.cost}' for i in order])
        text = f"Корзина:\n{temp}"
    user.save()
    context.bot.edit_message_text(
        chat_id=user_id,
        message_id=msg_id,
        text=text,
        reply_markup=mrk.delete_cart_items(order)
    )


def order_finished(update, context):
    user_id = update.callback_query.message.chat.id
    msg_id = update.callback_query.message.message_id
    user = TgUser.objects.get(chat_id=user_id)
    context.bot.edit_message_text(
        chat_id=user_id,
        message_id=msg_id,
        text="Спасибо за ваш заказ.😊",
        reply_markup=None
    )
    context.bot.send_message(
        chat_id=user_id,
        text="Нажнимате на кпонку ОТПРАВИТЬ ЛОКАЦИЮ чтоб мы знали куда доставить ваш заказ",
        reply_markup=mrk.send_location(user.language)
    )


def get_location(update, context):
    user_id = update.message.chat_id
    location = update.message.location
    lat = location['latitude']
    lon = location['longitude']
    text = msg.check_location.format(request(lat, lon))
    context.bot.send_message(
        chat_id=user_id,
        text="Ваша локация обрабатывается",
        reply_markup=mrk.remove()
    )
    context.bot.send_message(
        chat_id=user_id,
        text=text,
        reply_markup=mrk.check_location_markups()
    )


def check_location(update, context):
    user_id = update.callback_query.message.chat_id
    msg_id = update.callback_query.message.message_id
    data = update.callback_query.data
    if data == 'yes':
        Order.objects.filter(chat_id=user_id, status='in cart').update(status='finished')
        context.bot.edit_message_text(
            chat_id=user_id,
            message_id=msg_id,
            text='Спасибо что воспользовались нашим ботом\nЧтоб заново начать заказ нажмите на /start_order',
            reply_markup=None
        )
    else:
        pass
