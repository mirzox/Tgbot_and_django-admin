from telegram import ChatAction

from .models import TgUser, Order, FoodType, Food
from . import messages as msg
from . import markups as mrk
from .messages import translates


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
    foodtype = FoodType.objects.get(calldata=data)
    print(foodtype)
    order = Order.objects.get(chat_id=user_id, status='in cart')
    print(type(foodtype))
    user.stage = 4
    order.type = foodtype
    order.save()
    user.save()
    context.bot.edit_message_text(
        chat_id=user_id,
        message_id=msg_id,
        text=f"{translates[user.language]['food_type_chosen']}{data}",
        reply_markup=mrk.generate_food(data)
    )
