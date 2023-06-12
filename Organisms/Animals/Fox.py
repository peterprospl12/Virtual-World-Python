import random

from Organisms.Animals.Animal import Animal

FOX_STRENGTH = 3
FOX_INITIATIVE = 7


class Fox(Animal):

    def __init__(self, pos_x, pos_y, curr_world):
        super().__init__(FOX_STRENGTH, FOX_INITIATIVE, pos_x, pos_y, 'F', "Fox", curr_world)

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
                    if self.curr_world_.getOrganism(newX, newY) is None:
                        return newX, newY
                    else:
                        if self.curr_world_.getOrganism(newX, newY).strength_ > self.strength_:
                            continue
                        else:
                            return self.pos_x_, self.pos_y_

    def clone(self, clone_pos_x, clone_pos_y):
        cloned = Fox(clone_pos_x, clone_pos_y, self.curr_world_)
        cloned.decrementAge()
        return cloned
