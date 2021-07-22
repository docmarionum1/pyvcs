from .game_lib import helper
#from pyvcs import set_background

def bar(a):
    return a*a

def foo():
    c = 0
    print('bar')
    a = 1 + 1
    for i in range(1200000):
        if i % 100000 == 0:
            print(i)
        if i % 2:
            a += a + i

    b = bar(a + 2)
    print('barb', b % 30000)
    #print("tickle", ticks, monitor.ticks)
    return b*a % 50000
    #print('barbar')
    #print('barbarbar')

#foo()
# def game():
#     #USER_CODE_2 = 2
#     a = 1
#     b = a + 1
#     c = helper(b)
#     print(a, b, c)
#
# game()

color = 128
pyvcs.set_background(255)
ball = pyvcs.Ball(4)
ball.x = 50
ball_y = 50
ball.dx = 1
ball.dy = 1
ball_y_end = 54
#pyvcs.set_playfield(255)
player_sprite = [
    [0],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 0, 1, 0, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 0, 0, 0, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
]

player_height = len(player_sprite)

x = 12
y = 12

player = pyvcs.Player(player_sprite[0])
player.y = y

player_dict = {(player.y + i): player_sprite[i] for i in range(player_height)}



pyvcs.playfield.sprite = [255, 255] #[128, 0]
pyvcs.playfield.reflect = True
pyvcs.playfield.enable()




quit = 0

#ball.enable()
#while True:
#    continue

playfield = pyvcs.playfield
top_bottom = [255, 255]
wall = [128, 0]

missiles = {}

#objects = [player]

# Size within the playfield walls
WALL_WIDTH = 4
WIDTH = pyvcs.WIDTH - WALL_WIDTH * 2
HEIGHT = pyvcs.HEIGHT - WALL_WIDTH * 2

missle_spawn_counter = 0
num_missiles = 0

pyvcs.wait_for_vsync()

while True:
    # Set the color before starting the frame
    pyvcs.playfield.color = color

    # Count visible scanlines
    i = -1

    # Vsync leaves us with one scanline before the visible
    # section begins; so wait till the next scanline
    pyvcs.wait_for_hsync()

    # height the top of the playfield
    for j in range(3):
        pyvcs.wait_for_hsync()

    # The following lines kill just under one scanline of waiting. We need to do this
    # to allow drawing the player in the top left corner. Otherwise it gets cut off.
    #for j in range(19):
    #    pass

    sprite = player_dict.get(i, None)
    if sprite:
        player.display(sprite=sprite)
    else:
        player.disable()

    if i == ball_y:
        ball.disable(4)

    pyvcs.wait_for_hsync()

    i = 0

    # After doing the top of the playfield, switch to the sides
    pyvcs.playfield.sprite = wall

    while i < HEIGHT:
        sprite = player_dict.get(i, None)
        if sprite:
            player.display(sprite=sprite)
        #else:
        #    player.disable()

        if i in missiles:
            for missile in missiles[i]:
                missile.disable(1)

        #if (i >= ball_y) and (i < ball_y_end):
        #    ball.enable()
        #else:
        #3    ball.disable()

        if i == ball_y:
            ball.disable(4)
        #elif i == ball_y_end:
        #    ball.disable()


        #pyvcs.wait_for_hsync()

        #if (i - 1) in missiles:
        #    for missile in missiles[i - 1]:
        #        missile.disable(0)

        #if i >= ball.y and


        pyvcs.wait_for_hsync()

        # j = (i - player.y)
        # if j >= 0 and j < len(player_sprite):
        #     player.enable()
        #     player.sprite = player_sprite[j]
        # else:
        #     player.disable()

        i += 1


    # height the bottom of the playfield
    playfield.sprite = top_bottom
    for i in range(WALL_WIDTH):
        pyvcs.wait_for_hsync()



    # Vertical positioning of the player
    #for i in range(y - 4):
    #    pyvcs.wait_for_hsync()

    # Enable with x
    #ball.enable(x)
    #player.enable()

    # Vertical height
    # for i in range(5):
    #     #print("y,",i)
    #     player.sprite = player_sprite[i]
    #     pyvcs.wait_for_hsync()

    #player.disable()

    #  Position the bottom of the playfield
    #for i in range(pyvcs.HEIGHT - y - 8):
    #    pyvcs.wait_for_hsync()

    #playfield.sprite = top_bottom

    if pyvcs.get_key_state(pyvcs.sdl2.SDLK_LEFT):
        x = max(x - 1, 0)
        color = (color - 1) % 256
        player.reflect = True
    if pyvcs.get_key_state(pyvcs.sdl2.SDLK_RIGHT):
        x = min(x + 1, WIDTH - 8)
        color = (color + 1) % 256
        player.reflect = False
    if pyvcs.get_key_state(pyvcs.sdl2.SDLK_UP):
        y = max(y - 1, 0)
        color = (color - 16) % 256
    if pyvcs.get_key_state(pyvcs.sdl2.SDLK_DOWN):
        y = min(y + 1, HEIGHT - player_height)
        color = (color + 16) % 256
    if pyvcs.get_key_state(pyvcs.sdl2.SDLK_SPACE) and (num_missiles < 3) and (missle_spawn_counter <= 0):
        missle_spawn_counter = 6
        num_missiles += 1
        missile = player.spawn_missile(4)
        missile.y = y + 2
        # Player is facing left
        if player.reflect:
            missile.x = x + 8
            missile.dx = -2
        else: # Player is facing right
            missile.x = x + 4
            missile.dx = 2
        #missiles.append(missile)
        if missile.y not in missiles:
            missiles[missile.y] = []
        missiles[missile.y].append(missile)
    missle_spawn_counter -= 1
    if pyvcs.get_key_state(pyvcs.sdl2.SDLK_ESCAPE):
        break

    player.x = x + WALL_WIDTH
    player.y = y

    # Update the missiles
    #for y, missile in list(missiles.items())[:]:
    to_delete = []
    for missile_list in missiles.values():
        for missile in missile_list:
            #if isinstance(missile, pyvcs.Missile):
            missile.x += missile.dx

            if missile.x < 0 or missile.x > pyvcs.WIDTH:
                to_delete.append(missile)

    for missile in to_delete:
        num_missiles -= 1
        missiles[missile.y].remove(missile)
        if len(missiles[missile.y]) == 0:
            del missiles[missile.y]
        #del missile
        missile.delete()

    ball.x += ball.dx
    if ball.x < 4:
        ball.x = 4
        ball.dx = -ball.dx
    if ball.x > WIDTH:
        ball.x = WIDTH
        ball.dx = -ball.dx

    print(ball_y, ball.dy)
    ball_y += ball.dy
    if ball_y < -1:
        ball_y = -1
        ball.dy = -ball.dy
    if ball_y > (HEIGHT - 4):
        ball_y = HEIGHT - 4
        ball.dy = -ball.dy
    ball_y_end = ball_y + 4


    # Sort the list of objects by their y position
    # Create a dictionary of the y positions of objects for the next frame
    #y_dict = {object.y: object for object in objects}

    player_dict = {(player.y + i - 1): player_sprite[i] for i in range(player_height)}

    pyvcs.wait_for_vsync()
