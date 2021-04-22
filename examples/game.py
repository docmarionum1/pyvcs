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

background = 128
pyvcs.set_background(255)
ball = pyvcs.Ball(4)
pyvcs.set_playfield(255)
x = 0
y = 0
pyvcs.wait_for_vsync()

#ball.enable()
#while True:
#    continue

while True:
    #pyvcs.set_background([background & 0xff, (background & 0xff00) >> 8, (background & 0xff0000) >> 16])
    #background += 1
    #print("hi")
    #pyvcs.wait_for_hsync()
    #pyvcs.wait_for_vsync()
    #for i in range(int(x/10)):
    #pass
    #pass
    #pass
    #pass
    #for i in range(2):
    #    pass

    #for i in range(x):
    #    pass

    pyvcs.set_playfield(background)

    # Vertical positioning
    for i in range(y + 63):
        pyvcs.wait_for_hsync()

    # Enable with x
    ball.enable(x)

    # Vertical height
    for i in range(4):
        #print("y,",i)
        pyvcs.wait_for_hsync()

    ball.disable()

    #print(x,y)

    #x = (x + 1) % 188
    #background = (background + 1) % 256

    #print(pyvcs.KEY)
    #key = pyvcs.get_keycode()
    #print(key)
    if pyvcs.get_key_state(pyvcs.sdl2.SDLK_LEFT):
        #print("lf")
        x = max(x - 1, 0)
        background = (background - 1) % 256
    if pyvcs.get_key_state(pyvcs.sdl2.SDLK_RIGHT):
        #print("ri")
        x = min(x + 1, 188)
        background = (background + 1) % 256
    if pyvcs.get_key_state(pyvcs.sdl2.SDLK_UP):
        background = (background - 16) % 256
        y = max(y - 1, 0)
    if pyvcs.get_key_state(pyvcs.sdl2.SDLK_DOWN):
        y = min(y + 1, 104)
        background = (background + 16) % 256
    if pyvcs.get_key_state(0x1b):
        break
    #else:
    #    print(key)

    #for i in range(10):
    #    pyvcs.wait_for_hsync()
    pyvcs.wait_for_vsync()
    #for i in range(100):
    #    continue

    #ball.disable()
