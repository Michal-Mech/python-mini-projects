import customtkinter as ctk
from random import randint
from sys import exit
from settings import *

class Game(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('Snake')
        self.geometry(f'{WINDOW_SIZE[0]}x{WINDOW_SIZE[1]}')

        # Grid layout 20 columns x 15 rows
        self.columnconfigure(list(range(FIELDS[0])),weight=1,uniform='a')
        self.rowconfigure(list(range(FIELDS[1])),weight=1,uniform='a')

        # State
        self.game_over = False
        self.game_over_frame = None

        # Snake starts as 3 horizontal segments
        self.snake = [START_POS, (START_POS[0]-1,START_POS[1]),(START_POS[0]-2,START_POS[1])]
        self.direction = DIRECTIONS['right']

        # Keyboard controls
        self.bind('<Key>',self.get_input)

        self.place_apple()
        self.draw_frames = []
        self.animate()

    def run(self):
        self.mainloop()

    # Main game loop - called every REFRESH_SPEED ms
    def animate(self):
        if self.game_over:
            self.show_game_over()
            return  # ← nie planujemy kolejnej klatki

        # Move snake and add new head in current direction
        new_head = (self.snake[0][0] + self.direction[0],self.snake[0][1] + self.direction[1])
        self.snake.insert(0, new_head)

        # Eating an apple
        if self.snake[0] == self.apple_pos:
            self.place_apple()
        else:
            self.snake.pop()

        # Check for collision
        self.check_game_over()
        if self.game_over:
            self.show_game_over()
            return

        # Drawing
        self.draw()
        self.after(REFRESH_SPEED,self.animate)

    # Set game_over flag if snake hits the wall or its own tail
    def check_game_over(self):
        snake_head = self.snake[0]
        if snake_head[0] >= RIGHT_LIMIT or snake_head[1] >= BOTTOM_LIMIT or \
                snake_head[0] < LEFT_LIMIT or snake_head[1] < TOP_LIMIT or \
                snake_head in self.snake[1:]:
            self.game_over = True

    # Arrows controls and 'R'-restart and 'Q'-quit logic
    def get_input(self,event):
        # Game over controls
        if self.game_over:
            if event.keysym.lower() == 'r':
                self.restart()
            elif event.keysym.lower() == 'q':
                self.destroy()
            return

        # Gameplay controls
        match event.keycode:
            case  37: self.direction = DIRECTIONS['left'] if self.direction != DIRECTIONS['right'] else self.direction
            case  38: self.direction = DIRECTIONS['up'] if self.direction != DIRECTIONS['down'] else self.direction
            case  39: self.direction = DIRECTIONS['right'] if self.direction != DIRECTIONS['left'] else self.direction
            case  40: self.direction = DIRECTIONS['down'] if self.direction != DIRECTIONS['up'] else self.direction

    # Pick a random position for apple which is not on the snake
    def place_apple(self):
        while True:
            new_pos = (randint(0, FIELDS[0] - 1), randint(0, FIELDS[1] - 1))
            if new_pos not in self.snake:
                self.apple_pos = new_pos
                return

    # Redraw snake and apple on the grid
    def draw(self):
        # Remove old frames
        if self.draw_frames:
            for frame, pos in self.draw_frames:
                frame.destroy()

            self.draw_frames.clear()

        # Create apple frame
        apple_frame =ctk.CTkFrame(self, fg_color=APPLE_COLOR)
        self.draw_frames.append((apple_frame,self.apple_pos))

        # Create snake frames
        for index, pos in enumerate(self.snake):
            color = SNAKE_BODY_COLOR if index != 0 else SNAKE_HEAD_COLOR
            snake_frame =ctk.CTkFrame(self,fg_color=color,corner_radius=0)
            self.draw_frames.append((snake_frame,pos))

        # Place all frames in grid
        for frame, pos in self.draw_frames:
            frame.grid(column=pos[0],row=pos[1])

    # Display game over panel with score and instructions
    def show_game_over(self):
        # Remove snake and apple from the screen
        for frame, pos in self.draw_frames:
            frame.destroy()
        self.draw_frames.clear()

        # Score (3 is the initial snake length)
        score = len(self.snake) - 3

        self.game_over_frame = ctk.CTkFrame(self, fg_color=GAME_OVER_COLOR, corner_radius=0)
        self.game_over_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        # "Game Over" label
        title = ctk.CTkLabel(
            self.game_over_frame,
            text='GAME OVER',
            text_color=GAME_OVER_TEXT_COLOR,
            font=ctk.CTkFont(family=FONT, size=GAME_OVER_FONT_SIZE, weight='bold')
        )
        title.place(relx=0.5, rely=0.35, anchor='center')

        # Score label
        score_label = ctk.CTkLabel(
            self.game_over_frame,
            text=f'Score: {score}',
            text_color=SCORE_TEXT_COLOR,
            font=ctk.CTkFont(family=FONT, size=SCORE_FONT_SIZE, weight='bold')
        )
        score_label.place(relx=0.5, rely=0.5, anchor='center')

        # Instructions how to restart or quit the game
        info = ctk.CTkLabel(
            self.game_over_frame,
            text='Press R to restart  |  Press Q to quit',
            text_color=INFO_TEXT_COLOR,
            font=ctk.CTkFont(family=FONT, size=INFO_FONT_SIZE)
        )
        info.place(relx=0.5, rely=0.65, anchor='center')

    # Reset the game state and start a new game
    def restart(self):
        if self.game_over_frame:
            self.game_over_frame.destroy()
            self.game_over_frame = None

        # Reset game state
        self.game_over = False
        self.snake = [START_POS, (START_POS[0] - 1, START_POS[1]), (START_POS[0] - 2, START_POS[1])]
        self.direction = DIRECTIONS['right']
        self.place_apple()
        self.draw_frames = []

        # Restart animation
        self.animate()

if __name__ == '__main__':
    game = Game()
    game.run()