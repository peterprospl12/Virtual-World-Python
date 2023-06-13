import random

from Organisms.Animals.Animal import Animal

ANTELOPE_STRENGTH = 4
ANTELOPE_INITIATIVE = 4


class Antelope(Animal):

    def __init__(self, pos_x, pos_y, curr_world):
        super().__init__(ANTELOPE_STRENGTH, ANTELOPE_INITIATIVE, pos_x, pos_y, 'A', "Antelope", curr_world)

    def makeMove(self, newX, newY):
        newX = self.pos_x_
        newY = self.pos_y_

        moves = [
            [-2, -2], [-2, 0], [-2, 2], [0, -2], [0, 2], [2, -2], [2, 0], [2, 2],
            [-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]
        ]

        try_counter = 0

        while try_counter < 40:
            try_counter += 1
            rand_number = random.randint(0, 15)
            dx = moves[rand_number][0]
            dy = moves[rand_number][1]

            if 0 <= newX + dx < self.curr_world_.board_size_x and 0 <= newY + dy < self.curr_world_.board_size_y:
                newX += dx
                newY += dy

                if newX != self.pos_x_ or newY != self.pos_y_:
                    return newX, newY
        return self.pos_x_, self.pos_y_

    def collision(self, attacker):
        rand_number = random.randint(0, 1)
        counter = 0

        if rand_number == 0:
            newX = self.pos_x_
            newY = self.pos_y_

            oldX = self.pos_x_
            oldY = self.pos_y_

            while self.curr_world_.getOrganism(newX, newY) is not None:
                newX, newY = self.makeMove(newX, newY)
                counter += 1
                if counter > 40:
                    return False

            self.setNewPosition(newX, newY)
            attacker.setNewPosition(oldX, oldY)

            self.curr_world_.infoStream_.append(
                self.getOrganismInfo() + " escaped from " + attacker.getOrganismInfo() + " to (" + str(
                    newX) + ", " + str(newY) + ") \n")
            return True
        else:
            return False

    def clone(self, clone_pos_x, clone_pos_y):
        cloned = Antelope(clone_pos_x, clone_pos_y, self.curr_world_)
        cloned.decrementAge()
        return cloned
