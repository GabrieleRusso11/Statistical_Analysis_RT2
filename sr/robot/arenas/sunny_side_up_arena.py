from __future__ import division

import pygame
from math import pi
from random import random
import random as py_random  # Use py_random to avoid any conflicts with other modules or variables

from .arena import Arena, ARENA_MARKINGS_COLOR, ARENA_MARKINGS_WIDTH

from ..markers import Token
from ..vision import MARKER_TOKEN_GOLD, MARKER_TOKEN_SILVER

class GoldToken(Token):
    def __init__(self, arena, marker_number):
        super(GoldToken, self).__init__(arena, marker_number,
                                        marker_type=MARKER_TOKEN_GOLD, damping=10)

    @property
    def surface_name(self):
        return 'sr/token_gold_grabbed.png' if self.grabbed else 'sr/token.png'


class SilverToken(Token):
    def __init__(self, arena, marker_number):
        super(SilverToken, self).__init__(arena, marker_number,
                                          marker_type=MARKER_TOKEN_SILVER, damping=10)

    @property
    def surface_name(self):
        return 'sr/token_silver_grabbed.png' if self.grabbed else 'sr/token_silver.png'

class SunnySideUpArena(Arena):
    size = (19, 10)
    start_locations = [( -8, -4)]

    start_headings = [pi/2]

    zone_size = 1

    def __init__(self, seed=None, objects=None, wall_markers=True):
        super(SunnySideUpArena, self).__init__(objects, wall_markers)

        # Seed the random number generator if a seed is provided
        if seed is not None:
            py_random.seed(seed)

        # Minimum distance from walls (gold tokens)
        min_distance_from_walls = 0.9  # Adjust this value as necessary
	count=0
	for i in range(38):
            token = GoldToken(self, count)
            token.location = (-9, -4.5+i*0.25)
            self.objects.append(token)
            count+1
	
        for i in range(23):
            token = GoldToken(self, count)
            token.location = (-7, -2.75+i*0.25)
            self.objects.append(token)
            count+1
        
        #for i in range(55):
        #    token = Token(self, i, damping=10)
        #    token.location = (-6.75+i*0.25, 3)
        #    self.objects.append(token)
	
        #for i in range(71):
        #    token = Token(self, i, damping=10)
        #    token.location = (-8.75+i*0.25, 5)
        #    self.objects.append(token) 
            
        for i in range(13):
             token = GoldToken(self, count)
             token.location = (-6.75+i*0.25, 3)
             self.objects.append(token)
             count+1
	
        for i in range(29):
            token = GoldToken(self, count)
            token.location = (-8.75+i*0.25, 5)
            self.objects.append(token) 
            count+1
            
        for i in range(16):
            token = GoldToken(self, count)
            token.location = (-3.5, -1+i*0.25)
            self.objects.append(token) 
            count+1
            
        for i in range(16):
            token = GoldToken(self, count)
            token.location = (-1.5, 1+i*0.25)
            self.objects.append(token) 
            count+1
            
        
        for i in range(11):
            token = GoldToken(self, count)
            token.location = (-1.25+i*0.25, 0.75)
            self.objects.append(token)
            count+1
            
        for i in range(27):
            token = GoldToken(self, count)
            token.location = (-3.25+i*0.25, -1.25)
            self.objects.append(token)
            count+1
      
        
        for i in range(16):
            token = GoldToken(self, count)
            token.location = (3.5, -1+i*0.25)
            self.objects.append(token)
            count+1 
            
        for i in range(16):
            token = GoldToken(self, count)
            token.location = (1.5, 1+i*0.25)
            self.objects.append(token) 
            count+1
            
        for i in range(13):
             token = GoldToken(self, count)
             token.location = (3.75+i*0.25, 3)
             self.objects.append(token)
             count+1
	
        for i in range(29):
            token = GoldToken(self, count)
            token.location = (1.75+i*0.25, 5)
            self.objects.append(token)
            count+1
            
        count = 0
            
        for i in range(55):
            token = GoldToken(self, count)
            token.location = (-6.75+i*0.25, -3)
            self.objects.append(token)
            count+1
	
        for i in range(71):
            token = GoldToken(self, count)
            token.location = (-8.75+i*0.25, -4.75)
            self.objects.append(token)  
            count+1 
            
        for i in range(38):
            token = GoldToken(self, count)
            token.location = (9, -4.5+i*0.25)
            self.objects.append(token)
            count+1
	
        for i in range(23):
            token = GoldToken(self, count)
            token.location = (7, -2.75+i*0.25)
            self.objects.append(token) 
            count+1

        # Predefined positions where the silver tokens will be randomly placed around
        silver_token_positions = [
            (-8, 0),
            (-6, 3.75),
            (-2.5, 1.25),
            (1.5, -0.25),
            (6, 3.75),
            (8, 0.0),
            (-4.0, -4.0)
        ]

        def is_far_enough_from_walls(x, y):
            """Ensure the silver token is not placed too close to the walls (gold tokens)."""
            # Check if the distance from the token to any wall is greater than the minimum distance
            for token in self.objects:
                if isinstance(token, GoldToken):
                    distance = ((x - token.location[0]) ** 2 + (y - token.location[1]) ** 2) ** 0.5
                    if distance < min_distance_from_walls:
                        return False
            return True

        for i, pos in enumerate(silver_token_positions):
            attempts = 0
            while attempts < 10:  # Limit attempts to avoid infinite loops
                x = py_random.uniform(pos[0] - 1.0, pos[0] + 1.0)  # Larger range for randomization
                y = py_random.uniform(pos[1] - 1.0, pos[1] + 1.0)
                if is_far_enough_from_walls(x, y):
                    token = SilverToken(self, count)
                    token.location = (x, y)
                    self.objects.append(token)
                    count += 1
                    break
                attempts += 1

    def draw_background(self, surface, display):
        super(SunnySideUpArena, self).draw_background(surface, display)

        # Corners of the inside square
        top_left     = display.to_pixel_coord((self.left + self.zone_size, self.top + self.zone_size), self)
        top_right    = display.to_pixel_coord((self.right - self.zone_size, self.top + self.zone_size), self)
        bottom_right = display.to_pixel_coord((self.right - self.zone_size, self.bottom - self.zone_size), self)
        bottom_left  = display.to_pixel_coord((self.left + self.zone_size, self.bottom - self.zone_size), self)

        # Lines separating zones
        def line(start, end):
            pygame.draw.line(surface, ARENA_MARKINGS_COLOR, \
                             start, end, ARENA_MARKINGS_WIDTH)

        line((0, 0), top_left)
        line((display.size[0], 0), top_right)
        line(display.size, bottom_right)
        line((0, display.size[1]), bottom_left)

        # Square separating zones from centre
        pygame.draw.polygon(surface, ARENA_MARKINGS_COLOR, \
                            [top_left, top_right, bottom_right, bottom_left], 2)
