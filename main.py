import logging
import asyncio
import telegram.error
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

from tictactoe import TicTacToe, EMPTY, PLAYER, AI
import os
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

games = {}

AI_DELAY = 0.70

PROJECT_INFO = {
    "name": "Tic-Tac-Toe AI Bot",
    "description": "A Telegram bot that lets you play Tic-Tac-Toe against an unbeatable AI using the MINIMAX algorithm.",
    "technologies": [
        "Python 3.8+",
        "python-telegram-bot library",
        "MINIMAX algorithm"
    ],
    "Developers": [
        {
            "name": "Ahmed Abbas",
            "role": "Backend Developer, interested in AI",
            "linkedin": "https://www.linkedin.com/in/3bbaas/"
        }, {
            "name": "Rokiya-Abdelsatar",
            "role": "Flutter, AI, Embedded, Front-end, UI-UX, ترابيزات بلياردو و بينج",
            "linkedin": "https://linkedin.com/in/rokiya-abdelsatar"
        },
        {
            "name": "Hasnaa Nageh",
            "role": "Front-end",
            "linkedin": "https://www.linkedin.com/in/hasnaa-nageh-a884a6265"
        }, {
            "name": "Ahmed Ibrahim",
            "role": "Flutter Developer, interested in AI",
            "linkedin": "https://www.linkedin.com/in/hasnaa-nageh-a884a6265"
        }, {
            "name": "Seif Al-Din Sayed",
            "role": "Data Scientist",
            "linkedin": "https://www.linkedin.com/in/seif-al-din-sayed-299baa264/"
        }, ]
}


class TicTacToeGame(TicTacToe):

    def __init__(self):
        super().__init__()
        self.ai_thinking = False

    def get_board_markup(self, disable_buttons=False):
        """
        Create an InlineKeyboardMarkup for the current board state

        Parameters:
        disable_buttons (bool): If True, all buttons will be disabled during AI's turn
        """
        keyboard = []
        for i in range(0, 9, 3):
            row = []
            for j in range(3):
                cell = i + j
                text = self.board[cell] if self.board[cell] != EMPTY else "  "

                if text == EMPTY:
                    if disable_buttons:
                        row.append(InlineKeyboardButton(text, callback_data="wait"))
                    else:
                        row.append(InlineKeyboardButton(text, callback_data=f"move_{cell}"))
                else:
                    row.append(InlineKeyboardButton(text, callback_data=f"filled_{cell}"))
            keyboard.append(row)

        keyboard.append([InlineKeyboardButton("🔄 Restart Game", callback_data="restart")])

        return InlineKeyboardMarkup(keyboard)

    def get_result_markup(self):

        keyboard = [[InlineKeyboardButton("🎮 Play Again", callback_data="play_again")]]
        return InlineKeyboardMarkup(keyboard)

    def get_game_board_message(self):

        if self.ai_thinking:
            return "🤖 AI is thinking..."
        else:
            return "Your turn! You are ❌ and the AI is ⭕."

    def get_result_message(self):

        board_text = ""
        for i in range(0, 9, 3):
            row = ""
            for j in range(3):
                cell = i + j
                symbol = self.board[cell]
                if symbol == EMPTY:
                    symbol = "⬜"
                row += symbol + " "
            board_text += row + "\n"

        if self.winner == PLAYER:
            result = "🎉 <b>You won! Congratulations!</b> 🏆"
        elif self.winner == AI:
            result = "🤖 <b>The AI won!</b> Better luck next time."
        else:
            result = "🤝 <b>It's a draw!</b> Nice game."

        return f"{result}\n\nFinal board:\n{board_text}"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    games[user_id] = TicTacToeGame()

    instructions = (
        "Welcome to Tic-Tac-Toe AI Bot! 🎮\n\n"
        "Don't forget star this project on <a href='https://github.com/3bbaas/TelegramBot-XO-Game'>Github</a>\n\n"
        "📋 <b>How to Play:</b>\n"
        "1. You are ❌ and the AI is ⭕\n"
        "2. Tap on an empty square to place your mark\n"
        "3. Get three in a row to win!\n\n"
        "Use /help for more information and /about to learn about the project.\n\n"
        "Let's play! Start first ya Negm 👇"
    )

    await update.message.reply_html(
        instructions,
        reply_markup=games[user_id].get_board_markup()
    )


async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    project_info = PROJECT_INFO

    about_text = (
        f"<b>🤖 {project_info['name']}</b>\n\n"
        f"{project_info['description']}\n\n"
        "<b>🛠️ Technologies Used:</b>\n"
    )

    for tech in project_info['technologies']:
        about_text += f"• {tech}\n"

    about_text += "\n<b>👨‍💻 Team Members:</b>\n"

    for member in project_info['Developers']:
        about_text += f"• <a href='{member['linkedin']}'>{member['name']}</a> - <code>{member['role']}</code>\n"

    await update.message.reply_html(
        about_text,
        disable_web_page_preview=True
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = (
        "<b>🎮 Tic-Tac-Toe AI Bot - Help</b>\n\n"
        "<b>Game Rules:</b>\n"
        "• Players take turns placing their marks (❌ or ⭕) on the board\n"
        "• First player to get three of their marks in a row wins\n"
        "• If all squares are filled with no winner, it's a draw\n\n"
        "<b>How to Play:</b>\n"
        "1. Tap on any empty square to place your ❌\n"
        "2. The AI will respond by placing its ⭕\n"
        "3. Continue until someone wins or it's a draw\n\n"
        "<b>Commands:</b>\n"
        "/start - Start a new game\n"
        "/help - Show this help message\n"
        "/about - Project information and team\n\n"
        "<b>Tips:</b>\n"
        "• The center square is often a strategic position\n"
        "• Try to block the AI from getting three in a row\n"
        "• The AI uses MINIMAX algorithm and plays optimally - it can't be beaten!"
    )

    await update.message.reply_html(help_text)


async def update_game_message(query, game, disable_buttons=False):
    """
    Helper function to update game message with error handling

    Parameters:
    disable_buttons (bool): If True, buttons will be disabled (during AI's turn)
    """
    try:
        await query.edit_message_text(
            text=game.get_game_board_message(),
            reply_markup=game.get_board_markup(disable_buttons)
        )
    except telegram.error.BadRequest as e:
        if "Message is not modified" in str(e):
            pass
        else:
            raise


async def show_game_result(query, game):
    try:
        await query.edit_message_text(
            text=game.get_result_message(),
            reply_markup=game.get_result_markup(),
            parse_mode="HTML"
        )
    except telegram.error.BadRequest as e:
        if "Message is not modified" in str(e):
            pass
        else:
            raise


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query

    user_id = update.effective_user.id

    if query.data == "play_again":
        await query.answer("Starting a new game!")
        games[user_id] = TicTacToeGame()
        await update_game_message(query, games[user_id])
        return

    if user_id not in games:
        await query.answer()
        games[user_id] = TicTacToeGame()
        await query.edit_message_text(
            text="Starting a new game. You are ❌ and the AI is ⭕. Your move first!",
            reply_markup=games[user_id].get_board_markup()
        )
        return

    game = games[user_id]

    if query.data == "wait":
        await query.answer("Please wait, AI is thinking...\n\nاستني دورك!!")
        return

    if query.data.startswith("filled_"):
        await query.answer("That position is already filled!\n\n طب ايه الكلام مش نشوف كويس؟")
        return

    await query.answer()

    if query.data == "restart":
        games[user_id] = TicTacToeGame()
        await update_game_message(query, games[user_id])
        return

    if query.data.startswith("move_"):
        position = int(query.data.split("_")[1])

        if game.game_over:
            await query.answer("Game is already over. Start a new game!\n\nيعوضك ربنا عليك بقي")
            return

        if game.ai_thinking:
            await query.answer("Please wait, AI is thinking...\n\nاستني دورك")
            return

        if game.make_move(position):
            if game.game_over:
                await show_game_result(query, game)
                return

            game.ai_thinking = True
            await update_game_message(query, game, disable_buttons=True)

            await asyncio.sleep(AI_DELAY)

            game.ai_move()

            game.ai_thinking = False

            if game.game_over:
                await show_game_result(query, game)
            else:
                await update_game_message(query, game)
        else:
            await query.answer("Invalid move! Try again.")


def main() -> None:
    application = Application.builder().token(f"{os.getenv('BOT_TOKEN')}").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about_command))
    application.add_handler(CallbackQueryHandler(button_callback))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
