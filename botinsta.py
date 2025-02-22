import asyncio
import logging
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

init(autoreset=True)

TOKEN = "7834807188:AAHIwCflT9qY-Vhjyu22HhSKHGyHANGUZHA"  # Thay thế bằng token cố định của b

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

WELCOME_MESSAGE = """⥃ Chào mừng bạn đến với bot mở khóa tài khoản Instagram ♯
⥃ Bot hỗ trợ dịch vụ mở khóa VIP ✰
⥃ Xử lý yêu cầu nhanh chóng ⥉
ID của bạn ⥃ {user_id}.👤"""

def get_main_menu():
    buttons = [
        [InlineKeyboardButton(text='🔓 Mở khóa tài khoản', callback_data='unlockinsta')],
        [
            InlineKeyboardButton(text='📢 Kênh thông tin', url='https://t.me/ndmmo'),
            InlineKeyboardButton(text='💻 Lập trình viên', url='https://t.me/zlzflf')
        ],
        [InlineKeyboardButton(text='📜 Hướng dẫn sử dụng', url='https://t.me/ndmmo')]
    ]
    return InlineKeyboardMarkup(buttons)

async def unlockinsta(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id  # Lấy ID của người dùng từ tin nhắn
    message = WELCOME_MESSAGE.format(user_id=user_id)
    await update.message.reply_text(message, reply_markup=get_main_menu())

async def start_unlock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("• Gửi tên tài khoản:")
    context.user_data["step"] = "enter_full_name"
    context.user_data["user_id"] = query.from_user.id  # Lấy và lưu ID của người dùng

async def enter_full_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["full_name"] = update.message.text
    await update.message.reply_text("• Gửi tên người dùng:")
    context.user_data["step"] = "enter_username"

async def enter_username(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["username"] = update.message.text
    await update.message.reply_text("• Gửi email tài khoản:")
    context.user_data["step"] = "enter_email"

async def enter_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["email"] = update.message.text
    await update.message.reply_text("⏳ Đang gửi yêu cầu mở khóa...")

    # Phần gửi yêu cầu đến Facebook (giữ nguyên như trước)
    url = "https://www.facebook.com/ajax/help/contact/submit/page"
    headers = {
        'accept': "*/*",
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "en-US,en;q=0.9,vi;q=0.8",
        'content-type': "application/x-www-form-urlencoded",
        'cookie': "fr=07trjqu9vVEDWnFgc..BggI_u...1.0.BggI_u.; datr=NpCAYGDo9894gkBjdeQep6Gb; wd=1366x581",
        'origin': "https://www.facebook.com",
        'referer': "https://www.facebook.com/help/instagram/contact/1652567838289083",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36",
        'x-fb-lsd': "AVrZo3HBsNc"
    }
    data = {
        'jazoest': "2947",
        'lsd': "AVrZo3HBsNc",
        'AccountType': "Personal",
        'name': context.user_data["full_name"],
        'Field1489970557888767': context.user_data["username"],
        'email': context.user_data["email"],
        'Field236858559849125': "Vietnam",
        'support_form_id': "1652567838289083",
        'support_form_hidden_fields': """{"904224879693114":false,"495070633933955":false,"1489970557888767":false,"488955464552044":false,"236858559849125":false,"1638971086372158":true,"1615324488732156":true,"236548136468765":true}""",
        'support_form_fact_false_fields': "[]",
        '__user': '0',
        '__a': '1',
        '__dyn': "7xe6Fo4OQ1PyUbFuC1swgE98nwgU6C7UW8xi642-7E2vwXx60kO4o3Bw5VCwjE3awbG782Cwooa87i0n2US1kyE1e42C2218w5uwtU6e0D83mwaS0zE0I6aw",
        '__csr': '',
        '__req': '5',
        '__beoa': '0',
        '__pc': "PHASED:DEFAULT",
        '__bhv': '2',
        '__no_rdbl': '0',
        'dpr': '1',
        '__ccg': "MODERATE",
        '__rev': "1003660634",
        '__s': "xn9ebq:cuks1u:d7qd87",
        '__hsi': "6953722469318193550-0",
        '__comet_req': '0',
        '__spin_r': "1003660634",
        '__spin_b': "trunk",
        '__spin_t': "1619039678"
    }

    try:
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            await update.message.reply_text("✅ Yêu cầu mở khóa đã được gửi thành công. Vui lòng kiểm tra email trong thời gian tới.")
        else:
            await update.message.reply_text("❌ Có lỗi xảy ra khi gửi yêu cầu. Vui lòng thử lại sau.")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Lỗi xảy ra: {str(e)}")

async def process_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Kiểm tra ID người dùng
    if context.user_data.get("user_id") != update.message.from_user.id:
        return  # Bỏ qua nếu không phải người dùng đã bắt đầu

    step = context.user_data.get("step", "")
    if step == "enter_full_name":
        await enter_full_name(update, context)
    elif step == "enter_username":
        await enter_username(update, context)
    elif step == "enter_email":
        await enter_email(update, context)

def run_bot():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("unlockinsta", unlockinsta))
    app.add_handler(CallbackQueryHandler(start_unlock, pattern="^unlockinsta$"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_message))

    print(Fore.GREEN + "✅ Bot đang chạy...")
    app.run_polling()

if __name__ == "__main__":
    run_bot()
