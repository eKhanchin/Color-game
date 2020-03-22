#!/usr/intel/bin/python -w


from tkinter import *
from tkinter import ttk
import random


class ColorGameApp:
    def __init__(self, master):
        self._master = master
        self._master.title('Color Game')
        self._master.geometry('500x320+500+300')
        self._master.resizable(0, 0)

        # App's variables
        self._header_label_font = ('Calibri', '12')
        self._body_label_font = ('Calibri', '14')
        self._start_label_font = ('Calibri', '18')
        self._color_label_font = ('Calibri', '46', 'bold')
        self._colors = ('red', 'blue', 'green', 'pink', 'black', 'yellow', \
                        'orange', 'white', 'purple', 'brown')
        self._colors_x_table = {'red': 203, 'blue': 196, 'green': 180, 'pink': 197,
                                'black': 184, 'yellow': 173, 'orange': 165,
                                'white': 184, 'purple': 174, 'brown': 174}
        self._colors_y = 109
        self._number_of_colors = len(self._colors)
        self._score = 0
        self._time_left = 31

        ### View 1 - start the game
        # Horizontal separator
        ttk.Separator(self._master, orient=HORIZONTAL)\
            .place(x=5, y=30, width=490)

        # Vertical separator
        ttk.Separator(self._master, orient=VERTICAL)\
            .place(x=250, y=0, height=30)
        
        # Time left
        self._time_left_label = ttk.Label(self._master, text='Time left: 30', \
            font=self._header_label_font)
        self._time_left_label.place(x=93, y=7)

        # Score
        self._score_label = ttk.Label(self._master, text='Score: 0', \
            font=self._header_label_font)
        self._score_label.place(x=342, y=7)

        # Start the game
        self._start_game_label = ttk.Label(\
            self._master, text='[Press "Space" to start]', \
            font=self._start_label_font)
        self._start_game_label.place(x=155, y=127)
        self._master.bind('<space>', self.start_game)

        # Enter name of the color
        ttk.Label(self._master, text='Type in the colour of the words, and not the word text:', \
            font=self._body_label_font)\
            .place(x=78, y=240)
        self._entered_name = StringVar()
        self._entered_name_entry = ttk.Entry(\
            self._master, width=30, textvariable=self._entered_name)
        self._entered_name_entry.place(x=143, y=265)
        ttk.Label(self._master, text='(Press "Enter")', font=self._body_label_font)\
            .place(x=201, y=287)
        ### End of View 1

        ### View 2 - Playing the game
        self._color_label = ttk.Label(self._master, font=self._color_label_font)
        ### End of View 2

        ### View 3 - End of the game (start again?)
        self._timed_out_label = ttk.Label(self._master, text='Time is out!',\
            font=self._body_label_font)
        self._player_score_label = ttk.Label(self._master, \
            font=self._body_label_font)
        self._start_again_label = ttk.Label(self._master, \
            text='[Press "Space" to start again]', font=self._start_label_font)
        ### End of View 3

    def start_game(self, event=None):
        # Disables "Space" bind key
        self._master.unbind('<space>')
        
        # Enabled "Enter" bind key
        self._master.bind('<Return>', self.check_entered_name)
        
        # Hides unnecessary labels
        self.hide_labels()

        # Restores default values
        self.restores_defaults()

        # Randomly selects color
        self.select_random_color()

        # Focus on Entry
        self._entered_name_entry.focus_set()

        # Turn on timer
        self.update_timer()

    def hide_labels(self):
        self._start_game_label.place_forget()
        self._timed_out_label.place_forget()
        self._player_score_label.place_forget()
        self._start_again_label.place_forget()

    def restores_defaults(self):
        self._score = 0
        self._time_left = 31
        self._score_label.config(text=f'Score: {self._score}')
        self._time_left_label.config(text=f'Time left: {self._time_left}')
        self._entered_name.set('')
        
    def select_random_color(self):
        # Name of the color
        index = random.randrange(self._number_of_colors)
        name_of_color = self._colors[index]

        # Color itself
        index = random.randrange(self._number_of_colors)
        color = self._colors[index]
        self._current_color = color

        # Color's label coordinates
        x = self._colors_x_table[name_of_color]
        y = self._colors_y

        # Configures color's label and displays it
        name_of_color = name_of_color.capitalize()
        self._color_label.config(text=name_of_color)
        self._color_label.config(foreground=color)
        self._color_label.place(x=x, y=y)

    def update_timer(self):
        self._time_left -= 1
        self._time_left_label.config(text=f'Time left: {self._time_left}')
        if self._time_left == 0:
            # End of the game
            self._master.after_cancel(self._job)
            self._job = None
            self.end_game()
            return
        self._job = self._master.after(1000, self.update_timer)

    def end_game(self):
        self._entered_name.set('')

        # Hides color's label
        self._color_label.place_forget()

        # Displays end of the game messages
        self.display_labels()

        # Enables "Space" bind key
        self._master.bind('<space>', self.start_game)

        # Disables "Enter" bind key
        self._master.unbind('<Return>')

    def display_labels(self):
        self._timed_out_label.place(x=213, y=57)
        self._player_score_label.config(text=f'Your score is: {self._score}!')
        self._player_score_label.place(x=190, y=87)
        self._start_again_label.place(x=130, y=127)

    def check_entered_name(self, event=None):
        # Get entered name of a color
        name_of_color = self._entered_name.get()
        self._entered_name.set('')
        if self._time_left>0 and name_of_color:
            # When something was enetered
            if name_of_color == self._current_color:
                # Right answer
                self.increase_score()
            self.select_random_color()

    def increase_score(self):
        self._score += 1
        self._score_label.config(text=f'Score: {self._score}')


def main():
    root = Tk()
    app = ColorGameApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()