# bot.py

import os
import asyncio
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from cv_fields import USER_FIELDS
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
    if step < len(USER_FIELDS):
        return USER_FIELDS[step]
    return None


# ── Handlers ───────────────────────────────────────────────

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to *CV Generator Bot!*\n\n"
        "I'll ask you a few questions and generate a professional CV for you.\n\n"
        "Type /generate to start.\n"
        "Type /help to see all commands.",
        parse_mode="Markdown"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 *CV Generator Bot — Help*\n\n"
        "/start — Welcome message\n"
        "/generate — Start building your CV\n"
        "/cancel — Stop and clear your current session\n"
        "/help — Show this message\n\n"
        "💡 Just answer each question and I'll handle the rest.\n"
        "AI will automatically write your descriptions.",
        parse_mode="Markdown"
    )


async def generate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if get_session(user_id):
        await update.message.reply_text(
            "⚠️ You already have a CV in progress.\n"
            "Type /cancel first if you want to start over."
        )
        return

    create_session(user_id)

    await update.message.reply_text(
        "📝 Let's build your CV!\n"
        "Answer each question and I'll take care of the rest.\n"
        "Type /cancel at any time to stop.\n"
    )

    first_field = get_next_user_field(0)
    total = len(USER_FIELDS)
    await update.message.reply_text(f"[1/{total}] {first_field['question']}")


async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    session = get_session(user_id)

    if session is None:
        await update.message.reply_text(
            "Type /generate to start building your CV."
        )
        return

    user_answer = update.message.text.strip()

    # Validate input
    if len(user_answer) < 2:
        await update.message.reply_text(
            "⚠️ That looks too short. Please give a valid answer."
        )
        return

    if len(user_answer) > 300:
        await update.message.reply_text(
            "⚠️ That's too long. Please keep it under 300 characters."
        )
        return

    current_step = get_step(user_id)
    current_field = get_next_user_field(current_step)

    if current_field is None:
        return

    # Save answer
    update_session_data(user_id, current_field["key"], user_answer)
    advance_step(user_id)
    next_step = get_step(user_id)
    next_field = get_next_user_field(next_step)

    if next_field:
        total = len(USER_FIELDS)
        await update.message.reply_text(
            f"[{next_step + 1}/{total}] {next_field['question']}"
        )
    else:
        await update.message.reply_text(
            "✅ Got all your info!\n\n"
            "⏳ AI is writing your descriptions and generating your CV...\n"
            "This may take a few seconds."
        )

        try:
            # Run AI generation
            from ai_writer import fill_ai_fields
            completed_data = await asyncio.to_thread(
                fill_ai_fields, session["data"]
            )

            # Generate PDF
            from pdf_generator import generate_pdf
            pdf_path = await asyncio.to_thread(generate_pdf, completed_data)

            # Send PDF
            with open(pdf_path, "rb") as pdf_file:
                await update.message.reply_document(
                    document=pdf_file,
                    filename=f"CV_{completed_data.get('full_name', 'output').replace(' ', '_')}.pdf",
                    caption="✅ Here is your professional CV! Good luck! 🚀"
                )

        except Exception as e:
            print(f"CV generation error: {e}")
            await update.message.reply_text(
                "⚠️ Something went wrong while generating your CV.\n"
                "Please type /generate to try again."
            )

        finally:
            # Always cleanup
            try:
                os.remove(pdf_path)
            except Exception:
                pass
            delete_session(user_id)


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    delete_session(user_id)
    await update.message.reply_text(
        "❌ CV generation cancelled.\n"
        "Type /generate to start again."
    )


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    print(f"Unhandled error: {context.error}")
    if isinstance(update, Update) and update.message:
        await update.message.reply_text(
            "⚠️ Something went wrong. Type /generate to start again."
        )
        if update.effective_user:
            delete_session(update.effective_user.id)


# ── Main ───────────────────────────────────────────────────

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("generate", generate))
    app.add_handler(CommandHandler("cancel", cancel))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_answer))
    app.add_error_handler(error_handler)

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()