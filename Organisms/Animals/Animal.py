import random
from abc import abstractmethod

from Organisms.Organism import Organism


class Animal(Organism):
    def __init__(self, strength, initiative, pos_x, pos_y, prefix, name, curr_world):
        super().__init__(strength, initiative, pos_x, pos_y, prefix, name, curr_world)

    def action(self):
        newX = self.pos_x_
        newY = self.pos_y_

        newX, newY = self.makeMove(newX, newY)

        if newX == self.pos_x_ and newY == self.pos_y_:
            return

        if self.curr_world_.getOrganism(newX, newY) is not None:


            defender = self.curr_world_.getOrganism(newX, newY)

            if isinstance(defender, Animal):
                if self.checkMultiply(defender):
                    print(self.name_, "has multiplied at", self.pos_x_, self.pos_y_)
                    return

            if defender.collision(self):
                return

            if defender.hasBlocked(self):
                print(self.name_, "has been killed by", defender.name_, "at", defender.pos_x_, defender.pos_y_)
                self.curr_world_.removeOrganism(self)
            else:
                print(defender.name_, "has been killed by", self.name_, "at", self.pos_x_, self.pos_y_)
                self.curr_world_.removeOrganism(self.curr_world_.getOrganism(newX, newY))
                self.setNewPosition(newX, newY)
        else:
            # add to infostream
            self.setNewPosition(newX, newY)

    def collision(self, attacker):
        return False

    def makeMove(self, newX, newY):
        newX = self.pos_x_
        newY = self.pos_y_
        moves = [[0, -1], [0, 1], [-1, 0], [1, 0], [-1, -1], [1, -1], [-1, 1], [1, 1]]
        try_counter = 0

        while try_counter < 40:
            try_counter += 1
            rand_number = random.randint(0, 7)
            dx = moves[rand_number][0]
            dy = moves[rand_number][1]

            if 0 <= newX + dx < self.curr_world_.board_size_x and 0 <= newY + dy < self.curr_world_.board_size_y:
                newX += dx
                newY += dy

                if newX != self.pos_x_ or newY != self.pos_y_:
                    return newX, newY

        return newX, newY

    @abstractmethod
    def clone(self, clone_pos_x, clone_pos_y):
        pass

    def checkMultiply(self, defender):
        if defender is None:
            return False

        if isinstance(defender, self.__class__):
            newX = self.pos_x_
            newY = self.pos_y_
            try_counter = 0
            while self.curr_world_.getOrganism(newX, newY) is not self and try_counter < 40:
                rand_number = random.randint(1, 2)

                if rand_number == 1:
                    self.makeMove(newX, newY)
                else:
                    defender.makeMove(newX, newY)
                try_counter += 1

            if try_counter >= 40:
                return True

            kid = self.clone(newX, newY)
            self.curr_world_.addOrganism(kid)
            # add to infostream
            return True

        return False
