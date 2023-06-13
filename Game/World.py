from Game.GUI import GUI
from Organisms.Animals.Antelope import Antelope
from Organisms.Animals.BlackSheep import BlackSheep
from Organisms.Animals.Fox import Fox
from Organisms.Animals.Human import Human
from Organisms.Animals.Sheep import Sheep
from Organisms.Animals.Turtle import Turtle
from Organisms.Animals.Wolf import Wolf
from Organisms.Plants.Dandelion import Dandelion
from Organisms.Plants.Grass import Grass
from Organisms.Plants.Guarana import Guarana
from Organisms.Plants.PineBorscht import PineBorscht
from Organisms.Plants.Wolfberries import WolfBerries


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
        self.pine_borscht_exist_ = False
        self.infoStream_ = []
        self.gui = GUI(self)
        self.gui.start()

    def addOrganism(self, organism):
        if isinstance(organism, Human):
            self.human_alive_ = True
        self.organisms_.append(organism)
        self.board_[organism.pos_y][organism.pos_x] = organism

    def getOrganism(self, pos_x, pos_y):
        return self.board_[pos_y][pos_x]

    def removeOrganism(self, organism):
        if isinstance(organism, Human):
            self.human_alive_ = False

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

        for organism in self.organisms_:
            if isinstance(organism, PineBorscht):
                self.pine_borscht_exist = True
                break
            else:
                self.pine_borscht_exist = False

        for currOrg in self.organisms_:
            if self.human_alive_ is False:
                break

            if self.game_saved_ is True:
                continue

            if currOrg.age_ > 0:
                currOrg.action()
                currOrg.incrementAge()
            else:
                currOrg.incrementAge()
        self.game_saved_ = False
        self.drawWorld()

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

    @property
    def pine_borscht_exist(self):
        return self.pine_borscht_exist_

    @pine_borscht_exist.setter
    def pine_borscht_exist(self, value):
        self.pine_borscht_exist_ = value

    def changeBoardSize(self, new_x, new_y):
        self.board_size_x_ = new_x
        self.board_size_y_ = new_y
        self.board_ = [[None] * new_x for _ in range(new_y)]

    def saveWorld(self, filename):
        filename = filename + ".world"

        with open(filename, "w") as saveFile:
            saveFile.write(str(self.board_size_x_) + " " + str(self.board_size_y_) + "\n")

            for organism in self.organisms_:
                saveFile.write(str(organism.prefix) + " ")
                if isinstance(organism, Human):
                    human = organism
                    saveFile.write(str(human.skill_cooldown) + " " + str(human.skill_used) + " ")
                saveFile.write(str(organism.strength) + " " + str(organism.pos_x) + " " +
                               str(organism.pos_y) + " " + str(organism.age) + "\n")

        self.drawWorld()

    def loadWorld(self, file):
        with open(file, 'r') as reader:
            line = reader.readline()
            size = line.split(" ")
            self.board_size_x = int(size[0])
            self.board_size_y = int(size[1])
            self.board_ = [[None] * self.board_size_x for _ in range(self.board_size_y)]
            self.organisms_.clear()

            cooldown = 0
            skillUsed = False
            counter = 0

            for line in reader:
                organism = line.split(" ")
                if organism[counter] == "H":
                    counter += 1
                    cooldown = int(organism[counter])
                    counter += 1
                    skillUsed = bool(organism[counter])

                counter += 1
                strength = int(organism[counter])
                counter += 1
                posX = int(organism[counter])
                counter += 1
                posY = int(organism[counter])
                counter += 1
                age = int(organism[counter])
                counter = 0

                if organism[0] == "H":
                    human = Human(posX, posY, self)
                    human.skill_cooldown = cooldown
                    human.skill_used_ = skillUsed
                    human.age = age
                    human.strength = strength
                    self.addOrganism(human)
                elif organism[0] == "A":
                    antelope = Antelope(posX, posY, self)
                    antelope.strength = strength
                    antelope.age = age
                    self.addOrganism(antelope)
                elif organism[0] == "F":
                    fox = Fox(posX, posY, self)
                    fox.strength = strength
                    fox.age = age
                    self.addOrganism(fox)
                elif organism[0] == "S":
                    sheep = Sheep(posX, posY, self)
                    sheep.strength = strength
                    sheep.age = age
                    self.addOrganism(sheep)
                elif organism[0] == "T":
                    turtle = Turtle(posX, posY, self)
                    turtle.strength = strength
                    turtle.age = age
                    self.addOrganism(turtle)
                elif organism[0] == "W":
                    wolf = Wolf(posX, posY, self)
                    wolf.strength = strength
                    wolf.age = age
                    self.addOrganism(wolf)
                elif organism[0] == "D":
                    dandelion = Dandelion(posX, posY, self)
                    dandelion.strength = strength
                    dandelion.age = age
                    self.addOrganism(dandelion)
                elif organism[0] == "G":
                    grass = Grass(posX, posY, self)
                    grass.age = age
                    self.addOrganism(grass)
                elif organism[0] == "U":
                    guarana = Guarana(posX, posY, self)
                    guarana.age = age
                    self.addOrganism(guarana)
                elif organism[0] == "P":
                    pineBorscht = PineBorscht(posX, posY, self)
                    pineBorscht.age = age
                    self.addOrganism(pineBorscht)
                elif organism[0] == "B":
                    wolfberries = WolfBerries(posX, posY, self)
                    wolfberries.age = age
                    self.addOrganism(wolfberries)
                elif organism[0] == "O":
                    blacksheep = BlackSheep(posX, posY, self)
                    blacksheep.age = age
                    self.addOrganism(blacksheep)

            self.game_saved_ = True
            for organism in self.organisms_:
                if isinstance(organism, PineBorscht):
                    self.pine_borscht_exist = True
                    break
                else:
                    self.pine_borscht_exist = False
            self.drawWorld()
