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

        # РИСОВАНИЕ ЕДИНИЧНОЙ ОКРУЖНОСТИ

        WIDTH = self.w
        HEIGHT = self.h
        # Set background color to white
        self.context.set_source_rgb(1, 1, 1)
        self.context.rectangle(0, 0, WIDTH, HEIGHT)
        self.context.fill()

        # Function to help with coordinate transformation
        def to_user_coordinates(x, y):
            return (WIDTH / 2.0) * (x + 1), (HEIGHT / 2.0) * (1 - y)

        # Draw axes
        self.context.set_line_width(2)

        self.context.set_source_rgb(0, 1, 0)

        x0, y0 = to_user_coordinates(0, 0)
        x1, y1 = to_user_coordinates(1, 0)
        # Тут надо что то изменить чтобы он не закрышивал линии при перемещении поинтера вот
        self.context.move_to(*to_user_coordinates(-1, 0))
        self.context.line_to(*to_user_coordinates(1, 0))
        self.context.move_to(*to_user_coordinates(0, -1))
        self.context.line_to(*to_user_coordinates(0, 1))


        self.context.set_source_rgb(0, 0, 1)
        x, y = to_user_coordinates(1, 0)
        self.context.arc(WIDTH / 2.0, HEIGHT / 2.0, WIDTH / 4.0, 0, 2 * math.pi)

        self.context.stroke()


        # Закрашиваем круг под мышкой (дугу от 0 до 2pi)
        self.context.set_source_rgba(0, 0, 1, 0.5)
        self.context.arc(self.mouse_x, self.mouse_y, 5, 0 ,2*math.pi)
        self.context.fill()

        #Далее нарисованное помещается в объект Label на окне
        self._image_ref = ImageTk.PhotoImage(Image.frombuffer("RGBA", (self.w, self.h), self.surface.get_data().tobytes(), "raw", "BGRA", 0, 1))
        self.label.image = self._image_ref
        self.label.configure(image = self._image_ref)
        self.label.pack(expand=True, fill="both")


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print('Передан параметр ', PARAMETER_1)
        self.mouse_x = 0
        self.mouse_y = 0
        self.w, self.h = 800, 600

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


# if len(sys.argv) < 2:
#     print("Передайте хотя бы один параметр через командную строку. Например, \npython3 lab.py 8")
#     sys.exit()



# PARAMETER_1 = sys.argv[1]
PARAMETER_1 = 1

## ДОБАВЬТЕ ДОПОЛНИТЕЛЬНЫЕ ПРОВЕРКИ ДЛЯ ПЕРЕДАННОГО ПАРАМЕТРА ЗДЕСЬ

if __name__ == "__main__":
    WindowWithLabel()