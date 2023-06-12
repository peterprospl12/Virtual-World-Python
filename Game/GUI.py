from tkinter import Tk, Scale, Button, messagebox, Canvas, Toplevel
from tkinter.ttk import Style, Label, Frame
import tkinter.font as tkfont
from PIL import Image, ImageTk

from Organisms.Animals.Antelope import Antelope
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
        self.board_window = None
        self.root = Tk()
        self.root.title("Main Menu")
        self.root.geometry("800x600")  # Ustawienie rozmiaru okna

        self.curr_world_ = curr_world
        self.board_size_x = curr_world.board_size_x_  # Domyślne rozmiary planszy
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
        }
        self.animal_icons_on_board = []  # Initialize the list

        self.selected_animal_icon = None

        self.create_main_menu()

    def create_main_menu(self):
        font = tkfont.Font(size=20)  # Ustalenie rozmiaru czcionki dla przycisków

        start_button = Button(self.root, text="START GAME", command=self.show_board_size_selection, font=font)
        start_button.pack(pady=20, side="bottom")

        load_button = Button(self.root, text="LOAD GAME", command=self.load_game, font=font)
        load_button.pack(pady=20, side="bottom")

        exit_button = Button(self.root, text="EXIT", command=self.root.quit, font=font)
        exit_button.pack(pady=20, side="bottom")

    def show_board_size_selection(self):
        self.board_size_x_scale = None
        self.board_size_y_scale = None

        if self.root.winfo_ismapped():
            self.root.withdraw()  # Ukryj główne menu

        self.board_size_window = Toplevel(self.root)
        self.board_size_window.title("Board Size Selection")
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
        self.board_size_window.withdraw()  # Ukryj okno wyboru rozmiaru planszy

        self.board_window = Toplevel(self.root)
        self.board_window.title("Game Board")
        self.board_window.geometry("800x600")

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
        if organism is not None:
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

                # Aktualizujemy powiązanie zdarzenia dla kwadratu
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

        buttons_frame = Frame(self.board_window)
        buttons_frame.pack(side="right", padx=20)
        self.update_board()
        self.curr_world_.performTurn()

        self.board_window.mainloop()



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

        self.board_window.after(1000, self.update_board)  # Odświeżanie planszy co 1000 ms


    def load_game(self):
        messagebox.showinfo("Load Game", "Loading game...")
        # Tutaj możesz dodać kod wczytujący zapisaną grę

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
