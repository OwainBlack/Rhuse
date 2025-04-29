import pygame
from sprite_setup import Text, Button, Player, LaggingPlayer
from font_setup import main_title_font, button_font, song_title_font, song_subtitle_font



pygame.font.init()

res = (1920, 1080)
screen = pygame.display.set_mode(res, pygame.HWSURFACE)  # Set the surface up (with hardware acceleration)



title = Text(screen, 550, 500, 250, main_title_font, (255, 255, 255), 'Rhuse')

start = Button(screen, 800, 550, 100, button_font, (204, 204, 204), 'Start')

skydiver_button = Button(screen, 700, 500, 100, button_font, (204, 204, 204), 'Skydiver')

skydiver_title = Text(screen, 500, 100, 100, song_title_font, (255, 255, 255), 'Skydiver')

meganeko_title = Text(screen, 500, 200, 50, song_subtitle_font, (255, 255, 255), 'by Meganeko')

player = Player(screen, 20, (0, 128, 255))

player_tail1 = LaggingPlayer(screen, 14, (85,170,255), 0.1)

player_tail2 = LaggingPlayer(screen, 14, (85,170,255), 0.15)

player_tail3 = LaggingPlayer(screen, 14, (85,170,255), 0.175)

pause_text = Text(screen, 750, 500, 100, main_title_font, (255, 255, 255), 'Paused')