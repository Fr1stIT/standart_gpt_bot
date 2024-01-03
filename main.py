import asyncio
from aiogram import Bot, Dispatcher, F, types
import  openai
from aiogram.types import Message
from conf import bot_api, openai_api_key

openai.api_key  = openai_api_key
bot = Bot(token=bot_api)
dp = Dispatcher()
async def main():
    await dp.start_polling(bot)

messages = []




@dp.message(F.data == '/start')
async  def start_command (message: types.Message):
    await  message.answer(text = "Бот с ChatGPT приветствуюет тебя!")


@dp.message(F.content_type.in_({'text'}))
async def message_handler(message: Message):
    user_id = message.chat.id
    user_message = message.text

    # Добавляем сообщение пользователя в список сообщений
    messages.append({"role": "user", "content": message.text})

    # Получаем ответ от ChatGPT
    chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    reply = chat.choices[0].message.content

    # Отправляем ответ пользователю
    if len(reply) > 4096:
        for x in range(0, len(reply), 4096):
            await bot.send_message(message.chat.id, reply[x:x + 4096])
    else:
        await bot.send_message(message.chat.id, reply)

    # Добавляем ответ ChatGPT в список сообщений
    messages.append({"role": "assistant", "content": reply})


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    asyncio.run(main())