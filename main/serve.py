import os
import sys
import json
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ConversationHandler
from telegram.request import HTTPXRequest

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

sys.path.append(os.path.dirname(__file__))

MAIN_MENU, SIMULATION_ACTIVE, WAITING_CHOICE, SCENARIO_SELECT = range(4)

def main():
    print("🚀 Запуск бота...")
    
    os.makedirs('data', exist_ok=True)
    
    if not os.path.exists('data/users.json'):
        with open('data/users.json', 'w', encoding='utf-8') as f:
            json.dump({"users": {}}, f)
        print("✅ Создан users.json")
    
    try:
        import database
        import generator
        import bot_handlers
        print("✅ Модули загружены")
    except ImportError as e:
        print(f"❌ Ошибка импорта: {e}")
        return
    
    try:
        data_storage = database.DataStorage('data/users.json')
        scenario_gen = generator.ScenarioGenerator('data/content_bank.json')
        bot = bot_handlers.EvolutionBot(data_storage, scenario_gen)
        print("✅ Классы инициализированы")
    except Exception as e:
        print(f"❌ Ошибка инициализации: {e}")
        return
    
    TOKEN = "8523833913:AAHktN6-MBu_aq2x2mWL3OZWlUdd5VnbXkg"
    
    request = HTTPXRequest(
        connection_pool_size=10,
        connect_timeout=30.0,
        read_timeout=30.0,
        write_timeout=30.0,
        pool_timeout=30.0
    )
    
    application = Application.builder().token(TOKEN).request(request).build()
    
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
            SCENARIO_SELECT: [
                CallbackQueryHandler(bot.button_handler)
            ],
        },
        fallbacks=[CommandHandler('start', bot.start)]
    )
    
    application.add_handler(conv_handler)
    
    print("✅ Бот готов!")
    print(f"📊 Сценариев: {scenario_gen.get_scenario_count()}")
    print("\n▶️ Запуск polling...")
    print("Нажмите Ctrl+C для остановки")
    
    application.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Бот остановлен")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
