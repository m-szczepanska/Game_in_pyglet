import pyglet


WINDOW_HEIGHT = 740
WINDOW_WIDTH = 1020
SHELF_HEIGHT = 30
PLAYER_JUMP_HEIGHT = 210
PLAYER_JUMP_VELOCITY = 420  # blaze it

pyglet.resource.path = ["../pictures"]
pyglet.resource.reindex()

solid_orange = pyglet.image.SolidColorImagePattern((200, 100, 50, 0))
background_image = solid_orange.create_image(1020, 1020)

# TODO: Cut her arms off or find a better image
player_image = pyglet.resource.image("girl.png")
shelf_image = pyglet.resource.image("shelf.png")
bisquit_image = pyglet.resource.image("cookie.png")
dog_image = pyglet.resource.image("chief.png")
text_image = pyglet.resource.image("letsgo.png")




def distance(point_1, point_2):
    return abs(point_1[0] - point_2[0]) + abs(point_1[1] - point_2[1])
