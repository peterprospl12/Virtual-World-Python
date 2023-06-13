import random

from Organisms.Animals.Animal import Animal

TURTLE_STRENGTH = 2
TURTLE_INITIATIVE = 1


class Turtle(Animal):

    def __init__(self, pos_x, pos_y, curr_world):
        super().__init__(TURTLE_STRENGTH, TURTLE_INITIATIVE, pos_x, pos_y, 'T', "Turtle", curr_world)

    def makeMove(self, newX, newY):
        rand_number = random.randint(0, 3)

        if rand_number != 1:
            return self.pos_x_, self.pos_y_

        return super().makeMove(newX, newY)

    def clone(self, clone_pos_x, clone_pos_y):
        cloned = Turtle(clone_pos_x, clone_pos_y, self.curr_world_)
        cloned.decrementAge()
        return cloned

    def collision(self, attacker):
        if attacker.strength < 5:
            self.curr_world_.infoStream_.append(
                self.getOrganismInfo() + " has defended itself from " + attacker.getOrganismInfo() + " attack! \n")
            return True
        else:
            return False
