'''
Лабораторная работа №7
Требуется для своего варианта второй части л.р. №6 (усложненной программы) разработать реализацию с использованием графического интерфейса. Допускается использовать любую графическую библиотеку питона.  
Рекомендуется использовать внутреннюю библиотеку питона  tkinter.
В программе должны быть реализованы минимум одно окно ввода, одно окно вывода (со скролингом), одно текстовое поле, одна кнопка.
'''
import itertools
import time
import tkinter as tk
from tkinter import messagebox

# Функция для проверки, что все точки находятся в пределах области
def valid_path(path, area_limit):
    for p in path:
        if not (area_limit[0] <= p[0] <= area_limit[2] and area_limit[1] <= p[1] <= area_limit[3]):
            return False
    return True

# Алгоритмическая реализация с возвратом для генерации перестановок
def generate_algorithmic(points):
    def generate(current, remaining):
        if len(remaining) == 0:
            permutations.append(list(current))
        else:
            for i in range(len(remaining)):
                generate(current + [remaining[i]], remaining[:i] + remaining[i+1:])
    
    permutations = []
    generate([], points)
    return permutations

# Встроенная функция Python для генерации перестановок
def generate_permutations_python(points):
    return list(itertools.permutations(points))

# Алгоритмическая реализация с ограничениями
def generate_algorithmic_with_limit(points, area_limit):
    def generate(current, remaining):
        if len(remaining) == 0:
            if valid_path(current, area_limit):  # Проверка на корректность пути
                permutations.append(list(current))
        else:
            for i in range(len(remaining)):
                generate(current + [remaining[i]], remaining[:i] + remaining[i+1:])
    
    permutations = []
    generate([], points)
    return permutations

# Встроенная функция Python с ограничениями
def generate_permutations_python_with_limit(points, area_limit):
    valid_permutations = []
    for perm in itertools.permutations(points):
        if valid_path(perm, area_limit):
            valid_permutations.append(perm)
    return valid_permutations

# Функция для запуска генерации и вывода результатов
def run_permutations():
    # Получаем данные из полей ввода
    points_input = points_entry.get()
    area_input = area_entry.get()

    # Преобразуем введенные данные в список точек
    try:
        points = [tuple(map(int, point.split(','))) for point in points_input.split(';')]
        area_limit = tuple(map(int, area_input.split(',')))
    except ValueError:
        messagebox.showerror("Ошибка ввода", "Неверный формат ввода данных. Пожалуйста, введите правильные координаты.")
        return

    # Измеряем время выполнения для алгоритмической реализации без ограничений
    start_time = time.time()
    algorithmic_permutations = generate_algorithmic(points)
    algorithmic_time = time.time() - start_time

    # Измеряем время выполнения для встроенной функции Python без ограничений
    start_time = time.time()
    python_permutations = generate_permutations_python(points)
    python_time = time.time() - start_time

    # Формируем результат для первой части
    result_text.set(f"Алгоритмическая реализация без ограничений: {algorithmic_time:.6f} секунд\n"
                    f"Встроенная функция Python без ограничений: {python_time:.6f} секунд\n")

    # Измеряем время выполнения для алгоритмической реализации с ограничениями
    start_time = time.time()
    algorithmic_permutations_with_limit = generate_algorithmic_with_limit(points, area_limit)
    algorithmic_time_with_limit = time.time() - start_time

    # Измеряем время выполнения для встроенной функции Python с ограничениями
    start_time = time.time()
    python_permutations_with_limit = generate_permutations_python_with_limit(points, area_limit)
    python_time_with_limit = time.time() - start_time

    # Формируем результат для второй части
    result_text.set(result_text.get() + f"Алгоритмическая реализация с ограничениями: {algorithmic_time_with_limit:.6f} секунд\n"
                                        f"Встроенная функция Python с ограничениями: {python_time_with_limit:.6f} секунд\n")

# Настройка графического интерфейса с использованием Tkinter
root = tk.Tk()
root.title("Генерация перестановок точек")

# Создаем поля ввода для точек и области
tk.Label(root, text="Введите точки (x1,y1;x2,y2;...):").pack(pady=5)
points_entry = tk.Entry(root, width=50)
points_entry.pack(pady=5)

tk.Label(root, text="Введите область (x_min,y_min,x_max,y_max):").pack(pady=5)
area_entry = tk.Entry(root, width=50)
area_entry.pack(pady=5)

# Кнопка для запуска генерации
generate_button = tk.Button(root, text="Сгенерировать перестановки", command=run_permutations)
generate_button.pack(pady=10)

# Текстовое поле для отображения результатов с прокруткой
result_text = tk.StringVar()
result_label = tk.Label(root, textvariable=result_text, justify=tk.LEFT, width=70, height=10, relief="solid")
result_label.pack(pady=5)

# Создаем виджет Text с прокруткой для вывода результатов
text_box = tk.Text(root, width=70, height=15, wrap=tk.WORD)
text_box.pack(pady=5)
text_box.config(state=tk.DISABLED)  # Делаем поле текстовым, чтобы нельзя было редактировать

# Функция для обновления текста в поле
def update_text_box(text):
    text_box.config(state=tk.NORMAL)
    text_box.delete(1.0, tk.END)  # Очищаем текстовое поле
    text_box.insert(tk.END, text)  # Вставляем новый текст
    text_box.config(state=tk.DISABLED)

# Запуск графического интерфейса
root.mainloop()
