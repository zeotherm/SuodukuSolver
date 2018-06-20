class cell:
    def __init__(self, row, col, answer=0):
        if answer==0:
            self.answer = 0
            self.possible = set([1,2,3,4,5,6,7,8,9])
            self.solved = False
        else:
            self.answer = answer
            self.possible = set()
            self.solved = True
        self.row = row
        self.col = col
    def __repr__(self):
        if self.solved: return f'[{self.row},{self.col}] solved, {self.answer}'
        else: return f'[{self.row},{self.col}] not solved, possible answers = {self.possible}'
    def __str__(self):
        if self.solved: return str(self.answer)
        else: return 'X'
    def solve(self, n):
        self.answer = n
        self.solved = True
        self.possible = set()

class row_slice:
    def __init__(self, vals):
        self.idx = 0
        self.slice = vals
    def __iter__(self):
        return self
    def __next__(self):
        self.idx += 1
        try:
            return self.slice[self.idx-1]
        except IndexError:
            self.idx = 0
            raise StopIteration
    def __repr__(self):
        resp = 'ROW\n'
        for i in range(9):
            resp += repr(self.slice[i]) + '\n'
        return resp
    def __str__(self):
        resp = ""
        for i in range(9):
            if(self.slice[i].solved): resp += str(self.slice[i].answer)
            else: resp += '_'
        resp += '\n'
        return resp

class col_slice:
    def __init__(self, vals):
        self.idx = 0
        self.slice = vals
    def __iter__(self):
        return self
    def __next__(self):
        self.idx += 1
        try:
            return self.slice[self.idx-1]
        except IndexError:
            self.idx = 0
            raise StopIteration
    def __repr__(self):
        resp = "COLUMN:\n"
        for i in range(9):
            resp += repr(self.slice[i]) + '\n'
        return resp
    def __str__(self):
        resp = ""
        for i in range(9):
            if(self.slice[i].solved): resp += str(self.slice[i].answer)
            else: resp += '_'
            resp += '\n'
        return resp
    
class set_chunk:
    def __init__(self, vals):
        self.idx = 0
        self.chunk = vals
    def __iter__(self):
        return self
    def __next__(self):
        self.idx += 1
        try:
            return self.chunk[(self.idx-1)//3][(self.idx-1)%3]
        except IndexError:
            self.idx = 0
            raise StopIteration
    def __repr__(self):
        resp = ""
        for i in range(3):
            for j in range(3):
                resp += repr(self.chunk[i][j]) + '\n'
        return resp
    def __str__(self):
        resp = ""
        for i in range(3):
            for j in range(3):
                if self.chunk[i][j].solved: resp += str(self.chunk[i][j].answer)
                else: resp += '_'
            resp += '\n'
        return resp
    
class board:
    
    def __init__(self, inp = ""):
        self.b = [[cell(i,j) for i in range(9)] for j in range(9)]
        if( inp != ""):
            rows = inp.split('\n')
            row_count = 0
            for row in rows:
                col_count = 0
                for entry in row:
                    if entry.isdigit(): self.b[row_count][col_count].solve(int(entry))
                    col_count += 1
                row_count += 1
    def __repr__(self):
        resp = ""
        for i in range(9):
            for j in range(9):
                resp += str(self.b[i][j]) + '\n'
        return resp
    def __str__(self):
        resp = ""
        for i in range(9):
            for j in range(9):
                if self.b[i][j].solved: resp += str(self.b[i][j].answer)
                else: resp += '_'
            resp += '\n'
        return resp
    def solveSpace(self, row, col, n):
        self.b[row][col].solve(n)
    def row(self, n):
        return row_slice([self.b[n][c] for c in range(9)])
    def col(self, n):
        return col_slice([self.b[r][n] for r in range(9)])
    def group_idx(self, n):
        if  ( n == 1): upper, lower = (0, 0), (3, 3)
        elif( n == 2): upper, lower = (0, 3), (3, 6)
        elif( n == 3): upper, lower = (0, 6), (3, 9)
        elif( n == 4): upper, lower = (3, 0), (6, 3)
        elif( n == 5): upper, lower = (3, 3), (6, 6)
        elif( n == 6): upper, lower = (3, 6), (6, 9)
        elif( n == 7): upper, lower = (6, 0), (9, 3)
        elif( n == 8): upper, lower = (6, 3), (9, 6)
        else         : upper, lower = (6, 6), (9, 9)
        data = [[self.b[r][c] for c in range(upper[0], lower[0])] for r in range(upper[1], lower[1])]
        return set_chunk(data)
    def group(self, r, c):
        return self.group_idx(self.det_group(r, c))
    def det_group(self, r, c):
        b_groups = [[1, 1, 1, 4, 4, 4, 7, 7, 7],
                    [1, 1, 1, 4, 4, 4, 7, 7, 7],
                    [1, 1, 1, 4, 4, 4, 7, 7, 7],
                    [2, 2, 2, 5, 5, 5, 8, 8, 8],
                    [2, 2, 2, 5, 5, 5, 8, 8, 8],
                    [2, 2, 2, 5, 5, 5, 8, 8, 8],
                    [3, 3, 3, 6, 6, 6, 9, 9, 9],
                    [3, 3, 3, 6, 6, 6, 9, 9, 9],
                    [3, 3, 3, 6, 6, 6, 9, 9, 9]]
        return b_groups[r][c]
    def known(self, r, c):
        #return everything known in the row r
        s = set([cell.answer for cells in self.row(r) if cells.solved])
        return s
if __name__ == "__main__":
    test_board ="""   26 7 1
68  7  9
19   45
82 1   4
  46 29
 5   3 28
  93   74
 4  5  36
7 3 18   """
    b = board(test_board)
    
