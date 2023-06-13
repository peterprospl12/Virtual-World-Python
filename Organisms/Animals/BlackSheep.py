from Organisms.Animals.Animal import Animal
from Organisms.Plants.PineBorscht import PineBorscht

BLACK_SHEEP_STRENGTH = 11
BLACK_SHEEP_INITIATIVE = 4


class BlackSheep(Animal):

    def __init__(self, pos_x, pos_y, curr_world):
        super().__init__(BLACK_SHEEP_STRENGTH, BLACK_SHEEP_INITIATIVE, pos_x, pos_y, 'O', "BlackSheep", curr_world)

    def action(self):
        if self.curr_world_.pine_borscht_exist:
            self.strength = 11
            closest_pine_borscht_x, closest_pine_borscht_y = self.find_closest_pine_borscht()
            direction_x = self.pos_x_ - closest_pine_borscht_x
            direction_y = self.pos_y_ - closest_pine_borscht_y

            if direction_x < 0:
                direction_x = 1
            elif direction_x > 0:
                direction_x = -1
            else:
                direction_x = 0

            if direction_y < 0:
                direction_y = 1
            elif direction_y > 0:
                direction_y = -1
            else:
                direction_y = 0

            newX = self.pos_x_ + direction_x
            newY = self.pos_y_ + direction_y

            if 0 <= newX < self.curr_world_.board_size_x and 0 <= newY < self.curr_world_.board_size_y:
                if isinstance(self.curr_world_.getOrganism(newX, newY), PineBorscht):
                    self.curr_world_.infoStream_.append(self.getOrganismInfo() + " ate PineBorscht")
                    self.curr_world_.removeOrganism(self.curr_world_.getOrganism(newX, newY))
                    self.setNewPosition(newX, newY)
                    for organism in self.curr_world_.organisms_:
                        if isinstance(organism, PineBorscht):
                            self.curr_world_.pine_borscht_exist = True
                            break
                        else:
                            self.curr_world_.pine_borscht_exist = False
                else:
                    if newX == self.pos_x_ and newY == self.pos_y_:
                        return

                    if self.curr_world_.getOrganism(newX, newY) is not None:

                        defender = self.curr_world_.getOrganism(newX, newY)

                        if isinstance(defender, Animal):
                            if self.checkMultiply(defender):
                                return

                        if defender.collision(self):
                            return

                        if defender.hasBlocked(self):
                            self.curr_world_.infoStream_.append(
                                self.getOrganismInfo() + " blocked and killed " + defender.getOrganismInfo() + "\n")
                            self.curr_world_.removeOrganism(self)
                        else:
                            self.curr_world_.infoStream_.append(
                                self.getOrganismInfo() + " killed " + defender.getOrganismInfo() + " and moved to (" +
                                str(newX) + ", " + str(newY) + ") \n")
                            self.curr_world_.removeOrganism(self.curr_world_.getOrganism(newX, newY))
                            self.setNewPosition(newX, newY)
                    else:
                        self.curr_world_.infoStream_.append(
                            self.getOrganismInfo() + " has moved to (" + str(newX) + ", " + str(newY) + ") \n")
                        self.setNewPosition(newX, newY)

        else:
            self.strength = 4
            super().action()

    def collision(self, attacker):
        if isinstance(attacker, PineBorscht):
            self.curr_world_.infoStream_.append(attacker.getOrganismInfo() + " ate " + self.getOrganismInfo())
            self.curr_world_.removeOrganism(attacker)
            for organism in self.curr_world_.organisms_:
                if isinstance(organism, PineBorscht):
                    self.curr_world_.pine_borscht_exist = True
                    break
                else:
                    self.curr_world_.pine_borscht_exist = False
        else:
            super().collision(attacker)

    def find_closest_pine_borscht(self):
        closest_pine_borscht = None
        closest_pine_borscht_distance = 1000000
        for i in range(self.curr_world_.board_size_x):
            for j in range(self.curr_world_.board_size_y):
                if self.curr_world_.getOrganism(i, j) is not None and self.curr_world_.getOrganism(i, j).prefix == 'P':
                    distance = abs(self.pos_x_ - i) + abs(self.pos_y_ - j)
                    if distance < closest_pine_borscht_distance:
                        closest_pine_borscht_distance = distance
                        closest_pine_borscht = self.curr_world_.getOrganism(i, j)
        return closest_pine_borscht.pos_x, closest_pine_borscht.pos_y

    def clone(self, clone_pos_x, clone_pos_y):
        cloned = BlackSheep(clone_pos_x, clone_pos_y, self.curr_world_)
        cloned.decrementAge()
        return cloned
