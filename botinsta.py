import requests 
import telebot 
from telebot import types
import requests
from uuid import uuid4
import random
import os
import json
from user_agent import generate_user_agent
import sys
from datetime import datetime
from bs4 import BeautifulSoup
import datetime

# Token cố định thay vì nhập từ người dùng
tok = "7834807188:AAFtO6u6mJ-1EaDm4W4qA_cb4KgICqSo734"  # Thay YOUR_FIXED_TOKEN_HERE bằng token thực tế của bạn
zzk = 0
bot = telebot.TeleBot(tok)

@bot.message_handler(commands=['start'])
def start(message):
    global zzk
    zzk += 1
    nm = message.from_user.first_name
    id2 = message.from_user.id
    userk = message.from_user.username
    zxu = datetime.datetime.now()
    tt = f'''
- Thành viên đang sử dụng bot👥… 
ـــــــــــــــــــــــــــــــــــــــ
Tên người dùng: {nm}
Username: @{userk}
ID người dùng: {id2}
Số thứ tự người dùng: {zzk}
Thời gian: {zxu}
ـــــــــــــــــــــــــــــــــــــــ
'''
    key = types.InlineKeyboardMarkup()
    bot.send_message(message.chat.id, f"<strong>{tt}</strong>", parse_mode="html", reply_markup=key)
    
    zin = types.InlineKeyboardButton(text="Báo cáo tự tử", callback_data='zn')
    zge = types.InlineKeyboardButton(text="Thù hận hoặc lời nói kích động", callback_data='zx')
    zon = types.InlineKeyboardButton(text="Thông tin gây hại hoặc giả mạo", callback_data='zo')
    zan = types.InlineKeyboardButton(text="Lừa đảo hoặc gian lận", callback_data='ze')
    
    fr = message.from_user.first_name
    maac = types.InlineKeyboardMarkup()
    maac.row_width = 2
    maac.add(zin, zge, zon, zan)
    bot.send_message(message.chat.id, f"<strong>Chào mừng bạn: | {fr} | đến với bot báo cáo TikTok thực tế. Để xem thông tin của bạn [ /info ]</strong>", parse_mode="html", reply_markup=maac)

@bot.callback_query_handler(func=lambda call: True)
def st(call):
    if call.data == "zn":
        nc1 = types.InlineKeyboardMarkup(row_width=2)
        MC = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Gửi số lượng báo cáo cần hoàn thành', reply_markup=nc1)
        bot.register_next_step_handler(MC, z1)
    
    elif call.data == "zo":
        nc1 = types.InlineKeyboardMarkup(row_width=2)
        MC = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Gửi số lượng báo cáo cần hoàn thành', reply_markup=nc1)
        bot.register_next_step_handler(MC, z3)

    elif call.data == "ze":
        nc1 = types.InlineKeyboardMarkup(row_width=2)
        MC = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Gửi số lượng báo cáo cần hoàn thành', reply_markup=nc1)
        bot.register_next_step_handler(MC, z4)    
    elif call.data == "zx":
        nc1 = types.InlineKeyboardMarkup(row_width=2)
        MC = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Gửi số lượng báo cáo cần hoàn thành', reply_markup=nc1)
        bot.register_next_step_handler(MC, z2)

def z1(message):
    try:
        sufi = int(message.text)
    except:
        key = types.InlineKeyboardMarkup()
        bot.send_message(message.chat.id, f"<strong>Bạn đã nhập giá trị sai…</strong>", parse_mode="html", reply_markup=key)
        return
    mw = bot.send_message(message.chat.id, 'Gửi username cần báo cáo:')
    bot.register_next_step_handler(mw, ass, sufi)

def ass(message, sufi):
    addd = 0
    b = message.chat.id
    user = message.text
    try:
        headers = {
            'Host': 'www.woodrowpoe.top',
            'Connection': 'keep-alive',
            'package': 'woodrowpoe.tik.realfans',
            'apptype': 'android',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 13; ANY-LX2 Build/HONORANY-L22CQ; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/124.0.6367.124 Mobile Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'idfa': '6160fb46-9862-4d44-95b9-b1911283231f',
            'Accept': 'application/json, text/plain, */*',
            'version': '1.1',
            'Origin': 'http://www.woodrowpoe.top',
            'X-Requested-With': 'woodrowpoe.tik.realfans',
            'Referer': 'http://www.woodrowpoe.top//',
            'Accept-Language': 'ar-IQ,ar;q=0.9,en-IQ;q=0.8,en-US;q=0.7,en;q=0.6',
        }
        data = {
            'username': user,
        }
        ress = requests.post('http://www.woodrowpoe.top/api/v1/tikTokGetUserProfileInfo', headers=headers, data=data).json()
        iiid = ress['data']['pk']
        bot.send_message(message.chat.id, f"<strong>Đã trích xuất ID người dùng thành công ✅\n📜 ID: {iiid}</strong>", parse_mode="html", reply_markup=types.InlineKeyboardMarkup())
    except:
        bot.send_message(message.chat.id, f"<strong>Username không đúng, vui lòng kiểm tra lại và thử lại</strong>", parse_mode="html", reply_markup=types.InlineKeyboardMarkup())
        return
    
    add = int(sufi)
    bot.send_message(message.chat.id, f"<strong>Đang gửi báo cáo, vui lòng chờ...</strong>", parse_mode="html", reply_markup=types.InlineKeyboardMarkup())
    for i in range(add):
        addd += 1
        cookies = {
            'odin_tt': '40c40ad4772022e96afc8c9e5ce6440a94936ed1bd537e7879ee88784cfe22fca0848fe32c54174d839784124b12b8c27d20352b659177c2f833576358d3c1579c239bd3c573702ec998bbcd2e1e8878',
        }
        headers = {
            'Host': 'api16-normal-c-alisg.tiktokv.com',
            'x-ss-req-ticket': '1719661750667',
            'x-tt-token': '034151afef2522b5e1c2add1168b0ca8db05a23b3056f1eed37d978de66524ba11681c8643b9fc579bc98e660ed51b1e4582cb1559e6188d3cf61df9d0e0aa45a337d96e167c5f6d764bd9f526fb9d46bf27572ff8fe1dc7e38b1aaeaec2f1340cac6-CkAyOGZkZjliNzgzNDQ5ZDVmMWE0Mzk5MTczZGZkYzg2NjdjOTU1MzMwMzI4ZDgyMmMxMjdhZjFlYjM5OThiNzQ4-2.0.0',
            'sdk-version': '1',
            'x-ss-dp': '1233',
            'x-tt-trace-id': '00-63d3eb311062c1cf916902c6055b04d1-63d3eb311062c1cf-01',
            'user-agent': 'com.zhiliaoapp.musically/2021306050 (Linux; U; Android 13; ar_IQ_#u-nu-latn; ANY-LX2; Build/HONORANY-L22CQ; Cronet/TTNetVersion:57844a4b 2019-10-16)',
            'x-khronos': '1719661750',
            'x-gorgon': '030090c00400ea7f1dc018e27740ee56e70a592b81f21cdde9f8',
        }
        re = requests.get(
            f'https://api16-normal-c-alisg.tiktokv.com/aweme/v2/aweme/feedback/?object_id={iiid}&owner_id={iiid}&report_type=user&locale=ar&locale=ar&isFirst=1&report_desc=&uri=&reason=90061&category=&request_tag_from=h5&manifest_version_code=2021306050&_rticket=1719661750669&current_region=IQ&app_language=ar&app_type=normal&iid=7385890279574865669&channel=googleplay&device_type=ANY-LX2&language=ar&resolution=1080*2298&openudid=39e9b96bb5c6e336&update_version_code=2021306050&ac2=wifi&sys_region=IQ&os_api=33&uoo=0&is_my_cn=0&timezone_name=Asia%2FBaghdad&dpi=480&residence=IQ&carrier_region=IQ&ac=wifi&device_id=7116197109661091333&pass-route=1&mcc_mnc=41805&os_version=13&timezone_offset=10800&version_code=130605&carrier_region_v2=418&app_name=musical_ly&ab_version=13.6.5&version_name=13.6.5&device_brand=HONOR&ssmix=a&pass-region=1&device_platform=android&build_number=13.6.5&region=ar&aid=1233&ts=1719661750',
            cookies=cookies,
            headers=headers,
        ).text
        if "status_message" in re or "status_code" in re or "extra" in re:
            bot.send_message(message.chat.id, f"<strong>Đã gửi báo cáo số {addd} thành công ✅</strong>", parse_mode="html", reply_markup=types.InlineKeyboardMarkup())
        else:
            bot.send_message(message.chat.id, f"<strong>Gửi báo cáo số {addd} thất bại ❌</strong>", parse_mode="html", reply_markup=types.InlineKeyboardMarkup())
        
        if int(addd) == int(add):
            bot.send_message(message.chat.id, f"<strong>Đã hoàn thành số báo cáo yêu cầu thành công ✅</strong>", parse_mode="html", reply_markup=types.InlineKeyboardMarkup())

def z2(message):
    try:
        sufi = int(message.text)
    except:
        key = types.InlineKeyboardMarkup()
        bot.send_message(message.chat.id, f"<strong>Bạn đã nhập giá trị sai…</strong>", parse_mode="html", reply_markup=key)
        return
    mw = bot.send_message(message.chat.id, 'Gửi username cần báo cáo:')
    bot.register_next_step_handler(mw, asss, sufi)

def asss(message, sufi):
    addd = 0
    b = message.chat.id
    user = message.text
    try:
        headers = {
            'Host': 'www.woodrowpoe.top',
            'Connection': 'keep-alive',
            'package': 'woodrowpoe.tik.realfans',
            'apptype': 'android',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 13; ANY-LX2 Build/HONORANY-L22CQ; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/124.0.6367.124 Mobile Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'idfa': '6160fb46-9862-4d44-95b9-b1911283231f',
            'Accept': 'application/json, text/plain, */*',
            'version': '1.1',
            'Origin': 'http://www.woodrowpoe.top',
            'X-Requested-With': 'woodrowpoe.tik.realfans',
            'Referer': 'http://www.woodrowpoe.top//',
            'Accept-Language': 'ar-IQ,ar;q=0.9,en-IQ;q=0.8,en-US;q=0.7,en;q=0.6',
        }
        data = {
            'username': user,
        }
        ress = requests.post('http://www.woodrowpoe.top/api/v1/tikTokGetUserProfileInfo', headers=headers, data=data).json()
        iiid = ress['data']['pk']
        bot.send_message(message.chat.id, f"<strong>Đã trích xuất ID người dùng thành công ✅\n📜 ID: {iiid}</strong>", parse_mode="html", reply_markup=types.InlineKeyboardMarkup())
    except:
        bot.send_message(message.chat.id, f"<strong>Username không đúng, vui lòng kiểm tra lại và thử lại</strong>", parse_mode="html", reply_markup=types.InlineKeyboardMarkup())
        return
    
    add = int(sufi)
    bot.send_message(message.chat.id, f"<strong>Đang gửi báo cáo, vui lòng chờ...</strong>", parse_mode="html", reply_markup=types.InlineKeyboardMarkup())
    for i in range(add):
        addd += 1
        cookies = {
            'odin_tt': '40c40ad4772022e96afc8c9e5ce6440a94936ed1bd537e7879ee88784cfe22fca0848fe32c54174d839784124b12b8c27d20352b659177c2f833576358d3c1579c239bd3c573702ec998bbcd2e1e8878',
            'msToken': 'SDcH0HN9daA5EUvWTrZQvwROEZak08vvXhd34ckAknKx7K8OD6AMmoH6DbATDF1BXAiYfDslEyEu0_OyNg8o9fJPBDnLnud81JQ1i7PueNrgdDQYazKGLKUVlA==',
        }
        headers = {
            'Host': 'api16-normal-c-alisg.tiktokv.com',
            'x-ss-req-ticket': '1719661996880',
            'x-tt-token': '034151afef2522b5e1c2add1168b0ca8db05a23b3056f1eed37d978de66524ba11681c8643b9fc579bc98e660ed51b1e4582cb1559e6188d3cf61df9d0e0aa45a337d96e167c5f6d764bd9f526fb9d46bf27572ff8fe1dc7e38b1aaeaec2f1340cac6-CkAyOGZkZjliNzgzNDQ5ZDVmMWE0Mzk5MTczZGZkYzg2NjdjOTU1MzMwMzI4ZDgyMmMxMjdhZjFlYjM5OThiNzQ4-2.0.0',
            'sdk-version': '1',
            'x-ss-dp': '1233',
            'x-tt-trace-id': '00-63d7ace61062c1cf916902c6054c04d1-63d7ace61062c1cf-01',
            'user-agent': 'com.zhiliaoapp.musically/2021306050 (Linux; U; Android 13; ar; ANY-LX2; Build/HONORANY-L22CQ; Cronet/TTNetVersion:57844a4b 2019-10-16)',
            'x-khronos': '1719661996',
            'x-gorgon': '0300b06f04008a23ba6ef10af5a029eaa64c4086b5bfc1baacd2',
        }
        re = requests.get(
            f'https://api16-normal-c-alisg.tiktokv.com/aweme/v2/aweme/feedback/?object_id={iiid}&owner_id={iiid}&report_type=user&locale=ar&locale=ar&isFirst=1&report_desc=&uri=&reason=9002&category=&request_tag_from=h5&manifest_version_code=2021306050&_rticket=1719661996881&current_region=IQ&app_language=ar&app_type=normal&iid=7385890279574865669&channel=googleplay&device_type=ANY-LX2&language=ar&resolution=1080*2298&openudid=39e9b96bb5c6e336&update_version_code=2021306050&ac2=wifi&sys_region=IQ&os_api=33&uoo=0&is_my_cn=0&timezone_name=Asia%2FBaghdad&dpi=480&residence=IQ&carrier_region=IQ&ac=wifi&device_id=7116197109661091333&pass-route=1&mcc_mnc=41805&os_version=13&timezone_offset=10800&version_code=130605&carrier_region_v2=418&app_name=musical_ly&ab_version=13.6.5&version_name=13.6.5&device_brand=HONOR&ssmix=a&pass-region=1&device_platform=android&build_number=13.6.5&region=ar&aid=1233&ts=1719661996',
            cookies=cookies,
            headers=headers,
        ).text
        if "status_message" in re or "status_code" in re or "extra" in re:
            bot.send_message(message.chat.id, f"<strong>Đã gửi báo cáo số {addd} thành công ✅</strong>", parse_mode="html", reply_markup=types.InlineKeyboardMarkup())
        else:
            bot.send_message(message.chat.id, f"<strong>Gửi báo cáo số {addd} thất bại ❌</strong>", parse_mode="html", reply_markup=types.InlineKeyboardMarkup())
        
        if int(addd) == int(add):
            bot.send_message(message.chat.id, f"<strong>Đã hoàn thành số báo cáo yêu cầu thành công ✅</strong>", parse_mode="html", reply_markup=types.InlineKeyboardMarkup())

def z3(message):
    try:
        sufi = int(message.text)
    except:
        key = types.InlineKeyboardMarkup()
        bot.send_message(message.chat.id, f"<strong>Bạn đã nhập giá trị sai…</strong>", parse_mode="html", reply_markup=key)
        return
    mw = bot.send_message(message.chat.id, 'Gửi username cần báo cáo:')
    bot.register_next_step_handler(mw, assss, sufi)

def assss(message, sufi):
    addd = 0
    b = message.chat.id
    user = message.text
    try:
        headers = {
            'Host': 'www.woodrowpoe.top',
            'Connection': 'keep-alive',
            'package': 'woodrowpoe.tik.realfans',
            'apptype': 'android',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 13; ANY-LX2 Build/HONORANY-L22CQ; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/124.0.6367.124 Mobile Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'idfa': '6160fb46-9862-4d44-95b9-b1911283231f',
            'Accept': 'application/json, text/plain, */*',
            'version': '1.1',
            'Origin': 'http://www.woodrowpoe.top',
            'X-Requested-With': 'woodrowpoe.tik.realfans',
            'Referer': 'http://www.woodrowpoe.top//',
            'Accept-Language': 'ar-IQ,ar;q=0.9,en-IQ;q=0.8,en-US;q=0.7,en;q=0.6',
        }
        data = {
            'username': user,
        }
        ress = requests.post('http://www.woodrowpoe.top/api/v1/tikTokGetUserProfileInfo', headers=headers, data=data).json()
        iiid = ress['data']['pk']
        bot.send_message(message.chat.id, f"<strong>Đã trích xuất ID người dùng thành công ✅\n📜 ID: {iiid}</strong>", parse_mode="html", reply_markup=types.InlineKeyboardMarkup())
    except:
        bot.send_message(message.chat.id, f"<strong>Username không đúng, vui lòng kiểm tra lại và thử lại</strong>", parse_mode="html", reply_markup=types.InlineKeyboardMarkup())
        return
    
    add = int(sufi)
    bot.send_message(message.chat.id, f"<strong>Đang gửi báo cáo, vui lòng chờ...</strong>", parse_mode="html", reply_markup=types.InlineKeyboardMarkup())
    for i in range(add):
        addd += 1
        cookies = {
            'odin_tt': '40c40ad4772022e96afc8c9e5ce6440a94936ed1bd537e7879ee88784cfe22fca0848fe32c54174d839784124b12b8c27d20352b659177c2f833576358d3c1579c239bd3c573702ec998bbcd2e1e8878',
            'msToken': 'bLTHideWB0A4rwUNbFuXaOfox-RaP8ujtCAUIdbT1lJqD_DuKQuyzr5eHQFRAWkQWMDDyvD-oY-wo6_PFSeezMuMJQGew8fZWy2TT4lG2fSH0EthAUtiOltD2A==',
        }
        headers = {
            'Host': 'api16-normal-c-alisg.tiktokv.com',
            'x-ss-req-ticket': '1719662188204',
            'x-tt-token': '034151afef2522b5e1c2add1168b0ca8db05a23b3056f1eed37d978de66524ba11681c8643b9fc579bc98e660ed51b1e4582cb1559e6188d3cf61df9d0e0aa45a337d96e167c5f6d764bd9f526fb9d46bf27572ff8fe1dc7e38b1aaeaec2f1340cac6-CkAyOGZkZjliNzgzNDQ5ZDVmMWE0Mzk5MTczZGZkYzg2NjdjOTU1MzMwMzI4ZDgyMmMxMjdhZjFlYjM5OThiNzQ4-2.0.0',
            'sdk-version': '1',
            'x-ss-dp': '1233',
            'x-tt-trace-id': '00-63da984e1062c1cf916902c605b504d1-63da984e1062c1cf-01',
            'user-agent': 'com.zhiliaoapp.musically/2021306050 (Linux; U; Android 13; ar; ANY-LX2; Build/HONORANY-L22CQ; Cronet/TTNetVersion:57844a4b 2019-10-16)',
            'x-khronos': '1719662188',
            'x-gorgon': '0300c0d00400ba7b3b32b5cf363902ab51deeb776fbf3dc359a1',
        }
        re = requests.get(
            f'https://api16-normal-c-alisg.tiktokv.com/aweme/v2/aweme/feedback/?object_id={iiid}&owner_id={iiid}&report_type=user&locale=ar&locale=ar&isFirst=1&report_desc=&uri=&reason=90115&category=&request_tag_from=h5&manifest_version_code=2021306050&_rticket=1719662188204&current_region=IQ&app_language=ar&app_type=normal&iid=7385890279574865669&channel=googleplay&device_type=ANY-LX2&language=ar&resolution=1080*2298&openudid=39e9b96bb5c6e336&update_version_code=2021306050&ac2=wifi&sys_region=IQ&os_api=33&uoo=0&is_my_cn=0&timezone_name=Asia%2FBaghdad&dpi=480&residence=IQ&carrier_region=IQ&ac=wifi&device_id=7116197109661091333&pass-route=1&mcc_mnc=41805&os_version=13&timezone_offset=10800&version_code=130605&carrier_region_v2=418&app_name=musical_ly&ab_version=13.6.5&version_name=13.6.5&device_brand=HONOR&ssmix=a&pass-region=1&device_platform=android&build_number=13.6.5&region=ar&aid=1233&ts=1719662188',
            cookies=cookies,
            headers=headers,
        ).text
        if "status_message" in re or "status_code" in re or "extra" in re:
            bot.send_message(message.chat.id, f"<strong>Đã gửi báo cáo số {addd} thành công ✅</strong>", parse_mode="html", reply_markup=types.InlineKeyboardMarkup())
        else:
            bot.send_message(message.chat.id, f"<strong>Gửi báo cáo số {addd} thất bại ❌</strong>", parse_mode="html", reply_markup=types.InlineKeyboardMarkup())
        
        if int(addd) == int(add):
            bot.send_message(message.chat.id, f"<strong>Đã hoàn thành số báo cáo yêu cầu thành công ✅</strong>", parse_mode="html", reply_markup=types.InlineKeyboardMarkup())

def z4(message):
    try:
        sufi = int(message.text)
    except:
        key = types.InlineKeyboardMarkup()
        bot.send_message(message.chat.id, f"<strong>Bạn đã nhập giá trị sai…</strong>", parse_mode="html", reply_markup=key)
        return
    mw = bot.send_message(message.chat.id, 'Gửi username cần báo cáo:')
    bot.register_next_step_handler(mw, asssss, sufi)

def asssss(message, sufi):
    addd = 0
    b = message.chat.id
    user = message.text
    try:
        headers = {
            'Host': 'www.woodrowpoe.top',
            'Connection': 'keep-alive',
            'package': 'woodrowpoe.tik.realfans',
            'apptype': 'android',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 13; ANY-LX2 Build/HONORANY-L22CQ; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/124.0.6367.124 Mobile Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'idfa': '6160fb46-9862-4d44-95b9-b1911283231f',
            'Accept': 'application/json, text/plain, */*',
            'version': '1.1',
            'Origin': 'http://www.woodrowpoe.top',
            'X-Requested-With': 'woodrowpoe.tik.realfans',
            'Referer': 'http://www.woodrowpoe.top//',
            'Accept-Language': 'ar-IQ,ar;q=0.9,en-IQ;q=0.8,en-US;q=0.7,en;q=0.6',
        }
        data = {
            'username': user,
        }
        ress = requests.post('http://www.woodrowpoe.top/api/v1/tikTokGetUserProfileInfo', headers=headers, data=data).json()
        iiid = ress['data']['pk']
        bot.send_message(message.chat.id, f"<strong>Đã trích xuất ID người dùng thành công ✅\n📜 ID: {iiid}</strong>", parse_mode="html", reply_markup=types.InlineKeyboardMarkup())
    except:
        bot.send_message(message.chat.id, f"<strong>Username không đúng, vui lòng kiểm tra lại và thử lại</strong>", parse_mode="html", reply_markup=types.InlineKeyboardMarkup())
        return
    
    add = int(sufi)
    bot.send_message(message.chat.id, f"<strong>Đang gửi báo cáo, vui lòng chờ...</strong>", parse_mode="html", reply_markup=types.InlineKeyboardMarkup())
    for i in range(add):
        addd += 1
        cookies = {
            'odin_tt': '40c40ad4772022e96afc8c9e5ce6440a94936ed1bd537e7879ee88784cfe22fca0848fe32c54174d839784124b12b8c27d20352b659177c2f833576358d3c1579c239bd3c573702ec998bbcd2e1e8878',
            'msToken': 'JmSfyyPDgNCuw6yh5eBpq0_o7K_hHBSsamNWylgt4n2jvZ2BPETkS1v6q4SDcrlhDwCu4zL1UhMXnn51bRTIZu0wWBFD85ciRMHH8XRQMULwkaN19UonoS6S3A==',
        }
        headers = {
            'Host': 'api16-normal-c-alisg.tiktokv.com',
            'x-ss-req-ticket': '1719662290959',
            'x-tt-token': '034151afef2522b5e1c2add1168b0ca8db05a23b3056f1eed37d978de66524ba11681c8643b9fc579bc98e660ed51b1e4582cb1559e6188d3cf61df9d0e0aa45a337d96e167c5f6d764bd9f526fb9d46bf27572ff8fe1dc7e38b1aaeaec2f1340cac6-CkAyOGZkZjliNzgzNDQ5ZDVmMWE0Mzk5MTczZGZkYzg2NjdjOTU1MzMwMzI4ZDgyMmMxMjdhZjFlYjM5OThiNzQ4-2.0.0',
            'sdk-version': '1',
            'x-ss-dp': '1233',
            'x-tt-trace-id': '00-63dc29ad1062c1cf916902c6059104d1-63dc29ad1062c1cf-01',
            'user-agent': 'com.zhiliaoapp.musically/2021306050 (Linux; U; Android 13; ar; ANY-LX2; Build/HONORANY-L22CQ; Cronet/TTNetVersion:57844a4b 2019-10-16)',
            'x-khronos': '1719662290',
            'x-gorgon': '0300300704005d745c06cb07cb8311468b85cc99c94d91f97ff8',
        }
        re = requests.get(
            f'https://api16-normal-c-alisg.tiktokv.com/aweme/v2/aweme/feedback/?object_id={iiid}&owner_id={iiid}&report_type=user&locale=ar&locale=ar&isFirst=1&report_desc=&uri=&reason=9004&category=&request_tag_from=h5&manifest_version_code=2021306050&_rticket=1719662290960&current_region=IQ&app_language=ar&app_type=normal&iid=7385890279574865669&channel=googleplay&device_type=ANY-LX2&language=ar&resolution=1080*2298&openudid=39e9b96bb5c6e336&update_version_code=2021306050&ac2=wifi&sys_region=IQ&os_api=33&uoo=0&is_my_cn=0&timezone_name=Asia%2FBaghdad&dpi=480&residence=IQ&carrier_region=IQ&ac=wifi&device_id=7116197109661091333&pass-route=1&mcc_mnc=41805&os_version=13&timezone_offset=10800&version_code=130605&carrier_region_v2=418&app_name=musical_ly&ab_version=13.6.5&version_name=13.6.5&device_brand=HONOR&ssmix=a&pass-region=1&device_platform=android&build_number=13.6.5&region=ar&aid=1233&ts=1719662291',
            cookies=cookies,
            headers=headers,
        ).text
        if "status_message" in re or "status_code" in re or "extra" in re:
            bot.send_message(message.chat.id, f"<strong>Đã gửi báo cáo số {addd} thành công ✅</strong>", parse_mode="html", reply_markup=types.InlineKeyboardMarkup())
        else:
            bot.send_message(message.chat.id, f"<strong>Gửi báo cáo số {addd} thất bại ❌</strong>", parse_mode="html", reply_markup=types.InlineKeyboardMarkup())
        
        if int(addd) == int(add):
            bot.send_message(message.chat.id, f"<strong>Đã hoàn thành số báo cáo yêu cầu thành công ✅</strong>", parse_mode="html", reply_markup=types.InlineKeyboardMarkup())

bot.polling(none_stop=True)