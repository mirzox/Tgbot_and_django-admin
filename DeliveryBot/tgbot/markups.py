from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from .models import FoodType, Food


def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        for i in footer_buttons:
            menu.append([i])
    return menu


def choose_lang():
    items = [
        [
            InlineKeyboardButton(
                text="Русский 🇷🇺",
                callback_data="ru"),
            InlineKeyboardButton(
                text="O'zbek 🇺🇿",
                callback_data='uz'
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=items)


def send_contact(lang):
    if lang == 'ru':
        item = [
            [KeyboardButton("Отправить контакт", request_contact=True)]
        ]
    elif lang == 'uz':
        item = [
            [KeyboardButton("Raqamni jonatish", request_contact=True)]
        ]
    else:
        pass
    return ReplyKeyboardMarkup(item, resize_keyboard=True, one_time_keyboard=True)


def generate_food_type(cart=None):
    foodtypes = FoodType.objects.all().values('text', 'calldata')
    items = [InlineKeyboardButton(text=i['text'], callback_data=i['calldata']) for i in foodtypes]
    if cart is None:
        return InlineKeyboardMarkup(build_menu(items, 2))
    cart = [InlineKeyboardButton(text='Корзина', callback_data='cart')]
    return InlineKeyboardMarkup(build_menu(items, 2, footer_buttons=cart))


def generate_food(data):
    foods = Food.objects.filter(type=data).values('text', 'calldata')
    items = [InlineKeyboardButton(text=i['text'], callback_data=i['calldata']) for i in foods]
    footer = [InlineKeyboardButton(text="⬅Назад", callback_data="back")]
    return InlineKeyboardMarkup(build_menu(items, 2, footer_buttons=footer))


def quantity_for_food():
    items = []
    for i in range(1, 10, 3):
        items.append(
            [
                InlineKeyboardButton(text=str(i), callback_data=str(i)),
                InlineKeyboardButton(text=str(i+1), callback_data=str(i+1)),
                InlineKeyboardButton(text=str(i+2), callback_data=str(i+2))
            ]
        )
    items.append([InlineKeyboardButton(text="⬅ Назад", callback_data="back")])
    return InlineKeyboardMarkup(inline_keyboard=items)


def quantity_chosen_mrk(lang):
    if lang == 'ru':
        items = [
            [
                InlineKeyboardButton(text='Оформить заказ😊', callback_data='finish_order'),
                InlineKeyboardButton(text='Далее >>', callback_data='next')
             ]
        ]

    elif lang == 'uz':
        items = [
            [
                InlineKeyboardButton(text='Buyurtmani davometirish😊', callback_data='finish_order'),
                InlineKeyboardButton(text='Dalee >>', callback_data='next')
             ]
        ]
    else:
        items = []
    return InlineKeyboardMarkup(items)