# print(pyvcs.X)
# print(pyvcs.X)
# print(pyvcs.X)
#
# for i in range(10):
#     pyvcs.wait_for_hsync()
#     print(pyvcs.X, pyvcs.Y)
#a = 1
#b = 2
#pyvcs.set_background(a + b)
#c = 3
#pyvcs.playfield.color = a * b
#c
def f():
    pyvcs.playfield.color = 1
    #pyvcs.PLAYFIELD_COLOR = 1
    pyvcs.set_background(pyvcs.playfield.color + 2)
    a = "hi"
    print(a.zfill(pyvcs.playfield.color).upper())

f()

#print(pyvcs.PLAYFIELD_COLOR, pyvcs.playfield.color)
