import pygame
import unittest
from game_object_setup import GameObject

class TestGameObject(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.id = 1
        self.x = 50
        self.y = 50
        self.width = 50
        self.height = 50
        self.r = 255
        self.g = 0
        self.b = 0
        self.alpha = 255
        self.danger = "yes"
        self.parent = None
        self.timestart = 0
        self.timestop = 100
        self.movex = 0
        self.movey = 0

    def tearDown(self):
        pygame.quit()

    def test_initialization(self):
        # Test that the object is initialized correctly
        game_object = GameObject(self.screen, self.id, self.x, self.y, self.width, self.height, self.r, self.g, self.b, self.alpha, self.danger, self.parent, self.timestart, self.timestop, self.movex, self.movey)
        self.assertEqual(game_object.id, self.id)
        self.assertEqual(game_object.rect.x, self.x)
        self.assertEqual(game_object.rect.y, self.y)
        self.assertEqual(game_object.danger, self.danger)

    def test_collision_detection(self):
        # Test collision detection with the mouse
        game_object = GameObject(self.screen, self.id, self.x, self.y, self.width, self.height, self.r, self.g, self.b, self.alpha, self.danger, self.parent, self.timestart, self.timestop, self.movex, self.movey)
        pygame.mouse.set_pos(self.x + 10, self.y + 10)
        game_object.update()
        self.assertTrue(game_object.lifelost)

        # Simulate mouse position outside the object
        pygame.mouse.set_pos(0, 0)
        game_object.update()
        self.assertFalse(game_object.lifelost)

    def test_parent_object(self):
        # Test the parent object functionality
        game_object = GameObject(self.screen, self.id, self.x, self.y, self.width, self.height, self.r, self.g, self.b, self.alpha, self.danger, self.parent, self.timestart, self.timestop, self.movex, self.movey)
        
        # Create a parent object
        parent_x = 100
        parent_y = 100
        parent_width = 100
        parent_height = 100
        parent_object = GameObject(self.screen, 2, parent_x, parent_y, parent_width, parent_height, self.r, self.g, self.b, self.alpha, self.danger, self.parent, self.timestart, self.timestop, self.movex, self.movey)
        game_object.parent_object = parent_object
        game_object.update()
        self.assertEqual(game_object.rect.x, parent_x)
        self.assertEqual(game_object.rect.y, parent_y)

if __name__ == '__main__':
    unittest.main()