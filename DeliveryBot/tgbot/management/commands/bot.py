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
)
from ...models import FoodType


class Command(BaseCommand):
    help = "Delivery bot"

    def handle(self, *args, **options):
        updater = Updater(TOKEN)
        dp = updater.dispatcher

        dp.add_handler(CommandHandler('start', start))
        dp.add_handler(MessageHandler(Filters.contact, take_contact))

        for i in ['ru', 'uz']:
            dp.add_handler(CallbackQueryHandler(pattern=i, callback=language_chosen))

        for i in FoodType.objects.all().values('calldata'):
            dp.add_handler(CallbackQueryHandler(pattern=i['calldata'], callback=food_type_chosen))
        updater.start_polling()
        updater.idle()
