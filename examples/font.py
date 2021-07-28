import string

pyvcs.set_background(255)

space_down = False

pages = [
    (string.ascii_lowercase, None),
    (string.ascii_uppercase, None),
    (string.digits + '.,:;\'"\\/!?$@-+=', None),
    (string.digits + '.,:;\'"\\/!?$@-+=', True),
]

page_num = 0
left_margin = 30
per_line = 5
spacing = 15

lines = []

def switch_page():
    for line in lines:
        for character in line:
            character.delete()

    current_page, uppercase = pages[page_num]
    new_lines = []
    for i in range(0, len(current_page), per_line):
        new_lines.append([
            pyvcs.Text(current_page[j], uppercase, x=left_margin + (j - i) * spacing)
            for j in range(i, min(i+per_line, len(current_page)))
        ])

    return new_lines

lines = switch_page()

while True:
    pyvcs.wait_for_vsync()
    for i in range(5):
        pyvcs.wait_for_hsync()

    for line in lines:
        i = 0

        for character in line:
            character.display(i=i)

        i += 1
        pyvcs.wait_for_hsync()
        pyvcs.wait_for_hsync()

        while i < 7:
            for character in line:
                character.display(i=i)

            i += 1
            pyvcs.wait_for_hsync()

        for character in line:
            character.display(i=i, disable=0)

        pyvcs.wait_for_hsync()
        pyvcs.wait_for_hsync()

    if pyvcs.get_key_state(pyvcs.sdl2.SDLK_ESCAPE):
        break

    if pyvcs.get_key_state(pyvcs.sdl2.SDLK_SPACE) and not space_down:
        page_num = (page_num + 1) % len(pages)
        lines = switch_page()
        space_down = True

    if not pyvcs.get_key_state(pyvcs.sdl2.SDLK_SPACE) and space_down:
        space_down = False
