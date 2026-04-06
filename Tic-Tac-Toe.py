import tkinter as tk
from tkinter import messagebox
import numpy as np
import random


class TicTacToeGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tic Tac Toe - Ultimate Edition")
        self.root.geometry("1280x980")
        self.root.configure(bg='white')
        self.root.resizable(False, False)
        self.center_window()

        self.board = np.array([[' ' for _ in range(3)] for _ in range(3)])
        self.player1_symbol = 'X'
        self.player2_symbol = 'O'
        self.current_player = 'X'
        self.game_active = False
        self.game_mode = None
        self.exit_countdown = None
        self.exit_timer_id = None

        self.stats = {'player1': {'wins': 0, 'losses': 0, 'ties': 0},
                      'player2': {'wins': 0, 'losses': 0, 'ties': 0}}

        self.colors = {'bg_primary': 'white', 'bg_secondary': '#f8f9fa', 'accent_blue': '#007bff',
                       'accent_red': '#dc3545', 'accent_green': '#28a745', 'accent_orange': '#fd7e14',
                       'accent_purple': '#6f42c1', 'text_primary': '#212529', 'text_secondary': '#6c757d',
                       'button_bg': '#e9ecef', 'button_hover': '#dee2e6', 'board_border': '#dee2e6'}

        self.setup_ui()
        self.root.bind('<Escape>', lambda e: self.initiate_exit())
        self.root.bind('<F1>', lambda e: self.show_help())
        self.root.bind('<r>', lambda e: self.restart_game())

    def center_window(self):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - 1280) // 2
        y = (self.root.winfo_screenheight() - 980) // 2
        self.root.geometry(f'1280x980+{x}+{y}')

    def show_help(self):
        messagebox.showinfo("Game Help",
                            "🎯 TIC TAC TOE - ULTIMATE EDITION\n\nMODES:\n• Player vs Player\n• Player vs CPU\n\nSYMBOLS:\n• Choose X or O for Player 1\n\nGAMEPLAY:\n• Click empty squares to place your symbol\n• Get three in a row to win\n\n⌨️ SHORTCUTS:\n• R - Restart Game\n• F1 - Help\n• ESC - Exit (2-sec countdown)")

    def setup_ui(self):
        main = tk.Frame(self.root, bg='white')
        main.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)

        # Header
        header = tk.Frame(main, bg='white')
        header.pack(fill=tk.X, pady=(0, 20))
        tk.Label(header, text="TIC TAC TOE", font=('Arial', 28, 'bold'), fg=self.colors['text_primary'],
                 bg='white').pack(side=tk.LEFT)
        self.status_label = tk.Label(header, text="Select game mode to start", font=('Arial', 14),
                                     fg=self.colors['accent_blue'], bg='white')
        self.status_label.pack(side=tk.RIGHT)

        # Options
        options = tk.Frame(main, bg='white', relief='groove', bd=2)
        options.pack(fill=tk.X, pady=(0, 20))

        # Mode selection
        mode_frame = tk.Frame(options, bg='white')
        mode_frame.pack(fill=tk.X, pady=10)
        tk.Label(mode_frame, text="GAME MODE:", font=('Arial', 12, 'bold'), bg='white').pack(side=tk.LEFT,
                                                                                             padx=(20, 10))
        self.mode_var = tk.StringVar(value='pvp')
        tk.Radiobutton(mode_frame, text="Player vs Player", variable=self.mode_var, value='pvp', bg='white',
                       command=self.select_mode).pack(side=tk.LEFT, padx=10)
        tk.Radiobutton(mode_frame, text="Player vs CPU", variable=self.mode_var, value='pvc', bg='white',
                       command=self.select_mode).pack(side=tk.LEFT, padx=10)

        tk.Frame(options, bg=self.colors['board_border'], height=1).pack(fill=tk.X, padx=20, pady=5)

        # Symbol selection
        symbol_frame = tk.Frame(options, bg='white')
        symbol_frame.pack(fill=tk.X, pady=10)
        tk.Label(symbol_frame, text="PLAYER 1 SYMBOL:", font=('Arial', 12, 'bold'), bg='white').pack(side=tk.LEFT,
                                                                                                     padx=(20, 10))
        self.symbol_var = tk.StringVar(value='X')
        tk.Radiobutton(symbol_frame, text="X", variable=self.symbol_var, value='X', bg='white',
                       command=self.select_symbol).pack(side=tk.LEFT, padx=10)
        tk.Radiobutton(symbol_frame, text="O", variable=self.symbol_var, value='O', bg='white',
                       command=self.select_symbol).pack(side=tk.LEFT, padx=10)

        # Game Board & Stats
        content = tk.Frame(main, bg='white')
        content.pack(fill=tk.BOTH, expand=True)

        # Board
        board_container = tk.Frame(content, bg='white')
        board_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        board_bg = tk.Frame(board_container, bg='white')
        board_bg.pack(expand=True)

        self.buttons = []
        for i in range(3):
            row = []
            for j in range(3):
                cell = tk.Frame(board_bg, bg='white', highlightbackground=self.colors['board_border'],
                                highlightthickness=1)
                cell.grid(row=i, column=j, padx=2, pady=2)
                btn = tk.Button(cell, text='', font=('Arial', 32, 'bold'), width=4, height=2, bg='white', relief='flat',
                                cursor='hand2',
                                command=lambda r=i, c=j: self.player_click(r, c))
                btn.pack(padx=1, pady=1)
                btn.bind("<Enter>", lambda e, b=btn: b.config(bg=self.colors['button_hover']) if b[
                                                                                                     'state'] == 'normal' and self.game_active else None)
                btn.bind("<Leave>",
                         lambda e, b=btn: b.config(bg='white') if b['state'] == 'normal' and self.game_active else None)
                row.append(btn)
            self.buttons.append(row)

        # Statistics Panel
        stats = tk.Frame(content, bg='white', width=300)
        stats.pack(side=tk.RIGHT, fill=tk.Y, padx=(40, 0))
        stats.pack_propagate(False)

        tk.Label(stats, text="SCORES", font=('Arial', 18, 'bold'), bg='white').pack(pady=(0, 20))

        scores_row = tk.Frame(stats, bg='white')
        scores_row.pack(fill=tk.X, pady=(0, 30))

        # Player 1 score
        p1_frame = tk.Frame(scores_row, bg='white')
        p1_frame.pack(side=tk.LEFT, expand=True)
        self.player1_label = tk.Label(p1_frame, text="PLAYER 1 (X)", font=('Arial', 12, 'bold'),
                                      fg=self.colors['accent_blue'], bg='white')
        self.player1_label.pack()
        self.player1_score_label = tk.Label(p1_frame, text="0", font=('Arial', 24, 'bold'), bg='white')
        self.player1_score_label.pack(pady=(5, 0))

        # Tie
        tie_frame = tk.Frame(scores_row, bg='white')
        tie_frame.pack(side=tk.LEFT, expand=True)
        tk.Label(tie_frame, text="TIE", font=('Arial', 12, 'bold'), fg=self.colors['text_secondary'], bg='white').pack()
        self.tie_score_label = tk.Label(tie_frame, text="0", font=('Arial', 24, 'bold'), bg='white')
        self.tie_score_label.pack(pady=(5, 0))

        # Player 2 score
        p2_frame = tk.Frame(scores_row, bg='white')
        p2_frame.pack(side=tk.LEFT, expand=True)
        self.player2_label = tk.Label(p2_frame, text="PLAYER 2 (O)", font=('Arial', 12, 'bold'),
                                      fg=self.colors['accent_red'], bg='white')
        self.player2_label.pack()
        self.player2_score_label = tk.Label(p2_frame, text="0", font=('Arial', 24, 'bold'), bg='white')
        self.player2_score_label.pack(pady=(5, 0))

        # Detailed stats
        tk.Label(stats, text="Detailed Statistics", font=('Arial', 14, 'bold'), bg='white').pack(pady=(20, 10))

        p1_stats = tk.Frame(stats, bg=self.colors['bg_secondary'])
        p1_stats.pack(fill=tk.X, pady=5)
        self.player1_stats_label = tk.Label(p1_stats, text="Player 1 (X)", font=('Arial', 11, 'bold'),
                                            fg=self.colors['accent_blue'], bg=self.colors['bg_secondary'])
        self.player1_stats_label.pack(anchor='w', padx=10, pady=5)
        self.player1_wins_label = tk.Label(p1_stats, text="Wins: 0", font=('Arial', 10), bg=self.colors['bg_secondary'])
        self.player1_wins_label.pack(anchor='w', padx=10, pady=2)

        p2_stats = tk.Frame(stats, bg=self.colors['bg_secondary'])
        p2_stats.pack(fill=tk.X, pady=5)
        self.player2_stats_label = tk.Label(p2_stats, text="Player 2 (O)", font=('Arial', 11, 'bold'),
                                            fg=self.colors['accent_red'], bg=self.colors['bg_secondary'])
        self.player2_stats_label.pack(anchor='w', padx=10, pady=5)
        self.player2_wins_label = tk.Label(p2_stats, text="Wins: 0", font=('Arial', 10), bg=self.colors['bg_secondary'])
        self.player2_wins_label.pack(anchor='w', padx=10, pady=2)

        total_stats = tk.Frame(stats, bg=self.colors['bg_secondary'])
        total_stats.pack(fill=tk.X, pady=5)
        self.total_games_label = tk.Label(total_stats, text="Total Games: 0", font=('Arial', 10, 'bold'),
                                          bg=self.colors['bg_secondary'])
        self.total_games_label.pack(anchor='w', padx=10, pady=5)

        # Buttons
        controls = tk.Frame(stats, bg='white')
        controls.pack(fill=tk.X, pady=(20, 0))

        top_btns = tk.Frame(controls, bg='white')
        top_btns.pack(fill=tk.X, pady=(0, 10))

        btn_style = {'font': ('Arial', 10, 'bold'), 'padx': 15, 'pady': 8, 'width': 12, 'relief': 'flat',
                     'cursor': 'hand2'}
        tk.Button(top_btns, text="New Game", bg=self.colors['accent_blue'], fg='white', command=self.restart_game,
                  **btn_style).pack(side=tk.LEFT, padx=5)
        tk.Button(top_btns, text="Reset Scores", bg=self.colors['accent_red'], fg='white',
                  command=self.reset_statistics, **btn_style).pack(side=tk.LEFT, padx=5)

        # Large Exit Button
        self.exit_button = tk.Button(controls, text="🚪 EXIT GAME", font=('Arial', 14, 'bold'),
                                     bg=self.colors['accent_purple'], fg='white',
                                     padx=30, pady=15, relief='raised', bd=3, cursor='hand2',
                                     command=self.initiate_exit)
        self.exit_button.pack(fill=tk.X, pady=5)
        self.exit_button.bind("<Enter>", lambda e: self.exit_button.config(bg='#5a359c') if self.exit_button[
                                                                                                'state'] == 'normal' else None)
        self.exit_button.bind("<Leave>",
                              lambda e: self.exit_button.config(bg=self.colors['accent_purple']) if self.exit_button[
                                                                                                        'state'] == 'normal' else None)

        # Footer
        footer = tk.Frame(main, bg='white')
        footer.pack(fill=tk.X, pady=(20, 0))
        tk.Label(footer, text="Tip: Press R to restart • F1 for help • ESC to exit (2-second countdown)",
                 font=('Arial', 9), fg=self.colors['text_secondary'], bg='white').pack()

        self.update_statistics_display()

    def initiate_exit(self):
        if self.exit_countdown is None:
            self.exit_countdown = 2
            self.exit_button.config(text=f"🚪 EXITING IN {self.exit_countdown}...", bg=self.colors['accent_orange'],
                                    state='disabled')
            self.status_label.config(text="Exiting game in 2 seconds...", fg=self.colors['accent_orange'])
            self.start_exit_countdown()
        else:
            self.cancel_exit()

    def start_exit_countdown(self):
        if self.exit_countdown > 0:
            self.exit_button.config(text=f"🚪 EXITING IN {self.exit_countdown}...")
            self.exit_countdown -= 1
            self.exit_timer_id = self.root.after(1000, self.start_exit_countdown)
        else:
            self.root.quit()

    def cancel_exit(self):
        if self.exit_timer_id:
            self.root.after_cancel(self.exit_timer_id)
        self.exit_countdown = None
        self.exit_button.config(text="🚪 EXIT GAME", bg=self.colors['accent_purple'], state='normal')
        if self.game_active:
            self.status_label.config(text=f"Player 1's turn ({self.player1_symbol})", fg=self.colors['accent_blue'])
        else:
            self.status_label.config(text="Select game mode to start", fg=self.colors['accent_blue'])

    def select_mode(self):
        self.game_mode = self.mode_var.get()
        self.game_active = True
        self.player2_label.config(text="PLAYER 2" if self.game_mode == 'pvp' else "CPU")
        self.player2_stats_label.config(text="Player 2" if self.game_mode == 'pvp' else "CPU")
        self.select_symbol()
        self.status_label.config(text=f"Player 1's turn ({self.player1_symbol})", fg=self.colors['accent_blue'])

    def select_symbol(self):
        if hasattr(self, 'symbol_var'):
            self.player1_symbol = self.symbol_var.get()
            self.player2_symbol = 'O' if self.player1_symbol == 'X' else 'X'
            self.update_symbol_display()

    def update_symbol_display(self):
        if not hasattr(self, 'player1_label'): return
        self.player1_label.config(text=f"PLAYER 1 ({self.player1_symbol})")
        if self.game_mode == 'pvp':
            self.player2_label.config(text=f"PLAYER 2 ({self.player2_symbol})")
            self.player2_stats_label.config(text=f"Player 2 ({self.player2_symbol})")
        else:
            self.player2_label.config(text=f"CPU ({self.player2_symbol})")
            self.player2_stats_label.config(text=f"CPU ({self.player2_symbol})")
        self.player1_stats_label.config(text=f"Player 1 ({self.player1_symbol})")

        if self.player1_symbol == 'X':
            self.player1_label.config(fg=self.colors['accent_blue'])
            self.player2_label.config(fg=self.colors['accent_red'])
        else:
            self.player1_label.config(fg=self.colors['accent_red'])
            self.player2_label.config(fg=self.colors['accent_blue'])

    def update_statistics_display(self):
        self.player1_score_label.config(text=str(self.stats['player1']['wins']))
        self.player2_score_label.config(text=str(self.stats['player2']['wins']))
        self.tie_score_label.config(text=str(self.stats['player1']['ties']))
        self.player1_wins_label.config(
            text=f"Wins: {self.stats['player1']['wins']} • Losses: {self.stats['player1']['losses']} • Ties: {self.stats['player1']['ties']}")
        self.player2_wins_label.config(
            text=f"Wins: {self.stats['player2']['wins']} • Losses: {self.stats['player2']['losses']} • Ties: {self.stats['player2']['ties']}")
        total = sum(self.stats['player1'].values())
        self.total_games_label.config(text=f"Total Games Played: {total}")

    def update_statistics(self, result):
        if result == 'player1':
            self.stats['player1']['wins'] += 1
            self.stats['player2']['losses'] += 1
        elif result == 'player2':
            self.stats['player2']['wins'] += 1
            self.stats['player1']['losses'] += 1
        else:
            self.stats['player1']['ties'] += 1
            self.stats['player2']['ties'] += 1
        self.update_statistics_display()

    def reset_statistics(self):
        self.stats = {'player1': {'wins': 0, 'losses': 0, 'ties': 0}, 'player2': {'wins': 0, 'losses': 0, 'ties': 0}}
        self.update_statistics_display()
        messagebox.showinfo("Scores Reset", "All scores have been reset to zero!")

    def player_click(self, row, col):
        if not self.game_active or self.board[row][col] != ' ': return
        if self.current_player == self.player1_symbol:
            self.make_move(row, col, self.player1_symbol)
            if not self.check_game_over():
                self.current_player = self.player2_symbol
                if self.game_mode == 'pvp':
                    self.status_label.config(text=f"Player 2's turn ({self.player2_symbol})",
                                             fg=self.colors['accent_red'])
                else:
                    self.status_label.config(text="CPU's turn...", fg=self.colors['accent_purple'])
                    self.root.after(800, self.cpu_move)
        elif self.game_mode == 'pvp':
            self.make_move(row, col, self.player2_symbol)
            if not self.check_game_over():
                self.current_player = self.player1_symbol
                self.status_label.config(text=f"Player 1's turn ({self.player1_symbol})", fg=self.colors['accent_blue'])

    def cpu_move(self):
        if not self.game_active or self.current_player != self.player2_symbol: return
        empty = [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == ' ']
        if empty:
            # Try to win
            for r, c in empty:
                self.board[r][c] = self.player2_symbol
                if self.check_winner(self.player2_symbol):
                    self.make_move(r, c, self.player2_symbol)
                    self.check_game_over()
                    return
                self.board[r][c] = ' '
            # Block player
            for r, c in empty:
                self.board[r][c] = self.player1_symbol
                if self.check_winner(self.player1_symbol):
                    self.board[r][c] = ' '
                    self.make_move(r, c, self.player2_symbol)
                    self.current_player = self.player1_symbol
                    self.status_label.config(text=f"Player 1's turn ({self.player1_symbol})",
                                             fg=self.colors['accent_blue'])
                    return
                self.board[r][c] = ' '
            # Strategic move
            if self.board[1][1] == ' ':
                r, c = 1, 1
            else:
                corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
                available = [pos for pos in corners if pos in empty]
                r, c = random.choice(available) if available else random.choice(empty)
            self.make_move(r, c, self.player2_symbol)
            if not self.check_game_over():
                self.current_player = self.player1_symbol
                self.status_label.config(text=f"Player 1's turn ({self.player1_symbol})", fg=self.colors['accent_blue'])

    def make_move(self, row, col, player):
        self.board[row][col] = player
        color = self.colors['accent_blue'] if player == 'X' else self.colors['accent_red']
        self.buttons[row][col].config(text=player, fg=color, state='disabled', bg='white')

    def check_winner(self, player):
        for i in range(3):
            if all(self.board[i][j] == player for j in range(3)): return True
            if all(self.board[j][i] == player for j in range(3)): return True
        if all(self.board[i][i] == player for i in range(3)): return True
        if all(self.board[i][2 - i] == player for i in range(3)): return True
        return False

    def check_game_over(self):
        if self.check_winner(self.player1_symbol):
            self.game_active = False
            self.highlight_winning_line()
            self.status_label.config(text="Player 1 Wins!", fg=self.colors['accent_green'])
            self.update_statistics('player1')
            messagebox.showinfo("Game Over", "Player 1 wins!")
            return True
        elif self.check_winner(self.player2_symbol):
            self.game_active = False
            self.highlight_winning_line()
            winner = "Player 2 Wins!" if self.game_mode == 'pvp' else "CPU Wins!"
            self.status_label.config(text=winner, fg=self.colors['accent_green'])
            self.update_statistics('player2')
            messagebox.showinfo("Game Over", winner)
            return True
        elif all(self.board[i][j] != ' ' for i in range(3) for j in range(3)):
            self.game_active = False
            self.status_label.config(text="It's a Tie!", fg=self.colors['accent_orange'])
            self.update_statistics('tie')
            messagebox.showinfo("Game Over", "It's a tie!")
            return True
        return False

    def highlight_winning_line(self):
        color = '#d4edda'
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != ' ':
                for j in range(3): self.buttons[i][j].config(bg=color)
                return
        for j in range(3):
            if self.board[0][j] == self.board[1][j] == self.board[2][j] != ' ':
                for i in range(3): self.buttons[i][j].config(bg=color)
                return
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            for i in range(3): self.buttons[i][i].config(bg=color)
        elif self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            for i in range(3): self.buttons[i][2 - i].config(bg=color)

    def restart_game(self):
        if not self.game_mode:
            messagebox.showinfo("Select Mode", "Please select a game mode first!")
            return
        self.board = np.array([[' ' for _ in range(3)] for _ in range(3)])
        self.game_active = True
        self.current_player = self.player1_symbol
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text=' ', bg='white', state='normal')
        self.status_label.config(text=f"Player 1's turn ({self.player1_symbol})", fg=self.colors['accent_blue'])

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    print("🎮 Starting Tic Tac Toe - Ultimate Edition...")
    game = TicTacToeGUI()
    game.run()