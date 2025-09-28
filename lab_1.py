from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver("SCIP")


n = 8
A = []

for i in range(n):
    row = []
    for j in range(n):
        row.append(solver.IntVar(0, 1, f'x_{i}_{j}'))
    A.append(row)

fixed_ceils = [
    (0,5) , (1,1) , (2,5) , (3,4) ,
    (3,5) , (4,5) , (5,1) , (6,5)]

for i, j in fixed_ceils:
    solver.Add(A[i][j] == 1)

moves = [
    (-2, -1) , (-2, 1) , (-1, -2) , (-1, 2) , 
    (1, -2) , (1 , 2) , (2 , -1) , (2 , 1) ]

for i in range(n):
    for j in range(n):
        for mi , mj in  moves:
            i1, j1 = i + di, j + dj
            try:
                temp = A[i1][j1]
                solver.Add(A[i2][j2] <= 1 - A[i][j])
            
            except IndexError:
                continue
