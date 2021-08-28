NUM_WAVEFORMS = 5

pyvcs.audio.volume = 1
pyvcs.audio.channel_1.volume = 1
pyvcs.audio.channel_1.waveform = 0
pyvcs.audio.channel_1.frequency = 16

pyvcs.background = 255

DEBOUNCE_FRAMES = 8
debounce = 0

wave_text = [
    pyvcs.Text("W", x = pyvcs.constants.WIDTH//2 - 16),
    pyvcs.Text("a", x = pyvcs.constants.WIDTH//2 - 6),
    pyvcs.Text("v", x = pyvcs.constants.WIDTH//2),
    pyvcs.Text("e", x = pyvcs.constants.WIDTH//2 + 6),
    pyvcs.Text(0, upper=True, x=pyvcs.constants.WIDTH//2 + 16)
]

freq_text = [
    pyvcs.Text("F", x = pyvcs.constants.WIDTH//2 - 16),
    pyvcs.Text("r", x = pyvcs.constants.WIDTH//2 - 6),
    pyvcs.Text("e", x = pyvcs.constants.WIDTH//2),
    #pyvcs.Text("q", x = pyvcs.constants.WIDTH//2 + 6),
    pyvcs.Text(1, upper=True, x=pyvcs.constants.WIDTH//2 + 16),
    pyvcs.Text(6, upper=True, x=pyvcs.constants.WIDTH//2 + 26)
]

while True:
    pyvcs.wait_for_vsync()

    for i in range(16):
        pyvcs.wait_for_hsync()

    for character in wave_text:
        character.enable(1)

    pyvcs.wait_for_hsync()

    for i in range(8):
        for character in wave_text:
            character.display(i=i, disable=7-i)
        pyvcs.wait_for_hsync()


    for i in range(8):
        pyvcs.wait_for_hsync()

    for character in freq_text:
       character.enable(1)

    pyvcs.wait_for_hsync()

    for i in range(8):
        for character in freq_text:
            character.display(i=i, disable=7-i)
        pyvcs.wait_for_hsync()

    pyvcs.wait_for_hsync()

    if pyvcs.get_key_state(pyvcs.sdl2.SDLK_ESCAPE):
        break
    if debounce < 0:
        if pyvcs.get_key_state(pyvcs.sdl2.SDLK_UP):
            debounce = DEBOUNCE_FRAMES
            pyvcs.audio.channel_1.waveform = (pyvcs.audio.channel_1.waveform + 1) % NUM_WAVEFORMS
        if pyvcs.get_key_state(pyvcs.sdl2.SDLK_DOWN):
            debounce = DEBOUNCE_FRAMES
            pyvcs.audio.channel_1.waveform = (pyvcs.audio.channel_1.waveform - 1) % NUM_WAVEFORMS
        if pyvcs.get_key_state(pyvcs.sdl2.SDLK_LEFT):
            debounce = DEBOUNCE_FRAMES
            pyvcs.audio.channel_1.frequency = max(pyvcs.audio.channel_1.frequency - 1, 1)
        if pyvcs.get_key_state(pyvcs.sdl2.SDLK_RIGHT):
            debounce = DEBOUNCE_FRAMES
            pyvcs.audio.channel_1.frequency = min(pyvcs.audio.channel_1.frequency + 1, 99)


    else:
        debounce -= 1

    wave_text[-1].set_character(str(pyvcs.audio.channel_1.waveform), upper=True)

    for index, character in enumerate(str(pyvcs.audio.channel_1.frequency).zfill(2)):
        freq_text[index + 3].set_character(character, upper=True)
