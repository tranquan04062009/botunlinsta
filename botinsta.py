# CRE: TRANHAI AND SEA
import requests
import concurrent.futures
import time
import secrets
import string
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from datetime import datetime, timedelta

# Tạo key ngẫu nhiên
def generate_key(length=16):
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

# Lưu trữ key và trạng thái sử dụng
keys = {}  # {key: is_used (True/False)}

def save_key(key):
    keys[key] = False  # False: chưa sử dụng, True: đã sử dụng

def use_key(key):
    if key in keys and not keys[key]:
        keys[key] = True  # Đánh dấu đã sử dụng
        return True
    return False

# Tạo URL gốc chứa key
def create_url(key):
    return f"https://tranquankeybot.blogspot.com/2025/02/keybot.html?ma={key}"

# Rút gọn URL bằng API Yeumoney
def shorten_url(url):
    api_url = "https://yeumoney.com/QL_api.php"  # Endpoint của Yeumoney (dựa trên yêu cầu của bạn)
    token = "5f8ca8734e93fabf98f50400ca8744f5d929aa41768059813680cc3f52fd4b1e"  # Token của bạn
    try:
        response = requests.get(f"{api_url}?token={token}&url={url}", timeout=10)
        post_url = response.json()
        if post_url['status'] == "error":
            print(post_url['message'])
            return url, None  # Trả về URL gốc và None nếu API lỗi
        shortened_url = post_url.get('shortenedUrl', url)
        return shortened_url, post_url.get('key', None)  # Trả về URL rút gọn và key nếu có
    except Exception as e:
        print(f"Lỗi khi gọi API Yeumoney: {e}")
        return url, None  # Trả về URL gốc nếu có lỗi

# Thay YOUR_TELEGRAM_BOT_TOKEN bằng token bot của bạn từ BotFather
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

# Lưu trữ thông tin người dùng đã xác thực và thời gian hết hạn
verified_users = {}  # {user_id: {'key': key, 'expiry': datetime}}

# Hàm kiểm tra key còn hiệu lực không
def is_key_valid(user_id):
    if user_id not in verified_users:
        return False
    expiry = verified_users[user_id]['expiry']
    return datetime.now() < expiry

# Hàm chạy spam (giữ nguyên từ code gốc, cần định nghĩa các hàm bên trong)
def run(phone, i):
    functions = [
        tv360, robot, fb, mocha, dvcd, myvt, phar, dkimu, fptshop, meta, blu,
        tgdt, concung, money, sapo, hoang, winmart, alf, guma, kingz, acfc, phuc, medi, emart, hana,
        med, ghn, shop, gala, fa, cathay, vina, ahamove, air, otpmu, vtpost, shine, domi, fm, cir, hoanvu, tokyo, shop, beau, fu, lote, lon
    ]
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
        futures = [executor.submit(fn, phone) for fn in functions]
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as exc:
                print(f'Generated an exception: {exc}')
    return f"Spam thành công lần: {i}"

# Xử lý lệnh /verify
async def verify_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    args = context.args

    if len(args) != 1:
        await context.bot.send_message(chat_id=chat_id, text="Vui lòng sử dụng: /verify <key>")
        return

    input_key = args[0]
    
    # Kiểm tra key có hợp lệ và chưa được sử dụng
    if not use_key(input_key):
        shortened_url, current_key = shorten_url(create_url(generate_key()))  # Tạo mới key và rút gọn URL
        await context.bot.send_message(chat_id=chat_id, text=f"Key không đúng hoặc đã được sử dụng! Lấy key mới tại: {shortened_url}")
        return

    # Xác thực key thành công
    expiry_time = datetime.now() + timedelta(days=1)  # Hết hạn sau 1 ngày
    verified_users[user_id] = {'key': input_key, 'expiry': expiry_time}
    await context.bot.send_message(chat_id=chat_id, text="Xác thực key thành công! Bạn có thể sử dụng /sms trong 24 giờ tới.")

# Xử lý lệnh /sms
async def sms_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    args = context.args

    try:
        # Kiểm tra xác thực
        if not is_key_valid(user_id):
            new_key = generate_key()
            save_key(new_key)  # Lưu key mới
            url = create_url(new_key)
            shortened_url, _ = shorten_url(url)  # Rút gọn URL qua Yeumoney
            await context.bot.send_message(
                chat_id=chat_id,
                text=f"Bạn cần xác thực key trước!\nLấy key tại: {shortened_url}\nSau đó dùng: /verify {new_key}"
            )
            return

        # Kiểm tra định dạng đầu vào
        if len(args) != 2:
            await context.bot.send_message(chat_id=chat_id, text="Vui lòng sử dụng: /sms <sdt> <số lần spam>")
            return

        phone, count = args[0], args[1]
        
        try:
            count = int(count)
        except ValueError:
            await context.bot.send_message(chat_id=chat_id, text="Số lần spam phải là số nguyên!")
            return

        await context.bot.send_message(chat_id=chat_id, text=f"Bắt đầu spam số {phone} {count} lần...")

        # Thực hiện spam
        for i in range(1, count + 1):
            result = run(phone, i)
            await context.bot.send_message(chat_id=chat_id, text=result)
            for j in range(4, 0, -1):
                await context.bot.send_message(chat_id=chat_id, text=f"Vui lòng chờ {j} giây")
                time.sleep(1)

    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text=f"Lỗi: {str(e)}")
        print(f"Lỗi trong xử lý /sms: {e}")

# Hàm khởi động bot
def main():
    application = Application.builder().token(TOKEN).build()

    # Thêm handler cho các lệnh
    application.add_handler(CommandHandler("verify", verify_command))
    application.add_handler(CommandHandler("sms", sms_command))

    # Chạy bot
    print("Bot đang chạy...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()