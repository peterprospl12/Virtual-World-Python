from Organisms.Animals.Animal import Animal
from Organisms.Plants.Plant import Plant

PINE_BORSCHT_STRENGTH = 10
PINE_BORSCHT_INITIATIVE = 0


class PineBorscht(Plant):

    def __init__(self, pos_x, pos_y, curr_world):
        super().__init__(PINE_BORSCHT_STRENGTH, PINE_BORSCHT_INITIATIVE, pos_x, pos_y, 'B', "PineBorscht", curr_world)

    def action(self):
        newX = self.pos_x_
        newY = self.pos_y_

        moves = [[0, -1], [0, 1], [-1, 0], [1, 0], [-1, -1], [1, -1], [-1, 1], [1, 1]]

        for i in range(8):
            pos_to_kill_X = newX + moves[i][0]
            pos_to_kill_Y = newY + moves[i][1]

            if 0 <= pos_to_kill_X < self.curr_world_.board_size_x and 0 <= pos_to_kill_Y < self.curr_world_.board_size_y:
                org_to_kill = self.curr_world_.getOrganism(pos_to_kill_X, pos_to_kill_Y)

                if isinstance(org_to_kill, Animal):
                    # add to info stream
                    self.curr_world_.removeOrganism(org_to_kill)

        super().action()

    def collision(self, invader):
        self.curr_world_.removeOrganism(invader)
        # add info stream
        return True

    def clone(self, clone_pos_x, clone_pos_y):
        cloned = PineBorscht(clone_pos_x, clone_pos_y, self.curr_world_)
        cloned.decrementAge()
        return cloned