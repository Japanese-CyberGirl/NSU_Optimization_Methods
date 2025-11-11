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

y = [solver.IntVar(0 , 1 , f"y_{i}") for i in range(I)]

destroyed = solver.IntVar(0 , I , "destroyed") #количество уничтоженных объектов

u = solver.IntVar(0 , 1 , "u") #индикатор (уничтожили всё или не всё)

solver.Add(sum(c[i] * x[i] for i in range(I)) <= M) #не выходить за бюджет M

for i in range(I):
    solver.Add(y[i] <= x[i]) #нельзя уничтожать не построенные предприятия

solver.Add(destroyed == solver.Sum(y[i] for i in range(I))) #устанавливаем количество уничтоженных

builded = solver.Sum(x[i] for i in range(I)) #количество построенных

solver.Add(destroyed <= K) #очевидно

solver.Add(destroyed <= builded) #очевидно



solver.Add(builded - K + 1 <= I * u) #если уничтожили всё, то u = 0, иначе 1

solver.Add(destroyed >= K - I * (1 - u)) #если уничтожили не всё, то des >= K => des = K
                #если уничтожили всё => des >= K - I (это может быть как меньше 0, так и больше 0, так и равно 0)

solver.Add(destroyed >= builded - I * u)

#если уничтожили не всё, то des >= builded - I => des >= 0

#если уничтожили всё, то des >= builded => des = builded

#что мы получили к этому моменту
#destroyed = min(K, builded) (если уничтожили всё)
#destroyed = K (если уничтожили не всё)

for i in range(I):
    for j in range(I):
        if p[i] > p[j]:
            solver.Add(y[j] <= y[i] + (1 - x[i])) #нельзя уничтожать, если можно уничтожить другое, более дорогое

solver.Maximize(solver.Sum(p[i] * (x[i] - y[i]) for i in range(I)))

status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL:

    x_answer = [int(x[i].solution_value()) for i in range(I)]
    y_answer = [int((y[i].solution_value())) for i in range(I)]
    destroyed_val = int(destroyed.solution_value())
    builded_val = int(builded.solution_value())


    opened = [i for i in range(I) if x_answer[i] == 1]
    attacked = [i for i in range(I) if y_answer[i] == 1]
    dohod_do = sum(p[i] for i in opened)
    dohod_posle = sum(p[i] for i in opened if y_answer[i] == 0) 


    print("\n \n \n \n Оптимальное решение найдено! \n")
    print(f"\nИтоговый доход после атаки : {dohod_posle}")
    print(f"\nОткрытые предприятия : {[i+1 for i in opened]}")
    print(f"\nАтакованные предприятия : {[i+1 for i in attacked]}\n")

    print("Предприятия:")
    print("i | c_i | p_i | открыт (x) | атакован (y)")
    for i in range(I):
        print(f"{i+1} | {c[i]}  | {p[i]} |    {x_answer[i]}    |    {y_answer[i]}")

    print(f"Количество построенных : {builded_val}")
    print(f"Количество уничтоженных : {destroyed_val}")
    print(f"Доход до атаки конкурента : {dohod_do}")
    print(f"Доход после атаки конкурента : {dohod_posle}")

else:
    print("\n Оптимальное решение не найдено.")