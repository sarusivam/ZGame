import pygame
import math
import os
import random
import time

all_objects = []
WIDTH, HEIGHT = 1000, 800


class StaticObject:
    def __init__(self,x, y, width, height,color, cirlce=False, hidden=False):
        self.rect = pygame.Rect(x, y, width, height)
        self.isCircle = cirlce
        self._hidden = hidden
        self.color = color
        
    @property
    def hidden(self):
        return self._hidden

    @hidden.setter
    def hidden(self, new_val):
        assert new_val in [True, False], "Hidden is boolean type"
        self._hidden = new_val

    
    def draw(self, win):
        if not self.hidden:
            pygame.draw.rect(win, self.color, self.rect) if not self.isCircle else pygame.draw.circle(win, self.color, (self.rect.x, self.rect.y), (self.rect.width + self.rect.height) / 2)

class MovableObject(StaticObject):
    def __init__(self, x, y, width, height, color,object_x_vel, object_y_vel, cirlce=False, hidden=False):
        super().__init__(x, y, width, height, color, cirlce, hidden)
        self.x_vel = 0
        self.y_vel = 0
        self.object_x_vel = object_x_vel
        self.object_y_vel  = object_y_vel
    def move_right(self):
        self.x_vel = self.object_x_vel
    def move_left(self):
        self.x_vel = self.object_x_vel * -1
    def move_up(self):
        self.y_vel = self.object_y_vel
    def move_down(self):
        self.y_vel = self.object_y_vel * -1

    def move(self):
        self.rect.x += self.x_vel
        self.rect.y -= self.y_vel
    def handle_keydown(self, key):
        pass
    def handle_keyup(self, key):
        pass
    

    def update(self):
        self.move()



class Player(MovableObject):
    def __init__(self, x, y, width, height, color, object_x_vel, object_y_vel, cirlce=False, hidden=False):
        super().__init__(x, y, width, height, color, object_x_vel, object_y_vel, cirlce, hidden)
        self.bullets = []
        self.reload_counter = 0
        self.reload_time = 10
        self.bullet_colors = [(255, 255, 0), (255, 0, 0), (0, 0, 255)]
        self.bullet_color_index = 0
    def update(self):
        self.move()
        self.reload_counter += 1
    
        for bullet in self.bullets:
            bullet.update()
    def handle_movement(self):
            self.x_vel = self.y_vel = 0
            keys= pygame.key.get_pressed()
            if keys[pygame.K_d] and self.rect.x + self.object_x_vel + self.rect.width <= WIDTH:
                self.move_right()
            if keys[pygame.K_a] and self.rect.x - self.object_x_vel >= 0:
                self.move_left()
            if keys[pygame.K_w] and self.rect.y - self.object_y_vel >= 0:
                self.move_up()
            if keys[pygame.K_s] and self.rect.y + self.rect.height + self.object_y_vel <= HEIGHT:
                self.move_down()

    def draw(self, win):
        super().draw(win)            

        for bullet in self.bullets:
            bullet.color = self.bullet_colors[self.bullet_color_index % 3]
            bullet.draw(win) 

    def shoot(self):
        if self.reload_counter >= self.reload_time:
            self.bullets.append(Bullet(min(50, self.reload_counter), 10, (255,255,0), 15,0,self))
            self.reload_counter = 0
    def handle_keydown(self, key):
        super().handle_keydown(key)
        if key == pygame.K_SPACE:
            self.shoot()
        if (key == pygame.K_DOWN or key == pygame.K_LEFT):
                self.bullet_color_index -= 1
        if (key == pygame.K_UP or key == pygame.K_RIGHT):
                self.bullet_color_index += 1

class Enemy(MovableObject):
    def __init__(self, x, y, width, height, color, object_x_vel, object_y_vel, cirlce=False, hidden=False):
        super().__init__(x, y, width, height, color, object_x_vel, object_y_vel, cirlce, hidden)
class Bullet(MovableObject):
    def __init__(self, width, height, color, object_x_vel, object_y_vel,host, cirlce=False, hidden=False):
        self.host = host
        super().__init__(self.host.rect.x + self.host.rect.width, self.host.rect.y + (self.host.rect.height / 2), width, height, color, object_x_vel, object_y_vel, cirlce, hidden)
        self.x_vel = self.object_x_vel
        self.y_vel = self.object_y_vel
    def update(self):
        super().update()
        if self.rect.x + self.x_vel + self.rect.width > WIDTH or self.rect.y + self.y_vel + self.rect.height > HEIGHT:
            del self

class Text():
    def __init__(self, x, y, font_size, color,text,font_type='Comic Sans MS'):
        pygame.font.init()
        self._text = text
        self.x = x
        self.y = y
        self.color = color

        self.font = pygame.font.SysFont(font_type, font_size)
    @property
    def text(self):
        return self._text
    @text.setter
    def text(self, text : str):
        assert type(text) is str, "Text should be of str type !!!"
        self._text = text
    @classmethod
    def get_text_from_dict(cls, dictionary:dict):
        return cls(**dictionary)
 
    def draw(self, screen):
        my_font = self.font.render(self.text,False, self.color)
        screen.blit(my_font,(self.x, self.y))
    def update_font(self, font):
        self.font = pygame.font.SysFont(font)


