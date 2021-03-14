import pygame
import math
import time
import random
from focus_utilities import *

pygame.init()
color = {"red": (255, 0, 0), "blue": (0, 0, 255),
         "light_blue": (173, 216, 230), "yellow": (255, 249, 10),
         "dark_brown": (77, 38, 2), "brown": (247, 125, 10),
         "orange": (247, 46, 10), "yellow": (247, 239, 10),
         "bright_blue": (10, 247, 208), "lilac": (247, 10, 232),
         "pink": (247, 10, 10), "grey": (150, 150, 150),
         "light_grey": (210, 210, 210), "bright_green": (0, 255, 0),
         "green": (0, 150, 0), "bright_red": (255, 0, 0), "red": (200, 0, 0)}
white = (255, 255, 255)
black = (0, 0, 0)
gray = (200, 200, 200)
# pygame variables
screen_width, screen_height = 600, 600
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
click = pygame.mouse.get_pressed
mouse = pygame.mouse.get_pos
def_font = pygame.font.get_default_font()
# global variables
default_coef, default_fps = (5, 4), 10
fps = default_fps
pause = False
arr = []
ins, outs = 0, 0
# buttons
grun, gquit, gcontinue, gpause = None, None, None, None
gchange_settings, gline, gspeed = None, None, None
# messages
title_msg, descr_msg = None, None
pick_line_msg, pick_speed_msg = None, None


def set_buttons():
    global grun, gquit, gcontinue, gpause, gchange_settings
    global gline, gspeed
    colors = [color["red"], color["blue"], color["green"], color["yellow"]]
    line_images = ["rose_5-4.png", "rose_6-7.png", "rose_7-8.png",
                   "rose_9-10.png"]
    line_coef = [(5, 4), (6, 7), (7, 8), (9, 10)]
    line_rect = (150, 80, 300, 300)
    gline = GroupButton(line_rect, 2, 2, 4, 5, colors, images=line_images,
                        values=line_coef)
    gline.set_group()
    speed_rect = (150, 430, 300, 50)
    fps_val = [15, 25, 40]
    gspeed = GroupButton(speed_rect, 1, 3, 3, 5, colors, text=["1", "2", "3"],
                         values=fps_val)
    gspeed.set_group()
    runcolors = [color["steel_blue"], color["green"], color["green"]]
    run_rect = (100, 500, 100, 50)
    grun = GButton(run_rect, runcolors, text="Run", action=run_loop)
    gcontinue = GButton(run_rect, runcolors, text="Continue", action=unpause)
    pause_rect = (screen_width//2 - 80, 560, 160, 40)
    gpause = GButton(pause_rect, runcolors, text="Pause", action=pause_game)
    change_rect = (screen_width//2 - 100, screen_height//2, 200, 70)
    gchange_settings = GButton(change_rect, runcolors, text="Change settings",
                               action=focus_intro)
    quitcolors = [color["dark_orange"], color["red"], color["red"]]
    quit_rect = (400, 500, 100, 50)
    gquit = GButton(quit_rect, quitcolors, text="Quit", action=quit_game)


def set_messages():
    global title_msg, pick_line_msg, pick_speed_msg, descr_msg
    title_msg = Message(screen, "Train your focus", 'freesansbold.ttf', 30,
                        (screen_width/2, 15), color['blue'])
    descr_msg = Message(screen, "Just keep the mouse inside the yellow circle",
                        'freesansbold.ttf', 15, (screen_width/2, 37),
                        color['blue'])
    pick_line_msg = Message(screen, "Pick your line", 'freesansbold.ttf', 20,
                            (screen_width/2, gline.group_rect[1] - 20),
                            color['blue'])
    pick_speed_msg = Message(screen, "Pick your speed", 'freesansbold.ttf', 20,
                             (screen_width/2, gspeed.group_rect[1] - 20),
                             color['blue'])


def get_rose_curve(coef=default_coef):
    global arr
    arr = []
    n, d = coef
    k = n / d
    for i in range(3601):
        theta = math.radians(i)
        x = math.cos(k * theta) * math.cos(theta)
        y = math.cos(k * theta) * math.sin(theta)
        arr.append((x, y))


def create_background(width=screen_width,
                      height=screen_height,
                      coef=default_coef):
    get_rose_curve(coef)
    left, right, up, down = screen_width, 0, screen_height, 0
    x_cent, y_cent = width // 2, height // 2
    mult = min(width, height) * 5/12
    background = pygame.Surface((width, height))
    background.fill(gray)
    pixAr = pygame.PixelArray(background)
    for i in range(len(arr)):
        x, y = int(mult * arr[i][0] + x_cent), int(mult * arr[i][1] + y_cent)
    arr[i] = x, y
    left, right = min(left, x), max(right, x)
    up, down = min(up, y), max(down, y)
    pixAr[x - 2: x + 3, y - 2: y + 3] = color['blue']
    line_rect = pygame.Rect(left, up, right - left, down - up)
    return background, line_rect


background, line_rect = create_background()


def get_score(font_size, coords):
    global ins, outs
    score = ins - outs
    x, y = coords
    text1 = f'SCORE: {score}'
    text1 += ' :( ' if score < 0 else ' :)'
    font = pygame.font.Font(def_font, font_size)
    total_text = font.render(text1, False, black)
    screen.blit(total_text, coords)
    pygame.display.update()


def focus_intro():
    global background, fps, line_rect
    set_buttons()
    set_messages()
    screen.fill(white)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            gline.check_group(event)
            gspeed.check_group(event)
            grun.button_check(event)
            gquit.button_check(event)
        gline.display_group(screen)
        gspeed.display_group(screen)
        grun.button_draw(screen)
        gquit.button_draw(screen)
        title_msg.display_msg()
        descr_msg.display_msg()
        pick_line_msg.display_msg()
        pick_speed_msg.display_msg()
        coef = gline.get_choice(default_coef)
        background, line_rect = create_background(screen_width,
                                                  screen_height, coef)
        fps = gspeed.get_choice(default_fps)
        pygame.display.update()
        clock.tick(10)


def unpause():
    global pause
    pause = False


def pause_game():
    global gcontinue, gquit, gchange_settings, gpause
    global pause
    pause = True
    gpause.release_button()
    gcontinue.release_button()
    gchange_settings.release_button()
    while pause:
        pygame.draw.rect(screen, gray, gpause.rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            gcontinue.button_check(event)
            gquit.button_check(event)
            gchange_settings.button_check(event)
        gcontinue.button_draw(screen)
        gquit.button_draw(screen)
        gchange_settings.button_draw(screen)
        pygame.display.flip()
        clock.tick(10)


def run_loop():
    global background, fps, line_rect, gpause
    global ins, outs
    screen = pygame.display.set_mode((screen_width, screen_height))
    gpause.release_button()
    ins, outs = 0, 0
    i = 0
    leap = random.randint(0, len(arr)//4)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            gpause.button_check(event)
        screen.blit(background, (0, 0))
        gpause.button_draw(screen)
        if i == leap:
            i = random.randint(0, len(arr) - 20)
        leap = random.randint(i, i + (len(arr)-i)//2)
        circ = pygame.draw.circle(screen, color['yellow'], arr[i], 14)
        if line_rect.collidepoint(mouse()):
            pygame.draw.circle(screen, color['green'], mouse(), 6)
        if not circ.inflate(12, 12).collidepoint(mouse()):
            pygame.draw.circle(screen, color['red'], mouse(), 6)
            outs += 1
        else:
            ins += 1
        get_score(20, (10, 10))
        pygame.display.flip()
        clock.tick(fps)
        i += 1
        if i == len(arr) - 1:
            i = 0


def quit_game():
    pygame.quit()
    quit()
focus_intro()

    



    
