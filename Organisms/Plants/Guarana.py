from Organisms.Plants.Plant import Plant

GUARANA_STRENGTH = 0
GUARANA_INITIATIVE = 0


class Guarana(Plant):

    def __init__(self, pos_x, pos_y, curr_world):
        super().__init__(GUARANA_STRENGTH, GUARANA_INITIATIVE, pos_x, pos_y, 'U', "Guarana", curr_world)

    def collision(self, invader):
        invader.strength += 3
        self.curr_world_.infoStream_.append(invader.getOrganismInfo() + " has eaten " + self.getOrganismInfo() + " and gained 3 strength points! \n")
        return False

    def clone(self, clone_pos_x, clone_pos_y):
        cloned = Guarana(clone_pos_x, clone_pos_y, self.curr_world_)
        cloned.decrementAge()
        return cloned
