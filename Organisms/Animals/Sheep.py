from Organisms.Animals.Animal import Animal

SHEEP_STRENGTH = 4
SHEEP_INITIATIVE = 4


class Sheep(Animal):

    def __init__(self, pos_x, pos_y, curr_world):
        super().__init__(SHEEP_STRENGTH, SHEEP_INITIATIVE, pos_x, pos_y, 'S', "Sheep", curr_world)

    def clone(self, clone_pos_x, clone_pos_y):
        cloned = Sheep(clone_pos_x, clone_pos_y, self.curr_world_)
        cloned.decrementAge()
        return cloned
