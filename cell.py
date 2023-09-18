from tkinter import Button, Label, PhotoImage
from random import sample
import settings
import ctypes
import sys

class Cell:
    all = []
    cell_label_object = None
    cell_count = settings.CELL_COUNT
    
    def __init__(self, x, y, is_mine=False):
        self.is_mine = is_mine
        self.is_mine_candidate = False
        self.is_opened = False
        self.cell_btn_object = None
        self.x = x
        self.y = y
        
    def create_btn_object(self, location):
        btn = Button(
            location,
            image=settings.idle,
            width=24,
            height=24
        )
        btn.bind('<Button-1>', self.left_click_actions)
        btn.bind('<Button-3>', self.right_click_actions)
        self.cell_btn_object = btn

        Cell.all.append(self)
        
    @property
    def surrounded_cells(self):
        cells = [
            self.get_cell_by_axis(self.x - 1, self.y - 1),
            self.get_cell_by_axis(self.x - 1, self.y),
            self.get_cell_by_axis(self.x - 1, self.y + 1),
            self.get_cell_by_axis(self.x, self.y - 1),
            self.get_cell_by_axis(self.x, self.y + 1),
            self.get_cell_by_axis(self.x + 1, self.y - 1),
            self.get_cell_by_axis(self.x + 1, self.y),
            self.get_cell_by_axis(self.x + 1, self.y + 1),
        ]
        
        cells = [cell for cell in cells if cell is not None]
        return cells
        
    @property
    def surrounded_mines_count(self):
        count = 0

        for cell in self.surrounded_cells:
            if cell.is_mine:
                count += 1        
        
        return count
        
    def get_cell_by_axis(self, x, y):
        for cell in Cell.all:
            if cell.x == x and cell.y == y:
                return cell
        return None
    
    def show_cell(self):
        if not self.is_opened:
            Cell.cell_count -= 1
            match self.surrounded_mines_count:
                case 0:
                    self.cell_btn_object.config(image=settings.cell0)
                case 1:
                    self.cell_btn_object.config(image=settings.cell1)
                case 2:
                    self.cell_btn_object.config(image=settings.cell2)
                case 3:
                    self.cell_btn_object.config(image=settings.cell3)
                case 4:
                    self.cell_btn_object.config(image=settings.cell4)
                case 5:
                    self.cell_btn_object.config(image=settings.cell5)
                case 6:
                    self.cell_btn_object.config(image=settings.cell6)
                case 7:
                    self.cell_btn_object.config(image=settings.cell7)
                case 8:
                    self.cell_btn_object.config(image=settings.cell8)
            if Cell.cell_label_object:
                Cell.cell_label_object.config(text=f'Cells left: {Cell.cell_count}')
        self.is_opened = True
        
    def show_mine(self):
        self.cell_btn_object.config(image=settings.mine)
        ctypes.windll.user32.MessageBoxW(0, 'You clicked on a mine', 'Game Over', 0)
        sys.exit()
        
    def left_click_actions(self, event):
        if not self.is_mine_candidate:
            if self.is_mine:
                self.show_mine()
            else:
                if self.surrounded_mines_count == 0:
                    safe_cells = [self]
                    while safe_cells:
                        safe_cell = safe_cells.pop()
                        for cell in safe_cell.surrounded_cells:
                            if cell.surrounded_mines_count == 0 and not cell.is_opened:
                                safe_cells.append(cell)
                            cell.show_cell()
                self.show_cell()

    def right_click_actions(self, event):
        if not self.is_opened:
            if not self.is_mine_candidate:
                self.cell_btn_object.config(image=settings.flag)
                self.is_mine_candidate = True
            else:
                self.cell_btn_object.config(image=settings.idle)
                self.is_mine_candidate = False
    
    @staticmethod
    def random_safe_cell(event):
        for cell in Cell.all:
            if cell.surrounded_mines_count == 0 and not cell.is_mine and not cell.is_opened:
                cell.is_mine_candidate = False
                cell.cell_btn_object.config(image=settings.smile)
                break
    
    @staticmethod
    def create_cell_label_object(location):
        label = Label(
            location,
            bg='#4d4d4d',
            fg='white',
            font=('', 30),
            text = f'Cells left: {Cell.cell_count}'
        )
        Cell.cell_label_object = label
    
    @staticmethod
    def randomize_mines():
        picked_mines = sample(
            Cell.all,
            settings.MINES_COUNT
        )
        for mine in picked_mines:
            mine.is_mine = True
    
    def __repr__(self):
        return f'Cell({self.x}, {self.y})'
