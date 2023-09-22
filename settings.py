from tkinter import PhotoImage
from PIL import Image, ImageTk

WIDTH = 720
HEIGHT = 720
BOARD_WIDTH = WIDTH * 90 / 100
BOARD_HEIGHT = HEIGHT * 90 / 100
GRID_SIZE = 20
CELL_COUNT = GRID_SIZE ** 2
CELL_SIZE = 30
MINES_COUNT = GRID_SIZE ** 2 // 6

changed = ImageTk.PhotoImage((Image.open('./images/changed.png')).resize((CELL_SIZE, CELL_SIZE)))
flag = ImageTk.PhotoImage((Image.open('./images/flag.png')).resize((CELL_SIZE, CELL_SIZE)))
idle = ImageTk.PhotoImage((Image.open('./images/idle.png')).resize((CELL_SIZE, CELL_SIZE)))
mine = ImageTk.PhotoImage((Image.open('./images/mine.png')).resize((CELL_SIZE, CELL_SIZE)))
smile = ImageTk.PhotoImage((Image.open('./images/smile.png')).resize((CELL_SIZE, CELL_SIZE)))
cell0 = ImageTk.PhotoImage((Image.open('./images/0.png')).resize((CELL_SIZE, CELL_SIZE)))
cell1 = ImageTk.PhotoImage((Image.open('./images/1.png')).resize((CELL_SIZE, CELL_SIZE)))
cell2 = ImageTk.PhotoImage((Image.open('./images/2.png')).resize((CELL_SIZE, CELL_SIZE)))
cell3 = ImageTk.PhotoImage((Image.open('./images/3.png')).resize((CELL_SIZE, CELL_SIZE)))
cell4 = ImageTk.PhotoImage((Image.open('./images/4.png')).resize((CELL_SIZE, CELL_SIZE)))
cell5 = ImageTk.PhotoImage((Image.open('./images/5.png')).resize((CELL_SIZE, CELL_SIZE)))
cell6 = ImageTk.PhotoImage((Image.open('./images/6.png')).resize((CELL_SIZE, CELL_SIZE)))
cell7 = ImageTk.PhotoImage((Image.open('./images/7.png')).resize((CELL_SIZE, CELL_SIZE)))
cell8 = ImageTk.PhotoImage((Image.open('./images/8.png')).resize((CELL_SIZE, CELL_SIZE)))


