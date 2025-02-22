import asyncio
import logging
import aiohttp
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Chat
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ChatType

TOKEN = "7834807188:AAHIwCflT9qY-Vhjyu22HhSKHGyHANGUZHA"  # Replace with your bot token
ALLOWED_GROUP_ID = -1002370805497  # Replace with your group's ID (must be negative)

WELCOME_MESSAGE = """⥃ Chào mừng bạn đến với bot mở khóa tài khoản Instagram ♯
⥃ Bot hỗ trợ dịch vụ mở khóa VIP ✰
⥃ Xử lý yêu cầu nhanh chóng ⥉
ID của bạn ⥃ {user_id}.👤"""

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def get_main_menu(include_stop=False):
    buttons = [
        [InlineKeyboardButton(text='🔓 Mở khóa tài khoản', callback_data='unlockinsta')],
        [
            InlineKeyboardButton(text='📢 Kênh thông tin', url='https://t.me/grouptmq'),
            InlineKeyboardButton(text='💻 Lập trình viên', url='https://t.me/tranquan46')
        ],
        [InlineKeyboardButton(text='📜 Hướng dẫn sử dụng', url='https://t.me/grouptmq/494')]
    ]
    if include_stop:
        buttons.append([InlineKeyboardButton(text='🛑 Dừng', callback_data='stop')])
    return InlineKeyboardMarkup(buttons)

async def unlockinsta(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /unlockinsta command."""
    if update.message.chat.type == ChatType.PRIVATE:
          await update.message.reply_text("Bot này chỉ hoạt động trong nhóm chat.")
    elif update.message.chat.type == ChatType.GROUP or update.message.chat.type == ChatType.SUPERGROUP:
          if update.message.chat.id != ALLOWED_GROUP_ID:
            await update.message.reply_text("Bot này chỉ hoạt động trong nhóm chat đã được chỉ định.")
            return

          # Check if already in progress
          if "step" in context.user_data:
              await update.message.reply_text("Bạn đã có một yêu cầu đang xử lý. Vui lòng hoàn thành hoặc dừng yêu cầu đó trước.")
              return

          user_id = update.message.chat_id  # Lấy ID của người dùng từ tin nhắn
          message = WELCOME_MESSAGE.format(user_id=user_id)
          await update.message.reply_text(message, reply_markup=get_main_menu(include_stop=True))
          context.user_data["step"] = "enter_full_name"
          context.user_data["user_id"] = update.message.from_user.id  # Store user ID for later checks

    else:
        await update.message.reply_text("Bot này không hỗ trợ loại nhóm này.")


async def enter_full_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gets the full name from the user."""
    context.user_data["full_name"] = update.message.text
    await update.message.reply_text("• Gửi tên người dùng:", reply_markup=get_main_menu(include_stop=True))
    context.user_data["step"] = "enter_username"

async def enter_username(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gets the username from the user."""
    context.user_data["username"] = update.message.text
    await update.message.reply_text("• Gửi email tài khoản:", reply_markup=get_main_menu(include_stop=True))
    context.user_data["step"] = "enter_email"

async def enter_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gets the email from the user and sends the unlock request."""
    context.user_data["email"] = update.message.text
    await update.message.reply_text("⏳ Đang gửi yêu cầu mở khóa...", reply_markup=get_main_menu())

    # --- Asynchronous Request with aiohttp ---
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
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=data) as response:
                if response.status == 200:
                    await update.message.reply_text("✅ Yêu cầu mở khóa đã được gửi thành công. Vui lòng kiểm tra email trong thời gian tới.")
                else:
                    await update.message.reply_text(f"❌ Có lỗi xảy ra khi gửi yêu cầu.  Mã trạng thái: {response.status}")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Lỗi xảy ra: {e}")
    finally:
        # Clear user data after processing
        context.user_data.clear()



async def process_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Processes incoming messages during the unlock flow."""
    # Check if the message is from the correct user and in the correct chat
    if context.user_data.get("user_id") != update.message.from_user.id or update.message.chat.id != ALLOWED_GROUP_ID:
        return  # Ignore if not the correct user or chat

    step = context.user_data.get("step", "")
    if step == "enter_full_name":
        await enter_full_name(update, context)
    elif step == "enter_username":
        await enter_username(update, context)
    elif step == "enter_email":
        await enter_email(update, context)
    else:
        # If no step is defined, but user sends a message, prompt them to start
        await update.message.reply_text("Vui lòng sử dụng lệnh /unlockinsta để bắt đầu.", reply_markup=get_main_menu())

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancels the unlock process and clears user data."""
    query = update.callback_query
    await query.answer()

    # Clear user data
    context.user_data.clear()
    await query.message.edit_text("Đã dừng quy trình mở khóa.  Bạn có thể bắt đầu lại bằng /unlockinsta.", reply_markup=get_main_menu())

def run_bot():
    """Starts the bot."""
    app = Application.builder().token(TOKEN).build()

    # Command handlers
    # Removed the /start command, only /unlockinsta is used
    app.add_handler(CommandHandler("unlockinsta", unlockinsta))


    # Callback query handlers
    app.add_handler(CallbackQueryHandler(unlockinsta, pattern="^unlockinsta$"))  # Still needed for button press
    app.add_handler(CallbackQueryHandler(stop, pattern="^stop$"))

    # Message handler (only in allowed group)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND & filters.Chat(chat_id=ALLOWED_GROUP_ID), process_message))


    logger.info("Bot is running...")
    app.run_polling()
if __name__ == "__main__":
    run_bot()