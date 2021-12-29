from django.core.management.base import BaseCommand
from django.conf import settings

from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackQueryHandler
)

from ...const import TOKEN
from ...functions import (
    start, take_contact,
    language_chosen,
    food_type_chosen,
    food_chosen,
    back_button,
    quantity_chosen,
    continue_order,
    finish_order,
    delete_item_from_cart,
    order_finished,
    get_location,
    check_location,
    send_food_type
)
from ...models import FoodType, Food


class Command(BaseCommand):
    help = "Delivery bot"

    def handle(self, *args, **options):
        updater = Updater(TOKEN)
        dp = updater.dispatcher

        dp.add_handler(CommandHandler('start', start))
        dp.add_handler(CommandHandler('start_order', send_food_type))
        dp.add_handler(MessageHandler(Filters.contact, take_contact))
        dp.add_handler(MessageHandler(Filters.location, get_location))
        dp.add_handler(CallbackQueryHandler(pattern='back', callback=back_button))
        dp.add_handler(CallbackQueryHandler(pattern='next', callback=continue_order))
        dp.add_handler(CallbackQueryHandler(pattern='finish_order', callback=finish_order))
        dp.add_handler(CallbackQueryHandler(pattern='order_finished', callback=order_finished))

        for i in ['yes', 'no']:
            dp.add_handler(CallbackQueryHandler(pattern=i, callback=check_location))

        for i in ['ru', 'uz']:
            dp.add_handler(CallbackQueryHandler(pattern=i, callback=language_chosen))

        for i in FoodType.objects.all().values('calldata'):
            dp.add_handler(CallbackQueryHandler(pattern=i['calldata'], callback=food_type_chosen))

        for i in Food.objects.all().values('calldata'):
            dp.add_handler(CallbackQueryHandler(pattern=i['calldata'], callback=food_chosen))

        for j in range(1, 10):
            dp.add_handler(CallbackQueryHandler(pattern=str(j), callback=quantity_chosen))

        for k in Food.objects.all().values('calldata'):
            dp.add_handler(CallbackQueryHandler(pattern=f"delete_{k['calldata']}", callback=delete_item_from_cart))

        updater.start_polling()
        updater.idle()
