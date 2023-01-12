from aiogram import Bot, Dispatcher, executor, types
from bot_config import BOT_TOKEN, HELP_CMD
from keyboards import i_start_kb, auth_kb, cat_kb, ready_kb, last_quest_kb
from aiogram.dispatcher.filters import Text
from ms_office_questions import mso_quest, mso_answers
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot)
number = 0
user_answers = {}


async def on_startup(_):
    print('Start working')


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer(text='Hi there! This is a test bot!',
                         reply_markup=i_start_kb,
                         parse_mode='html')


@dp.message_handler(commands=['help'])
async def cmd_help(message: types.Message):
    await message.answer(text=HELP_CMD,
                         parse_mode='html')
    await message.delete()


@dp.message_handler(content_types=['text'])
async def check_name_token(message: types.Message):
    text = message.text
    if tmp == 'name':
        await message.answer(text=f'Your name is {text}?',
                             reply_markup=auth_kb)
    elif tmp == 'token':
        await message.answer(text=f'Your token is {text}?',
                             reply_markup=auth_kb)


@dp.callback_query_handler(text=['name', 'token'])
async def auth(callback: types.CallbackQuery):
    global tmp
    if callback.data == 'name':
        tmp = 'name'
        await callback.message.answer(text='Enter name like in the example:\n'
                                           '<i>Ivanov Ivan</i>',
                                      parse_mode='html')
        await callback.message.delete()
        await callback.answer()

    elif callback.data == 'token':
        tmp = 'token'
        await callback.message.answer(text='Enter your token')
        await callback.message.delete()
        await callback.answer()


@dp.callback_query_handler(text=['start', 'okay'])
async def auth_step_2(callback: types.CallbackQuery):
    if callback.data == 'okay':
        await callback.message.edit_text(text='Choose one of this category',
                                        reply_markup=cat_kb)
        await callback.answer()

    elif callback.data == 'start':
        await callback.message.edit_text(text='Welcome to menu!',
                                         reply_markup=i_start_kb)
        await callback.answer()


@dp.callback_query_handler(text=['office'])
async def office_quest(callback: types.CallbackQuery):
    if callback.data == 'office':
        await callback.message.edit_text(text='Are you ready for the test?',
                                      reply_markup=ready_kb)
        await callback.answer()


@dp.callback_query_handler(text=['ready_yes', 'back_to_cat', '1', '2', '3', '4'])
async def office_quest(callback: types.CallbackQuery):
    global number
    if callback.data == 'ready_yes':
        number = 0
        quest = mso_quest[str(number)]['quest']
        variants = mso_quest[str(number)]['variants']

        ikb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(variants[0], callback_data='1'), InlineKeyboardButton(variants[1], callback_data='2')],
            [InlineKeyboardButton(variants[2], callback_data='3'), InlineKeyboardButton(variants[3], callback_data='4')]
        ])

        await callback.message.edit_text(text=quest, reply_markup=ikb)

    elif callback.data in ['1', '2', '3', '4']:
        if number < int(max(list(mso_quest.keys()))):
            user_answers[number] = callback.data
            number += 1
            quest = mso_quest[str(number)]['quest']
            variants = mso_quest[str(number)]['variants']

            ikb = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(variants[0], callback_data='1'), InlineKeyboardButton(variants[1], callback_data='2')],
                [InlineKeyboardButton(variants[2], callback_data='3'), InlineKeyboardButton(variants[3], callback_data='4')]
            ])
            await callback.message.edit_text(text=quest, reply_markup=ikb)

        elif number == int(max(list(mso_quest.keys()))):
            user_answers[number] = callback.data
            await callback.message.edit_text(text='Do you want to end the test?', reply_markup=last_quest_kb)

    elif callback.data == 'back_to_cat':
        await callback.message.edit_text(text='Choose one of this category',
                                         reply_markup=cat_kb)


@dp.callback_query_handler(text=['last_quest_yes'])
async def end_of_test(callback: types.CallbackQuery):
    correct_answers = 0
    if callback.data == 'last_quest_yes':
        for key, value in user_answers.items():
            if mso_answers[key] == value:
                correct_answers += 1
        await callback.message.edit_text(text=f'You result is {correct_answers}/{len(mso_answers)}')


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp,
                           skip_updates=True,
                           on_startup=on_startup)
