# TriIntellectBot 🧠

Telegram-бот с тремя ИИ-моделями в одном интерфейсе.

## Модели

| Режим | Модель | Назначение |
|-------|--------|------------|
| `/chat` | Google Gemma 4 31B | Общение, любые вопросы |
| `/code` | OpenAI GPT-OSS 20B | Программирование, код |
| `/think` | NVIDIA Nemotron 3 Ultra 550B | Сложные задачи, аналитика |

## Команды
- `/start` — запуск бота
- `/chat` — режим общения
- `/code` — режим программирования
- `/think` — режим сложных задач
- `/models` — список моделей
- `/help` — справка

## Технологии
- Python 3
- pyTelegramBotAPI
- OpenRouter API
- Google Gemma 4
- OpenAI GPT-OSS
- NVIDIA Nemotron 3

## Установка и запуск

```bash
pip install pyTelegramBotAPI requests
python triintellectbot.py
