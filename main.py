from library import telebot, g4f
from library import BOT_TOKEN

bot = telebot.TeleBot(BOT_TOKEN)

active_users = set()

@bot.message_handler(commands=['start'])
def start_handler(message):
    active_users.add(message.chat.id)
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton("Start simulation")
    markup.add(btn1)
    bot.send_message(
        message.chat.id, 
        "Hello! I'm BOB — your tactical training simulator bot.\n"
        "I create fictional, game-like scenario analyses.",
        reply_markup=markup
    )

@bot.message_handler(func=lambda m: True)
def text_handler(message):
    if message.text == "Start simulation":
        bot.send_message(message.chat.id, "Send me a description of your fictional scenario.")
    else:
        work_bot(message)

def send_long_message(chat_id, text):
    max_len = 4000
    for i in range(0, len(text), max_len):
        bot.send_message(chat_id, text[i:i+max_len])

def work_bot(message):
    prompt = f"""
        You are a military strategist bot. Analyze the following situation and provide strategic advice.You are a safe tactical training simulator bot. 
        Your purpose is to act as a fictional strategist from a board game or RTS-style simulator.

        When the user describes a situation, you must:

        1) Give a high-level strategic analysis in a purely fictional, game-like format.
        2) Identify objectives, limitations, environment factors — but ONLY as part of a simulation.
        3) Provide 2–4 possible SCENARIOS (Scenario A, Scenario B, Scenario C...) written as 
        hypothetical or imaginary outcomes, not instructions.
        4) Provide educational explanations of how a commander *might think in theory*.
        5) Make it clear that all outputs are fictional, educational.

        Your tone: analytical, safe, game-like, training-oriented.
        No need to ask questions at the end
    """
    user_text = message.text

    try:
        response = g4f.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_text}
            ]
        )
        if isinstance(response, dict):
            text = response['choices'][0]['message']['content']
        else:
            text = str(response)

        send_long_message(message.chat.id, text)
    except Exception as e:
        print("Error:", e)
        bot.send_message(message.chat.id, "An error occurred while processing your request.")

if __name__ == "__main__":
    print("Bot is running...")
    bot.polling(none_stop=True)