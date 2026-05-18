database.py - работа с пользователями (загрузка, сохранение, данные игрока)

generator.py - логика сценариев и популяции (этапы, выборы, параметры)

bot_handlers.py - обработка команд и кнопок, игровой процесс

serve.py - запуск бота (подключение к Telegram API)

data/users.json - база пользователей (создается автоматически)

data/content_bank.json - файл со сценариями
Запуск:
pip install python-telegram-bot==21.10
python create_final_bank.py
python serve.py

Токен бота в serve.py
