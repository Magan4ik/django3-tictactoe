from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class TicTacToe(models.Model):
    board = models.CharField(max_length=9, default='---------')
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    player = models.CharField(max_length=100, blank=True)  #username
    current_player = models.CharField(max_length=1, default="X")  #username
    winner = models.CharField(max_length=100, default='', blank=True)
    is_draw = models.BooleanField(default=False)
    is_finished = models.BooleanField(default=False)

    def make_move(self, position):  #int [0, 8]
        if not self.is_finished and self.board[position] == '-':
            board_list = list(self.board)
            board_list[position] = self.current_player
            self.board = ''.join(board_list)
            self.check_winner()
            self.check_draw()
            self.switch_players()
            self.save()
            return True
        else:
            return False

    def check_winner(self):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Горизонтальные линии
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Вертикальные линии
            [0, 4, 8], [2, 4, 6]              # Диагональные линии
        ]

        for combination in winning_combinations:
            if (self.board[combination[0]] == self.board[combination[1]] == self.board[combination[2]] != '-'):
                if self.current_player == "X":
                    self.winner = self.creator.username
                else:
                    self.winner = self.player
                self.is_finished = True
                self.save()
                return

    def check_draw(self):
        if '-' not in self.board:
            self.is_draw = True
            self.is_finished = True
            self.save()

    def switch_players(self):
        if self.current_player == "X":
            self.current_player = "O"
        else:
            self.current_player = "X"

    def get_current_player(self):
        if self.current_player == "X":
            return self.creator.username
        else:
            return self.player

    def __str__(self):
        return self.creator.username
