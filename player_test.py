import pygame
import unittest
from sprite_setup import Player

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.radius = 20
        self.color = (0, 128, 255)
        self.screen = pygame.display.set_mode((800, 600))
    
    def tearDown(self):
        pygame.quit()
    
    def test_initialization(self):
        # Test that the player initializes properly
        player = Player(self.screen, self.radius, self.color)
        self.assertEqual(player.screen, self.screen)
        self.assertEqual(player.radius, self.radius)
        self.assertEqual(player.color, self.color)
    
    def test_color_change(self):
        # Test that the player's color can change
        player = Player(self.screen, self.radius, self.color)
        player.new_color((255, 0, 0))
        player.update()
        self.assertEqual(player.color, (255, 0, 0))

if __name__ == '__main__':
    unittest.main()