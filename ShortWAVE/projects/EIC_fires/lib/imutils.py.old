from PIL import Image, ImageDraw, ImageFont

def im_paste_file(bg, fname, xpos, ypos, xsize=None, ysize=None):

    img     = Image.open(fname)
    
    if xsize:
        ratio   = float(img.size[1]) / float(img.size[0])
        ysize   = int(xsize * ratio)
    
    elif ysize:
        ratio   = float(img.size[0]) / float(img.size[1])
        xsize   = int(ysize * ratio)
    
    if xsize and ysize:
        img = img.resize((xsize, ysize), Image.LANCZOS)

    xsize = img.size[0]
    ysize = img.size[1]
    
    bg.paste(img, (xpos, ypos), img)
    
    img.close()

    return (xsize, ysize)

class HersheyDraw(object):
    """
    Defines methods for drawing formatted text on an image.

    The methods in this class use the PIL library to draw text
    on an image. The text may contain format control characters
    as defined by the GrADS Hershey font for super- and sub-scripting.

    Requirements
    ------------
    from PIL import ImageDraw, ImageFont
    """

    def __init__(self, im, font, size, color, **kwargs):
        """
        Initializer

        Parameters
        ----------
        im : Image
            PIL image object.
        font : string
            Name of font file (Truetype etc.).
        size : integer
            Font size (pixels). Super and sub-scripting font size
            is set to size/2.
        color : tuple
            RGB(A) value for font color (R, G, B, A)

        Returns
        -------
        None
            No return value

        """

        self.color = color
        self.d     = ImageDraw.Draw(im)
        self.fn    = ImageFont.truetype(font, size)
        self.fs    = ImageFont.truetype(font, int(size/2))
        self.hn    = self.d.textbbox((0,0), '1', font=self.fn)[3]
        self.hs    = self.d.textbbox((0,0), '1', font=self.fs)[3]

    def text_size(self, text):
        """
        Returns the size of the text string in pixels.

        This method returns the size of the string in pixels after
        resolving the Hershey font control characters.

        Parameters
        ----------
        text : string
            Text string with or without Hershey control characters. Only
            superscripting (`a), subscripting (`b) and normal (`n) formatting
            sequences are recognized.

        Returns
        -------
        size : tuple
            width and height of the text string (w, h) where "h" is the
            maximum height of the string.

        """

        if not text: return (0, 0)

        words = text.split('`')
        if words[0]: words[0] = 'n' + words[0]

        nText, sText = ('', '')

        for s in words:

            if not s: continue
            if len(s) == 1: continue

            if s[0] == 'n':
                nText += s[1:]
            else:
                sText += s[1:]

        wn, hn, ws, hs = (0, 0, 0, 0)
        if nText: wn, hn = self.d.textbbox((0,0), nText, font=self.fn)[2:4]
        if sText: ws, hs = self.d.textbbox((0,0), sText, font=self.fs)[2:4]

        return (wn + ws, max(hn,hs))

    def draw_text(self, x, y, text):
        """
        Draws text on an image.

        This method uses the PIL library to draw text on the image.
        The text may contain format control characters as defined by
        the GrADS Hershey font for super- and sub-scripting.

        Parameters
        ----------
        x : integer
            Left pixel location of string.

        y : integer
            Top pixel location of string.

        text : string
            Text string with or without Hershey control characters. Only
            superscripting (`a), subscripting (`b) and normal (`n) formatting
            sequences are recognized.

        Returns
        -------
        None
            No return value

        """

        if not text: return

        words = text.split('`')
        if words[0]: words[0] = 'n' + words[0]
 
        for s in words:

            if not s: continue
            if len(s) == 1: continue

            if s[0] == 'n':
                self.d.text( (x, y), s[1:], font=self.fn, fill=self.color)
                w, h = self.d.textbbox((0,0), s[1:], font=self.fn)[2:4]
                x += w
            elif s[0] == 'a':
                self.d.text( (x, y), s[1:], font=self.fs,
                                                      fill=self.color)
                w, h = self.d.textbbox((0,0), s[1:], font=self.fs)[2:4]
                x += w
            elif s[0] == 'b':
                self.d.text( (x, y+self.hn-self.hs), s[1:], font=self.fs,
                                                      fill=self.color)
                w, h = self.d.textbbox((0,0), s[1:], font=self.fs)[2:4]
                x += w
