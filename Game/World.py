from Game.GUI import GUI
from Organisms.Animals.Sheep import Sheep


def swap(lst, i, j):
    lst[i], lst[j] = lst[j], lst[i]


class World:
    def __init__(self, board_size_x, board_size_y):
        self.board_size_x_ = board_size_x
        self.board_size_y_ = board_size_y
        self.board_ = [[None] * board_size_x for _ in range(board_size_y)]
        self.organisms_ = []
        self.human_alive_ = False
        self.game_saved_ = False
        self.infoStream_ = []
        self.gui = GUI(self)
        self.gui.start()

    def addOrganism(self, organism):
        # dodaj opcje human alive = true
        self.organisms_.append(organism)
        self.board_[organism.pos_y][organism.pos_x] = organism

    def getOrganism(self, pos_x, pos_y):
        return self.board_[pos_y][pos_x]

    def removeOrganism(self, organism):
        # dodac warunek dla humana

        self.board_[organism.pos_y][organism.pos_x] = None
        self.organisms_.remove(organism)

    def setOrganism(self, organism, pos_x, pos_y):
        self.board_[pos_y][pos_x] = organism

    def drawWorld(self):
        print("[ Piotr Sulewski 19254 ]")

        for i in range(-1, self.board_size_y + 1):
            for j in range(-1, self.board_size_x + 1):
                if j == -1:
                    print("# ", end="")
                elif j == self.board_size_x:
                    print("#")
                elif i == -1 or i == self.board_size_y:
                    print("# ", end="")
                else:
                    if self.board_[i][j] is None:
                        print(". ", end="")
                    else:
                        self.board_[i][j].draw()
                        print(" ", end="")

    def sort_organisms(self):
        size = len(self.organisms_)

        for i in range(size):
            for j in range(size - 1):
                if self.organisms_[j].initiative < self.organisms_[j + 1].initiative:
                    swap(self.organisms_, j, j + 1)
                elif self.organisms_[j].initiative == self.organisms_[j + 1].initiative:
                    if self.organisms_[j].age < self.organisms_[j + 1].age:
                        swap(self.organisms_, j, j + 1)

    def performTurn(self):
        self.sort_organisms()

        for currOrg in self.organisms_:
            if self.human_alive_ is False:
                # break
                pass

            if self.game_saved_ is True:
                continue

            if currOrg.age_ > 0:
                currOrg.action()
                currOrg.incrementAge()
            else:
                currOrg.incrementAge()
        self.game_saved_ = False
        self.drawWorld()

        self.gui.board_window.after(1000, self.performTurn)  # Wywołanie performTurn po 1000 ms

    @property
    def board_size_x(self):
        return self.board_size_x_

    @board_size_x.setter
    def board_size_x(self, value):
        self.board_size_x_ = value

    @property
    def board_size_y(self):
        return self.board_size_y_

    @board_size_y.setter
    def board_size_y(self, value):
        self.board_size_y_ = value

    def changeBoardSize(self, new_x, new_y):
        self.board_size_x_ = new_x
        self.board_size_y_ = new_y
        self.board_ = [[None] * new_x for _ in range(new_y)]
