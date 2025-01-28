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
from tkinter import ttk, messagebox

def generate_permutations_algorithmic(points):
    """Алгоритмическое создание перестановок с учетом ограничений."""
    def permute(points, l, r, result):
        if l == r:
            if satisfies_constraints(points):  # Проверяем ограничение
                result.append(points[:])  # Создаем копию текущего состояния
        else:
            for i in range(l, r + 1):
                points[l], points[i] = points[i], points[l]  # Меняем местами элементы
                permute(points, l + 1, r, result)
                points[l], points[i] = points[i], points[l]  # Возвращаем порядок обратно

    result = []
    permute(points, 0, len(points) - 1, result)
    return result

def generate_permutations_pythonic(points):
    """Создание перестановок с помощью itertools с учетом ограничений."""
    return [list(perm) for perm in itertools.permutations(points) if satisfies_constraints(perm)]

def satisfies_constraints(permutation):
    """Проверяет, удовлетворяет ли перестановка заданным ограничениям."""
    # ограничения: точка P1 должна быть на первом или втором месте
    if "P1" in permutation:
        return permutation.index("P1") in [0, 1]
    return True

def objective_function(permutation):
    """Целевая функция для оценки перестановки."""
    # минимизируем расстояние между первой и последней точкой (условно их индексы)
    return abs(permutation.index("P1") - permutation.index("P5"))

def run_algorithmic(points, output_text):
    start_time = time.time()
    permutations = generate_permutations_algorithmic(points)
    elapsed_time = time.time() - start_time
    output_text.insert(tk.END, f"Алгоритмический метод: {len(permutations)} перестановок за {elapsed_time:.6f} секунд.\n")
    for perm in permutations:
        output_text.insert(tk.END, f"{perm}\n")
    return permutations

def run_pythonic(points, output_text):
    start_time = time.time()
    permutations = generate_permutations_pythonic(points)
    elapsed_time = time.time() - start_time
    output_text.insert(tk.END, f"\nPython функции: {len(permutations)} перестановок за {elapsed_time:.6f} секунд.\n")
    for perm in permutations:
        output_text.insert(tk.END, f"{perm}\n")
    return permutations

def find_best(permutations, output_text):
    best_permutation = min(permutations, key=objective_function)
    best_value = objective_function(best_permutation)
    output_text.insert(tk.END, f"\nОптимальная перестановка: {best_permutation} с целевой функцией: {best_value}\n")

def on_run():
    try:
        k = int(entry_k.get())
        points = [f"P{i}" for i in range(1, k + 1)]
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"Точки: {points}\n\n")

        permutations_algorithmic = run_algorithmic(points, output_text)
        permutations_pythonic = run_pythonic(points, output_text)

        find_best(permutations_pythonic, output_text)
    except ValueError:
        messagebox.showerror("Ошибка", "Введите корректное число точек.")
    except AssertionError as e:
        messagebox.showerror("Ошибка", str(e))

# Создаем графический интерфейс
root = tk.Tk()
root.title("Перестановки точек")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

label_k = ttk.Label(frame, text="Количество точек (k):")
label_k.grid(row=0, column=0, sticky=tk.W)

entry_k = ttk.Entry(frame, width=10)
entry_k.grid(row=0, column=1, sticky=(tk.W, tk.E))

run_button = ttk.Button(frame, text="Запустить", command=on_run)
run_button.grid(row=0, column=2, sticky=tk.E)

output_text = tk.Text(frame, wrap="word", width=80, height=20)
output_text.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E))

scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=output_text.yview)
scrollbar.grid(row=1, column=3, sticky=(tk.N, tk.S))
output_text["yscrollcommand"] = scrollbar.set

root.mainloop()



