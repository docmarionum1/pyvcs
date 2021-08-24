#from .game_lib import helper
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

# Size within the playfield walls
WALL_WIDTH = 4
TOP_HEIGHT = 6
WIDTH = pyvcs.WIDTH - WALL_WIDTH * 2
HEIGHT = pyvcs.HEIGHT - WALL_WIDTH - TOP_HEIGHT

color = 128
pyvcs.set_background(255)
ball = pyvcs.Ball(4)
ball.x = WIDTH - 12
ball_y = 12
ball.dx = -1
ball.dy = -1
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
player.x = x + WALL_WIDTH
player.y = y

player_dict = {(player.y + i - 1): player_sprite[i] for i in range(player_height)}
player_dict[player.y + player_height] = 0



pyvcs.playfield.sprite = [255, 255] #[128, 0]
pyvcs.playfield.reflect = False
pyvcs.playfield.enable()




quit = False

#ball.enable()
#while True:
#    continue

playfield = pyvcs.playfield
top_bottom = [255, 255]
wall = [128, 0]

missiles = {}
#missile_list = []

#objects = [player]



colliding = False
hp = HEIGHT
score = 0
score_text = [pyvcs.Text(0, x=WIDTH//2-5), pyvcs.Text(0, x=WIDTH//2), pyvcs.Text(0, x=WIDTH//2+5)]

missle_spawn_counter = 6
num_missiles = 0
hurt_animation = 0
score_sound = 0
jingle = 60

alive = True

press_space_lines = []

pyvcs.audio.volume = 1

# Missle sound
pyvcs.audio.channel_1.waveform = 4
pyvcs.audio.channel_1.frequency = 32

# collision sound
pyvcs.audio.channel_2.waveform = 7
pyvcs.audio.channel_2.frequency = 10

pyvcs.wait_for_vsync()

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

    x = 27
    P = pyvcs.Text("P", color=color, x=x)
    x += 10
    r = pyvcs.Text("r", color=color, x=x)
    x += 6
    e1 = pyvcs.Text("e", color=color, x=x)
    x += 6
    s1 = pyvcs.Text("s", color=color, x=x)
    x += 6
    s2 = pyvcs.Text("s", color=color, x=x)

    x += 16
    s3 = pyvcs.Text("s", color=color, x=x)
    x += 6
    p = pyvcs.Text("p", color=color, x=x)
    x += 6
    a = pyvcs.Text("a", color=color, x=x)
    x +=6
    c = pyvcs.Text("c", color=color, x=x)
    x += 6
    e2 = pyvcs.Text("e", color=color, x=x)

    while True:
        for i in range(len(left_start_screen)*4):
            j = i // 4
            if j < len(left_start_screen):
                pyvcs.playfield.sprite = left_start_screen[j]
                for k in range(4): # Kill some time
                    pass
                k # Kill slightly more time
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

        if pyvcs.get_key_state(pyvcs.sdl2.SDLK_ESCAPE):
            for f in [P, r, e1, s1, s2, s3, p, a, c, e2]:
                f.delete()

            return True

        if pyvcs.get_key_state(pyvcs.sdl2.SDLK_SPACE):
            for f in [P, r, e1, s1, s2, s3, p, a, c, e2]:
                f.delete()

            return False

        pyvcs.playfield.color = color
        #P.color = color
        for f in [P, r, e1, s1, s2, s3, p, a, c, e2]:
            f.color = color
        color = (color + 1) % 256

        pyvcs.wait_for_vsync()

quit = start_screen()

pyvcs.playfield.reflect = True

while not quit:
    # Set the color before starting the frame
    pyvcs.playfield.color = color

    # Vsync leaves us with one scanline before the visible
    # section begins; so wait till the next scanline
    #pyvcs.wait_for_hsync()

    for character in score_text:
        character.enable(1)

    pyvcs.wait_for_hsync()
    pyvcs.wait_for_hsync()

    # height the top of the playfield
    for j in range(TOP_HEIGHT - 2):
        if j < 4:
            for character in score_text:
                character.display(i=4+j, disable=3-j)
        pyvcs.wait_for_hsync()

    # The following lines kill just under one scanline of waiting. We need to do this
    # to allow drawing the player in the top left corner. Otherwise it gets cut off.
    #for j in range(19):
    #    pass

    # Count visible scanlines
    i = -1

    if alive:
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
        if alive:
            sprite = player_dict.get(i, None)
            if sprite:
                player.display(sprite=sprite)
            elif sprite == 0:
                player.disable(hp)

            if i in missiles:
                for missile in missiles[i]:
                    missile.disable(1)
        else:
            if i in press_space_map:
                j, [a, b, c, d, e] = press_space_map[i]
                a.display(i=j)
                b.display(i=j)
                c.display(i=j)
                d.display(i=j)
                e.display(i=j)

        if i == ball_y:
            ball.disable(4)

        pyvcs.wait_for_hsync()

        i += 1

    player.sprite = [0]
    # height the bottom of the playfield
    playfield.sprite = top_bottom
    for i in range(WALL_WIDTH):
        pyvcs.wait_for_hsync()

    # VBLANK Operations:
    # Check collisions
    # Update locations
    # Play sounds

    if jingle >= 0:
        if jingle == 60:
            pyvcs.audio.channel_1.volume = 2
            pyvcs.audio.channel_1.frequency = 8
        elif jingle == 50:
            pyvcs.audio.channel_1.frequency -= 1
        elif jingle == 40:
            pyvcs.audio.channel_1.frequency -= 1
        elif jingle == 30:
            pyvcs.audio.channel_1.frequency -= 1
        elif jingle == 0:
            pyvcs.audio.channel_1.frequency = 32
            pyvcs.audio.channel_1.volume = 0

        jingle -= 1
        pyvcs.wait_for_vsync()
        continue

    if ball in player.collisions:
        player.reset_collisions()
        if not colliding:
            colliding = True
            hp -= HEIGHT // 4
            hurt_animation = 20
            pyvcs.audio.channel_2.volume = 2
            pyvcs.audio.channel_2.frequency = 31
            player.color = 0
            if hp < 1:
                alive = False

                spacing = 8
                press_space_lines = []
                for word, left_margin in [("press", WIDTH//2 - 16), ("space", WIDTH//2 - 16)]:
                    press_space_lines.append([
                        pyvcs.Text(character, x=left_margin + idx*spacing) for idx, character in enumerate(word)
                    ])

                press_space_map = {16 + j: (j, press_space_lines[0]) for j in range(9)}
                press_space_map.update({32 + j: (j, press_space_lines[1]) for j in range(9)})
    elif ball not in player.collisions and colliding:
        colliding = False

    if hurt_animation > 0:
        hurt_animation -= 1
        if player.color == 0:
            player.color = 128
        else:
            player.color = 0
    if hurt_animation > 10 or (not alive and pyvcs.audio.channel_2.volume > 0):
        pyvcs.audio.channel_2.volume -= .2
        pyvcs.audio.channel_2.frequency += 1
    elif (hurt_animation == 10) or not alive:
        pyvcs.audio.channel_2.volume = 0
    # if hurt_animation == 18:
    #     pyvcs.audio.channel_2.frequency = 10
    #     pyvcs.audio.channel_2.volume -= .2
    # elif hurt_animation == 16:
    #     pyvcs.audio.channel_2.frequency = 9
    #     pyvcs.audio.channel_2.volume -= .2
    # elif hurt_animation == 14:
    #     pyvcs.audio.channel_2.volume = 0
        #hurt_animation -= 1


    if pyvcs.get_key_state(pyvcs.sdl2.SDLK_ESCAPE):
        quit = True
        break
    if alive:
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

            pyvcs.audio.channel_1.volume = 1
    else:
        if pyvcs.get_key_state(pyvcs.sdl2.SDLK_SPACE) and (missle_spawn_counter <= -60):
            for line in press_space_lines:
                for character in line:
                    character.delete()
            alive = True
            hp = HEIGHT
            x = 12
            y = 12
            player.x = x + WALL_WIDTH
            player.y = y
            player.reflect = False
            missle_spawn_counter = 6
            score = 0
            ball.dx = 1
            ball.dy = 1
            ball.x = WIDTH - 12
            ball_y = 12
            jingle = 60

    missle_spawn_counter -= 1

    if missle_spawn_counter == 0:
        pyvcs.audio.channel_1.volume = 0

    player.x = x + WALL_WIDTH
    player.y = y

    # Update the missiles
    to_delete = []
    for missile_list in missiles.values():
        for missile in missile_list:
            if ball in missile.collisions:
                to_delete.append(missile)
                ball.dx += missile.dx
                #ball.dy += 1
                score += 1
                score_sound = 6
                pyvcs.audio.channel_2.frequency = 8
                pyvcs.audio.channel_2.volume = 1



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
        missile.delete()

    ball.x += ball.dx
    if ball.x < WALL_WIDTH:
        ball.x = WALL_WIDTH
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

    if score_sound == 4:
        pyvcs.audio.channel_2.frequency = 10
        pyvcs.audio.channel_2.volume -= .2
    elif score_sound == 2:
        pyvcs.audio.channel_2.frequency = 9
        pyvcs.audio.channel_2.volume -= .2
    elif score_sound == 0:
        pyvcs.audio.channel_2.volume = 0

    score_sound -= 1


    for score_index, character in enumerate(str(score).zfill(3)):
        score_text[score_index].set_character(character)


    # Sort the list of objects by their y position
    # Create a dictionary of the y positions of objects for the next frame
    #y_dict = {object.y: object for object in objects}

    player_dict = {(player.y + i - 1): player_sprite[i] for i in range(player_height)}
    player_dict[player.y + player_height] = 0

    pyvcs.wait_for_vsync()
