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
#pyvcs.set_playfield(255)

pyvcs.playfield.bits = [255, 255] #[128, 0]
pyvcs.playfield.mode = pyvcs.PlayfieldMode.REFLECT
pyvcs.playfield.enable()

x = 12
y = 12


quit = 0

#ball.enable()
#while True:
#    continue

playfield = pyvcs.playfield
top_bottom = [255, 255]
wall = [128, 0]

pyvcs.wait_for_vsync()

while True:
    # Set the color before starting the frame
    pyvcs.playfield.color = color

    # Vsync leaves us with one scanline before the visible
    # section begins; so wait till the next scanline
    pyvcs.wait_for_hsync()

    # height the top of the playfield
    for i in range(4):
        pyvcs.wait_for_hsync()

    # After doing the top of the playfield, switch to the sides
    pyvcs.playfield.bits = wall

    # Vertical positioning of the ball
    for i in range(y - 4):
        pyvcs.wait_for_hsync()

    # Enable with x
    ball.enable(x)

    # Vertical height
    for i in range(4):
        #print("y,",i)
        pyvcs.wait_for_hsync()

    ball.disable()

    #  Position the bottom of the playfield
    for i in range(pyvcs.HEIGHT - y - 8):
        pyvcs.wait_for_hsync()

    playfield.bits = top_bottom

    if pyvcs.get_key_state(pyvcs.sdl2.SDLK_LEFT):
        x = max(x - 1, 4)
        color = (color - 1) % 256
    #pyvcs.wait_for_hsync()
    if pyvcs.get_key_state(pyvcs.sdl2.SDLK_RIGHT):
        x = min(x + 1, 120)
        color = (color + 1) % 256
    #pyvcs.wait_for_hsync()
    if pyvcs.get_key_state(pyvcs.sdl2.SDLK_UP):
        color = (color - 16) % 256
        y = max(y - 1, 4)
    #pyvcs.wait_for_hsync()
    if pyvcs.get_key_state(pyvcs.sdl2.SDLK_DOWN):
        y = min(y + 1, 64)
        color = (color + 16) % 256
    #pyvcs.wait_for_hsync()
    if pyvcs.get_key_state(pyvcs.sdl2.SDLK_ESCAPE):
        break



    pyvcs.wait_for_vsync()





    #print(x,y)

    #x = (x + 1) % 188
    #background = (background + 1) % 256

    #print(pyvcs.KEY)
    #key = pyvcs.get_keycode()
    #print(key)

        #print(pyvcs.KEYS)
        # quit += 1
        # if quit > 100:
        #     print(pyvcs.KEYS)
        #     print(quit)
        #     break
    #else:
    #    print(key)

    #for i in range(10):
    #    pyvcs.wait_for_hsync()

    #pyvcs.wait_for_vsync()
    #for i in range(100):
    #    continue

    #ball.disable()
