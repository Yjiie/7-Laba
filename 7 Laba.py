'''
Лабораторная работа №7
Требуется для своего варианта второй части л.р. №6 (усложненной программы) разработать реализацию с использованием графического интерфейса. Допускается использовать любую графическую библиотеку питона.  
Рекомендуется использовать внутреннюю библиотеку питона  tkinter.
В программе должны быть реализованы минимум одно окно ввода, одно окно вывода (со скролингом), одно текстовое поле, одна кнопка.
'''
import tkinter as tk
from tkinter import messagebox
import itertools
import math


# Функция для вычисления расстояния между двумя точками
def distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


# Функция для проверки ограничения на расстояние
def check_distance_constraint(permutation, max_distance):
    for i in range(len(permutation) - 1):
        if distance(permutation[i], permutation[i + 1]) > max_distance:
            return False
    return True


# Функция для нахождения всех допустимых обходов с ограничением
def find_valid_tours(points, max_distance):
    valid_tours = []
    for permutation in itertools.permutations(points):
        if check_distance_constraint(permutation, max_distance):
            valid_tours.append(permutation)
    return valid_tours


# Функция для обработки нажатия кнопки
def on_button_click():
    try:
        points_input = points_entry.get()
        points = eval(points_input)
        max_distance = float(max_distance_entry.get())

        valid_tours = find_valid_tours(points, max_distance)

        output_text.delete(1.0, tk.END)
        for tour in valid_tours:
            output_text.insert(tk.END, str(tour) + "\n")

        if not valid_tours:
            messagebox.showinfo("Результат", "Нет допустимых обходов.")

    except Exception as e:
        messagebox.showerror("Ошибка", str(e))


# Создание главного окна
root = tk.Tk()
root.title("Допустимые обходы точек")

# Создание и размещение элементов интерфейса
tk.Label(root, text="Введите точки (например, [(1, 2), (3, 4), (5, 6)]):").pack(pady=5)
points_entry = tk.Entry(root, width=50)
points_entry.pack(pady=5)

tk.Label(root, text="Введите максимальное расстояние:").pack(pady=5)
max_distance_entry = tk.Entry(root, width=10)
max_distance_entry.pack(pady=5)

button = tk.Button(root, text="Найти допустимые обходы", command=on_button_click)
button.pack(pady=10)

output_text = tk.Text(root, height=10, width=50)
output_text.pack(pady=10)

# Запуск главного цикла обработки событий
root.mainloop()

