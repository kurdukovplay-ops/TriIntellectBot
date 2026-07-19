import telebot
import requests
import time

TOKEN = "TOKEN"
AI_KEY = "API KEY"

bot = telebot.TeleBot(TOKEN)

MODELS = {
    "chat": "google/gemma-4-31b-it:free",
    "code": "openai/gpt-oss-20b:free",
    "think": "nvidia/nemotron-3-ultra-550b-a55b:free"
}

user_mode = {}

def send_typing(chat_id):
    bot.send_chat_action(chat_id, 'typing')

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    user_mode[user_id] = "chat"
    text = """🧠 Добро пожаловать в TriIntellectBot!

Три интеллекта в одном боте:

🤖 /chat — режим общения (Gemma 4)
💻 /code — режим программирования (GPT-OSS)  
🧠 /think — режим сложных задач (Nemotron)

Выбери режим и задавай вопрос!
📋 /help — все команды
📊 /models — список моделей"""
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['chat', 'code', 'think'])
def set_mode(message):
    user_id = message.chat.id
    mode = message.text.replace('/', '')
    if mode in MODELS:
        user_mode[user_id] = mode
        bot.send_message(message.chat.id, f"✅ Режим {mode} включен! Задавай вопрос.")
    else:
        bot.send_message(message.chat.id, "❌ Неизвестный режим")

@bot.message_handler(func=lambda message: True)
def ask_ai(message):
    user_id = message.chat.id
    
    if user_id not in user_mode:
        user_mode[user_id] = "chat"
    
    mode = user_mode[user_id]
    
    send_typing(user_id)
    
    try:
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {AI_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://t.me/TriIntellectBot",
            "X-Title": "TriIntellectBot"
        }
        data = {
            "model": MODELS[mode],
            "messages": [
                {"role": "user", "content": message.text}
            ]
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        result = response.json()
        
        if 'choices' in result and len(result['choices']) > 0:
            answer = result['choices'][0]['message']['content']
            if len(answer) > 4000:
                answer = answer[:4000] + "..."
            bot.send_message(message.chat.id, answer)
        elif 'error' in result:
            bot.send_message(message.chat.id, f"❌ Ошибка API: {result['error'].get('message', 'Неизвестная ошибка')}")
        else:
            bot.send_message(message.chat.id, "❌ Неизвестный ответ от API. Попробуй другой режим.")
            
    except requests.exceptions.Timeout:
        bot.send_message(message.chat.id, "⏰ Превышено время ожидания. Попробуй еще раз.")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Ошибка: {e}")

@bot.message_handler(commands=['help'])
def help_command(message):
    text = """🧠 Команды TriIntellectBot:

/start — запустить бота
/chat — режим общения
/code — режим программирования
/think — режим сложных задач
/models — список моделей
/help — эта справка"""
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['models'])
def models_command(message):
    text = """🧠 Мои модели:

1. 🤖 Gemma 4 31B — общение, любые вопросы
2. 💻 GPT-OSS 20B — программирование, код
3. 🧠 Nemotron 3 Ultra 550B — аналитика, сложные задачи

Все модели бесплатные!"""
    bot.send_message(message.chat.id, text)

bot.polling()