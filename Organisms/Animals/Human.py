import time

from Organisms.Animals.Animal import Animal

HUMAN_STRENGTH = 5
HUMAN_INITIATIVE = 4


class Human(Animal):

    def __init__(self, pos_x, pos_y, curr_world):
        super().__init__(HUMAN_STRENGTH, HUMAN_INITIATIVE, pos_x, pos_y, 'H', "Human", curr_world)
        self.skill_cooldown_ = 0
        self.skill_used_ = False
        self.board_window_ = None
        self.current_key = None

    def makeMove(self, newX, newY):
        self.current_key = None
        self.move_ready = False
        self.board_window_ = self.curr_world_.gui.board_window
        self.board_window_.bind("<KeyPress>", self.on_key_press)
        self.board_window_.focus_set()

        while not self.move_ready:
            self.board_window_.update()
            time.sleep(0.1)

        moveX = newX
        moveY = newY

        if self.current_key == "Up" and newY >= 1:
            print("up")
            moveY -= 1
        elif self.current_key == "Down" and newY < self.curr_world_.board_size_y - 1:
            print("down")
            moveY += 1
        elif self.current_key == "Left" and newX >= 1:
            print("left")
            moveX -= 1
        elif self.current_key == "Right" and newX < self.curr_world_.board_size_x - 1:
            print("right")
            moveX += 1
        elif self.current_key == "Escape":
            self.curr_world_.gui.load_game()
        elif self.current_key == "Caps_Lock":
            if self.skill_cooldown == 0:
                self.skill_used = True
                self.skill_cooldown = 11
                self.curr_world_.infoStream_.append(self.getOrganismInfo() + " used skill!")
            else:
                self.curr_world_.infoStream_.append(self.getOrganismInfo() + " skill is on cooldown!")

            return self.pos_x_, self.pos_y_

        if self.skill_used is True:
            self.skill_cooldown -= 1
            if self.skill_cooldown < 6:
                if self.skill_cooldown == 0:
                    self.skill_used = False
            else:
                curr_pos_x = self.pos_x_
                curr_pos_y = self.pos_y_
                pos_to_skip_x = -10
                pos_to_skip_y = -10
                moves = [[0, -1], [0, 1], [-1, 0], [1, 0], [-1, -1], [1, -1], [-1, 1], [1, 1]]

                for i in range(8):
                    pos_to_kill_x = curr_pos_x + moves[i][0]
                    pos_to_kill_y = curr_pos_y + moves[i][1]

                    if pos_to_kill_x == pos_to_skip_x and pos_to_kill_y == pos_to_skip_y:
                        continue

                    if 0 <= pos_to_kill_x < self.curr_world_.board_size_x and 0 <= pos_to_kill_y < self.curr_world_.board_size_y:
                        if self.curr_world_.getOrganism(pos_to_kill_x, pos_to_kill_y) is not None:
                            self.curr_world_.infoStream_.append(
                                self.getOrganismInfo() + " has killed " + self.curr_world_.getOrganism(pos_to_kill_x,
                                                                                                       pos_to_kill_y).getOrganismInfo() + " with his skill! \n")
                            self.curr_world_.removeOrganism(self.curr_world_.getOrganism(pos_to_kill_x, pos_to_kill_y))

                self.curr_world_.infoStream_.append(
                    self.getOrganismInfo() + " skill is activated for " + str(self.skill_cooldown - 5) + " turns! \n")

        return moveX, moveY

    def on_key_press(self, event):
        if event.keysym in ["Up", "Down", "Left", "Right", "Caps_Lock", "Escape"]:
            self.current_key = event.keysym
            self.move_ready = True

    @property
    def skill_cooldown(self):
        return self.skill_cooldown_

    @skill_cooldown.setter
    def skill_cooldown(self, value):
        self.skill_cooldown_ = value

    @property
    def skill_used(self):
        return self.skill_used_

    @skill_used.setter
    def skill_used(self, value):
        self.skill_used_ = value

    def clone(self, clone_pos_x, clone_pos_y):
        return None
