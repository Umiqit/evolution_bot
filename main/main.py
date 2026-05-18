# main.ipynb

import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ConversationHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

from database import DataStorage, User, AchievementSystem
from generator import ScenarioGenerator
from bot_handlers import EvolutionBot, MAIN_MENU, SIMULATION_ACTIVE, WAITING_CHOICE

data_storage = DataStorage('../data/users.json')
scenario_generator = ScenarioGenerator('../data/content_bank.json')
bot = EvolutionBot(data_storage, scenario_generator)

TOKEN = "8523833913:AAHktN6-MBu_aq2x2mWL3OZWlUdd5VnbXkg"

def main():
    application = Application.builder().token(TOKEN).build()
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', bot.start)],
        states={
            MAIN_MENU: [
                CommandHandler('help', bot.help_command),
                CommandHandler('status', bot.status_command),
                CommandHandler('inventory', bot.inventory_command),
                CommandHandler('next', bot.next_command),
                CallbackQueryHandler(bot.button_handler)
            ],
            SIMULATION_ACTIVE: [
                CommandHandler('status', bot.status_command),
                CommandHandler('inventory', bot.inventory_command),
                CommandHandler('next', bot.next_command),
                CallbackQueryHandler(bot.button_handler)
            ],
            WAITING_CHOICE: [
                CommandHandler('status', bot.status_command),
                CommandHandler('inventory', bot.inventory_command),
                CallbackQueryHandler(bot.button_handler)
            ],
        },
        fallbacks=[CommandHandler('start', bot.start)]
    )
    
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler('help', bot.help_command))
    application.add_handler(CommandHandler('status', bot.status_command))
    application.add_handler(CommandHandler('inventory', bot.inventory_command))
    application.add_handler(CommandHandler('next', bot.next_command))
    
    print("Бот запущен...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
