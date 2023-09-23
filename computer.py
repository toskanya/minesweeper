from cell import *
import random
import copy

class Sentence:
    def __init__(self, cells, mine_count):
        self.cells = set(cells)
        self.mine_count = mine_count
        self.length = len(cells)

    # Return all mines if the sentence contains only mines
    def known_mines(self):
        if len(self.cells) == self.mine_count:
            return self.cells
        else:
            return None

    # Return all safes if the sentence contains only safes
    def known_safes(self):
        if self.mine_count == 0:
            return self.cells
        else:
            return None
    
    # Remove the mines from the sentence because its not an unknown cell anymore
    def mark_mine(self, cell):
        if cell in self.cells:
            self.cells.discard(cell)
            self.mine_count -= 1
        else:
            pass
    
    # Remove the safes from the sentence because its not an unknown cell anymore
    def mark_safe(self, cell):
        if cell in self.cells:
            self.cells.discard(cell)
        else:
            pass

class AI:
    def __init__(self, game):
        # safes and mines which the AI discover
        self.safes = set()
        self.mines = set()
        
        # move made and first move made
        self.moves_made = set()
        self.first_move_made = False

        self.loop = False
        self.finish = False
        self.game = game
        # knowledge base where the AI know if:
        # - the cells surrounding a cell
        # - the mine number of the cell
        self.knowledge = []

    @property
    # return the safe moves which is the substraction of safes set and move_made set
    def safe_move(self):
        return self.safes - self.moves_made
    
    # add the known mine to the mines set and remove it from the knowledge
    def mark_mine(self, cell):
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    # add the known safe to the safes set and remove it from the knowledge
    def mark_safe(self, cell):
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)
        
    # update the knowledge
    def add_knowledge(self, cell):
        # mark as move made
        self.moves_made.add(cell)

        # mark as safe cell
        self.mark_safe(cell)        
        
        
        # get the unknown cells around the current cell and count its total surrounding mines
        count = copy.deepcopy(cell.surrounded_mines_count)
        sur_cells = []
        for sur_cell in cell.surrounded_cells:
            # decrease the initial number of mines if its already known
            if sur_cell in self.mines:
                count -= 1
            # add the surrouding cell into the list if its not known yet
            if sur_cell not in self.mines | self.safes:
                sur_cells.append(sur_cell)
        
        # add sentence to knowledge if the sentence is not empty
        sentence = Sentence(sur_cells, count)
        if len(sentence.cells) > 0:
            self.knowledge.append(sentence)
            
        self.check_knowledge()
                
        self.do_inference()

    # update knowledge if theres any known cells
    def check_knowledge(self):
        for sentence in self.knowledge:
            # if whole sentence contain only mines then get
            mines = sentence.known_mines()
            # if whole sentence contain only safes then get
            safes = sentence.known_safes()

            # remove all known mines in knowledge
            if mines:
                for mine in mines.copy():
                    self.mark_mine(mine)
            # remove all known mines in knowledge
            if safes:
                for safe in safes.copy():
                    self.mark_safe(safe)
    
            # remove empty sentences
            if len(sentence.cells) == 0:
                self.knowledge.remove(sentence)
                    
    # If sentence1 is a subset of sentence2 then:
    # - add new_cells = sentence2.cells - sentence1.cells
    # - add new_count = sentence2.count - sentence1.count
    def do_inference(self):
        knowledge_copy = self.knowledge.copy()
        for sentence1 in knowledge_copy:
            for sentence2 in knowledge_copy:
                if sentence1.cells.issubset(sentence2.cells) and sentence1.cells != sentence2.cells:
                    new_cells = sentence2.cells - sentence1.cells
                    new_count = sentence2.mine_count - sentence1.mine_count
                    new_sentence = Sentence(new_cells, new_count)
        
                    mines = new_sentence.known_mines()
                    safes = new_sentence.known_safes()
                    # remove all known mines in knowledge
                    if mines:
                        for mine in mines.copy():
                            self.mark_mine(mine)
                    # remove all known mines in knowledge
                    if safes:
                        for safe in safes.copy():
                            self.mark_safe(safe)
    
    # make save moves base on the substraction of safes set and moved sets
    def make_safe_move(self):
        for chose_cell in self.safe_move:
            return chose_cell, 'Safe Move: '
        return None, 'Safe Move: '
    
    # make random moves base on the current knowledge
    def make_random_move(self):
        for sentence in self.knowledge:
            if sentence.mine_count != len(sentence.cells):
                cells = list(sentence.cells - self.moves_made)
                random.shuffle(cells)
                for chose_cell in cells:
                    return chose_cell, 'Random Move: '
        return None, 'Random Move: '
    
    # make first move
    def make_first_move(self):
        if not self.first_move_made:
            self.first_move_made = True
            return Cell.random_safe_cell(None), 'First Move: '
        return None, 'First Move: '
        
    def make_move(self, event):
        move_text = None
        move_cell = None
        
        # place flag
        for mine in self.mines:
            if not mine.is_mine_candidate:
                mine.right_click_actions(None)
                print(f'Place flag: ({mine.x}, {mine.y})')
                return
            
        # first move
        move_cell, move_text = self.make_first_move()
        # save move
        if not move_cell:
            move_cell, move_text = self.make_safe_move()
        # random move
        if not move_cell:
            move_cell, move_text = self.make_random_move()
        # finished the game
        if not move_cell or move_cell.is_mine or self.finish:
            self.stop()
            self.finish = True
            if move_cell and move_cell.is_mine:
                print(f"{move_text}({move_cell.x}, {move_cell.y})")
                move_cell.left_click_actions(None)
            print('AI finished playing')
            return

        # using breadth first search to add knowledge
        self.add_knowledge(move_cell)
        if move_cell.surrounded_mines_count == 0:
            safe_cells = []
            safe_cells.append(move_cell)
            while safe_cells:
                safe_cell = safe_cells.pop()
                for cell in safe_cell.surrounded_cells:
                    if cell not in self.moves_made and cell.surrounded_mines_count == 0:
                        safe_cells.append(cell)
                    self.add_knowledge(cell)

        # print(f'Safe cell: {self.safes}')
        # print(f"Move made: {self.moves_made}")
        # print(f'Safe move: {self.safe_move}')
        # print("---------------------------------------------------------------")
        print(f"{move_text}({move_cell.x}, {move_cell.y})")
        # do left click actions
        move_cell.left_click_actions(None)
    
    # start AI loop
    def start(self):
        self.loop = True
        self.move_loop()
    
    # stop AI loop
    def stop(self):
        self.loop = False
        
    # main loop
    def move_loop(self):
        while self.loop:
            self.game.after(10, self.make_move(None))
            self.game.update()
        
    def printAI(self):
        for sentence in self.knowledge:
            print(f"{sentence.cells} = {sentence.mine_count}")
        print()