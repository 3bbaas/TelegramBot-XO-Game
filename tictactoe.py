EMPTY = "  "
PLAYER = "❌"
AI = "⭕"


class TicTacToe:
    def __init__(self):
        self.board = [EMPTY for _ in range(9)]
        self.current_player = PLAYER
        self.game_over = False
        self.winner = None

    def make_move(self, position):
        """Make a move on the board. Returns True if the move was valid."""
        if self.board[position] == EMPTY and not self.game_over:
            self.board[position] = self.current_player
            if self.check_winner():
                self.game_over = True
                self.winner = self.current_player
            elif EMPTY not in self.board:
                self.game_over = True
            else:
                self.current_player = AI if self.current_player == PLAYER else PLAYER
            return True
        return False

    def check_winner(self):
        """Check if there's a winner on the current board."""
        return self._check_winner_board(self.board, self.current_player)

    def _check_winner_board(self, board, player):
        """Check if the specified player has won on the given board."""
        # Check rows
        for i in range(0, 9, 3):
            if board[i] == board[i + 1] == board[i + 2] == player:
                return True

        # Check columns
        for i in range(3):
            if board[i] == board[i + 3] == board[i + 6] == player:
                return True

        # Check diagonals
        if board[0] == board[4] == board[8] == player:
            return True
        if board[2] == board[4] == board[6] == player:
            return True

        return False

    def minimax(self, board, depth, is_maximizing):
        """
        MINIMAX algorithm implementation for finding the optimal move.
        Returns the score for the current board state.
        """
        if self._check_winner_board(board, AI):
            return 10 - depth
        if self._check_winner_board(board, PLAYER):
            return depth - 10
        if EMPTY not in board:
            return 0

        if is_maximizing:
            best_score = float('-inf')
            for i in range(9):
                if board[i] == EMPTY:
                    board[i] = AI
                    score = self.minimax(board, depth + 1, False)
                    board[i] = EMPTY
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(9):
                if board[i] == EMPTY:
                    board[i] = PLAYER
                    score = self.minimax(board, depth + 1, True)
                    board[i] = EMPTY
                    best_score = min(score, best_score)
            return best_score

    def get_ai_move(self):
        best_score = float('-inf')
        best_move = None

        for i in range(9):
            if self.board[i] == EMPTY:
                self.board[i] = AI
                score = self.minimax(self.board, 0, False)
                self.board[i] = EMPTY

                if score > best_score:
                    best_score = score
                    best_move = i

        return best_move

    def ai_move(self):
        """Make the AI's move on the board."""
        best_move = self.get_ai_move()
        if best_move is not None:
            self.make_move(best_move)
            return best_move
        return None

    def get_game_status(self):
        if self.game_over:
            if self.winner == PLAYER:
                return "🎉 You won! Congratulations!"
            elif self.winner == AI:
                return "🤖 The AI won! Better luck next time."
            else:
                return "🤝 It's a draw!"
        return "Your turn! You are ❌ and the AI is ⭕."