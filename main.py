import sys
import math
from tkinter import Tk, Label
from PIL import Image, ImageTk
from cairo import ImageSurface, Context, FORMAT_ARGB32


# Установите зависимости! Команда:
# pip3 install pillow pycairo tk

# Запустить с параметром 1:
# python3 lab.py 1

class WindowWithLabel(Tk):
    """Класс для окна"""

    def redraw(self):
        '''
        Рисование при помощи cairo Context
        Вызывается при инициализации и при движении мышки
        '''

        self.context = Context(self.surface)

        WIDTH, HEIGHT = self.w, self.h
        x0, y0 = WIDTH // 2, HEIGHT // 2

        # Закрашивание фона белым
        self.context.set_source_rgb(1, 1, 1)
        self.context.rectangle(0, 0, WIDTH, HEIGHT)
        self.context.fill()

        # Рисуем круг ед. окружности
        self.context.set_source_rgb(0, 0, 1)
        self.context.arc(WIDTH / 2.0, HEIGHT / 2.0, WIDTH / 4.0, 0, 2 * math.pi)
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
        self.context.set_source_rgba(0, 0, 1, 0.5)
        self.context.arc(self.mouse_x, self.mouse_y, 5, 0, 2 * math.pi)
        # self.context.arc(self.mouse_x * 1.1, self.mouse_y * 1.1, 5, 0, 2 * math.pi)
        self.context.fill()

        # Считаем комплексное число и Закрашиваем круги соответсвующие корням
        self.context.set_source_rgb(255, 0, 0)

        x_now, y_now = self.mouse_x - x0, y0 - self.mouse_y

        if x_now == 0:
            x_now = x_now + 1
        if y_now == 0:
            y_now = y_now + 1

        # print(f"window {self.mouse_x, self.mouse_y}")
        print(f"axes: {x_now} / {y_now}")

        fi = math.atan(y_now / x_now)
        n = int(PARAMETER_1)
        z_module = math.sqrt(x_now ** 2 + y_now ** 2)

        for k in range(n):
            complex_root = (z_module ** (1 / n) * math.cos((fi + 2 * math.pi * k) / n) * 34,
                            z_module ** (1 / n) * math.sin((fi + 2 * math.pi * k) / n) * 34)
            print(complex_root)

            self.context.arc((complex_root[0] + x0), (complex_root[1] + y0), 4, 0, 2 * math.pi)
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


# ## ДОБАВЬТЕ ДОПОЛНИТЕЛЬНЫЕ ПРОВЕРКИ ДЛЯ ПЕРЕДАННОГО ПАРАМЕТРА ЗДЕСЬ
# if len(sys.argv) < 2:
#     print("Передайте хотя бы один параметр через командную строку. Например, \npython3 lab.py 8")
#     sys.exit()

PARAMETER_1 = 4

if __name__ == "__main__":
    WindowWithLabel()
