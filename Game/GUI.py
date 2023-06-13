from tkinter import Tk, Scale, Button, messagebox, Canvas, Toplevel, filedialog, ttk
from tkinter.ttk import Label, Frame
import tkinter.font as tkfont
from PIL import Image, ImageTk

from Organisms.Animals.Antelope import Antelope
from Organisms.Animals.BlackSheep import BlackSheep
from Organisms.Animals.Fox import Fox
from Organisms.Animals.Human import Human
from Organisms.Animals.Sheep import Sheep
from Organisms.Animals.Turtle import Turtle
from Organisms.Animals.Wolf import Wolf
from Organisms.Plants.Dandelion import Dandelion
from Organisms.Plants.Grass import Grass
from Organisms.Plants.Guarana import Guarana
from Organisms.Plants.PineBorscht import PineBorscht
from Organisms.Plants.Wolfberries import WolfBerries


class GUI:
    def __init__(self, curr_world):
        self.info_label = None
        self.square_size = None
        self.canvas = None
        self.board_size_y_scale = None
        self.board_size_x_scale = None
        self.board_size_window = None
        self.board_window = None
        self.root = Tk()
        self.root.title("Piotr Sulewski 19254 - Virtual World")
        self.root.geometry("800x600")

        self.curr_world_ = curr_world
        self.board_size_x = curr_world.board_size_x_
        self.board_size_y = curr_world.board_size_y_

        self.animal_icons = {
            "Antelope": "images/antelope.png",
            "Fox": "images/fox.png",
            "Sheep": "images/sheep.png",
            "Turtle": "images/turtle.png",
            "Wolf": "images/wolf.png",
            "Human": "images/human.png",
            "Grass": "images/grass.png",
            "Guarana": "images/guarana.png",
            "PineBorscht": "images/pineborscht.png",
            "WolfBerries": "images/wolfberries.png",
            "Dandelion": "images/dandelion.png",
            "BlackSheep": "images/blacksheep.png"
        }
        self.animal_icons_on_board = []

        self.selected_animal_icon = None

        self.create_main_menu()

    def create_main_menu(self):
        font = tkfont.Font(size=20)

        # Stylizacja przycisków
        button_style = ttk.Style()
        button_style.configure("Menu.TButton", font=font, padding=10, width=15)

        start_button = ttk.Button(self.root, text="START GAME", command=self.show_board_size_selection,
                                  style="Menu.TButton")
        start_button.pack(pady=10)

        load_button = ttk.Button(self.root, text="LOAD GAME", command=self.load_game, style="Menu.TButton")
        load_button.pack(pady=10)

        exit_button = ttk.Button(self.root, text="EXIT", command=self.root.quit, style="Menu.TButton")
        exit_button.pack(pady=10)


    def show_board_size_selection(self):
        self.board_size_x_scale = None
        self.board_size_y_scale = None

        if self.root.winfo_ismapped():
            self.root.withdraw()

        self.board_size_window = Toplevel(self.root)
        self.board_size_window.title("Piotr Sulewski 19254 - Virtual World")
        self.board_size_window.geometry("900x900")

        size_label = Label(self.board_size_window, text="Select Board Size:", font=("Arial", 14))
        size_label.pack(pady=10)

        self.board_size_x_scale = Scale(self.board_size_window, from_=5, to=20, orient="horizontal", length=200,
                                        command=self.update_board_size_x)
        self.board_size_x_scale.pack(pady=10)

        self.board_size_y_scale = Scale(self.board_size_window, from_=5, to=20, orient="horizontal", length=200,
                                        command=self.update_board_size_y)
        self.board_size_y_scale.pack(pady=10)

        confirm_button = Button(self.board_size_window, text="START", command=self.show_board, font=("Arial", 12))
        confirm_button.pack(pady=10)

    def update_board_size_x(self, value):
        self.board_size_x = int(value)

    def update_board_size_y(self, value):
        self.board_size_y = int(value)

    def show_board(self):
        self.curr_world_.changeBoardSize(self.board_size_x, self.board_size_y)
        self.board_size_window.withdraw()

        self.board_window = Toplevel(self.root)
        self.board_window.title("Piotr Sulewski 19254 - Virtual World")
        self.board_window.geometry("1500x1000")

        self.canvas = Canvas(self.board_window, width=600, height=600)
        self.canvas.pack(side="left")

        self.square_size = 600 // max(self.board_size_x, self.board_size_y)

        for i in range(self.board_size_x):
            for j in range(self.board_size_y):
                x = i * self.square_size
                y = j * self.square_size

                square = self.canvas.create_rectangle(x, y, x + self.square_size, y + self.square_size,
                                                      outline="black", fill="white")
                self.canvas.tag_bind(square, "<Button-1>", lambda event, x=i, y=j: self.square_clicked(x, y))

        buttons_frame = Frame(self.board_window)
        buttons_frame.pack(side="right", padx=20)

        for animal in self.animal_icons.keys():
            button = Button(buttons_frame, text=animal, font=("Arial", 12), width=15,
                            command=lambda animal=animal: self.animal_button_clicked(animal))
            button.pack(pady=10)

        start_button = Button(buttons_frame, text="START GAME", command=self.mainGame, font=("Arial", 12), width=15)
        start_button.pack(pady=10)

    def animal_button_clicked(self, animal):
        self.selected_animal_icon = self.animal_icons[animal]

    def square_clicked(self, x, y):
        organism = self.curr_world_.getOrganism(x, y)

        if self.selected_animal_icon == self.animal_icons["Human"] and self.curr_world_.human_alive_ \
                is True and not isinstance(organism, Human):
            messagebox.showinfo("You can't place more than one human on the board!",
                                "You can't place more than one human on the board!")
        elif organism is not None:
            self.curr_world_.removeOrganism(self.curr_world_.getOrganism(x, y))
            if organism.icon is not None:
                self.canvas.delete(organism.icon)
                organism.icon = None
        else:
            if self.selected_animal_icon is not None:
                animal_name = self.selected_animal_icon.split("/")[-1].split(".")[0]
                new_organism = self.create_new_organism(animal_name, x, y)
                image = Image.open(self.selected_animal_icon)
                image = image.resize((self.square_size, self.square_size), Image.ANTIALIAS)
                image = ImageTk.PhotoImage(image)
                if organism is not None and organism.icon is not None:
                    self.canvas.delete(organism.icon)
                new_organism.icon = self.canvas.create_image(x * self.square_size, y * self.square_size, image=image,
                                                             anchor="nw")
                self.curr_world_.addOrganism(new_organism)
                self.animal_icons_on_board.append(image)

                self.canvas.tag_bind(new_organism.icon, "<Button-1>", lambda event, x=x, y=y: self.square_clicked(x, y))

    def mainGame(self):
        for widget in self.board_window.winfo_children():
            widget.destroy()

        self.canvas = Canvas(self.board_window, width=600, height=600)
        self.canvas.pack(side="left")

        self.square_size = 600 // max(self.board_size_x, self.board_size_y)

        for i in range(self.board_size_x):
            for j in range(self.board_size_y):
                x = i * self.square_size
                y = j * self.square_size

                square = self.canvas.create_rectangle(x, y, x + self.square_size, y + self.square_size,
                                                      outline="black", fill="white")

                organism = self.curr_world_.getOrganism(i, j)
                if organism is not None:
                    image = Image.open(self.animal_icons[organism.name])
                    image = image.resize((self.square_size, self.square_size), Image.ANTIALIAS)
                    image = ImageTk.PhotoImage(image)
                    organism.icon = self.canvas.create_image(x, y, image=image, anchor="nw")
                    self.animal_icons_on_board.append(image)

        info_frame = Frame(self.board_window)
        info_frame.pack(side="right", padx=200)

        self.info_label = Label(info_frame, text="Game Information", font=("Arial", 12), wraplength=900, justify="left")
        self.info_label.pack()

        save_button = Button(self.board_window, text="Save Game", command=self.open_save_dialog)
        save_button.pack(side="top", pady=10)

        self.update_board()

    def open_save_dialog(self):
        filename = filedialog.asksaveasfilename(
            initialfile="game", defaultextension=".world", filetypes=[("World Files", "*.world"), ("All Files", "*.*")]
        )
        if filename:
            self.curr_world_.saveWorld(filename)

    def update_board(self):
        self.canvas.delete("all")

        for i in range(self.board_size_x):
            for j in range(self.board_size_y):
                x = i * self.square_size
                y = j * self.square_size

                square = self.canvas.create_rectangle(x, y, x + self.square_size, y + self.square_size,
                                                      outline="black", fill="white")

                organism = self.curr_world_.getOrganism(i, j)
                if organism is not None:
                    image = Image.open(self.animal_icons[organism.name])
                    image = image.resize((self.square_size, self.square_size), Image.ANTIALIAS)
                    image = ImageTk.PhotoImage(image)
                    organism.icon = self.canvas.create_image(x, y, image=image, anchor="nw")
                    self.animal_icons_on_board.append(image)

        game_info = "\n".join(self.curr_world_.infoStream_)
        game_info = game_info.replace("{", "").replace("}", "")
        self.info_label.config(text=game_info)
        self.curr_world_.infoStream_.clear()
        self.curr_world_.performTurn()
        self.board_window.after(0, self.update_board)
        self.board_window.mainloop()

    def load_game(self):
        file_path = filedialog.askopenfilename(filetypes=[("Game Files", "*.world")])
        if file_path:
            if self.board_window is not None:
                self.board_window.destroy()

            self.curr_world_.loadWorld(file_path)
            self.board_size_y = self.curr_world_.board_size_y
            self.board_size_x = self.curr_world_.board_size_x
            self.root.withdraw()

            self.board_window = Toplevel(self.root)
            self.board_window.title("Game Board")
            self.board_window.geometry("1500x1000")
            self.mainGame()

    def start(self):
        self.root.mainloop()

    def create_new_organism(self, name, posX, posY):
        if name == "antelope":
            return Antelope(posX, posY, self.curr_world_)
        elif name == "fox":
            return Fox(posX, posY, self.curr_world_)
        elif name == "sheep":
            return Sheep(posX, posY, self.curr_world_)
        elif name == "turtle":
            return Turtle(posX, posY, self.curr_world_)
        elif name == "wolf":
            return Wolf(posX, posY, self.curr_world_)
        elif name == "dandelion":
            return Dandelion(posX, posY, self.curr_world_)
        elif name == "grass":
            return Grass(posX, posY, self.curr_world_)
        elif name == "guarana":
            return Guarana(posX, posY, self.curr_world_)
        elif name == "pineborscht":
            return PineBorscht(posX, posY, self.curr_world_)
        elif name == "wolfberries":
            return WolfBerries(posX, posY, self.curr_world_)
        elif name == "human":
            return Human(posX, posY, self.curr_world_)
        elif name == "blacksheep":
            return BlackSheep(posX, posY, self.curr_world_)
