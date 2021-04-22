from argparse import Namespace
import array
import ctypes
from pathlib import Path
import sys
import time

import numpy as np
import sdl2
import sdl2.ext

RESOLUTION = (192, 108)
FRAME = [0] * (RESOLUTION[0] * RESOLUTION[1] * 1)
FRAME = array.array('B', FRAME)
HBLANK = 63
VBLANK = 63

MV = memoryview(FRAME).cast("B")
FRAME_PTR = ctypes.c_void_p(FRAME.buffer_info()[0])


sdl2.ext.init()
window = sdl2.ext.Window("window", size=RESOLUTION, flags=sdl2.SDL_WINDOW_FULLSCREEN_DESKTOP)

#window.maximize()
#sdl2.SDL_SetWindowFullscreen(window.window, sdl2.SDL_WINDOW_FULLSCREEN_DESKTOP)
renderer = sdl2.ext.Renderer(window, logical_size=RESOLUTION, flags=sdl2.SDL_RENDERER_ACCELERATED)
#window.show()

#window_surface = sdl2.SDL_GetWindowSurface(window.window)
#window_array = sdl2.ext.pixels3d(window_surface.contents, False)
#surface = sdl2.SDL_CreateRGBSurface(0, RESOLUTION[0], RESOLUTION[1], 8, 0, 0, 0, 0)
surface = sdl2.SDL_CreateRGBSurfaceWithFormat(0, *RESOLUTION, 8, sdl2.SDL_PIXELFORMAT_RGB332)

#surface_array = sdl2.ext.pixels3d(surface.contents, False)
#texture = sdl2.SDL_CreateTexture(renderer.renderer, sdl2.SDL_PIXELFORMAT_RGB332, sdl2.SDL_TEXTUREACCESS_STREAMING, *RESOLUTION)
#texture = sdl2.SDL_CreateTextureFromSurface(renderer.renderer, surface)
texture = sdl2.SDL_CreateTexture(renderer.renderer, sdl2.SDL_PIXELFORMAT_RGB332, sdl2.SDL_TEXTUREACCESS_STREAMING, *RESOLUTION)

#print(dir(texture))
window.show()
#texture_array =
#print(dir(surface.contents))

class SetTrace(object):
    def __init__(self, func):
        self.func = func

    def __enter__(self):
        sys.settrace(self.func)
        return self

    def __exit__(self, ext_type, exc_value, traceback):
        sys.settrace(None)

BACKGROUND_COLOR = 0

def set_background(color):
    global BACKGROUND_COLOR
    HELL_YEAH = True
    BACKGROUND_COLOR = color

PLAYFIELD_COLOR = 0
BALLS = []
X = -HBLANK
Y = -VBLANK

def set_playfield(color):
    global PLAYFIELD_COLOR
    PLAYFIELD_COLOR = color

def write_color_to_frame(color):
    i = Y*RESOLUTION[0] + X
    FRAME[i] = color

class Ball:
    def __init__(self, width):#, color=None):
        self.width = width
        self.enabled = False
        self.x = 0
        BALLS.append(self)

    def enable(self, x=None):
        if x is None:
            self.x = max(X, 0)
        else:
            self.x = x
        self.enabled = True

    def disable(self):
        self.enabled = False

HSYNC = False
WAIT_FOR_HSYNC = False

VSYNC = False
WAIT_FOR_VSYNC = False

def wait_for_hsync():
    USER_CODE = True
    global HSYNC, WAIT_FOR_HSYNC
    WAIT_FOR_HSYNC = True
    HSYNC = False
    while not HSYNC:
        continue
    WAIT_FOR_HSYNC = False

def wait_for_vsync():
    USER_CODE = True
    global VSYNC, WAIT_FOR_VSYNC
    WAIT_FOR_VSYNC = True
    VSYNC = False
    while not VSYNC:
        continue
    WAIT_FOR_VSYNC = False

#KEY = 0
KEYS = {
    sdl2.SDLK_UP: False,
    sdl2.SDLK_DOWN: False,
    sdl2.SDLK_LEFT: False,
    sdl2.SDLK_RIGHT: False,
    sdl2.SDLK_ESCAPE: False
}

#def get_keycode():
#    return KEY

def get_key_state(keycode):
    return KEYS[keycode]

START = time.time()

def display_step():
    global X, Y, START, HSYNC, VSYNC

    if X < 0:
        X += 1
        return

    if Y < 0:
        X += 1
        if X == RESOLUTION[0]:
            HSYNC = True
            X = -HBLANK
            Y += 1
        return

    wrote_pixel = False
    for ball in BALLS:
        #print(X, ball.x)
        if ball.enabled and (X >= ball.x) and (X < (ball.x + ball.width)):
            #print("hi")
            #print(Y)
            write_color_to_frame(PLAYFIELD_COLOR)
            wrote_pixel = True
            break

    if not wrote_pixel:
        write_color_to_frame(BACKGROUND_COLOR)

    X += 1
    if X == RESOLUTION[0]:
        HSYNC = True
        X = -HBLANK
        Y += 1
        if Y == RESOLUTION[1]:
            Y = -VBLANK

            # frame = np.array(FRAME, dtype=np.uint8).reshape(
            #     (RESOLUTION[1], RESOLUTION[0], 1)
            # )
            # add alpha
            #frame = np.insert(frame, 3, 255, axis=2)
            #frame = np.transpose(frame, [1, 0, 2])
            #cv2.imshow("window", frame)
            #KEY = cv2.waitKeyEx(1)
            #print(KEY)

            #np.copyto(surface_array, frame)
            #texture = sdl2.SDL_CreateTextureFromSurface(renderer.renderer, surface)
            #np.copyto()
            sdl2.SDL_UpdateTexture(
                texture.contents, None,
                #ctypes.cast(FRAME, ctypes.POINTER(ctypes.c_ubyte)),
                #ctypes.pointer(FRAME),
                #surface.contents.pixels,
                #renderer.renderer._screenbuffer_ptr,
                FRAME_PTR,
                RESOLUTION[0]
            )
            renderer.copy(texture.contents)
            renderer.present()
            renderer.clear()
            window.refresh()

            for event in sdl2.ext.get_events():
                if event.type == sdl2.SDL_KEYDOWN:
                    KEYS[event.key.keysym.sym] = True
                    #print(KEY)
                    #break
                elif event.type == sdl2.SDL_KEYUP:
                    KEYS[event.key.keysym.sym] = False
                    #break
                #print(event)

            sys.stdout.write('\r')
            sys.stdout.write("%.2f" % (1 / (time.time() - START)))#, str(KEY).zfill(8)))
            sys.stdout.flush()
            START = time.time()
            VSYNC = True
            #HSYNC = True
            #print("HYS  ", HSYNC)

def monitor(frame, event, arg):
    #global HYSNC, WAIT_FOR_HSYNC
    if "USER_CODE" not in frame.f_globals and "USER_CODE" not in frame.f_locals:# and (not frame.f_back or "USER_CODE" not in frame.f_back.f_globals):
    #if "USER_CODE" not in frame.f_globals:
        frame.f_trace_opcodes = False
        return monitor

    frame.f_trace_opcodes = True



    if "HELL_YEAH" in frame.f_locals:
        print("HELL NO")
        1/0

    if (HSYNC and WAIT_FOR_HSYNC) or (VSYNC and WAIT_FOR_VSYNC):
       return monitor

    if event == "opcode":
        # Do three system steps and then return
        for i in range(3):
            #if (HSYNC and WAIT_FOR_HSYNC) or (VSYNC and WAIT_FOR_VSYNC):
            #    return monitor
            display_step()
        #display_step()
        #display_step()
        #display_step()

    return monitor

def main():
    with SetTrace(monitor):
        exec(open(sys.argv[1]).read(), {
            "USER_CODE": True, "pyvcs":  Namespace(**globals()),
            "__name__": ".".join(Path(sys.argv[1].replace(".py", "")).parts)
        })

if __name__ == '__main__':
    main()
