"""
This example displays the color palette available using 8 bit 3-3-2 RGB color.
"""

pyvcs.wait_for_vsync()

y = -8

while True:
    # VBLANK
    for i in range(62):
        pyvcs.wait_for_hsync()

    # We only have time for *just* 8 transitions per scanline and only if
    # We unroll each scanline loop and also unroll the set of three scanlines
    for i in range(32):
        y += 8

        pyvcs.wait_for_hsync()
        pyvcs.set_background(y)
        pyvcs.set_background(y)
        pyvcs.set_background(y)
        pyvcs.set_background(y)
        pyvcs.set_background(y + 1)
        pyvcs.set_background(y + 2)
        pyvcs.set_background(y + 3)
        pyvcs.set_background(y + 4)
        pyvcs.set_background(y + 5)
        pyvcs.set_background(y + 6)
        pyvcs.set_background(y + 7)

        pyvcs.wait_for_hsync()
        pyvcs.set_background(y)
        pyvcs.set_background(y)
        pyvcs.set_background(y)
        pyvcs.set_background(y)
        pyvcs.set_background(y + 1)
        pyvcs.set_background(y + 2)
        pyvcs.set_background(y + 3)
        pyvcs.set_background(y + 4)
        pyvcs.set_background(y + 5)
        pyvcs.set_background(y + 6)
        pyvcs.set_background(y + 7)

        pyvcs.wait_for_hsync()
        pyvcs.set_background(y)
        pyvcs.set_background(y)
        pyvcs.set_background(y)
        pyvcs.set_background(y)
        pyvcs.set_background(y + 1)
        pyvcs.set_background(y + 2)
        pyvcs.set_background(y + 3)
        pyvcs.set_background(y + 4)
        pyvcs.set_background(y + 5)
        pyvcs.set_background(y + 6)
        pyvcs.set_background(y + 7)

    y = -8

    if pyvcs.get_key_state(0x1b):
        break

    pyvcs.wait_for_vsync()
