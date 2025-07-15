import random
import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error

MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1
ROWS = 3
COLS = 3

symbol_count = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8
}

symbol_value = {
    "A": 5,
    "B": 4,
    "C": 3,
    "D": 2
}

class SlotMachineApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Slot Machine Game")
        self.balance = 0

        # Connect to MySQL Database
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Hresy@wa2",
                database="slot_machine_db"
            )
            if self.conn.is_connected():
                print("Connected to MySQL Database")
                self.cursor = self.conn.cursor()
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            messagebox.showerror("Database Error", str(e))

        # GUI Components
        self.balance_label = tk.Label(root, text=f"Balance: ${self.balance}")
        self.balance_label.pack()

        self.deposit_label = tk.Label(root, text="Deposit Amount:")
        self.deposit_label.pack()
        self.deposit_entry = tk.Entry(root)
        self.deposit_entry.pack()
        self.deposit_button = tk.Button(root, text="Deposit", command=self.deposit)
        self.deposit_button.pack()

        self.lines_label = tk.Label(root, text="Number of Lines (1-3):")
        self.lines_label.pack()
        self.lines_entry = tk.Entry(root)
        self.lines_entry.pack()

        self.bet_label = tk.Label(root, text="Bet Amount Per Line:")
        self.bet_label.pack()
        self.bet_entry = tk.Entry(root)
        self.bet_entry.pack()

        self.spin_button = tk.Button(root, text="Spin", command=self.spin)
        self.spin_button.pack()

        self.result_label = tk.Label(root, text="")
        self.result_label.pack()

        self.slot_display = tk.Label(root, text="", font=("Helvetica", 20))
        self.slot_display.pack()

    def deposit(self):
        amount = self.deposit_entry.get()
        if amount.isdigit():
            self.balance += int(amount)
            self.balance_label.config(text=f"Balance: ${self.balance}")
            self.deposit_entry.delete(0, tk.END)

            # Save balance to database
            self.cursor.execute(
                "INSERT INTO players (balance, bet, winnings) VALUES (%s, %s, %s)",
                (self.balance, 0, 0)
            )
            self.conn.commit()
        else:
            messagebox.showerror("Error", "Please enter a valid amount to deposit.")

    def get_slot_machine_spin(self):
        all_symbols = []
        for symbol, count in symbol_count.items():
            all_symbols.extend([symbol] * count)

        columns = []
        for _ in range(COLS):
            column = random.sample(all_symbols, ROWS)
            columns.append(column)
        return columns

    def check_winnings(self, columns, lines, bet):
        winnings = 0
        winning_lines = []
        for line in range(lines):
            symbol = columns[0][line]
            for column in columns:
                if column[line] != symbol:
                    break
            else:
                winnings += symbol_value[symbol] * bet
                winning_lines.append(line + 1)
        return winnings, winning_lines

    def spin(self):
        try:
            lines = int(self.lines_entry.get())
            bet = int(self.bet_entry.get())

            if lines < 1 or lines > MAX_LINES:
                raise ValueError("Invalid number of lines. Must be between 1 and 3.")
            if bet < MIN_BET or bet > MAX_BET:
                raise ValueError(f"Bet must be between ${MIN_BET} and ${MAX_BET}.")

            total_bet = lines * bet
            if total_bet > self.balance:
                messagebox.showerror("Error", "Insufficient balance.")
                return

            self.balance -= total_bet
            slots = self.get_slot_machine_spin()
            winnings, winning_lines = self.check_winnings(slots, lines, bet)
            self.balance += winnings

            # Display slot machine result
            self.slot_display.config(text="\n".join([" | ".join(column) for column in zip(*slots)]))

            if winnings > 0:
                self.result_label.config(
                    text=f"You won ${winnings} on lines: {', '.join(map(str, winning_lines))}",
                    fg="green"
                )
            else:
                self.result_label.config(text="No winnings this time.", fg="red")

            self.balance_label.config(text=f"Balance: ${self.balance}")

            # Clear entries
            self.lines_entry.delete(0, tk.END)
            self.bet_entry.delete(0, tk.END)

            # Save the result to database
            self.cursor.execute(
                "INSERT INTO players (balance, bet, winnings) VALUES (%s, %s, %s)",
                (self.balance, total_bet, winnings)
            )
            self.conn.commit()

        except ValueError as e:
            messagebox.showerror("Input Error", str(e))

# Run the application
root = tk.Tk()
app = SlotMachineApp(root)
root.mainloop()
