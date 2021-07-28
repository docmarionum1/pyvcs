import copy

#canvas = [[0]*8]*8

_font = {
    'a': [
        [0, 1, 1, 0],
        [1, 0, 0, 1],
        [1, 1, 1, 1],
        [1, 0, 0, 1]
    ],
    'c': [
        [0, 1, 1, 1],
        [1, 0, 0, 0],
        [1, 0, 0, 0],
        [0, 1, 1, 1]
    ],
    'e': [
        [1, 1, 1, 1],
        [1, 1, 1, 0],
        [1, 0, 0, 0],
        [1, 1, 1, 1]
    ],
    'p': [
        [1, 1, 1, 0],
        [1, 0, 0, 1],
        [1, 1, 1, 0],
        [1, 0, 0, 0]
    ],
    'r': [
        [1, 1, 1, 0],
        [1, 0, 0, 1],
        [1, 1, 1, 0],
        [1, 0, 0, 1]
    ],
    's': [
        [0, 1, 1, 1],
        [1, 1, 0, 0],
        [0, 0, 1, 1],
        [1, 1, 1, 0]
    ],
    't': [
        [1, 1, 1, 0],
        [0, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 0, 0],
    ]
}

def pad_lower(letter):
    c = [[0]*8 for i in range(8)]
    for j in range(4):
        for i in range(4):
            c[j+4][i] = letter[j][i]

    return c

def make_upper(letter):
    c = [[0]*8 for i in range(8)]
    for j in range(4):
        for i in range(4):
            c[j*2][i*2] = letter[j][i]
            c[j*2 + 1][i*2] = letter[j][i]
            c[j*2][i*2 + 1] = letter[j][i]
            c[j*2 + 1][i*2 + 1] = letter[j][i]

    return c


#print(pad_lower(font["p"]))
#print(make_upper(font["p"]))

font = {k: pad_lower(v) for k,v in _font.items()}
font.update({k.upper(): make_upper(v) for k,v in _font.items()})
print(font)
