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
        for mi, mj in moves:
            i1, j1 = i + mi, j + mj
            if 0 <= i1 < n and 0 <= j1 < n:
               
                solver.Add(A[i][j] + A[i1][j1] <= 1)


result = solver.Sum(A[i][j] for i in range(n) for j in range(n))

solver.Maximize(result)

status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL:
    print(f"Максимальное количество коней: {solver.Objective().Value()}")
    print("\nМатрица А:")

    for i in range(n):
        for j in range(n):
            print(int(A[i][j].solution_value()), end = " ")
        print()
else:
    print("Решение не найдено.")