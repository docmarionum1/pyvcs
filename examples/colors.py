"""
This example displays the color palette available using 8 bit 3-3-2 RGB color.
"""

pyvcs.wait_for_vsync()

y = -8

while True:
    pyvcs.wait_for_vsync()

    # We only have time for *just* 8 transitions per scanline and only if
    # We unroll each scanline loop and also unroll the set of three scanlines
    for i in range(32):
        y += 8

        pyvcs.wait_for_hsync()
        for j in range(4):
            pyvcs.background = y

        pyvcs.background = y + 1
        pyvcs.background = y + 2
        pyvcs.background = y + 3
        pyvcs.background = y + 4
        pyvcs.background = y + 5
        pyvcs.background = y + 6
        pyvcs.background = y + 7

        pyvcs.wait_for_hsync()
        for j in range(4):
            pyvcs.background = y

        pyvcs.background = y + 1
        pyvcs.background = y + 2
        pyvcs.background = y + 3
        pyvcs.background = y + 4
        pyvcs.background = y + 5
        pyvcs.background = y + 6
        pyvcs.background = y + 7


    y = -8

    if pyvcs.get_key_state(pyvcs.sdl2.SDLK_ESCAPE):
        break
