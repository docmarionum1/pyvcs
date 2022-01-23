# "Hardware"

pyvcs is heavily inspired by the Atari VCS. If you are familiar with that system, much of
this will be familiar.

## CPU

The CPU in pyvcs is a pyvcs-Python CPU (PPC). The PPC runs a
[customized version](https://github.com/docmarionum1/pyvcs-python) of Python 3.9
that is built to interface with the rest of the pyvcs system. Otherwise it works exactly
like the Python that you are used to.

## Display Protocol

``` {image} ../img/display.png
:width: 100%
:align: center
```

pyvcs displays a picture that is 128 pixels wide by 72 pixels tall (128x72).
The vertical units are also known as [scanlines](https://en.wikipedia.org/wiki/Scan_line)
and the horizontal units are known as clock counts.

pyvcs uses a chip known as the pyvcs Display Adapter (PDA) to draw to the screen.
The PDA runs in parallel to the PPC. The PDA advances 3 clock counts for every[^opcode] one opcode
processed by the PPC.

The PDA can store various game objects with X coordinates, but not Y coordinates. Therefore
it is not possible to specify ahead of time which scanline an object should be drawn on.
Each scanline must be rendered by your program as the PDA draws it.

In addition to the visible picture,
there is additional 32 hidden scanlines called VBLANK and 64 hidden clock counts per
scanline. This gives a total of 192x104=19968 clock counts per frame. 128x72=9216 are
visible and 10752 are hidden.

Most of the CPU time during the visible picture will be dedicated to rendering the picture.
Therefore the BLANK areas are useful for game logic.

In pyvcs, we refer to the coordinates (X,Y) of the image with (0,0) at the top left of the
*visible* picture and (127,71) as the bottom right of the visible picture. We use negatives
to refer to the parts of the picture that are in the BLANK areas. (-64,-32) is the top
left of the entire display.

The picture is drawn starting from (-64,-32). Each scanline is drawn from left to right.
After reaching (127, -32) the PDA advances to (-64, -31) and so on. Nothing is drawn
while either X or Y are negative. When the PDA reaches (-64, -1) a signal called VSYNC is
sent to the PPC. This will be discussed more later. Starting at (-64, 0) the PDA has
reached the first line of the visible picture, but hasn't yet reached the visible part
of the scanline in the X direction. At (0, 0) it starts drawing to the screen based on
how it has been configured by your program. It draws 128 pixels from (0, 0) to (127, 0)
and then advances to (-64, 1). It advances in this way until (127, 71) at which point it
goes back to (-64, -32).

[^opcode]: The PPC runs python opcodes in constant time, equivalent to 3 clock counts of
the PDA with the exception of `LOAD_*` opcodes which run instantaneously, equivalent to 0
clock counts of the PDA.
