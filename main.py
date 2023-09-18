from tkinter import *

root = Tk()

from cell import Cell
import settings
import utilities

root.geometry(f'{settings.HEIGHT}x{settings.WIDTH}')
root.title('Minesweeper')
root.resizable(True, True)
root.configure(bg='#292929')

top_frame = Frame(
    root,
    bg='#4d4d4d',
    width=settings.WIDTH,
    height=utilities.height_prct(10)
)
top_frame.place(x=0, y=0)

center_frame = Frame(
    root,
    bg='#4d4d4d',
    width=settings.BOARD_WIDTH,
    height=settings.BOARD_HEIGHT
)
center_frame.place(x=utilities.width_prct(8.5), y=utilities.height_prct(14))

for x in range(settings.GRID_SIZE):
    for y in range(settings.GRID_SIZE):
        c = Cell(x, y)
        c.create_btn_object(center_frame)
        c.cell_btn_object.grid(
            column=x,
            row=y
        )

hint = Button(
    top_frame,
    text='Hint',
    width=5,
    height=1,
    
)
hint.bind('<Button-1>', Cell.random_safe_cell)
hint.place(x=50, y=27)

Cell.create_cell_label_object(top_frame)
Cell.cell_label_object.place(x=240, y=15)
Cell.randomize_mines()

root.mainloop()