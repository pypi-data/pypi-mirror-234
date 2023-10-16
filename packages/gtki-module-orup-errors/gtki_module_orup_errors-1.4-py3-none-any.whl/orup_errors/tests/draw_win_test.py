from tkinter import *
from orup_errors.main import OrupErrorsManager
from orup_errors.tests.args_test import args
import os

""" Тестируем отрисовку """
# Определяем пути
dirname = os.getcwd()
imgs_dir = os.path.join(dirname, 'imgs')

# Создаем всякие полезные ништяки
root = Tk()
canvas = Canvas(root, bg='black')

# Создаем фото для фона
brutto_bg_png = os.path.join(imgs_dir, 'redbg.png')
tara_bg_png = os.path.join(imgs_dir, 'redbgORupEx.png')
brutto_img = PhotoImage(file=brutto_bg_png)
tara_img = PhotoImage(file=tara_bg_png)

# Присвоим их списку, что бы сборщик мусора не забрал
imgs = [brutto_img, tara_img]

# Ну и главное - делаем  экземпляр проверяльшика, передаем ему все данные
operator = OrupErrorsManager(canvas, imgs[0], imgs[1], text_font="'Roboto' 25")
canvas.pack(fill=BOTH, expand=YES)

# Сформируем словарь с данными
my_args = {}
my_args.update(**args)
my_args['photo_object'] = brutto_img
my_args['xpos'] = 100
my_args['ypos'] = 100

# Кнопочку для вызова туда же
Button(root, text='Show Error', bg='white', command=lambda: operator.check_orup_errors(orup='tara', **my_args)).pack()

root.mainloop()