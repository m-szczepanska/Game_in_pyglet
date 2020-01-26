from random import randint
from time import sleep
import pyglet
from pyglet.window import key

from resources import (
    WINDOW_WIDTH, WINDOW_HEIGHT, SHELF_HEIGHT, PLAYER_JUMP_HEIGHT,
    PLAYER_JUMP_VELOCITY, player_image, shelf_image, bisquit_image, distance,
    dog_image, text_image
)

# We want to draw all shelves at the same time
shelf_batch = pyglet.graphics.Batch()
bisquit_batch = pyglet.graphics.Batch()


# NOTE: This should be a mixin, not a direct inheritance
class NamedSprite(pyglet.sprite.Sprite):
    """Intermediate abstract class that names all sides of a Sprite.
    """
    # NOTE: Properties are used here pretty much only because we don't want to
    #       write 'player.left()'; property allows us to do 'player.left'.
    @property
    def top(self):
        return self.y + self.height

    @property
    def bottom(self):
        return self.y

    @property
    def left(self):
        return self.x

    @property
    def right(self):
        return self.x + self.width


class Shelf(NamedSprite):
    def __init__(self, batch=shelf_batch, *args, **kwargs):
        super().__init__(img=shelf_image, batch=batch, *args, **kwargs)

    def shelf_top_center(self, shelf):
        x = shelf.left + shelf.width * 0.5
        y = shelf.top - 10
        return (x, y)

#TODO: Move this back down to bottom of the file after prototyping collisions
shelf_height_quantum = PLAYER_JUMP_HEIGHT - 100  # dunno why 20?
shelf_1 = Shelf(x=150, y=shelf_height_quantum * 0.8)
shelf_2 = Shelf(x=410, y=shelf_height_quantum + shelf_1.top)
shelf_3 = Shelf(x=60, y=shelf_height_quantum + shelf_2.top * 0.9)
shelf_4 = Shelf(x=590, y=shelf_height_quantum + shelf_3.top * 0.9)
shelf_5 = Shelf(x=130, y=shelf_height_quantum + shelf_4.top)
shelf_6 = Shelf(x=700, y=shelf_height_quantum)
shelf_7 = Shelf(x=750, y=shelf_height_quantum + shelf_4.top + 20)

shelves = shelf_1, shelf_2, shelf_3, shelf_4, shelf_5, shelf_6, shelf_7

class Bisquit(NamedSprite):
    def __init__(self, batch=bisquit_batch, *args, **kwargs):
        super().__init__(img=bisquit_image, batch=batch, *args, **kwargs)
        self.collected = False

    def bisquit_delete(self):
        if self.collected == True:
            self.scale = 0


bisquit_1 = Bisquit(
    x=shelf_1.shelf_top_center(shelf_1)[0],
    y=shelf_1.shelf_top_center(shelf_1)[1]
)
bisquit_2 = Bisquit(
    x=shelf_2.shelf_top_center(shelf_2)[0],
    y=shelf_2.shelf_top_center(shelf_2)[1]
)
bisquit_3 = Bisquit(
    x=shelf_3.shelf_top_center(shelf_3)[0],
    y=shelf_3.shelf_top_center(shelf_3)[1]
)
bisquit_4 = Bisquit(
    x=shelf_4.shelf_top_center(shelf_4)[0],
    y=shelf_4.shelf_top_center(shelf_4)[1]
)
bisquit_5 = Bisquit(
    x=shelf_5.shelf_top_center(shelf_5)[0],
    y=shelf_5.shelf_top_center(shelf_5)[1]
)
bisquit_6 = Bisquit(
    x=shelf_6.shelf_top_center(shelf_6)[0],
    y=shelf_6.shelf_top_center(shelf_6)[1]
)

bisquits = (bisquit_1, bisquit_2, bisquit_3, bisquit_4, bisquit_5, bisquit_6)


class Player(NamedSprite):
    """Player object responding to user input"""
    def __init__(self, *args, **kwargs):
        super().__init__(img=player_image, subpixel=True, *args, **kwargs)
        self.keys = dict(left=False, right=False, up=False)
        self.velocity_y = 0
        self.velocity_x = 250
        self.counter_collected = 0

    def can_jump(self):
        for shelf in shelves:
            collides_shelf = (
                (self.bottom <= shelf.top and self.bottom >= shelf.top - 10) and
                self.right >= shelf.left and
                self.left <= shelf.right
            )
            if collides_shelf:
                return True
        return self.bottom <= 0  # Standing on floor

    def can_fall(self):
        for shelf in shelves:
            collides_shelf = (
                (self.bottom <= shelf.top and self.bottom >= shelf.top - 10) and
                self.right >= shelf.left and
                self.left <= shelf.right
            )
            if collides_shelf:
                return False
        return self.bottom > 0

    def on_key_press(self, symbol, modifiers):
        if symbol == key.UP:
            self.keys['up'] = True
        if symbol == key.LEFT:
            self.keys['left'] = True
        if symbol == key.RIGHT:
            self.keys['right'] = True

    def on_key_release(self, symbol, modifiers):
        if symbol == key.UP:
            self.keys['up'] = False
        if symbol == key.LEFT:
            self.keys['left'] = False
        if symbol == key.RIGHT:
            self.keys['right'] = False

    def update(self, dt):
        self.move_horizontally(dt)
        self.move_vertically(dt)
        self.player_bisquit_collision(bisquits)

    def move_horizontally(self, dt):
        # Move left/right, don't exit the screen
        if self.keys['left'] and self.left >= 0:
            self.x -= self.velocity_x * dt
        if self.keys['right'] and self.right <= WINDOW_WIDTH:
            self.x += self.velocity_x * dt

    def move_vertically(self, dt):
        # First of all: let's fall (unless we stand on something)
        if self.can_fall():
            self.velocity_y -= 8
        else:
            self.velocity_y = 0

        # Then, let's jump
        if self.keys['up'] and self.can_jump():
            self.velocity_y = PLAYER_JUMP_VELOCITY
        self.y += self.velocity_y * dt

    def player_bisquit_collision(self, bisquits):
        for bisquit in bisquits:
            collision_distance = self.width/2 + bisquit.width/2
            actual_distance = distance(self.position, bisquit.position)
            if actual_distance <= collision_distance:
                if not bisquit.collected:  # bisquit.collected == False
                    self.counter_collected += 1
                bisquit.collected = True  # NOTE: not ==
                bisquit.bisquit_delete()


# Create all objects that we need
player = Player()

class Dog(NamedSprite):
    """Player object responding to user input"""
    def __init__(self, *args, **kwargs):
        super().__init__(img=dog_image, subpixel=True, *args, **kwargs)
        self.end_text = None
        self.velocity_y = 0
        self.velocity_x = 250

    def can_fall(self):
        for shelf in shelves:
            collides_shelf = (
                (self.bottom <= shelf.top and self.bottom >= shelf.top - 20) and
                self.right >= shelf.left and
                self.left <= shelf.right
            )
            if collides_shelf:
                return False
        return self.bottom > 0

    def move_horizontally(self, dt):
        # Move left, don't exit the screen
        if self.left >= 0:
            self.x -= self.velocity_x * dt

    def move_vertically(self, dt):
        # First of all: let's fall (unless we stand on something)
            if self.y >= 0:
                self.velocity_y -= 2
                self.y = self.velocity_y * dt


    def dog_collected(self, dt):
        if (
            player.counter_collected >= 1 and
            abs(player.x - self.x) <=10 and
            abs(player.y - self.y) <=25
        ):
            # def dog_moving_1(dt):
            #     self.x = 590
            #     self.y = 480
            # def dog_moving_2(dt):
            #     self.x = 420
            #     self.y = 250
            # def dog_moving_3(dt):
            #     self.x = 150
            #     self.y = 100
            # self.x = 150
            # self.y = 100
            # pyglet.clock.get_sleep_time(300)
            # self.x = 15
            # self.y = 0
            self.move_horizontally(dt)
            self.move_vertically(dt)

            # pyglet.clock.schedule_once(dog_moving_1, 0.5)
            # pyglet.clock.schedule_once(dog_moving_2, 0.5)
            # pyglet.clock.schedule_once(dog_moving_3, 0.5)
            # pyglet.clock.schedule_once(dog_moving_4, 0.3)
            if self.x <= 15 and self.y <= 0:
                self.end_text = pyglet.sprite.Sprite(img=text_image, x=15, y=80)
            if player.x <= 18 and player.y <= 0:
                exit()



    def update(self):
        self.dog_collected()
        self.move_vertically(dt)
        self.move_horizontally(dt)


dog = Dog(
    x=shelf_7.shelf_top_center(shelf_7)[0],
    y=shelf_7.shelf_top_center(shelf_7)[1]
)
