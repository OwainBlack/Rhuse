"""
Rhuse is a rhythm-based bullet hell
This game is in pre-alpha, expect many unpolished features
"""

import pygame
import sys
import math
import csv
from game_object_setup import create_game_objects
from object_values import (screen, title, start, skydiver_button, skydiver_title, meganeko_title,
                           player, player_tail1, player_tail2, player_tail3, pause_text)


pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=0)
pygame.init()



# Constants
FRAME = 1/240


# Sinusoidal easing
def sine_easing(t, amplitude,
                offset, frequency):
    return amplitude * math.sin(2*math.pi * frequency * t) + offset

t = 0  # For sin movement later

start_screen = True
level_selected = False

pygame.display.set_caption("Rhuse") # Game title



# CSV File Reader
def read_csv_data(filename):
    objects = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            objects.append(row)
    return objects

skydiver_data = read_csv_data('skydiverlevel.csv')  # File determines the state of ingame objects

# Ingame object setup
game_objects = create_game_objects(skydiver_data, screen)



# Song setup
skydiver_song = pygame.mixer.music.load('skydiver.mp3')

song = False



# Title scroll setup
pause = 0

g = 0

title_in = True

title_scroll = True



# Lives setup
lives = 3

heal = True

damage_taken = False

damage_r = 0
damage_g = 0
damage_b = 0

cooldown = 0



# Pause setup
paused = False

pause_alpha = True

music_paused = False



# Game over setup
game_over = False



# Music setup
frame_counter = 0

beat_counter = 0

frames_per_beat = 100.7

offset = 740



# BG color setup
bg_r = 0
bg_g = 0
bg_b = 0



# Clock setup
clock = pygame.time.Clock()



# Main game loop
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and skydiver_button.clicked:  # Press ESC to pause/unpause
                paused = not paused
            if event.key == pygame.K_BACKSPACE:
                pygame.quit()
                sys.exit()

    # Start screen
    if not start.clicked:
        paused = False

        song = False

        frame_counter = 0

        beat_counter = 0

        heal = True

        screen.fill((85,0,85)) # Dark violet bg

        title.rect.y = sine_easing(t, 25, 300, 0.025) # Title sin easing
        t += 0.1

        title.update()

        start.update()


    # Level select screen
    if start.clicked and not skydiver_button.clicked and not game_over:
        screen.fill((15,15,15))
        skydiver_button.update()
    


    if not paused:
        pause_alpha = True
        if skydiver_button.clicked:
            if music_paused:
                pygame.mixer.music.unpause()
                music_paused = False

            frame_counter += 1

            if frame_counter >= (((frames_per_beat*beat_counter)/4) + offset):  # Calculates frames per beat in quadruple time
                beat_counter += 1

            if  82 <= beat_counter < 137:
                bg_r += ((32*4) / (frames_per_beat*55))
                bg_g += ((51*4) / (frames_per_beat*55))
                bg_b += ((51*4) / (frames_per_beat*55))
            elif beat_counter >= 137:
                bg_r = 32
                bg_b = 32
                bg_g = 0


            screen.fill((bg_r, bg_g, bg_b))

            if heal: # Heal lives to full if they aren't already
                lives = 3
                heal = False

            skydiver_title.rect.x = sine_easing(g, -500, 1740, 0.01)
            meganeko_title.rect.x = sine_easing(g, -500, 1740, 0.01)
            
            if title_scroll: # Title of the song will smoothly slide in and out
                if g < 25 and title_in:
                    g += 0.1
                elif g >= 25 and title_in:
                    title_in = False
                elif pause < 1: # Pause 1 second
                    pause += FRAME
                elif g > -5:
                    g -= 0.1
                else:
                    title_in = True
                    pause = 0
                    g = 0
                    pygame.mixer.music.play()
                    title_scroll = False
                skydiver_title.update()
                meganeko_title.update()

            pygame.mouse.set_visible(False)


            for game_object in game_objects:
                if (beat_counter >= float(game_object.timestart)
                    and beat_counter < float(game_object.timestop)):
                    
                    if float(game_object.timestart) <= beat_counter < float(game_object.timestop):
                        if float(game_object.movex) != 0:  # Handles object's x movement
                            game_object.movextimer += (round((float(game_object.movex)
                                                      / ((float(game_object.timestop)
                                                      - float(game_object.timestart))
                                                      * frames_per_beat)))
                                                      * 4)
                            if game_object.movextimer >= 1:
                                game_object.rect.x += game_object.movextimer
                                game_object.movextimer = 0
                            elif game_object.movextimer <= -1:
                                game_object.rect.x -= game_object.movextimer
                                game_object.movextimer += 1



                        if float(game_object.movey) != 0:  # Handles object's y movement
                            game_object.moveytimer += (round((float(game_object.movey)
                                                      / ((float(game_object.timestop)
                                                      - float(game_object.timestart))
                                                      * frames_per_beat)))
                                                      * 4)
                            if game_object.moveytimer >= 1:
                                game_object.rect.y += game_object.moveytimer
                                game_object.moveytimer -= 1
                            elif game_object.moveytimer <= -1:
                                game_object.rect.y -= game_object.moveytimer
                                game_object.moveytimer += 1

                    game_object.update()

                    if game_object.lifelost and cooldown <= 0:  # Handles an event where the player is hit
                        damage_r = 255
                        damage_g = 0
                        damage_b = 0
                        lives -= 1
                        cooldown = 3

            if cooldown > 0:  # Invincibility frames
                cooldown -= FRAME

            if damage_r > 0:  # Damaged player color
                    player.new_color((damage_r, damage_g, damage_b))
                    damage_r -= 1
                    damage_g += 0.5
                    damage_b += 1
            else:
                player.new_color((0, 128, 255))

            # Player loses tail parts for lives lost
            if lives >= 3:
                player_tail3.update()
            if lives >= 2:
                player_tail2.update()
            if lives >= 1:
                player_tail1.update()
                player.update()

    elif paused: # Pause menu
        if not music_paused:
            pygame.mixer.music.pause()
            music_paused = True
        pygame.mouse.set_visible(True)
        screen.fill((0, 0, 0))
        pause_text.update()
        


    pygame.display.flip()
    clock.tick(240) # FPS