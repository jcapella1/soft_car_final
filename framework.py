from random import choice

class board:
    def __init__(self, size=5, colors=["r", "g", "b", "y"]):
        self.size = size
        self.colors = colors
        self.score = 0
        self.grid = [[choice(colors) for i in range(size)] for j in range(size)]
        self.match()
        self.score = 0
    
    def __repr__(self):
        for i in range(self.size):
            row = ""
            for j in range(self.size):
                row += str(self.grid[i][j]) + " "
            print(row)
        return "Score: " + str(self.score)

    def match(self):
        while True:
            coords = []
            for i in range(self.size):
                row = self.grid[i]
                if group_chk(row) is not None:
                    grps = group_chk(row).split("s")
                    for j in grps[:-1]:
                        self.score += 2 * len(j) - 5
                        listed = [k for k in j]
                        for k in listed:
                            coords.append((i, k))
        
            
            for i in range(self.size):
                column = [self.grid[j][i] for j in range(self.size)]
                if group_chk(column) is not None:
                    grps = group_chk(column).split("s")
                    for k in grps[:-1]:
                        listed = [l for l in k]
                        self.score += 2 * len(k) - 5
                        for l in listed:
                            if (l, i) in coords:
                                self.score += 2
                                continue
                            else:
                                coords.append((l, i))
            
            if coords == []:
                break

            for i in coords:
                self.grid[int(i[0])][int(i[1])] = choice(self.colors)

def group_chk(row):
    i = 0
    j = 0
    positions = []
    row.append("random garbage")
    while j < len(row):
        if row[i] == row[j]:
            j += 1
        elif j - i >= 3:
            for k in range(i, j):
                positions.append(str(k))
            positions.append("s")
            i = j
        else:
            i = j
    if positions == []:
        return None
    return ''.join(positions)


a = board()
print(a)
