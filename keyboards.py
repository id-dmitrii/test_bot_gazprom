from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

# ----- Start menu keyboard ------#

i_start_kb = InlineKeyboardMarkup()
ibt1 = InlineKeyboardButton(text='Enter name',
                            callback_data='name')
ibt2 = InlineKeyboardButton(text='Enter token',
                            callback_data='token')
i_start_kb.add(ibt1, ibt2)

# ----- auth menu keyboard ------#

auth_kb = InlineKeyboardMarkup(resize_keyboard=True)
auth_bt1 = InlineKeyboardButton(text='✅',
                                callback_data='okay')
auth_bt2 = InlineKeyboardButton('Back to main menu',
                                callback_data='start')
auth_kb.add(auth_bt1, auth_bt2)

# ----- categories list ------#

cat_kb = InlineKeyboardMarkup()
cat_bt1 = InlineKeyboardButton(text='MS Office',
                               callback_data='office')
cat_kb.add(cat_bt1)

# ----- ready keyboard ------#

ready_kb = InlineKeyboardMarkup()
rdy_bt1 = InlineKeyboardButton(text='Yes!',
                               callback_data='ready_yes')
rdy_bt2 = InlineKeyboardButton(text='Back to category',
                               callback_data='back_to_cat')
ready_kb.add(rdy_bt1, rdy_bt2)

# ----- last question keyboard ------#

last_quest_kb = InlineKeyboardMarkup()
last_quest_bt_1 = InlineKeyboardButton(text='Yes!',
                                       callback_data='last_quest_yes')
last_quest_bt_2 = InlineKeyboardButton(text='Back',
                                       callback_data='back')
last_quest_kb.add(last_quest_bt_1, last_quest_bt_2)