import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# ===== APNI SETTINGS YAHAN BHARO =====
BOT_TOKEN = "AAPKA_BOT_TOKEN"
CHANNEL_USERNAME = "@aapka_channel"  # Example: @mychannel
CHANNEL_LINK = "https://t.me/aapka_channel"
# =====================================

# --- Channel join check ---
async def is_user_joined(bot, user_id):
    try:
        member = await bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

# --- /start command ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    joined = await is_user_joined(context.bot, user_id)

    if not joined:
        keyboard = [
            [InlineKeyboardButton("✅ Channel Join Karein", url=CHANNEL_LINK)],
            [InlineKeyboardButton("🔄 Maine Join Kar Liya", callback_data="check_join")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "⚠️ Bot use karne ke liye pehle humara channel join karein!",
            reply_markup=reply_markup
        )
    else:
        await show_main_menu(update, context)

# --- Main menu ---
async def show_main_menu(update, context):
    keyboard = [
        [InlineKeyboardButton("❓ FAQ", callback_data="faq_menu")],
        [InlineKeyboardButton("📢 Channel", url=CHANNEL_LINK)],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = "👋 Welcome! Kya madad chahiye aapko?"

    if update.message:
        await update.message.reply_text(text, reply_markup=reply_markup)
    else:
        await update.callback_query.edit_message_text(text, reply_markup=reply_markup)

# --- Callback handler ---
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    # Join check button
    if query.data == "check_join":
        joined = await is_user_joined(context.bot, user_id)
        if joined:
            await show_main_menu(update, context)
        else:
            await query.answer("❌ Aapne abhi join nahi kiya!", show_alert=True)

    # FAQ Menu
    elif query.data == "faq_menu":
        keyboard = [
            [InlineKeyboardButton("❓ Bot kaise use karein?", callback_data="faq_1")],
            [InlineKeyboardButton("💰 Kya yeh free hai?", callback_data="faq_2")],
            [InlineKeyboardButton("📞 Support kaise milegi?", callback_data="faq_3")],
            [InlineKeyboardButton("🔙 Wapas Jaao", callback_data="back_main")],
        ]
        await query.edit_message_text(
            "📋 *FAQ - Aksar Puche Jane Wale Sawaal*\n\nKoi bhi sawaal chunein:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )

    # FAQ Answers
    elif query.data == "faq_1":
        await query.edit_message_text(
            "🤖 *Bot kaise use karein?*\n\n/start likhein aur menu se option chunein.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 FAQ Wapas", callback_data="faq_menu")]]),
            parse_mode="Markdown"
        )
    elif query.data == "faq_2":
        await query.edit_message_text(
            "💰 *Kya yeh free hai?*\n\nHaan, bilkul free hai! Channel join karein aur use karein.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 FAQ Wapas", callback_data="faq_menu")]]),
            parse_mode="Markdown"
        )
    elif query.data == "faq_3":
        await query.edit_message_text(
            "📞 *Support kaise milegi?*\n\n@AdminUsername pe message karein.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 FAQ Wapas", callback_data="faq_menu")]]),
            parse_mode="Markdown"
        )

    elif query.data == "back_main":
        await show_main_menu(update, context)

# --- Main ---
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("Bot chal raha hai...")
    app.run_polling()

if __name__ == "__main__":
    main()
