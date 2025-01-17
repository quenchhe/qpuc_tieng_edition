import pygame
import os
import ctypes
import yaml

ctypes.windll.user32.SetProcessDPIAware()

# Global vars

TITLE_DIM =  tuple([x * 1 for x in (600, 288)])
PROFILE_DIM = tuple([x * 1.2 for x in (100, 100)])
BUZZER_DIM = tuple([x * 1.2 for x in (129, 190)])
POINT_DIM = tuple([x * 1.2 for x in (74, 31)])
CONTESTANT_XPAD = 200
CONTESTANT_YPAD = 350
CONTESTANT_PER_ROW = 8
FIRST_ROW_X = 300
FIRST_COL_Y = 50
BUZZER_CONTESTANT_PAD = 100
POINT_X = 32
POINT_Y = 70
POINT_Y_PAD = 34
NAME_X = 30
NAME_Y = 135

# Contestant class

class Contestant:

    def __init__(self, name, score=0, pos=(0,0), is_buzzing=False, is_activated = True):

        self.name = name
        self.pos = pos
        self.score = score
        self.is_buzzing = is_buzzing
        self.is_activated = is_activated
        self.buzzer_state = "neutral"

        img_buzzer_path = f'data/media/images/buzzer/buzzer_neutral.png'
        self.img_buzzer = pygame.transform.scale(pygame.image.load(img_buzzer_path), BUZZER_DIM)

        img_profile_path = f'data/media/images/players/{name.lower()}.png'
        self.img_profile = pygame.transform.scale(pygame.image.load(img_profile_path), PROFILE_DIM)

        img_point_path = f'data/media/images/buzzer/empty_point.png'
        self.img_point = [None, None, None, None]
        self.img_point_pos = [None, None, None, None]
        for i in range (0,4):
            self.img_point[i] = pygame.transform.scale(pygame.image.load(img_point_path), POINT_DIM)

    def update_score(self, points):
        self.score += points
        if self.score >= 4 :
            self.score = 4
        for i in range(3, 3-self.score, -1):
            img_point_path = f'data/media/images/buzzer/filled_point.png'
            self.img_point[i] = pygame.transform.scale(pygame.image.load(img_point_path), POINT_DIM)


    def get_img_profile(self):
        return(self.img_profile)

    def get_img_buzzer(self):
        return(self.img_buzzer)
    
    def set_img_profile_pos(self, pos) :
        self.img_profile_pos = pos

    def set_img_buzzer_pos(self, pos) :
        self.img_buzzer_pos = pos

    def get_img_profile_pos(self) :
        return(self.img_profile_pos)

    def get_img_buzzer_pos(self) :
        return(self.img_buzzer_pos)
    
    def get_img_points(self, i) :
        return(self.img_point[i])

    def set_img_point_pos(self, i, pos):
        self.img_point_pos[i] = pos

    def get_img_point_pos(self, i):
        return(self.img_point_pos[i])

    def get_name(self):
        return(self.name)

    def get_name_pos(self):
        return(self.name_pos)

    def set_name_pos(self, pos):
        self.name_pos = pos

    def get_is_activated(self):
        return(self.is_activated)

    def set_is_activated(self, is_activated):
        self.is_activated = is_activated

    def get_is_buzzing(self):
        return(self.is_buzzing)

    def set_is_buzzing(self, is_buzzing):
        self.is_buzzing = is_buzzing

    def set_buzzer_state(self, state):
        self.buzzer_state = state
        img_buzzer_path = f'data/media/images/buzzer/buzzer_{state}.png'
        self.img_buzzer = pygame.transform.scale(pygame.image.load(img_buzzer_path), BUZZER_DIM)

    def get_buzzer_state(self):
        return(self.buzzer_state)

class GameState:

    def __init__(self):

        self.is_buzzing = False
        self.buzzing_player = ""
    
    def get_is_buzzing(self):
        return(self.is_buzzing)

    def get_buzzing_player_name(self):
        return(self.buzzing_player_name)

    def set_is_buzzing(self, is_buzzing):
        self.is_buzzing = is_buzzing

    def set_buzzing_player_name(self, buzzing_player_name):
        self.buzzing_player_name = buzzing_player_name

            

# Initialize Pygame
pygame.init()

# Constants for screen dimensions and colors
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1000
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


# Load images
background_image = pygame.image.load('data/media/images/background.png')
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
title_image = pygame.image.load('data/media/images/title.png')
title_image = pygame.transform.scale(title_image, TITLE_DIM)

# Load contestants

contestants = {}

# Read the YAML file
with open('config/contestants.yaml', 'r') as file:
    data = yaml.safe_load(file)
contestant_names = data['contestants_round_1']

list_pygame_keys = [pygame.K_a, pygame.K_z, pygame.K_e, pygame.K_r, pygame.K_t, pygame.K_y, pygame.K_u, pygame.K_i, pygame.K_q, pygame.K_s, pygame.K_d, pygame.K_f, pygame.K_g, pygame.K_h, pygame.K_j, pygame.K_k]
binding_contestant_key = {}
for i in range(0, len(contestant_names)):
    binding_contestant_key[contestant_names[i]] = list_pygame_keys[i]

for name in contestant_names:
    contestant = Contestant(name=name)
    contestants[name] = contestant

game_state = GameState()

# Initialize Pygame screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("QPUC Tieng Edition")

# Font initialization for score display
pygame.font.init()
font = pygame.font.SysFont('Arial', 24)

# Load buzzer sounds
buzzer_sound = pygame.mixer.Sound('data\media\sound\\buzzer.mp3')
bad_answer_sound = pygame.mixer.Sound('data\media\sound\\bad_answer.mp3')
good_answer_sound = pygame.mixer.Sound('data\media\sound\good_answer.mp3')
ticking_sound = pygame.mixer.Sound('data\media\sound\\ticking_sound.mp3')

# Functions

def buzz(contestant, game_state):
    is_buzzing = game_state.get_is_buzzing()
    if not is_buzzing and contestant.get_is_activated():
        game_state.set_buzzing_player_name(contestant.get_name())
        game_state.set_is_buzzing(True)
        contestant.set_is_activated(False)
        ticking_sound.stop()
        buzzer_sound.play()

# Timer event
BLINKING = pygame.USEREVENT + 1
pygame.time.set_timer(BLINKING, 250)

# Main loop
running = True
clock = pygame.time.Clock()

while running:
    # Handle events
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == BLINKING:
            if game_state.get_is_buzzing() :
                if contestants[game_state.get_buzzing_player_name()].get_buzzer_state() == "on" :
                    contestants[game_state.get_buzzing_player_name()].set_buzzer_state("neutral")
                elif contestants[game_state.get_buzzing_player_name()].get_buzzer_state() == "neutral" :
                    contestants[game_state.get_buzzing_player_name()].set_buzzer_state("on")

        elif event.type == pygame.KEYDOWN:

            # Buzzing contestant
            for contestant_name, key in binding_contestant_key.items() :
                if event.key == key :
                    buzz(contestants[contestant_name], game_state)

            # Right answer
            if event.key == pygame.K_w:
                if game_state.get_is_buzzing() :
                    good_answer_sound.play()
                    contestants[game_state.get_buzzing_player_name()].update_score(1)
                for contestant_name, contestant in contestants.items() :
                    contestant.set_buzzer_state("neutral")
                    contestant.set_is_activated(True)
                    contestant.set_is_buzzing(False)
                game_state.set_is_buzzing(False)
                game_state.set_buzzing_player_name("")

            # Reset all
            elif event.key == pygame.K_c:
                for contestant_name, contestant in contestants.items() :
                    contestant.set_buzzer_state("neutral")
                    contestant.set_is_activated(True)
                    contestant.set_is_buzzing(False)
                game_state.set_is_buzzing(False)
                game_state.set_buzzing_player_name("")
                ticking_sound.stop()
                ticking_sound.play(loops=-1)

            # Bad answer
            elif event.key == pygame.K_x:
                if game_state.get_is_buzzing() :
                    bad_answer_sound.play()
                    ticking_sound.stop()
                    ticking_sound.play(loops=-1)
                    game_state.set_is_buzzing(False)
                    contestants[game_state.get_buzzing_player_name()].set_buzzer_state("deactivated")
                    contestants[game_state.get_buzzing_player_name()].set_is_activated(False)
                    contestants[game_state.get_buzzing_player_name()].set_is_buzzing(False)



    # Clear the screen
    screen.fill(BLACK)

    # Draw background image
    screen.blit(background_image, (0, 0))

    # Draw title image
    screen.blit(title_image, ((SCREEN_WIDTH - TITLE_DIM[0]) // 2, 0))

    # Display contestant images and buzzers
    contestants_per_row_true = [CONTESTANT_PER_ROW, len(contestants) - CONTESTANT_PER_ROW]
    row = 0
    for i, (name, contestant) in enumerate(contestants.items()):

        col_slot = i % CONTESTANT_PER_ROW
        row = row + 1 if col_slot == 0 and i != 0 else row
        first_col_y_row_binded = (SCREEN_WIDTH - (contestants_per_row_true[row] * CONTESTANT_XPAD))/2

        # Display contestant image
        contestant_image = contestant.get_img_profile()
        contestant.set_img_profile_pos((first_col_y_row_binded + col_slot * CONTESTANT_XPAD, FIRST_ROW_X + row * CONTESTANT_YPAD))
        screen.blit(contestant_image, contestant.get_img_profile_pos())

        # Display buzzer image (pressed or neutral)
        buzzer_image = contestant.get_img_buzzer()
        contestant.set_img_buzzer_pos((first_col_y_row_binded + col_slot * CONTESTANT_XPAD, FIRST_ROW_X + row * CONTESTANT_YPAD + BUZZER_CONTESTANT_PAD))
        screen.blit(buzzer_image, contestant.get_img_buzzer_pos())

        # Display points
        for i in range(0,4):
            point_image = contestant.get_img_points(i)
            contestant.set_img_point_pos(i, (first_col_y_row_binded + col_slot * CONTESTANT_XPAD + POINT_X, FIRST_ROW_X + row * CONTESTANT_YPAD + BUZZER_CONTESTANT_PAD + POINT_Y + i*POINT_Y_PAD))
            screen.blit(point_image, contestant.get_img_point_pos(i))    

        # Render name
        text_surface = font.render(contestant.get_name(), False, (255, 255, 255))
        contestant.set_name_pos((first_col_y_row_binded + col_slot * CONTESTANT_XPAD + NAME_X, FIRST_ROW_X + row * CONTESTANT_YPAD + NAME_Y))
        screen.blit(text_surface,contestant.get_name_pos())



    # Update the screen
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(30)

# Quit Pygame
pygame.quit()
