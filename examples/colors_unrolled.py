"""
This example displays the color palette available using 8 bit 3-3-2 RGB color.
"""

def hexlify(i):
    return hex(i)[-1]

def kill_time(i):
    """
    Kill some time at the beginning of each line to center the colors
    """
    for j in range(3):
        pyvcs.background = i
    i

def get_line_def(i):
    """
    Return the code for one line of the display
    """
    return f"""
def line{i}():
    pyvcs.wait_for_hsync()
    kill_time(0x{i}0)
    pyvcs.background = 0x{i}1
    pyvcs.background = 0x{i}2
    pyvcs.background = 0x{i}3
    pyvcs.background = 0x{i}4
    pyvcs.background = 0x{i}5
    pyvcs.background = 0x{i}6
    pyvcs.background = 0x{i}7
    pyvcs.background = 0x{i}8
    pyvcs.background = 0x{i}9
    pyvcs.background = 0x{i}a
    pyvcs.background = 0x{i}b
    pyvcs.background = 0x{i}c
    pyvcs.background = 0x{i}d
    pyvcs.background = 0x{i}e
    pyvcs.background = 0x{i}f
    """


# construct the loop for all 16*4 lines
loop = ""
for i in range(16):
    i = hexlify(i)
    exec(get_line_def(i))

    for j in range(4):
        loop += f"line{i}()\n"

# Set the color to black for the bottom
loop += "pyvcs.wait_for_hsync()\npyvcs.background = 0"

print(loop)

while True:
    pyvcs.wait_for_vsync()

    for i in range(4):
        pyvcs.wait_for_hsync()
        pyvcs.background = 255

    exec(loop)

    if pyvcs.get_key_state(pyvcs.sdl2.SDLK_ESCAPE):
        break
