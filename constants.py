import sdl2

# Visible screen size
WIDTH = 128
HEIGHT = 72

# Blank parts of the screen at the top and left
HBLANK = 64
VBLANK = 32
VSYNC_LINE = -1 # 1 scanline before the visible part of the image starts

# How many steps the display advances for each operation on the CPU
DISPLAY_CLOCK_RATIO = 3

# WIDTH + HBLANK % 3 == 0 because the display does 3 steps per user instruction
assert (WIDTH + HBLANK) % DISPLAY_CLOCK_RATIO == 0

PLAYFIELD_WIDTH = WIDTH // 2 # The playfield is half the width of the screen
PLAYFIELD_RESOLUTION = 4 # Each bit of the playfield sprite is equal to 4 display clock counts
PLAYFIELD_SPRITE_WIDTH_BYTES = PLAYFIELD_WIDTH // PLAYFIELD_RESOLUTION // 8

#RESOLUTION = (WIDTH, HEIGHT)

# Use 1 byte per pixel in 332 format
PIXEL_FORMAT = sdl2.SDL_PIXELFORMAT_RGB332
PIXEL_FORMAT_BYTES = 1
