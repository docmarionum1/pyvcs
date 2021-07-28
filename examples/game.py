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
pyvcs.playfield.reflect = False
pyvcs.playfield.enable()




quit = 0

#ball.enable()
#while True:
#    continue

playfield = pyvcs.playfield
top_bottom = [255, 255]
wall = [128, 0]

missiles = {}
#missile_list = []

#objects = [player]

# Size within the playfield walls
WALL_WIDTH = 4
WIDTH = pyvcs.WIDTH - WALL_WIDTH * 2
HEIGHT = pyvcs.HEIGHT - WALL_WIDTH * 2

colliding = False
hp = HEIGHT
score = 0

missle_spawn_counter = 0
num_missiles = 0

pyvcs.wait_for_vsync()

alive = True

def start_screen():
    color = 128

    left_start_screen = [
        [0, 0],
        [0, 0],
        [0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1],
        [0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1],
        [0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1],
        [0, 0]
    ]

    right_start_screen = [
        [0, 0],
        [0, 0],
        [0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0],
        [0, 0],
    ]

    empty_sprite = [0]

    # P_sprite = pyvcs.font["P"]
    # r_sprite = pyvcs.font["r"]
    # e_sprite = pyvcs.font["e"]
    # s_sprite = pyvcs.font["s"]
    # p_sprite = pyvcs.font["p"]
    # a_sprite = pyvcs.font["a"]
    # c_sprite = pyvcs.font["c"]

    #s_sprite_tmp = [0]

    x = 27
    P = pyvcs.Font("P", color=color, x=x)
    x += 10
    r = pyvcs.Font("r", color=color, x=x)
    x += 6
    e1 = pyvcs.Font("e", color=color, x=x)
    x += 6
    s1 = pyvcs.Font("s", color=color, x=x)
    x += 6
    s2 = pyvcs.Font("s", color=color, x=x)

    x += 16
    s3 = pyvcs.Font("s", color=color, x=x)
    x += 6
    p = pyvcs.Font("p", color=color, x=x)
    x += 6
    a = pyvcs.Font("a", color=color, x=x)
    x +=6
    c = pyvcs.Font("c", color=color, x=x)
    x += 6
    e2 = pyvcs.Font("e", color=color, x=x)

    while True:
        #i = 0
        #while i < HEIGHT:
        for i in range(len(left_start_screen)*4):
            j = i // 4
            if j < len(left_start_screen):
                pyvcs.playfield.sprite = left_start_screen[j]
                for k in range(12): # Kill some time
                    pass
                pyvcs.playfield.sprite = right_start_screen[j]
            i += 1

            pyvcs.wait_for_hsync()

        for i in range(8):
            pyvcs.wait_for_hsync()

        P.display(i=0)
        r.display(i=0)
        e1.display(i=0)
        s1.display(i=0)
        s2.display(i=0)

        s3.display(i=0)
        p.display(i=0)
        a.display(i=0)
        c.display(i=0)
        e2.display(i=0)

        pyvcs.wait_for_hsync()
        pyvcs.wait_for_hsync()

        for i in range(1,7):
            P.display(i=i)
            r.display(i=i)
            e1.display(i=i)
            #s_sprite_tmp = s_sprite[i]
            s1.display(i=i)
            s2.display(i=i)

            s3.display(i=i)
            p.display(i=i)
            a.display(i=i)
            c.display(i=i)
            e2.display(i=i)

            pyvcs.wait_for_hsync()

        P.display_and_disable(i=7)
        r.display_and_disable(i=7)
        e1.display_and_disable(i=7)
        s1.display_and_disable(i=7)
        s2.display_and_disable(i=7)
        s3.display_and_disable(i=7)
        p.display_and_disable(i=7)
        a.display_and_disable(i=7)
        c.display_and_disable(i=7)
        e2.display_and_disable(i=7)

        #i += 1
        #P.display(i=7, disable=0)

        # r.display(i=7, disable=0)
        # e1.display(i=7, disable=0)
        # s1.display(i=7, disable=0)
        # s2.display(i=7, disable=0)
        #
        # s3.display(i=7, disable=0)
        # p.display(i=7, disable=0)
        # a.display(i=7, disable=0)
        # c.display(i=7, disable=0)
        # e2.display(i=7, disable=0)

        #pyvcs.wait_for_hsync()


        #for f in [P, r, e1, s1, s2, s3, p, a, c, e2]:
        #    f.display_and_disable(i=7)
        #    f.sprite = empty_sprite






        if pyvcs.get_key_state(pyvcs.sdl2.SDLK_ESCAPE):
            for f in [P, r, e1, s1, s2, s3, p, a, c, e2]:
                f.delete()

            return False

        if pyvcs.get_key_state(pyvcs.sdl2.SDLK_SPACE):
            for f in [P, r, e1, s1, s2, s3, p, a, c, e2]:
                f.delete()

            return True

        pyvcs.playfield.color = color
        #P.color = color
        for f in [P, r, e1, s1, s2, s3, p, a, c, e2]:
            f.color = color
        color = (color + 1) % 256

        pyvcs.wait_for_vsync()

alive = start_screen()

pyvcs.playfield.reflect = True

while alive:
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
        elif sprite == 0:
            player.disable(hp)

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

    #player.disable()
    player.sprite = [0]
    # height the bottom of the playfield
    playfield.sprite = top_bottom
    for i in range(WALL_WIDTH):
        pyvcs.wait_for_hsync()

    if ball in player.collisions:
        player.reset_collisions()
        if not colliding:
            colliding = True
            hp -= 10
            print("Ouch", hp)
            if hp < 1:
                alive = False
    elif ball not in player.collisions and colliding:
        colliding = False

    #for obj in ball.collisions:
    #    if isinstance(obj, pyvcs.Missile) and obj != ball:
    #        print("boom")
    #        ball.reset_collisions()
    #if ball.collisions.intersection(missiles):
    #    print("Boom")
    #    ball.reset_collisions()


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
            if ball in missile.collisions:
                to_delete.append(missile)
                ball.dx += missile.dx
                #ball.dy += 1
                score += 1
            else:
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
    player_dict[player.y + player_height] = 0

    pyvcs.wait_for_vsync()
