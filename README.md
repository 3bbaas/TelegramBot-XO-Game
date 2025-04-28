# TelegramBot XO Game

A Telegram bot that lets you play Tic-Tac-Toe against an unbeatable AI using the MINIMAX algorithm.

---

## Table of Contents

- [Features](#features)
- [Technologies](#technologies)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Environment Variables](#environment-variables)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- Interactive Tic-Tac-Toe game on Telegram
- Unbeatable AI powered by the MINIMAX algorithm
- Inline keyboard interface for easy play
- Commands:
  - `/start` – Start a new game
  - `/help` – Show help and game rules
  - `/about` – Information about the project and team

---

## Technologies

- **Python** 3.8+
- **python-telegram-bot** library
- **MINIMAX algorithm** for AI decision making
- **dotenv** for environment variable management

---

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/3bbaas/TelegramBot-XO-Game.git
   cd TelegramBot-XO-Game
   ```

2. **Create and activate a virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   - Copy `.env.example` to `.env`
   - Set your Telegram bot token in the `.env` file:
     ```dotenv
     BOT_TOKEN=your_bot_token_here
     ```

5. **Run the bot**

   ```bash
   python main.py
   ```

---

## Usage

Open Telegram, search for your bot by its username, and start a chat. Use the commands below to interact:

- `/start` – Begins a new Tic-Tac-Toe session
- `/help` – Displays game rules and tips
- `/about` – Shows project information and team members

Tap on the inline buttons to place your move. Enjoy the game! 🎮

---

## Project Structure

```
├── main.py           # Bot entrypoint and Telegram handlers
├── tictactoe.py      # Game logic & MINIMAX AI implementation
├── requirements.txt  # Python dependencies (frozen via pip)
├── .env.example      # Sample environment variables
├── .gitignore        # Ignored files and folders
└── README.md         # Project overview and setup instructions
```

---

## Environment Variables

- `BOT_TOKEN` – Your Telegram bot token (from BotFather)

Refer to `.env.example` for guidance.

---

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m "Add YourFeature"`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

---

## License

This project is MIT licensed. See the [LICENSE](LICENSE) file for details.

---

## .gitignore

```
venv/
.idea/
__pycache__/
*.py[cod]
.env
```

