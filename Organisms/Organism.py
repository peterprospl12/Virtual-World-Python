from abc import ABC, abstractmethod


class Organism(ABC):
    def __init__(self, strength, initiative, pos_x, pos_y, prefix, name, curr_world):
        self.strength_ = strength
        self.initiative_ = initiative
        self.pos_x_ = pos_x
        self.pos_y_ = pos_y
        self.curr_world_ = curr_world
        self.prefix_ = prefix
        self.name_ = name
        self.age_ = 1
        self.icon = None

    @abstractmethod
    def action(self):
        pass

    @abstractmethod
    def collision(self, attacker):
        pass

    @abstractmethod
    def makeMove(self, newX, newY):
        pass

    def hasBlocked(self, invader):
        invader_strength = invader.strength_
        defender_strength = self.strength_
        return invader_strength < defender_strength

    def draw(self):
        print(self.prefix_, end="")

    @property
    def pos_x(self):
        return self.pos_x_

    @property
    def pos_y(self):
        return self.pos_y_

    @property
    def strength(self):
        return self.strength_

    @strength.setter
    def strength(self, value):
        self.strength_ = value

    @property
    def age(self):
        return self.age_

    @age.setter
    def age(self, value):
        self.age_ = value

    @property
    def initiative(self):
        return self.initiative_

    def incrementAge(self):
        self.age_ += 1

    def decrementAge(self):
        self.age_ -= 1

    @property
    def name(self):
        return self.name_

    @property
    def prefix(self):
        return self.prefix_

    def getOrganismInfo(self):
        return "[" + self.name_ + "] " + "Age: " + str(self.age_)

    def setNewPosition(self, new_x, new_y):
        self.curr_world_.setOrganism(None, self.pos_x_, self.pos_y_)
        self.pos_x_ = new_x
        self.pos_y_ = new_y
        self.curr_world_.setOrganism(self, self.pos_x_, self.pos_y_)

    @pos_x.setter
    def pos_x(self, value):
        self.pos_x_ = value

    @pos_y.setter
    def pos_y(self, value):
        self.pos_y_ = value
