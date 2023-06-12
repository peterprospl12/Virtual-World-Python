from Organisms.Animals.Animal import Animal

WOLF_STRENGTH = 9
WOLF_INITIATIVE = 5


class Wolf(Animal):

    def __init__(self, pos_x, pos_y, curr_world):
        super().__init__(WOLF_STRENGTH, WOLF_INITIATIVE, pos_x, pos_y, 'W', "Wolf", curr_world)

    def clone(self, clone_pos_x, clone_pos_y):
        cloned = Wolf(clone_pos_x, clone_pos_y, self.curr_world_)
        cloned.decrementAge()
        return cloned
