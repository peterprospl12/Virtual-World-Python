from Organisms.Plants.Plant import Plant

WOLF_BERRIES_STRENGTH = 99
WOLF_BERRIES_INITIATIVE = 0


class WolfBerries(Plant):

    def __init__(self, pos_x, pos_y, curr_world):
        super().__init__(WOLF_BERRIES_STRENGTH, WOLF_BERRIES_INITIATIVE, pos_x, pos_y, 'B', "WolfBerries", curr_world)

    def collision(self, invader):
        self.curr_world_.removeOrganism(invader)
        self.curr_world_.infoStream_.append(invader.getOrganismInfo() + " has eaten " + self.getOrganismInfo() + " and died! \n")
        return True

    def clone(self, clone_pos_x, clone_pos_y):
        cloned = WolfBerries(clone_pos_x, clone_pos_y, self.curr_world_)
        cloned.decrementAge()
        return cloned
