import pygame
import os
import ctypes
import yaml
import random

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
QUESTION_X = 50
QUESTION_Y = 780
PROPOSITION_1_X = 510
PROPOSITION_1_Y = 910
PROPOSITION_2_X = 1085
PROPOSITION_2_Y = 910

# Contestant class

class Contestant:

    def __init__(self, name, life=2, pos=(0,0), is_buzzing=False, is_activated = True):

        self.name = name
        self.pos = pos
        self.life = life
        self.is_buzzing = is_buzzing
        self.is_activated = is_activated
        self.buzzer_state = "neutral"

        img_buzzer_path = f'data/media/images/buzzer/buzzer_green.png'
        self.img_buzzer = pygame.transform.scale(pygame.image.load(img_buzzer_path), BUZZER_DIM)

        img_profile_path = f'data/media/images/players/{name.lower()}.png'
        self.img_profile = pygame.transform.scale(pygame.image.load(img_profile_path), PROFILE_DIM)

    def set_life(self, life_delta):
        self.life += life_delta
        if self.life == 2:
            img_buzzer_path = f'data/media/images/buzzer/buzzer_green.png'
        elif self.life == 1:
            img_buzzer_path = f'data/media/images/buzzer/buzzer_orange.png'
        else :
            img_buzzer_path = f'data/media/images/buzzer/buzzer_red.png'
        self.img_buzzer = pygame.transform.scale(pygame.image.load(img_buzzer_path), BUZZER_DIM)

    def get_life(self):
        return(self.life)

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
        if state == "neutral" :
            self.set_life(0)
        elif state == "on" :
            img_buzzer_path = f'data/media/images/buzzer/buzzer_neutral.png'
            self.img_buzzer = pygame.transform.scale(pygame.image.load(img_buzzer_path), BUZZER_DIM)

    def get_buzzer_state(self):
        return(self.buzzer_state)

class GameState:

    def __init__(self, current_player = ""):
        self.current_player = current_player

        img_banner_path = f'data/media/images/empty.png'
        self.img_banner = pygame.transform.scale(pygame.image.load(img_banner_path), (SCREEN_WIDTH, SCREEN_HEIGHT))

        img_button_1_path = f'data/media/images/empty.png'
        self.img_button_1 = pygame.transform.scale(pygame.image.load(img_button_1_path), (SCREEN_WIDTH, SCREEN_HEIGHT))

        img_button_2_path = f'data/media/images/empty.png'
        self.img_button_2 = pygame.transform.scale(pygame.image.load(img_button_2_path), (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.question_states = ["empty", "show_question", "show_answer_1", "show_answer_2", "show_real_answer_2", "show_right_answer"]
        self.current_question_state = "empty"

        with open("data\questions\\round_2.yaml", 'r', encoding='utf-8') as file:
                self.dict_questions = yaml.safe_load(file)['questions']

        self.question_number = 1

        print(self.dict_questions)

        question_setup_raw = self.dict_questions[f'question_1']
        self.question = question_setup_raw["question"]
        shown_index = random.randint(0, 1)
        self.proposition_1 = question_setup_raw["proposition"][shown_index]
        self.proposition_2 = "L'autre"
        self.real_proposition_2 = question_setup_raw["proposition"][1 if shown_index == 0 else 0]
        self.answer = question_setup_raw["answer"]

        self.question_text = ""
        self.proposition_1_text = ""
        self.proposition_2_text = ""
    
    def get_current_player(self):
        return(self.current_player)

    def set_current_player(self, current_player):
        self.current_player = current_player

    def set_next_state(self):
        index = self.question_states.index(self.current_question_state)
        if index + 1 < len(self.question_states):
            self.current_question_state = self.question_states[index + 1]
        else:
            self.current_question_state = self.question_states[0]
        if self.current_question_state == "empty" :
            img_banner_path = f'data/media/images/empty.png'
            img_button_1_path = f'data/media/images/empty.png'
            img_button_2_path = f'data/media/images/empty.png'
            self.question_text = ""
            self.proposition_1_text = ""
            self.proposition_2_text = ""
        elif self.current_question_state == "show_question" :
            img_banner_path = f'data/media/images/banner_question.png'
            img_button_1_path = f'data/media/images/empty.png'
            img_button_2_path = f'data/media/images/empty.png'
            self.question_text = self.question
            self.proposition_1_text = ""
            self.proposition_2_text = ""
        elif self.current_question_state == "show_answer_1" :
            img_banner_path = f'data/media/images/banner_question.png'
            img_button_1_path = f'data/media/images/button_1_neutral_round_2.png'
            img_button_2_path = f'data/media/images/empty.png'
            self.question_text = self.question
            self.proposition_1_text = self.proposition_1
            self.proposition_2_text = ""
        elif self.current_question_state == "show_answer_2" :
            img_banner_path = f'data/media/images/banner_question.png'
            img_button_1_path = f'data/media/images/button_1_neutral_round_2.png'
            img_button_2_path = f'data/media/images/button_2_neutral_round_2.png'
            self.question_text = self.question
            self.proposition_1_text = self.proposition_1
            self.proposition_2_text = self.proposition_2
        elif self.current_question_state == "show_real_answer_2" :
            img_banner_path = f'data/media/images/banner_question.png'
            img_button_1_path = f'data/media/images/button_1_neutral_round_2.png'
            img_button_2_path = f'data/media/images/button_2_neutral_round_2.png'
            self.question_text = self.question
            self.proposition_1_text = self.proposition_1
            self.proposition_2_text = self.real_proposition_2
        elif self.current_question_state == "show_right_answer" :
            if self.proposition_1_text == self.answer : 
                img_banner_path = f'data/media/images/banner_question.png'
                img_button_1_path = f'data/media/images/button_1_good_round_2.png'
                img_button_2_path = f'data/media/images/button_2_bad_round_2.png'
            else :
                img_banner_path = f'data/media/images/banner_question.png'
                img_button_1_path = f'data/media/images/button_1_bad_round_2.png'
                img_button_2_path = f'data/media/images/button_2_good_round_2.png'             
        else :
            img_banner_path = f'data/media/images/empty.png'
            img_button_1_path = f'data/media/images/empty.png'
            img_button_2_path = f'data/media/images/empty.png'

        self.img_banner = pygame.transform.scale(pygame.image.load(img_banner_path), (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.img_button_1 = pygame.transform.scale(pygame.image.load(img_button_1_path), (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.img_button_2 = pygame.transform.scale(pygame.image.load(img_button_2_path), (SCREEN_WIDTH, SCREEN_HEIGHT))

    def get_img_banner(self):
        return(self.img_banner)

    def get_img_button_1(self):
        return(self.img_button_1)

    def get_img_button_2(self):
        return(self.img_button_2)

    def get_current_question_setup(self):
        question_setup_raw = self.dict_questions[f'question_{str(self.question_number)}']
        self.question = question_setup_raw["question"]
        shown_index = random.randint(0, 1)
        self.proposition_1 = question_setup_raw["proposition"][shown_index]
        self.proposition_2 = "L'autre"
        self.real_proposition_2 = question_setup_raw["proposition"][1 if shown_index == 0 else 0]
        self.answer = question_setup_raw["answer"]
        return(self.question, self.proposition_1, self.proposition_2, self.real_proposition_2, self.answer)

    def get_question_texts(self):
        return(self.question_text, self.proposition_1_text, self.proposition_2_text)

    def add_quesion_index(self, add):
        self.question_number += add



            

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
contestant_names = data['contestants_round_2']

list_pygame_keys = [pygame.K_a, pygame.K_z, pygame.K_e, pygame.K_r, pygame.K_t, pygame.K_y, pygame.K_u, pygame.K_i, pygame.K_q, pygame.K_s, pygame.K_d, pygame.K_f, pygame.K_g, pygame.K_h, pygame.K_j, pygame.K_k]
binding_contestant_key = {}
for i in range(0, len(contestant_names)):
    binding_contestant_key[contestant_names[i]] = list_pygame_keys[i]

for name in contestant_names:
    contestant = Contestant(name=name)
    contestants[name] = contestant

# Initialize Pygame screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("QPUC Tieng Edition")

# Font initialization for score display
pygame.font.init()
font = pygame.font.SysFont('Arial', 24)
font_question = pygame.font.SysFont('Impact', 60)
font_proposition = pygame.font.SysFont('Impact', 40)

# Load buzzer sounds
buzzer_sound = pygame.mixer.Sound('data\media\sound\\buzzer.mp3')
bad_answer_sound = pygame.mixer.Sound('data\media\sound\\bad_answer.mp3')
good_answer_sound = pygame.mixer.Sound('data\media\sound\good_answer.mp3')

# Game state
game_state = GameState(current_player = list(contestants.keys())[0])

# Functions

def lost(contestant):
    contestant.set_life(-1)
    bad_answer_sound.play()

def next_contestant_name(contestants_list, current_contestant_name):
    index = contestants_list.index(current_contestant_name)
    if index + 1 < len(contestants_list):
        return contestants_list[index + 1]
    else:
        return contestants_list[0]  # Return None if the element is the last in the list

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
            curent_player_name = game_state.get_current_player()
            if contestants[curent_player_name].get_buzzer_state() == "on" :
                contestants[curent_player_name].set_buzzer_state("neutral")
            elif contestants[curent_player_name].get_buzzer_state() == "neutral" :
                contestants[curent_player_name].set_buzzer_state("on")

        elif event.type == pygame.KEYDOWN:

            # Next contestant good answer
            if event.key == pygame.K_w:
                good_answer_sound.play()
                next_contestant = next_contestant_name(contestant_names, game_state.get_current_player())
                curent_player_name = game_state.get_current_player()
                contestants[curent_player_name].set_buzzer_state("neutral")
                game_state.add_quesion_index(1)
                game_state.get_current_question_setup()
                game_state.set_current_player(next_contestant)

            # Next contestant bad answer
            if event.key == pygame.K_x:
                curent_player_name = game_state.get_current_player()
                next_contestant = next_contestant_name(contestant_names, curent_player_name)
                contestants[curent_player_name].set_buzzer_state("neutral")
                lost(contestants[curent_player_name])
                if contestants[curent_player_name].get_life() == 0 :
                    contestant_names.remove(curent_player_name)
                game_state.add_quesion_index(1)
                game_state.get_current_question_setup()
                game_state.set_current_player(next_contestant)

            if event.key == pygame.K_c:
                game_state.set_next_state()



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

        # Render name
        text_surface = font.render(contestant.get_name(), False, (255, 255, 255))
        contestant.set_name_pos((first_col_y_row_binded + col_slot * CONTESTANT_XPAD + NAME_X, FIRST_ROW_X + row * CONTESTANT_YPAD + NAME_Y))
        screen.blit(text_surface,contestant.get_name_pos())

    # Banner questions
    screen.blit(game_state.get_img_banner(), (0,0))
    screen.blit(game_state.get_img_button_1(), (0,0))
    screen.blit(game_state.get_img_button_2(), (0,0))

    # Render questions texts
    (question_text, proposition_1_text, proposition_2_text) = game_state.get_question_texts()
    question_surface = font_question.render(question_text, False, (255, 255, 255))
    screen.blit(question_surface,(QUESTION_X, QUESTION_Y))
    proposition_1_surface = font_proposition.render(proposition_1_text, False, (255, 255, 255))
    screen.blit(proposition_1_surface,(PROPOSITION_1_X, PROPOSITION_1_Y))
    proposition_2_surface = font_proposition.render(proposition_2_text, False, (255, 255, 255))
    screen.blit(proposition_2_surface,(PROPOSITION_2_X, PROPOSITION_2_Y))

    # Update the screen
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(30)

# Quit Pygame
pygame.quit()
