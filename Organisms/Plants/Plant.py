import random
from abc import abstractmethod

from Organisms.Organism import Organism

PLANT_INITIATIVE = 0


class Plant(Organism):
    def __init__(self, strength, initiative, pos_x, pos_y, prefix, name, curr_world):
        super().__init__(strength, initiative, pos_x, pos_y, prefix, name, curr_world)

    def collision(self, attacker):
        return False

    def action(self):
        rand_number = random.randint(0, 7)

        if rand_number == 2:
            newX = self.pos_x_
            newY = self.pos_y_

            try_counter = 0

            while self.curr_world_.getOrganism(newX, newY) is not None and try_counter < 40:
                try_counter += 1
                self.makeMove(newX, newY)

            if try_counter >= 40:
                return

            kid = self.clone(newX, newY)
            self.curr_world_.addOrganism(kid)
            # add to infostream

    def makeMove(self, newX, newY):
        newX = self.pos_x_
        newY = self.pos_y_
        moves = [[0, -1], [0, 1], [-1, 0], [1, 0], [-1, -1], [1, -1], [-1, 1], [1, 1]]
        try_counter = 0

        while try_counter < 40:
            try_counter += 1
            rand_number = random.randint(0, 8)
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
