# CRE: TRANHAI AND SEA
import requests
import concurrent.futures
import time
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Tính toán key dựa trên ngày hiện tại
ngay = int(time.strftime('%d'))
key = str(ngay * 25937 + 469173)
urlwebkey = f'https://tranquankeybot.blogspot.com/2025/02/keybot.html?ma={key}'
token_yeumoney = "5f8ca8734e93fabf98f50400ca8744f5d929aa41768059813680cc3f52fd4b1e"
post_url = requests.get(f'https://yeumoney.com/QL_api.php?token={token_yeumoney}&url={urlwebkey}').json()

if post_url.get('status') == "error":
    print(post_url.get('message', 'Lỗi không xác định'))
    quit()
else:
    link_key = post_url.get('shortenedUrl')

# Token bot Telegram (thay bằng token của bạn)
TOKEN = "7834807188:AAFtO6u6mJ-1EaDm4W4qA_cb4KgICqSo734"

# Lưu trữ thông tin key và người dùng đã xác thực
verified_users = {}  # {chat_id: {'key': key, 'date': ngay}}
current_date = ngay

# Hàm kiểm tra ngày để reset key
def check_date_reset():
    global current_date, verified_users
    new_date = int(time.strftime('%d'))
    if new_date != current_date:
        current_date = new_date
        verified_users.clear()  # Xóa tất cả key đã xác thực khi sang ngày mới
        global key
        key = str(new_date * 25937 + 469173)  # Cập nhật key mới

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
    args = context.args

    check_date_reset()  # Kiểm tra ngày để reset key nếu cần

    if len(args) != 1:
        await context.bot.send_message(chat_id=chat_id, text="Vui lòng sử dụng lệnh đúng cú pháp: /verify <key>")
        return

    input_key = args[0]

    # Kiểm tra key
    if input_key != key:
        await context.bot.send_message(chat_id=chat_id, text="Key sai! Vui lòng lấy key đúng tại link sau và thử lại.\n" + link_key)
        return

    # Kiểm tra xem key đã được ai đó xác thực chưa
    for user_id, data in verified_users.items():
        if data['key'] == input_key and user_id != chat_id:
            await context.bot.send_message(chat_id=chat_id, text="Key này đã được người khác sử dụng! Mỗi key chỉ dành cho một người.")
            return

    # Lưu thông tin xác thực cho người dùng
    verified_users[chat_id] = {'key': input_key, 'date': current_date}
    await context.bot.send_message(chat_id=chat_id, text="Xác thực key thành công! Bạn có thể sử dụng lệnh /sms ngay bây giờ.\nLưu ý: Key chỉ có hiệu lực trong hôm nay.")

# Xử lý lệnh /sms
async def sms_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    args = context.args

    check_date_reset()  # Kiểm tra ngày để reset key nếu cần

    # Kiểm tra xem người dùng đã xác thực key chưa
    if chat_id not in verified_users or verified_users[chat_id]['date'] != current_date:
        await context.bot.send_message(chat_id=chat_id, text=f"Bạn cần xác thực key trước khi sử dụng! Lấy key tại: {link_key}\nSau đó dùng lệnh: /verify <key>")
        return

    if len(args) != 2:
        await context.bot.send_message(chat_id=chat_id, text="Vui lòng sử dụng lệnh đúng cú pháp: /sms <sdt> <số lần spam>")
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