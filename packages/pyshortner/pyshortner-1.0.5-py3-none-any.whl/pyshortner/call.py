from pyrogram import *
from pyrogram.errors import *
from pyrogram.types import *
import requests
from config import *



shortner_link = WebAppInfo(url=f"https://{SHORTNER_LINK}/member/tools/api?bot=true")



START_MESSAGE_REPLY_MARKUP  = InlineKeyboardMarkup([
    [
        InlineKeyboardButton('📢 Channel', url=f'{CHANNEL_LINK}'),
        InlineKeyboardButton('📕 About', callback_data='about_dkbotz')
    ],
    [
        InlineKeyboardButton('💵 Balance', callback_data='dkbotz_balance')
    ],
    [
        InlineKeyboardButton('📙 Help', callback_data='help_dkbotz'),
        InlineKeyboardButton('⚙️ Settings', callback_data='dkbotz_settings')
    ],
    [
        InlineKeyboardButton('📡 Connect To Bot', web_app=shortner_link)
    ],
    [
        InlineKeyboardButton('🏞️ Switch To Old Panel 🏞️', callback_data='old_btn_dkbotz')
    ]
])

OLD_START_MESSAGE_REPLY_MARKUP  = InlineKeyboardMarkup([
    [
        InlineKeyboardButton('📢 Channel', url=f'{CHANNEL_LINK}'),
        InlineKeyboardButton('📕 About', callback_data='about_dkbotz')
    ],
    [
        InlineKeyboardButton('💵 Balance', callback_data='dkbotz_balance')
    ],
    [
        InlineKeyboardButton('📙 Help', callback_data='help_dkbotz'),
        InlineKeyboardButton('⚙️ Settings', callback_data='dkbotz_settings')
    ],
    [
        InlineKeyboardButton('📡 Connect To Bot', url=f"https://{SHORTNER_LINK}/member/tools/api?bot=true")
    ],
    [
        InlineKeyboardButton('🏞️ Switch To New Panel 🏞️', callback_data='new_btn_dkbotz')
    ]
])



@Client.on_callback_query(filters.regex(r"^dkbotz_balance"))
async def shortner_balance(c:Client,m: CallbackQuery):
    try:
        user = await get_user(m.from_user.id)
        API = user["shortener_api"]
        URL = user["base_site"]
        vld = await user_api_check(user)
        if vld is not True:
            return await m.answer(f"Add API Key", show_alert=True)
        resp = requests.get(f'https://{URL}/api?api={API}').json()
        if resp['status'] == 1:
            username = resp['username']
            pbalance = resp['publisher_earnings']
            rbalance = resp['referral_earnings']
            tbalance = resp['total_earnings']
            await m.answer(BALANCE_TEXT.format(username=username, pbalance=pbalance, rbalance=rbalance, tbalance=tbalance), show_alert=True)
        if resp['status'] == 2:  
            await m.answer(f"Your Account in Pending", show_alert=True)
        if resp['status'] == 3:
            await m.answer(f"Your Account is Banned", show_alert=True)
    except Exception as e:
        await m.answer(e, show_alert=True)
