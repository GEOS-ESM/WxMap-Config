from PIL import Image

im = Image.open('bccmass_cbar.png')
rgb_im = im.convert('RGB')

j = int(round(im.height / 2.0))

for i in range(0, im.width, 3):
    r, g, b = rgb_im.getpixel((i, j))
    print '        -', r, g, b
