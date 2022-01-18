from argparse import Namespace
import array
from collections.abc import Iterable
import ctypes
import dis
from enum import IntEnum
from functools import partial
import opcode
from pathlib import Path
import sys
import time

import sdl2
import sdl2.ext

from audio import audio, audio_context
import constants
from font import uppercase, lowercase


class Input:
    def __init__(self):
        self.keys = {
            sdl2.SDLK_UP: False,
            sdl2.SDLK_DOWN: False,
            sdl2.SDLK_LEFT: False,
            sdl2.SDLK_RIGHT: False,
            sdl2.SDLK_ESCAPE: False,
            sdl2.SDLK_SPACE: False
        }

    # Process events once a frame
    def _get_events(self):
        for event in sdl2.ext.get_events():
            key = event.key.keysym.sym
            if key in self.keys:
                if event.type == sdl2.SDL_KEYDOWN:
                    self.keys[key] = True
                    #print(KEY)
                    #break
                elif event.type == sdl2.SDL_KEYUP:
                    self.keys[key] = False

    def get_key_state(self, keycode):
        return self.keys[keycode]

input = Input()


class Display:
    def __init__(self):
        self._set_contstants()

        self.x = 0
        self.y = 0
        self._background = 0
        self._players = []
        self._missiles = []

        self._start = time.time()

        self._init_sdl()

    def _set_contstants(self):
        self.width = constants.WIDTH
        self.height = constants.HEIGHT
        self.resolution = (self.width, self.height)

        # Create an array to store the pixel of each frame
        self.frame = array.array(
            'B',
            [0] * (self.width * self.height * constants.PIXEL_FORMAT_BYTES)
        )
        # Pointer to the frame
        self.frame_pointer = ctypes.c_void_p(self.frame.buffer_info()[0])

        self.hblank = constants.HBLANK
        self.vblank = constants.VBLANK
        self.vsync_line = constants.VSYNC_LINE
        self.display_clock_ratio = constants.DISPLAY_CLOCK_RATIO

    def _init_sdl(self):
        sdl2.ext.init()
        self.window = sdl2.ext.Window(
            "window",
            size=self.resolution,
            flags=sdl2.SDL_WINDOW_FULLSCREEN_DESKTOP
        )
        self.renderer = sdl2.ext.Renderer(
            self.window,
            logical_size=self.resolution,
            flags=sdl2.SDL_RENDERER_ACCELERATED | sdl2.SDL_RENDERER_PRESENTVSYNC
        )
        #self.surface = sdl2.SDL_CreateRGBSurfaceWithFormat(0, *RESOLUTION, 8, sdl2.SDL_PIXELFORMAT_RGB332)
        self.texture = sdl2.SDL_CreateTexture(
            self.renderer.renderer,
            constants.PIXEL_FORMAT,
            sdl2.SDL_TEXTUREACCESS_STREAMING,
            *self.resolution
        )

        self.window.show()

    def _quit(self):
        sdl2.SDL_DestroyTexture(self.texture)
        sdl2.SDL_DestroyRenderer(self.renderer.renderer)
        sdl2.SDL_DestroyWindow(self.window.window)
        sdl2.ext.quit()

    def _write_pixel(self, x, y):
        # Determine the color of this pixel by checking if any of the objects are set in this order
        #   players / text
        #   missiles / ball
        #   playfield
        #   background
        pixel = None
        collisions = set()

        for player in self._players:
            if player._enabled and (x >= player.x) and (x < (player.x + player._internal_width)):
                if player.reflect:
                    if player._reverse[x - player.x]:
                        if pixel is None:
                            pixel = player.color
                        if player.collidable:
                            collisions.add(player)
                else:
                    if player._bits[x - player.x]:
                        if pixel is None:
                            pixel = player.color
                        if player.collidable:
                            collisions.add(player)

        for missile in self._missiles:
            if (
                ((missile._enabled == 1) or (missile._enabled < 0)) and
                (x >= missile.x) and (x < (missile.x + missile.width))
            ):
                if pixel is None:
                    pixel = missile.player.color
                if missile.collidable:
                    collisions.add(missile)

        playfield = self._playfield
        if playfield._enabled:
            # Left half
            if x < playfield._internal_width:
                if playfield._bits[x]:
                    if pixel is None:
                        pixel = playfield.color
                    if playfield.collidable:
                        collisions.add(playfield)
            else:
                if playfield.reflect:
                    if playfield._reverse[x - playfield._internal_width]:
                        if pixel is None:
                            pixel = playfield.color
                        if playfield.collidable:
                            collisions.add(playfield)
                else:
                    if playfield._bits[x - playfield._internal_width]:
                        if pixel is None:
                            pixel = playfield.color
                        if playfield.collidable:
                            collisions.add(playfield)

        if len(collisions) > 1:
            for object in collisions:
                object.collisions.update(collisions)

        # TODO: Fun feature, turn off background filling for painting program
        if pixel is None:
            pixel = self._background# BACKGROUND_COLOR

        # Set the color; possibly return it and have someone else set it
        self.frame[y * self.width + x] = pixel

    def _present_frame(self):
        sdl2.SDL_UpdateTexture(
            self.texture.contents,
            None,
            self.frame_pointer,
            self.width
        )
        self.renderer.copy(self.texture.contents)
        self.renderer.present()
        self.renderer.clear()
        self.window.refresh()

    def _display_fps(self):
        sys.stdout.write('\r')
        sys.stdout.write("%.2f" % (1 / (time.time() - self._start)))
        sys.stdout.flush()
        self._start = time.time()

    def _display_step(self):
        # TODO: Figure out if this is more efficient to store them locally vs access them
        # as an attr constantly
        x, y = self.x, self.y

        # Process visible section of of the screen
        if (x >= 0) and (y >= 0):
            self._write_pixel(x, y)

        # X always increments by one for each display step
        x += 1

        if x == self.width:
            x = -self.hblank
            y += 1
            #print(y)
            # If we've finished the last line
            if y == self.height:
                self._present_frame()
                input._get_events()
                self._display_fps()
                y = -self.vblank
            # If we're in the visible secrtion, update the objects' enabled status
            elif y >= 0:
                for object in self._missiles + self._players + [self._playfield]:
                    object._enabled = object._next_enabled

                    if object._next_enabled > 1:
                        object._next_enabled -= 1
                    if object._next_enabled < 0:
                        object._next_enabled += 1

            # If we're on the vsync line, return vysnc code
            elif y == self.vsync_line:
                self.x, self.y = x, y
                return 2 # VSYNC returns 2, also counts as a hsync

            self.x, self.y = x, y
            return 1 # HYSNC

        # We didn't get to the end of a line yet
        self.x = x
        return 0

    def wait_for_hsync(self):
        while self._display_step() == 0:
            pass

    def wait_for_vsync(self):
        while self._display_step() < 2:
            pass



display = Display()


class Object:
    def __init__(self, collection=None, enabled=0, collidable=True):
        self._enabled = 0
        self._next_enabled = enabled
        self._drawing = False

        if collection is None:
            self.collection = []
        else:
            self.collection = collection
        self.collection.append(self)

        self.collidable = collidable
        if self.collidable:
            self.collisions = set()

    def enable(self, delay=0):
        self._next_enabled = 1 + delay

    def disable(self, delay=0):
        self._next_enabled = 0 - delay

    def display(self, x=None, enable=None, disable=None):
        """
        Convience function for setting the x location and enabling or disabling in one
        command.
        """
        if x is not None:
            self.x = x

        # Default when neither enable nor disable are passed is to enable(0)
        if enable is None and disable is None:
            self.enable()
        elif enable is not None:
            self.enable(enable)
        else:
            self.disable(disable)

    def display_and_disable(self, *args, **kwargs):
        self.display(*args, disable=0, **kwargs)

    def reset_collisions(self):
        self.collisions = set()

    def delete(self):
        self.collection.remove(self)

class Sprite(Object):
    def __init__(self, num_bytes, width_multiplier, *args, sprite=None, color=0, reflect=False, **kwargs):
        super().__init__(*args)

        self.num_bytes = num_bytes
        self.num_bits = num_bytes * 8
        self._width_multiplier = width_multiplier
        self._internal_width = self.num_bits * self.width_multiplier
        self.color = color
        self.reflect = reflect

        if sprite is None:
            self.sprite = bytes([0] * self.num_bytes)
        else:
            self.sprite = sprite

    @property
    def width_multiplier(self):
        return self._width_multiplier

    @width_multiplier.setter
    def width_multiplier(self, value):
        sprite = self.sprite
        self._width_multiplier = value
        self._internal_width = self.num_bits * self._width_multiplier
        self.sprite = sprite

    @property
    def sprite(self):
        """
        TODO: Update with actual width
        This defines which parts of the playfield are turned on.
        It's given by the user as 24 bits wide and then converted to 96 bits internally
        This represents half of the width of the resolution.
        The other half is either duplicated or mirrored from this.
        """
        return [self._bits[i*self.width_multiplier] for i in range(self.num_bits)]

    @sprite.setter
    def sprite(self, value):
        """
        TODO: Update with actual width
        bits can either be given as 3 bytes, in which case the individual bits are used or
        it can be given as an iterable of length 24 in which each value is truthy
        (0/1 or True/False).
        """
        assert len(value) == self.num_bits or len(value) == self.num_bytes

        # If given the compressed version, convert to the full one
        if len(value) == self.num_bytes:
            bits = []
            for i in range(self.num_bytes):
                bits += [(value[i] >> bit) & 1 for bit in range(7, -1, -1)]
        else:
            bits = value

        # Store as a full representation where each bit is repeated bit_width times
        self._bits = []
        for bit in bits:
            self._bits += [bit]*self.width_multiplier

        # Also store a reverse representation to make it easier to display the mirrored mode
        self._reverse = self._bits[::-1]

    def spawn_moveable(self, width=1):
        return Missile(self, width)

    def display(self, *args, sprite=None, **kwargs):
        """
        Convience function adding sprite changing to Object.display
        """
        super().display(*args, **kwargs)

        if sprite is not None:
            self.sprite = sprite

class Playfield(Sprite):
    def __init__(self):
        super().__init__(constants.PLAYFIELD_SPRITE_WIDTH_BYTES, constants.PLAYFIELD_RESOLUTION)
        self.spawn_ball = self.spawn_moveable


display._playfield = Playfield()

class Moveable:
    def __init__(self, x=0):
        self.x = x

class Player(Sprite, Moveable):
    def __init__(self, sprite, *args, color=0, width_multiplier=1, x=0, **kwargs):
        #super(Sprite, self).__init__(1, width_multiplier, sprite=sprite, color=color)
        Sprite.__init__(self, 1, width_multiplier, display._players, *args, sprite=sprite, color=color, **kwargs)
        #super(Moveable, self).__init__(x)
        Moveable.__init__(self, x)

        self.reflect = False

        self.spawn_missile = self.spawn_moveable

class Text(Player):
    def __init__(self, character, upper=None, *args, **kwargs):
        self.set_character(character, upper)
        super().__init__(self._sprite_map[0], collidable=False, *args, **kwargs)

    def display(self, *args, i=None, **kwargs):
        """
        Convience function that displays the ith line of the letter.
        """
        if i < len(self._sprite_map):
            super().display(*args, sprite=self._sprite_map[i], **kwargs)
        else:
            super().display(*args, sprite=[0], **kwargs)

    def display0(self, *args, **kwargs):
        self.display(*args, i=0, **kwargs)

    def set_character(self, character, upper=None):
        character = str(character)
        if upper is None and character.isupper():
            upper = True
        if upper:
            self._sprite_map = uppercase[character.lower()]
        else:
            self._sprite_map = lowercase[character.lower()]


class Missile(Object, Moveable):
    def __init__(self, player, width, x=0):
        Object.__init__(self, display._missiles)
        Moveable.__init__(self, x)

        self.player = player
        self.width = width

Ball = partial(Missile, display._playfield)

class PYVCS:
    constants = constants
    wait_for_hsync = display.wait_for_hsync
    wait_for_vsync = display.wait_for_vsync

    Player = Player
    Ball = Ball
    playfield = display._playfield
    Text = Text

    audio = audio
    sdl2 = sdl2
    get_key_state = input.get_key_state

    @property
    def background(self):
        return display._background

    @background.setter
    def background(self, color):
        display._background = color

def display_step3():
    #print("yo")
    display._display_step()
    display._display_step()
    display._display_step()

def main():
    # Flush events
    for event in sdl2.ext.get_events():
        pass

    with audio_context:
        #dis.dis(open(sys.argv[1]).read())
        try:
            exec(open(sys.argv[1]).read(), {
                "USER_CODE": True,
                "pyvcs": PYVCS(),
                #"pyvcs":  Namespace(**globals()),
                #"pyvcs": PYVCS(),
                "__name__": ".".join(Path(sys.argv[1].replace(".py", "")).parts),
                "_pyvcs_display_step": display_step3
            })
            if (not sys.argv[0]=="pyvcs-python"):
                print("PyVCS - Created by docmarionum1 and kevidryon2\nUsage: <path-to-pyvcs-python>/python pyvcs.py <file>\nYou should use the pyvcs-python interpreter and not the default one to run PyVCS correctly.")
                SystemExit()
        except:
            print("PyVCS - Created by docmarionum1 and kevidryon2\nUsage: <path-to-pyvcs-python>/python pyvcs.py <file>")
            SystemExit()
        display._quit()

if __name__ == '__main__':
    main()
