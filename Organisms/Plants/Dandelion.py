from Organisms.Plants.Plant import Plant

DANDELION_STRENGTH = 0
DANDELION_INITIATIVE = 0


class Dandelion(Plant):

    def __init__(self, pos_x, pos_y, curr_world):
        super().__init__(DANDELION_STRENGTH, DANDELION_INITIATIVE, pos_x, pos_y, 'D', "Dandelion", curr_world)

    def action(self):
        for i in range(3):
            super().action()

    def clone(self, clone_pos_x, clone_pos_y):
        cloned = Dandelion(clone_pos_x, clone_pos_y, self.curr_world_)
        cloned.decrementAge()
        return cloned
