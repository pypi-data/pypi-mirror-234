import tkinter as tk
from tkinter import messagebox

class TicTacToeGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.resizable(False, False)
        self.root.title("Tic Tac Toe")

        tk.Label(self.root, text="Tic Tac Toe", font=('Arial', 25)).pack()
        self.status_label = tk.Label(self.root, text="X's turn", font=('Arial', 15), bg='green', fg='snow')
        self.status_label.pack(fill=tk.X)

        self.current_chr = "X"
        self.play_area = tk.Frame(self.root, width=300, height=300, bg='white')
        self.XO_points = []
        self.X_points = []
        self.O_points = []
        self.play_again_button = tk.Button(self.root, text='Play again', font=('Arial', 15), command=self.play_again)

        for x in range(1, 4):
            for y in range(1, 4):
                self.XO_points.append(self.XOPoint(x, y))

        self.play_with = "Computer"
        self.play_with_button = tk.Button(self.root, text='Play with human', font=('Arial', 15), command=self.play_with_human)
        self.play_with_button.pack()

        self.play_area.pack(pady=10, padx=10)

        self.root.mainloop()

    def play_again(self):
        self.current_chr = 'X'
        for point in self.XO_points:
            point.button.configure(state=tk.NORMAL)
            point.reset()
        self.status_label.configure(text="X's turn")
        self.play_again_button.pack_forget()

    def play_with_human(self):
        self.play_with = "Human"
        self.play_with_button['text'] = "Play with computer"
        self.play_with_button['command'] = self.play_with_computer
        self.play_again()

    def play_with_computer(self):
        self.play_with = "Computer"
        self.play_with_button['text'] = "Play with human"
        self.play_with_button['command'] = self.play_with_human
        self.play_again()

    class XOPoint:
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.value = None
            self.button = tk.Button(self.play_area, text="", width=10, height=5, command=self.set)
            self.button.grid(row=x, column=y)

        def set(self):
            if not self.value:
                self.button.configure(text=self.current_chr, bg='snow', fg='black')
                self.value = self.current_chr
                if self.current_chr == "X":
                    self.X_points.append(self)
                    self.current_chr = "O"
                    self.status_label.configure(text="O's turn")
                elif self.current_chr == "O":
                    self.O_points.append(self)
                    self.current_chr = "X"
                    self.status_label.configure(text="X's turn")
            self.check_win()
            if self.play_with == "Computer" and self.status_label['text'] == "O's turn":
                self.auto_play()

        def reset(self):
            self.button.configure(text="", bg='lightgray')
            if self.value == "X":
                self.X_points.remove(self)
            elif self.value == "O":
                self.O_points.remove(self)
            self.value = None

    class WinningPossibility:
        def __init__(self, x1, y1, x2, y2, x3, y3):
            self.x1 = x1
            self.y1 = y1
            self.x2 = x2
            self.y2 = y2
            self.x3 = x3
            self.y3 = y3

        def check(self, for_chr):
            self.p1_satisfied = False
            self.p2_satisfied = False
            self.p3_satisfied = False
            if for_chr == 'X':
                for point in self.X_points:
                    if point.x == self.x1 and point.y == self.y1:
                        self.p1_satisfied = True
                    elif point.x == self.x2 and point.y == self.y2:
                        self.p2_satisfied = True
                    elif point.x == self.x3 and point.y == self.y3:
                        self.p3_satisfied = True
            elif for_chr == 'O':
                for point in self.O_points:
                    if point.x == self.x1 and point.y == self.y1:
                        self.p1_satisfied = True
                    elif point.x == self.x2 and point.y == self.y2:
                        self.p2_satisfied = True
                    elif point.x == self.x3 and point.y == self.y3:
                        self.p3_satisfied = True
            return all([self.p1_satisfied, self.p2_satisfied, self.p3_satisfied])

    def disable_game(self):
        for point in self.XO_points:
            point.button.configure(state=tk.DISABLED)
        self.play_again_button.pack()

    def check_win(self):
        winning_possibilities = [
            self.WinningPossibility(1, 1, 1, 2, 1, 3),
            self.WinningPossibility(2, 1, 2, 2, 2, 3),
            self.WinningPossibility(3, 1, 3, 2, 3, 3),
            self.WinningPossibility(1, 1, 2, 1, 3, 1),
            self.WinningPossibility(1, 2, 2, 2, 3, 2),
            self.WinningPossibility(1, 3, 2, 3, 3, 3),
            self.WinningPossibility(1, 1, 2, 2, 3, 3),
            self.WinningPossibility(3, 1, 2, 2, 1, 3)
        ]
        for possibility in winning_possibilities:
            if possibility.check('X'):
                self.status_label.configure(text="X won!")
                self.disable_game()
                return
            elif possibility.check('O'):
                self.status_label.configure(text="O won!")
                self.disable_game()
                return
        if len(self.X_points) + len(self.O_points) == 9:
            self.status_label.configure(text="Draw!")
            self.disable_game()

    def auto_play(self):
        # If winning is possible in the next move
        for winning_possibility in self.winning_possibilities:
            winning_possibility.check('O')
            if winning_possibility.p1_satisfied and winning_possibility.p2_satisfied:
                for point in self.XO_points:
                    if point.x == winning_possibility.x3 and point.y == winning_possibility.y3 and point not in self.X_points + self.O_points:
                        point.set()
                        return
            elif winning_possibility.p2_satisfied and winning_possibility.p3_satisfied:
                for point in self.XO_points:
                    if point.x == winning_possibility.x1 and point.y == winning_possibility.y1 and point not in self.X_points + self.O_points:
                        point.set()
                        return
            elif winning_possibility.p3_satisfied and winning_possibility.p1_satisfied:
                for point in self.XO_points:
                    if point.x == winning_possibility.x2 and point.y == winning_possibility.y2 and point not in self.X_points + self.O_points:
                        point.set()
                        return

        # If the opponent can win in the next move
        for winning_possibility in self.winning_possibilities:
            winning_possibility.check('X')
            if winning_possibility.p1_satisfied and winning_possibility.p2_satisfied:
                for point in self.XO_points:
                    if point.x == winning_possibility.x3 and point.y == winning_possibility.y3 and point not in self.X_points + self.O_points:
                        point.set()
                        return
            elif winning_possibility.p2_satisfied and winning_possibility.p3_satisfied:
                for point in self.XO_points:
                    if point.x == winning_possibility.x1 and point.y == winning_possibility.y1 and point not in self.X_points + self.O_points:
                        point.set()
                        return
            elif winning_possibility.p3_satisfied and winning_possibility.p1_satisfied:
                for point in self.XO_points:
                    if point.x == winning_possibility.x2 and point.y == winning_possibility.y2 and point not in self.X_points + self.O_points:
                        point.set()
                        return

        # If the center is free...
        center_occupied = False
        for point in self.X_points + self.O_points:
            if point.x == 2 and point.y == 2:
                center_occupied = True
                break
        if not center_occupied:
            for point in self.XO_points:
                if point.x == 2 and point.y == 2:
                    point.set()
                    return

        # Occupy corner or middle based on what opponent occupies
        corner_points = [(1, 1), (1, 3), (3, 1), (3, 3)]
        middle_points = [(1, 2), (2, 1), (2, 3), (3, 2)]
        num_of_corner_points_occupied_by_X = 0
        for point in self.X_points:
            if (point.x, point.y) in corner_points:
                num_of_corner_points_occupied_by_X += 1
        if num_of_corner_points_occupied_by_X >= 2:
            for point in self.XO_points:
                if (point.x, point.y) in middle_points and point not in self.X_points + self.O_points:
                    point.set()
                    return
        elif num_of_corner_points_occupied_by_X < 2:
            for point in self.XO_points:
                if (point.x, point.y) in corner_points and point not in self.X_points + self.O_points:
                    point.set()
                    return

