'''
Лабораторная работа №7
Требуется для своего варианта второй части л.р. №6 (усложненной программы) разработать реализацию с использованием графического интерфейса. Допускается использовать любую графическую библиотеку питона.  
Рекомендуется использовать внутреннюю библиотеку питона  tkinter.
В программе должны быть реализованы минимум одно окно ввода, одно окно вывода (со скролингом), одно текстовое поле, одна кнопка.
'''
import itertools
import time
import math
import tkinter as tk
from tkinter import ttk, scrolledtext
import random

def is_square(points):
    """Проверка, образуют ли 4 точки квадрат."""
    if len(points) != 4:
        return False

    # Вычисляем все расстояния между точками
    distances = []
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            dist = math.dist(points[i], points[j])
            distances.append(dist)

    distances.sort()

    # У квадрата должно быть 4 равных стороны и 2 равных диагонали
    if len(distances) != 6:
        return False

    side = distances[0]
    diagonal = distances[4]

    return (
        math.isclose(distances[0], side) and
        math.isclose(distances[1], side) and
        math.isclose(distances[2], side) and
        math.isclose(distances[3], side) and
        math.isclose(distances[4], diagonal) and
        math.isclose(distances[5], diagonal) and
        math.isclose(side * math.sqrt(2), diagonal)
    )

def generate_squares_functional(points):
    """Формирование квадратов с использованием функций Python."""
    squares = []
    for combination in itertools.combinations(points, 4):
        # Ограничение: отфильтруем только те комбинации, где минимальная сторона квадрата больше 5
        distances = [math.dist(combination[m], combination[n]) for m in range(4) for n in range(m + 1, 4)]
        if min(distances) > 5 and is_square(combination):
            squares.append(combination)
    return squares

def generate_squares_algorithmic(points):
    """Формирование квадратов алгоритмическим методом."""
    squares = []
    n = len(points)
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                for l in range(k + 1, n):
                    subset = [points[i], points[j], points[k], points[l]]
                    distances = [math.dist(subset[m], subset[n]) for m in range(4) for n in range(m + 1, 4)]
                    if min(distances) > 5 and is_square(subset):
                        squares.append(subset)
    return squares

def generate_random_points(k, x_range=(0, 100), y_range=(0, 100)):
    """Генерация K случайных точек."""
    points = [(random.randint(*x_range), random.randint(*y_range)) for _ in range(k // 2)]
    # Добавляем точки с потенциальной квадратной структурой
    for _ in range(k // 2):
        x, y = random.randint(*x_range), random.randint(*y_range)
        size = random.randint(5, 15)
        points.extend([(x, y), (x + size, y), (x, y + size), (x + size, y + size)])
    return random.sample(points, k)

def calculate():
    try:
        k = int(entry_k.get())
        points = generate_random_points(k)
        output_text.insert(tk.END, f"Сгенерированные точки: {points}\n")

        # Измеряем время для алгоритмического подхода
        start_time = time.time()
        squares_algorithmic = generate_squares_algorithmic(points)
        elapsed_time_algorithmic = time.time() - start_time

        # Измеряем время для функционального подхода
        start_time = time.time()
        squares_functional = generate_squares_functional(points)
        elapsed_time_functional = time.time() - start_time

        output_text.insert(tk.END, f"Найденные квадраты (алгоритмический подход): {squares_algorithmic}\n")
        output_text.insert(tk.END, f"Время выполнения (алгоритмический подход): {elapsed_time_algorithmic:.6f} секунд\n")

        output_text.insert(tk.END, f"Найденные квадраты (функциональный подход): {squares_functional}\n")
        output_text.insert(tk.END, f"Время выполнения (функциональный подход): {elapsed_time_functional:.6f} секунд\n\n")
    except ValueError:
        output_text.insert(tk.END, "Ошибка: Введите корректное число точек.\n")

# Интерфейс пользователя
root = tk.Tk()
root.title("Поиск квадратов на плоскости")

frame_input = ttk.Frame(root, padding="10")
frame_input.grid(row=0, column=0, sticky="EW")

label_k = ttk.Label(frame_input, text="Количество точек (K):")
label_k.grid(row=0, column=0, sticky="W")

entry_k = ttk.Entry(frame_input, width=10)
entry_k.grid(row=0, column=1, sticky="W")

button_calculate = ttk.Button(frame_input, text="Рассчитать", command=calculate)
button_calculate.grid(row=0, column=2, padx=5)

frame_output = ttk.Frame(root, padding="10")
frame_output.grid(row=1, column=0, sticky="NSEW")

output_text = scrolledtext.ScrolledText(frame_output, wrap=tk.WORD, width=50, height=20)
output_text.grid(row=0, column=0, sticky="NSEW")

root.columnconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

frame_output.columnconfigure(0, weight=1)
frame_output.rowconfigure(0, weight=1)

root.mainloop()

