import os.path, re#, pygame
from sdl2.sdlimage import *
from boxmodel import LetterBox, Glue, Caret

def load(path):
    dirname = os.path.dirname(path)
    with open(path) as fd:
        fontspec = fd.read()

    info = re.search(r"^info .*size=([0-9]+).*padding=([0-9]+),([0-9]+),([0-9]+),([0-9]+)", fontspec, re.M)
    common = re.search(r"^common .*lineHeight=([0-9]+).*base=([0-9]+)", fontspec, re.M)
    page = re.search(r'^page .*file="([^"]*)"', fontspec, re.M)

    filename = page.group(1)

    image = IMG_Load(filename.encode('utf-8'))
    width = image.contents.w
    height = image.contents.h
    #image = pygame.image.load(page.group(1))
    #width, height = image.get_size()

    font = Font()
    font.image = image
    font.width = width
    font.height = height

    font.size, p0, p1, p2, p3 = map(int, info.groups())
    font.line_height, font.base = map(int, common.groups())
    font.padding = p0, p1, p2, p3

    characters = {}
    for data in re.findall(r"^char +(.*) +$", fontspec, re.M):
        options = dict()
        for subline in re.split(r" +", data):
            name, value = subline.split('=')
            options[name] = int(value)
        characters[options['id']] = options
        options['texcoords'] = (
            float(options['x']) / width,
            float(options['y'] + options['height']) / height,
            float(options['x'] + options['width']) / width,
            float(options['y']) / height)
        options['s0'] = float(options['x']) / width
        options['s1'] = float(options['x'] + options['width']) / width
        options['t0'] = float(options['y'] + options['height']) / height
        options['t1'] = float(options['y']) / height
    font.characters = characters
    kernings = {}
    for data in re.findall(r"^kerning +(.*) +$", fontspec, re.M):
        options = dict()
        for subline in re.split(r" +", data):
            name, value = subline.split('=')
            options[name] = int(value)
        kernings[(options['first'], options['second'])] = options['amount']
    font.kernings = kernings
    return font

class Font(object):
    def __call__(self, text, size=16, index=0):
        result = []
        kern = (0, 0)
        scale = float(size) / self.size
        padding = tuple(p*scale for p in self.padding)
        result.append(Caret(text, index))
        for ch in text:
            kern = kern[1], ord(ch)
            kern_amt = self.kernings.get(kern, 0)
            if kern[1] not in self.characters:
                for ch in '\\x' + format(kern[1], '02x'):
                    char = self.characters[ord(ch)]
                    b = (self.base - char['yoffset']) * scale
                    w = char['width'] * scale * 0.5
                    h = char['height'] * scale
                    x1 = char['xoffset'] * scale * 0.5
                    x2 = x1 + w
                    x3 = (char['xadvance']) * scale * 0.5
                    result.append(Glue(x1))
                    result.append(LetterBox(w, b, h-b, self, char['texcoords'], padding))
                    result.append(Glue(x3 - x2))
            else:
                char = self.characters[kern[1]]
                b = (self.base - char['yoffset']) * scale
                w = char['width'] * scale
                h = char['height'] * scale
                x1 = char['xoffset'] * scale
                x2 = x1 + w
                x3 = (char['xadvance'] + kern_amt) * scale
                result.append(Glue(x1))
                result.append(LetterBox(w, b, h-b, self, char['texcoords'], padding))
                result.append(Glue(x3 - x2))
            index += 1
            result.append(Caret(text, index))
        return result
