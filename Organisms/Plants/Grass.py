from Organisms.Plants.Plant import Plant

GRASS_STRENGTH = 0
GRASS_INITIATIVE = 0


class Grass(Plant):

    def __init__(self, pos_x, pos_y, curr_world):
        super().__init__(GRASS_STRENGTH, GRASS_INITIATIVE, pos_x, pos_y, 'G', "Grass", curr_world)

    def clone(self, clone_pos_x, clone_pos_y):
        cloned = Grass(clone_pos_x, clone_pos_y, self.curr_world_)
        cloned.decrementAge()
        return cloned
