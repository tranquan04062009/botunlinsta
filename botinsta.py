# CRE: TRANHAI AND SEA
import requests
import concurrent.futures
import time
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from datetime import datetime, timedelta

# Thông tin key và token
def generate_key():
    ngay = int(time.strftime('%d'))
    return str(ngay * 25937 + 469173)

def get_shortened_url():
    key = generate_key()
    url = f'https://tranquankeybot.blogspot.com/2025/02/keybot.html?ma={key}'
    token = "5f8ca8734e93fabf98f50400ca8744f5d929aa41768059813680cc3f52fd4b1e"
    response = requests.get(f'https://yeumoney.com/QL_api.php?token={token}&url={url}')
    post_url = response.json()
    if post_url['status'] == "error":
        print(post_url['message'])
        return url, key  # Trả về URL gốc nếu không rút gọn được
    return post_url.get('shortenedUrl', url), key

# Thay YOUR_TELEGRAM_BOT_TOKEN bằng token bot của bạn từ BotFather
TOKEN = "7834807188:AAHIwCflT9qY-Vhjyu22HhSKHGyHANGUZHA"

# Lưu trữ thông tin người dùng đã xác thực và thời gian hết hạn
verified_users = {}  # {user_id: {'key': key, 'expiry': datetime}}

# Hàm kiểm tra key còn hiệu lực không
def is_key_valid(user_id):
    if user_id not in verified_users:
        return False
    expiry = verified_users[user_id]['expiry']
    return datetime.now() < expiry

# Hàm chạy spam (giữ nguyên từ code gốc)
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
    current_key = generate_key()
    shortened_url, _ = get_shortened_url()

    if input_key != current_key:
        await context.bot.send_message(chat_id=chat_id, text=f"Key không đúng! Lấy key tại: {shortened_url}")
        return

    # Kiểm tra xem key đã được sử dụng bởi người khác chưa
    for uid, data in verified_users.items():
        if data['key'] == input_key and uid != user_id:
            await context.bot.send_message(chat_id=chat_id, text="Key này đã được sử dụng bởi người khác!")
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

    # Kiểm tra xác thực
    if not is_key_valid(user_id):
        shortened_url, current_key = get_shortened_url()
        if shortened_url:
            await context.bot.send_message(
                chat_id=chat_id,
                text=f"Bạn cần xác thực key trước!\nLấy key tại: {shortened_url}\nSau đó dùng: /verify {current_key}"
            )
        else:
            await context.bot.send_message(
                chat_id=chat_id,
                text="Không thể tạo link rút gọn, vui lòng thử lại sau!"
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

# Hàm khởi động bot
def main():
    application = Application.builder().token(TOKEN).build()

    # Thêm handler cho các lệnh
    application.add_handler(CommandHandler("verify", verify_command))
    application.add_handler(CommandHandler("sms", sms_command))

    # Chạy bot
    print("Bot đang chạy...")
    application.run_polling()

if __name__ == "__main__":
    main()