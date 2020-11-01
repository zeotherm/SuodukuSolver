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
    def process_knowns(self):
        knowns = {i.answer for i in self.slice if i.solved}
        for i in self.slice:
            if not i.answer:
                i.possible -= knowns
        return
    def solve_knowns(self):
        num_solved = 0
        for i in self.slice:
            if len(i.possible) == 1:
                i.solve(i.possible.pop())
                self.process_knowns()
                num_solved += 1
        uniques = unique_element(*[i.possible for i in self.slice])
        while uniques:
            for u in uniques:
                for i in self.slice:
                    if u in i.possible:
                        i.solve(u)
                        self.process_knowns()
                        num_solved += 1
                        break
            uniques = unique_element(*[i.possible for i in self.slice])
        return num_solved


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
    def process_knowns(self):
        knowns = {i.answer for i in self.slice if i.solved}
        for i in self.slice:
            if not i.answer:
                i.possible -= knowns
        return
    def solve_knowns(self):
        num_solved = 0
        for i in self.slice:
            if len(i.possible) == 1:
                i.solve(i.possible.pop())
                self.process_knowns()
                num_solved += 1
        uniques = unique_element(*[i.possible for i in self.slice])
        while uniques:
            for u in uniques:
                for i in self.slice:
                    if u in i.possible:
                        i.solve(u)
                        self.process_knowns()
                        num_solved += 1
                        break
            uniques = unique_element(*[i.possible for i in self.slice])
        return num_solved

    
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

    def process_knowns(self):
        knowns = set([])
        for j in range(3):
            knowns |= {i.answer for i in self.chunk[j] if i.solved}
        for chunk_row in self.chunk:
            for c in chunk_row:
                if not c.answer:
                    c.possible -= knowns
        return
    def solve_knowns(self):
        num_solved = 0
        for r in range(3):
            for c in range(3):
                if len(self.chunk[r][c].possible) == 1:
                    self.chunk[r][c].solve(self.chunk[r][c].possible.pop())
                    num_solved += 1
        poss_sets = []
        for r in range(3):
            for c in range(3):
                poss_sets.append(self.chunk[r][c].possible)
        uniques = unique_element(*poss_sets)
        while uniques:
            for u in uniques:
                for r in range(3):
                    for c in range(3):
                        if u in self.chunk[r][c].possible:
                            self.chunk[r][c].solve(u)
                            self.process_knowns()
                            num_solved += 1
                            break
            poss_sets = []
            for r in range(3):
                for c in range(3):
                    poss_sets.append(self.chunk[r][c].possible)
            uniques = unique_element(*poss_sets)             
                   
        return num_solved


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
        line_break = '+---+---+---+---+---+---+---+---+---+\n'
        resp = ""

        for i in range(9):
            resp += line_break
            resp += '|'
            for j in range(9):
                resp += ' '
                if self.b[i][j].solved: resp += str(self.b[i][j].answer)
                else: resp += '_'
                resp += ' |'
            resp += '\n'
        resp += line_break
        return resp
    def solve_space(self, row, col, n):
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
        return self.group_idx(self._det_group(r, c))
    def _det_group(self, r, c):
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
    def process(self):
        for g in range(9):
            gs = self.group_idx(g)
            gs.process_knowns()
        for r in range(9):
            rs = self.row(r)
            rs.process_knowns()
        for c in range(9):
            cs = self.col(c)
            cs.process_knowns()
        return

    def sanity_check(self):
        for r in range(9):
            for c in range(9):
                if not self.b[r][c].possible and not self.b[r][c].solved:
                    raise RuntimeError('r: ' + str(r) + ', c: ' + str(c))

    def solve_knowns(self):
        num_solved = 0
        for g in range(9):
            num_solved += self.group_idx(g).solve_knowns()
            self.process()
            self.sanity_check()
        for r in range(9):
            num_solved += self.row(r).solve_knowns()
            self.process()
            self.sanity_check()
        for c in range(9):
            num_solved += self.col(c).solve_knowns()
            self.process()
            self.sanity_check()
        self.sanity_check()
        return num_solved

def unique_element(*sets):
    def occurs_in(x, *ss):
        return sum( [1 for s in ss if x in s])

    ans = {x: occurs_in(x, *sets) for x in set.union(*sets)}
    uniqs = {k for k in ans if ans[k] == 1}
    #remove any where multiple uniques occur in only one set
    for s in sets:
        if len(s & uniqs) == len(s) and len(s) > 1:
            for elem in s:
                uniqs.remove(elem)

    return uniqs 

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

    hard_board = """ 8    516
4        
 1 7    9
  729   3
   468   
2   758  
6    2 5 
        8
175    2 """

    hb2 = """  6 1   4
 4  3 178
  8    3 
 24      
 1 7 2 4 
      75 
 8    4  
295 4  8 
4   7 6  """

    v = unique_element(set([1,2,3]), set([2, 3]), set([3, 4]))

    b = board(hb2)
    print(b)
    ns = 1
    while ns > 0:
        b.process()
        ns = b.solve_knowns()
        print("Filled in", ns, "new entries in this pass", sep=' ')
        print(b)
        if ns == 0:
            b.process()
            b.solve_knowns()
            x = 1

    print("SOLVED!!!!")
    print(b)
    
