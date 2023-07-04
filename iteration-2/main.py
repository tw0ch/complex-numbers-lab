import sys
import math
from tkinter import Tk, Label
from PIL import Image, ImageTk
from cairo import ImageSurface, Context, FORMAT_ARGB32
import numpy as np


# Установите зависимости! Команда:
# pip3 install pillow pycairo tk

# Запустить с параметром 1000 (кл-во точек отображения):
# python3 main.py 1000

class WindowWithLabel(Tk):
    """Класс для окна"""

    def redraw(self):
        '''
        Рисование при помощи cairo Context
        Вызывается при инициализации и при движении мышки
        '''

        self.context = Context(self.surface)

        WIDTH, HEIGHT = self.w, self.h
        axes_x0, axes_y0 = WIDTH // 2, HEIGHT // 2

        # Закрашивание фона белым
        self.context.set_source_rgb(1, 1, 1)
        self.context.rectangle(0, 0, WIDTH, HEIGHT)
        self.context.fill()

        # Рисуем круг ед. окружности
        radius_unit_circle = WIDTH / 5

        self.context.set_source_rgb(0, 0, 1)
        self.context.arc(WIDTH / 2.0, HEIGHT / 2.0, radius_unit_circle, 0, 2 * math.pi)
        self.context.stroke()

        # Рисуем оси
        self.context.set_source_rgba(0, 0, 1, 0.5)
        self.context.set_line_width(2)  # Set line width to 2 pixels
        # X
        self.context.move_to(0, HEIGHT / 2)
        self.context.line_to(WIDTH, HEIGHT / 2)
        # Y
        self.context.move_to(WIDTH / 2, 0)
        self.context.line_to(WIDTH / 2, HEIGHT)
        self.context.stroke()

        # Закрашиваем круг под мышкой (дугу от 0 до 2pi)
        radius_mouse_circle = radius_unit_circle / 10
        self.context.set_source_rgba(0, 0, 1, 0.5)
        self.context.arc(self.mouse_x, self.mouse_y, radius_mouse_circle, 0, 2 * math.pi)
        self.context.fill()

        # Считаем комплексное число и Закрашиваем круги соответсвующие корням
        self.context.set_source_rgb(255, 0, 0)

        x_now, y_now = self.mouse_x - axes_x0, axes_y0 - self.mouse_y

        if x_now == 0:
            x_now = x_now + 1
        if y_now == 0:
            y_now = y_now + 1

        num_points = int(PARAMETER_1)  # Number of points on the airfoil

        lam = 1  # параметр трансформации
        scale = 50  # параметр увеличения
        x0, y0 = x_now / radius_unit_circle, y_now / radius_unit_circle
        R = radius_mouse_circle / 10  # радиус круга под мышкой
        print(f'x: {x0}, y: {y0}, r: {R}')

        # вычислеие кривой для z плоскости
        n = num_points

        x = np.linspace(-R + x0, R + x0, n)
        yu = np.sqrt(R ** 2 - (x - x0) ** 2) + y0  # верхний полу-круг
        yl = -np.sqrt(R ** 2 - (x - x0) ** 2) + y0  # нижний полу-круг

        zu = (x + 1j * yu)  # верхняя кривая
        zl = (x + 1j * yl)  # нижняя кривая

        # zeta plane curve
        zeta_u = (zu + lam ** 2 / zu) * scale
        zeta_l = (zl + lam ** 2 / zl) * scale

        zeta_u_real_list, zeta_u_imag_list = zeta_u.real.tolist(), zeta_u.imag.tolist()
        zeta_l_real_list, zeta_l_imag_list = zeta_l.real.tolist(), zeta_l.imag.tolist()

        for i in range(n):
            self.context.arc(zeta_u_real_list[i] + axes_x0, (-zeta_u_imag_list[i] + axes_y0), 1, 0, 2 * math.pi)
            self.context.arc(zeta_l_real_list[i] + axes_x0, (-zeta_l_imag_list[i] + axes_y0), 1, 0, 2 * math.pi)
            self.context.fill()

        # Далее нарисованное помещается в объект Label на окне
        self._image_ref = ImageTk.PhotoImage(
            Image.frombuffer("RGBA", (self.w, self.h), self.surface.get_data().tobytes(), "raw", "BGRA", 0, 1))
        self.label.image = self._image_ref
        self.label.configure(image=self._image_ref)
        self.label.pack(expand=True, fill="both")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print('Передан параметр ', PARAMETER_1)
        self.mouse_x = 0
        self.mouse_y = 0
        self.w = 800
        self.h = 600

        self.geometry("{}x{}".format(self.w, self.h))

        self.surface = ImageSurface(FORMAT_ARGB32, self.w, self.h)

        self.label = Label(self)
        self.label.bind('<Motion>', self.motion)

        # paint functions

        self.redraw()

        self.mainloop()

    def motion(self, event):
        self.mouse_x, self.mouse_y = event.x, event.y
        self.redraw()


# ДОБАВЬТЕ ДОПОЛНИТЕЛЬНЫЕ ПРОВЕРКИ ДЛЯ ПЕРЕДАННОГО ПАРАМЕТРА ЗДЕСЬ
if len(sys.argv) < 2:
    print("Передайте хотя бы один параметр через командную строку. Например, \npython3 lab.py 8")
    sys.exit()

PARAMETER_1 = sys.argv[1]

if __name__ == "__main__":
    WindowWithLabel()
