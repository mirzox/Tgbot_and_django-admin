from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from .models import FoodType, Food


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


def generate_food_type():
    foodtypes = FoodType.objects.all().values('text', 'calldata')
    print(foodtypes)
    items = [[InlineKeyboardButton(text=i['text'], callback_data=i['calldata'])] for i in foodtypes]
    return InlineKeyboardMarkup(items)


def generate_food(data):
    foods = Food.objects.get(type=data).values('text', 'calldata')
    items = [[InlineKeyboardButton(text=i['text'], callback_data=i['calldata'])] for i in foods]
    items.append([InlineKeyboardButton(text="⬅Назад", callback_data="back")])
    return InlineKeyboardMarkup(items)
    # if data == 'lavash':
    #     items = []
    #
    # elif data == 'burger':
    #     items = [
    #         [
    #             InlineKeyboardButton('Burger', callback_data='food_burger'),
    #             InlineKeyboardButton('Chiz burger', callback_data='food_chizburger')
    #         ],
    #         [
    #             InlineKeyboardButton('Big burger', callback_data='food_big_burger'),
    #             InlineKeyboardButton('Big chiz', callback_data='food_big_chiz')
    #         ],
    #         [
    #             InlineKeyboardButton(text="⬅Назад", callback_data="back")
    #         ]
    #     ]
    # else:
    #     pass
    # return InlineKeyboardMarkup(inline_keyboard=items)


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
    items += [
        [
            InlineKeyboardButton(text='0', callback_data='0'),
            InlineKeyboardButton(text="Удалить", callback_data='delete')
        ],
        [
            InlineKeyboardButton(text="⬅ Назад", callback_data="bc_to_food")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=items)