def f(q):
    return q ** 3

a = 1
b = 2
c = a + b
d = f(c)

print(a, b, c, d)
WIDTH = 10
pyvcs.set_background(255)
ball = pyvcs.Ball(4)
ball.x = WIDTH - 12

pyvcs.playfield.sprite = [255, 255]
pyvcs.playfield.reflect = False
pyvcs.playfield.enable()
#pyvcs.audio.channel_1.waveform = 7

#print(code)
#print(globals())
