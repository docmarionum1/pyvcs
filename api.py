Possible resolutions:
atari = 160, 192
atariT = 192, 160
squarePixels = 160, 90
spdenser = 192, 108
4x3 = 160, 120

Is vsync necessary?
vertical blank = 32
overscan = 32



#== 256 vertical lines # no because we're only 108 tall, == 172
hblank = 64 == 256 horizontal counts

if using 192, 108, total = 256 x 172 == 44032 counts per frame

pyvcs.wait_for_sync() # For syncing at the beginning of each line
blocks user code until the beam reaches the right end of the screen

pyvcs.new_frame / pyvcs.vsync # starts a new frame - necessary?

pyvcs.background(color)
pyvcs.playfield(bits, color, mode, enabled?)
pyvcs.playfield.set_color
                .set_bits # # of bits = width / 8
                .set_mode # mirror or duplicate
                .enable
                .disable

#pyvcs.Missle

Unlimited balls and players
players are associated with missles
balls share color with playfield

pyvcs.Ball
