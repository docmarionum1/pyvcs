# Part 1 - Your First pyvcs Program

In this tutorial you'll be introduced to the core concepts of programming for the pyvcs:
synchronization between the PPC and PDA and positioning objects.

## Creating and Running a Python File

First, simply create a blank python file called `part1.py`. In in put:

```
while True:
    pass
```

(TODO: Update this with more clear instructions once running pyvcs is easier)
Then run it with `python pyvcs.py part1.py`. You should see a black window pop up. You'll
need to kill your program by using `ctrl+C` in your shell. By default, the PDA is
configured to draw a black background. Since your program doesn't change this, all you see
is black while it loops forever.

## Access pyvcs and Changing the Background

When you run a python program via pyvcs, a `pyvcs` namespace is automatically in scope.
You can change the background color by assigning a number to `pyvcs.background`. Try
setting `pyvcs.background` to a number less than 256 and run `part1.py` again. For example:

```
pyvcs.background = 0b00011100 # Pure Green

while True: # Loop forever
    pass
```

pyvcs uses [8-bit color](https://en.wikipedia.org/wiki/8-bit_color),
so there are a total of 256 colors available. It uses RGB color where the first 3 bits are red,
the next 3 are green and the last 2 are blue. You can use binary integer syntax in Python to
make it easier to specify colors: `0bRRRGGGBB`.
Run `examples/colors.py` to view the full color palette.

``` {image} ../img/colors.png
:width: 100%
:align: center
```

## Displaying Game Objects

pyvcs has a number of different types of game objects available. The first ones we will
talk about are the playfield and balls.

### Playfield

The playfield is a static, non-moveable object that uses a sprite to draw objects such as
walls.

For example, put this at the top of your program:

```
pyvcs.playfield.sprite = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
pyvcs.playfield.color = 0b11100000 # Pure Red
pyvcs.playfield.enable()
```

If you run this program you will see two vertical red lines; one at the left edge
and one near the center.

The first line sets the playfield's sprite. The playfield supports a 16-bit sprite. Each
bit represents 4 pixels for a total of 64 pixels across. 64 pixels only covers
half of the screen. The other half is either duplicated or reflected from the first half.
So in this example, you've set the first 4 pixels to display the playfield and the first
4 pixels of the second half are also enabled. Try adding `pyvcs.playfield.reflect = True`.
Now you'll see two bars - one on each edge of the screen. The playfield can be used to
display more complex graphics as we'll see later. For now, lets move onto the ball object.

### Ball

Balls are moveable objects with a width and a color. The color of balls is inherited from
the color of the playfield, so the playfield and all balls will always be the same color
at any given time.

To create a ball add the following to your code:

```
ball = pyvcs.Ball(8) # Create a ball with width = 8
ball.x = 40 # Set the x location to 40
ball.enable() # Enable the ball
```

The first line creates a ball of a given width in pixels. The second line will set the horizontal
location of the ball. We'll adjust this as the ball moves around the screen. The third line
enables display of the ball. It will always draw at the given location while enabled.

If you run this program, you'll see that we get just another vertical red line, this time 8
pixels wide. As you may have noticed, we never specified either a height or vertical position.
This brings us to the next concept.

## Vertical Positioning and Synchronization

Recall from the [previous section](./hardware) that the display is divided into scanlines
and clock counts and that vertical positioning is done via timing. So far we haven't known where
in the frame the display is at any given time. There are two functions that we use to
synchronize.

- `pyvcs.wait_for_vsync`- This function pauses execution of your code until the PDA begins the
line before the first visible line, otherwise known as Y=-1. No matter where in the frame the
PDA is when you call `wait_for_vsync`, your code will halt until the next VSYNC line.
- `pyvcs.wait_for_hsync` - This function pauses execution until the beginning of the next
scanline (X=-64).

Using these two functions we can perform vertical positioning and height. For example, to give
your ball a height of 8 pixels and vertical position of 24 we would first wait for the 24th
scanline to begin, then enable the ball, and then disable the ball again after 8 lines, replace
your existing `while True` loop with the following.

```
...

ball.disable()
ball_y_position = 25 # specify where the ball will begin
ball_height = 8 # Specify the ball's height

while True: # Loop forever
    pyvcs.wait_for_vsync() # Synchronize with Y=-1
    pyvcs.wait_for_hsync() # Synchronize with Y=0

    # Wait until we get to the line before the ball starts
    for i in range(ball_y_position - 1):
        pyvcs.wait_for_hsync()

    ball.enable() # Now enable the ball; it will be visible starting on the next scanline

    # Wait for ball height scanlines before disabling the ball
    for i in range(ball_height):
        pyvcs.wait_for_hsync()

    ball.disable()
```

Now we have an 8x8 red ball displayed in the middle of the screen. It takes one scanline for
enabling and disabling changes to be reflected on the display, so we actually need to call
`ball.enable()` the line before we want to show it.

We can also change the
playfield during the frame to display more complex walls. For example, to display a floor
and a ceiling in addition to walls we would switch the playfield's sprite at the beginning
and end of the visible frame. With that change, the whole loop would be:

```
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
```

We decide that we want a border thickness of 4, to match the walls we already drew. So we need
to wait for 4 scanlines at the beginning before changing the playfield to be just the left and
right walls, then at the end we need to switch it to be the full playfield. The change at the
end of the loop persists till we change it again, so the ceiling will be the same as the floor
even though we only set the sprite at the end.

Here we use shorthand for declaring the sprite, using a list of two bytes instead of a list of
16 bits.

As you can see, the timing can start to get quite complex. You also might have noticed that
the ball actually moved down in this version because our second loop `for i in
range(ball_y_position - 1)` is the same, even though we added the 4 scanline loop at
the beginning.

## Wrapping Up

Here is a version of the program we made refactored to instead keep track of the
current scanline `y` and then change the ball and playfield depending on the current
line. This approach will be much more scalable as you add more objects to the game.

```
pyvcs.background = 0b00011100 # Pure Green

pyvcs.playfield.color = 0b11100000 # Pure Red
pyvcs.playfield.reflect = True # Set the playfield to reflect mode
pyvcs.playfield.enable()


ball = pyvcs.Ball(8) # Create a ball with width = 8
ball.x = 40 # Set the horizontal location to 40
ball.disable()

# The ball doesn't have built-in support for y position and height, so we need to
# track these manually.
ball_y_position = 25 # specify where the ball will begin
ball_height = 8 # Specify the ball's height

# Our desired thickness for the floor and ceiling
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

    # Quit the game if the escape key is pressed
    if pyvcs.get_key_state(pyvcs.sdl2.SDLK_ESCAPE):
          break
```

At the bottom of the program you'll see the first example of handling user input.
This will allow you to quit the game by pressing `Escape` instead of `Ctrl+C` in
the console.

In the next section we'll be discussing user input in more detail, along with
collision detection. 
