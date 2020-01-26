from random import randint

import pyglet
from pyglet.window import key

from game_objects import player, shelf_batch, bisquit_batch, dog
from resources import WINDOW_WIDTH, WINDOW_HEIGHT, background_image


window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT)
window.push_handlers(player)


def bisquits_counter(counter):
    score_label = pyglet.text.Label(
    text=("Cookies collected: {} ".format(counter)),
    bold=True,
    x=460,
    y=720
)
    return score_label


@window.event
def on_draw():
    window.clear()
    background_image.blit(0, 0)
    player.draw()
    shelf_batch.draw()
    bisquit_batch.draw()
    dog.draw()
    if dog.end_text:
        dog.end_text.draw()
    bisquits_counter(player.counter_collected).draw()



def update(dt):
    player.update(dt)
    dog.update(dt)


if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, 1 / 60)
    pyglet.app.run()
