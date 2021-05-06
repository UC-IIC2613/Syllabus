import copy
import random
import sys


class Board:
    size = 8

    def __init__(self, b=None):
        if b:
            self.board = copy.deepcopy(b.board)
            self.pos_score = b.pos_score
            self.neg_score = b.neg_score
        else:
            self.board = []
            for i in range(0, Board.size):
                row = [0]*Board.size
                self.board.append(row)
            mid = Board.size // 2
            self.board[mid][mid] = 1
            self.board[mid-1][mid-1] = 1
            self.board[mid-1][mid] = -1
            self.board[mid][mid-1] = -1
            self.pos_score = 2
            self.neg_score = 2
        self.legal_moves_pos = None
        self.legal_moves_neg = None

    def in_board(i, j):
        return i >= 0 and j >= 0 and i < Board.size and j < Board.size

    def legal_moves(self, piece):
        '''
            retorna un arreglo de tuplas de la forma (i,j)
            donde (i,j) es una movida legal
        '''

        if piece == 1 and self.legal_moves_pos:
            return self.legal_moves_pos
        elif piece == -1 and self.legal_moves_neg:
            return self.legal_moves_neg

        def is_legal(i, j):
            if self.board[i][j] != 0:
                return False
            for di in range(-1, 2):
                for dj in range(-1, 2):
                    if di == 0 and dj == 0: continue
                    counter = 0
                    ni = i + di; nj = j + dj
                    while Board.in_board(ni, nj):
                        if self.board[ni][nj] != -piece: break
                        counter += 1
                        ni += di; nj += dj
                    if counter > 0 and Board.in_board(ni, nj)\
                       and self.board[ni][nj] == piece:
                        return True
            return False

        moves = []
        for i in range(0, Board.size):
            for j in range(0, Board.size):
                if is_legal(i, j):
                    moves.append((i, j))
        # almacenamos las movidas en el objeto para hacer mas eficiente
        # multiples llamados a este metodo
        if piece == 1:
            self.legal_moves_pos = moves
        else:
            self.legal_moves_neg = moves
        return moves

    def final(self):
        '''
            Retorna una tuple (Val, piece)
            donde Val es True si el tablero es final (no se puede jugar mas)
        '''
        return self.legal_moves(1) == [] and self.legal_moves(-1) == []

    def winner(self):
        '''
            Suponiendo que el tablero es final, retorna la ficha que gana
        '''
        if self.pos_score > self. neg_score:
            return 1
        elif self.pos_score < self.neg_score:
            return -1
        else:
            return 0

    def piece2str(piece):
        if piece == 1:
            return 'O'
        elif piece == -1:
            return 'X'
        else:
            return '-'

    def show(self, piece=0, moves=None):
        '''
            Imprime el tablero suponiendo que quien juega ahora
            es piece
        '''
        KGRE = "\x1B[32m"
        RESET= "\033[0m"

        if piece!= 0 and not moves:
            moves = self.legal_moves(piece)
        else:
            moves = []
        for i in range(0, Board.size):
            for j in range(0, Board.size):
                if (i, j) in moves:
                    print(KGRE+'{:>2}'.format(moves.index((i, j))+1)+RESET,end='')
                else:
                    print('{:>2}'.format(Board.piece2str(self.board[i][j])),end='')
            print()

    def apply_move(self, m, piece):
        '''
            Suponiendo que la movida m es valida en self,
            retorna el board resultado de aplicar m a self.
        '''
        if not m:  # no hay movida, retornamos el tablero actual
            return self
        i, j = m
        newboard = Board(self)
        newboard.board[i][j] = piece
        if piece == 1:
            newboard.pos_score += 1
        else:
            newboard.neg_score += 1

        for di in range(-1, 2):
            for dj in range(-1, 2):
                if di == 0 and dj == 0: continue
                counter = 0
                ni = i + di; nj = j + dj
                while Board.in_board(ni, nj):
                    if newboard.board[ni][nj] != -piece: break
                    counter += 1
                    ni += di; nj += dj
                if counter > 0 and Board.in_board(ni, nj) \
                   and newboard.board[ni][nj] == piece:
                    ni -= di; nj -= dj
                    while (ni, nj) != (i, j):
                        newboard.board[ni][nj] = piece
                        newboard.pos_score += piece
                        newboard.neg_score -= piece
                        ni -= di; nj -= dj
        return newboard


class Player:
    def __init__(self, piece):
        self.piece = piece

    def get_next_move(self, b, next_move):
        '''
            Usa el metodo next_move para obtener la siguiente movida
            para el jugador. Retorna la movida.
        '''
        moves = b.legal_moves(self.piece)
        if moves == []:
            print('Jugador ' + Board.piece2str(self.piece) + ' pasa')
            return None
        else:
            print('Jugador '+ Board.piece2str(self.piece) +
                  ', ingresa tu movida [1-{}]: '.format(len(moves)),end='')
            sys.stdout.flush()
            m = next_move(b, moves)
            return m


class RandomPlayer(Player):

    def __init__(self, piece):
        super().__init__(piece)

    def get_random_move(self, b, moves):
        i = random.choice(range(0, len(moves)))
        print(i + 1)
        return moves[i]

    def play(self, b):
        return self.get_next_move(b, self.get_random_move)


class HumanPlayer(Player):

    def __init__(self, piece):
        super().__init__(piece)

    def get_move_from_keyboard(self, b, moves):
        while True:
            try:
                i = int(input())
            except ValueError:
                print('Por favor ingresa un número entre 1 y {}: '.format(len(moves)), end='')
                continue
            i -= 1
            if i < 0 or i >= len(moves):
                print('Por favor ingresa un número entre 1 y {}: '.format(len(moves)), end='')
            else:
                break
        return moves[i]

    def play(self, b):
        return self.get_next_move(b, self.get_move_from_keyboard)


class MinimaxPlayer(Player):
    INF = 1000

    def __init__(self, piece, max_depth):
        super().__init__(piece)
        self.max_depth = max_depth

    def minimax_root(self, b, moves):
        moves = b.legal_moves(self.piece)
        values = [self.minimax(b.apply_move(m, self.piece), -self.piece, 1) for m in moves]
        if self.piece == 1:
            play_index = values.index(max(values))
        else:
            play_index = values.index(min(values))
        print(play_index+1)
        return moves[play_index]

    def minimax(self, b, piece, depth):
        if b.final():
            if b.winner() == 1:
                return MinimaxPlayer.INF
            if b.winner() == -1:
                return -MinimaxPlayer.INF
        if depth == self.max_depth:
            return b.pos_score - b.neg_score
        moves = b.legal_moves(piece)
        if moves == []:
            return self.minimax(b, -piece, depth+1)  # pasa!
        values = [self.minimax(b.apply_move(m, piece), -piece, depth+1) for m in moves]
        if piece == 1:
            return max(values)
        else:
            return min(values)

    def play(self, b):
        return self.get_next_move(b, self.minimax_root)


b = Board()
cruz = MinimaxPlayer(-1, 5)
circulo = HumanPlayer(1)

while not b.final():
    b.show(cruz.piece)
    next_move = cruz.play(b)
    b = b.apply_move(next_move, cruz.piece)
    if b.final():
        break
    b.show(circulo.piece)
    next_move = circulo.play(b)
    b = b.apply_move(next_move, circulo.piece)

print('Tablero final:')
b.show()
if b.winner() != 0:
    scores = [b.pos_score, b.neg_score]
    print(Board.piece2str(b.winner())
          + ' ha ganado {}-{}'.format(max(scores), min(scores)))
else:
    print('Ha habido un empate ', b.pos_score, '-', b.neg_score)
