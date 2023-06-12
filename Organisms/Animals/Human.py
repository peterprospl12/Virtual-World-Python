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

    def on_key_press(self, event):
        if event.keysym == "Up":
            self.current_key = "Up"
        elif event.keysym == "Down":
            self.current_key = "Down"
        elif event.keysym == "Left":
            self.current_key = "Left"
        elif event.keysym == "Right":
            self.current_key = "Right"
        elif event.keysym == "space":
            self.current_key = "Space"
        elif event.keysym == "Escape":
            self.current_key = "Escape"

    def makeMove(self, newX, newY):
        newX = self.pos_x_
        newY = self.pos_y_
        self.board_window_ = self.curr_world_.gui.board_window
        self.board_window_.bind("<KeyPress>", self.on_key_press)
        self.board_window_.focus_set()
        self.curr_world_.drawWorld()
        while self.current_key not in ["Up", "Down", "Left", "Right"]:
            # Oczekiwanie na ruch gracza
            self.board_window_.update()  # Aktualizacja interfejsu użytkownika
            time.sleep(0.1)  # Opóźnienie, aby nie obciążać zbytnio procesora

        if self.current_key == "Up" and newY >= 1:
            print("up")
            newY -= 1
        elif self.current_key == "Down" and newY < self.curr_world_.board_size_y - 1:
            print("down")
            newY += 1
        elif self.current_key == "Left" and newX >= 1:
            print("left")
            newX -= 1
        elif self.current_key == "Right" and newX < self.curr_world_.board_size_x - 1:
            print("right")
            newX += 1
        self.current_key = None
        return newX, newY

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
