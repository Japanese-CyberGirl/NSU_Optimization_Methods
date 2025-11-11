from ortools.linear_solver import pywraplp

I = int(input("Укажите количество предприятий I: "))
c = list(map(int, input("Введите вектор 'c_i' стоимостей: ").split()))
p = list(map(int, input("Введите вектор 'p_i' доходов: ").split()))
M = int(input("Укажите бюджет компании M: "))
K = int(input("Укажите количество ракет конкурента K: "))

assert len(c) == I and len(p) == I, "Длины c и p должны совпадать с I"
assert M >= 0 and K >= 0

solver = pywraplp.Solver.CreateSolver("SCIP")

x = [solver.IntVar(0 , 1 , f"x_{i}") for i in range(I)]

alpha = solver.NumVar(0.0 , solver.infinity(), "alpha")
beta = [solver.NumVar(0.0 , solver.infinity(), f"beta_{i}") for i in range(I)]
gamma = [solver.NumVar(0.0 , solver.infinity(), f"gamma_{i}") for i in range(I)]

solver.Add(sum(c[i] * x[i] for i in range(I)) <= M)

for i in range(I):
    solver.Add(alpha + beta[i] >= p[i])
    solver.Add(beta[i] <= p[i])
    solver.Add(gamma[i] <= beta[i])
    solver.Add(gamma[i] <= p[i] * x[i])
    solver.Add(gamma[i] >= beta[i] - p[i] * (1 - x[i]))

solver.Maximize(
    solver.Sum(p[i] * x[i] for i in range(I))
    - solver.Sum(gamma[i] for i in range(I))
    - alpha * K
)

status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL:
    x_answer = [int(x[i].solution_value()) for i in range(I)]
    opened = [i for i in range(I) if x_answer[i] == 1]

    print("\n \n \n \n Оптимальное решение найдено! \n")
    print(f"\nИтоговый доход после атаки : {int(solver.Objective().Value())}")
    print(f"\nОткрытые предприятия : {[i+1 for i in opened]}")
    print(f"Количество построенных : {len(opened)}")



else:
    print("\n Оптимальное решение не найдено.")