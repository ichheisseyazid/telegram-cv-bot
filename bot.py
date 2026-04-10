# bot.py

import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from cv_fields import CV_FIELDS, USER_FIELDS
from sessions import (
    create_session,
    get_session,
    update_session_data,
    advance_step,
    get_step,
    delete_session,
)

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


# ── Helpers ────────────────────────────────────────────────

def get_next_user_field(step: int):
    """Return the USER_FIELDS entry at this step, or None if done."""
    if step < len(USER_FIELDS):
        return USER_FIELDS[step]
    return None


async def ask_question(update: Update, field: dict):
    """Send the question for a given field to the user."""
    await update.message.reply_text(field["question"])


# ── Handlers ───────────────────────────────────────────────

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to *CV Generator Bot!*\n\n"
        "I'll ask you a few questions and generate a professional CV for you.\n\n"
        "Type /generate to start.\n"
        "Type /cancel at any time to stop.",
        parse_mode="Markdown"
    )


async def generate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # Start a fresh session
    create_session(user_id)

    await update.message.reply_text(
        "Great! Let's build your CV. 📝\n"
        "Answer each question and I'll take care of the rest.\n"
    )

    # Ask the first question
    first_field = get_next_user_field(0)
    await ask_question(update, first_field)


async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    session = get_session(user_id)

    # User replied without starting
    if session is None:
        await update.message.reply_text(
            "Type /generate to start building your CV."
        )
        return

    current_step = get_step(user_id)
    current_field = get_next_user_field(current_step)

    if current_field is None:
        return  # Shouldn't happen, but safety net

    # Save the answer
    user_answer = update.message.text.strip()
    update_session_data(user_id, current_field["key"], user_answer)

    # Move to next step
    advance_step(user_id)
    next_step = get_step(user_id)
    next_field = get_next_user_field(next_step)

    if next_field:
        # More questions remaining
        await ask_question(update, next_field)
    else:
        # All user questions answered → hand off to AI + PDF
        await update.message.reply_text(
            "✅ Got all your info!\n\n"
            "⏳ Now generating your CV... this may take a few seconds."
        )
        # Step 5 and 6 will plug in here
        await update.message.reply_text(
            "🚧 AI writing and PDF generation coming in the next steps!"
        )
        delete_session(user_id)


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    delete_session(user_id)
    await update.message.reply_text(
        "❌ CV generation cancelled. Type /generate to start again."
    )


# ── Main ───────────────────────────────────────────────────

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("generate", generate))
    app.add_handler(CommandHandler("cancel", cancel))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_answer))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()