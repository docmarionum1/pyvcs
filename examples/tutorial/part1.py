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
    pyvcs.wait_for_hsync() # Synchronize with Y=0

    # Wait for a number of lines to give the top border a thickness of `border`
    for i in range(border):
        pyvcs.wait_for_hsync()

    # Use a shorthand to just set the first bit
    # This is equivalent to sprite = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    pyvcs.playfield.sprite = [128, 0]

    # Wait until we get to the first line of the ball
    for i in range(ball_y_position - 1):
        pyvcs.wait_for_hsync()

    ball.enable() # Now enable the ball; it will be visible starting on the next scanline

    # Wait for ball height scanlines before disabling the ball
    for i in range(ball_height):
        pyvcs.wait_for_hsync()

    ball.disable()

    # Calculate the lines remaining before the bottom border
    lines_remaining = pyvcs.constants.HEIGHT - ball_y_position - ball_height - 2*border + 1

    # Wait for that number of lines
    for i in range(lines_remaining):
        pyvcs.wait_for_hsync()

    pyvcs.playfield.sprite = [255, 255]

    if pyvcs.get_key_state(pyvcs.sdl2.SDLK_ESCAPE):
        break
