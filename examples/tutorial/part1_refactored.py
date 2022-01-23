pyvcs.playfield.sprite = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
pyvcs.playfield.color = 0b11100000 # Pure Red
pyvcs.playfield.enable()
pyvcs.playfield.reflect = True
pyvcs.background = 0b00011100 # Pure Green


ball = pyvcs.Ball(8) # Create a ball with width = 8
ball.x = 40 # Set the horizontal location to 40
ball.disable()
ball_y_position = 25 # specify where the ball will begin
ball_height = 8 # Specify the ball's height

border = 4 # Border thickness of 4

while True: # Loop forever
    pyvcs.wait_for_vsync() # Synchronize with Y=-1
    y = -1 # Since we just synchronized with y=-1, we can set y here to the known scanline

    # Loop until we reach the bottom of the frame
    while y < pyvcs.constants.HEIGHT:
        # For each iteration, synchronize with the beginning of the line and increment `y`
        pyvcs.wait_for_hsync()
        y += 1

        # Do something different based on the current y
        if y == border: # At the bottom of the ceiling, set the playfield to the wall sprite
            pyvcs.playfield.sprite = [128, 0]
        elif y == ball_y_position - 1: # Enable the ball on the scanline before it starts
            ball.enable()
        elif y = ball_y_position + ball_height: # Disable the ball on it's bottom scanline
            ball.disable()
        elif y == pyvcs.constants.HEIGHT - border: # Set the playfield to be the floor/ceiling
            pyvcs.playfield.sprite = [255, 255]

    if pyvcs.get_key_state(pyvcs.sdl2.SDLK_ESCAPE):
        break
