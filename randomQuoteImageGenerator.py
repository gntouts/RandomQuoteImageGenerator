import sqlite3
import requests
import textwrap
import argparse
from os import remove
from time import sleep
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageFilter
from random import randint
from bs4 import BeautifulSoup
from googletrans import Translator

def getQuote(ID):
    '''Gets a random quote and returns a dict containing {'quote','author','information'}

    Caution: May return an Error: No quotation found as a quote due to some pages in website being empty
    '''
    url = "http://www.quotationspage.com/quote/num.html".replace(
        'num', str(ID))
    response = requests.get(url=url, verify=False)
    soup = BeautifulSoup(response.text, 'html.parser')
    quote = soup.find('dt').text
    info = soup.find('dd').find_all('i')
    author = soup.find('dd').find('b').text
    information = ''
    for i in range(len(info)):
        information += info[i].text+', '
    information = information[:-2]
    temp = {'quote': quote, 'author': author, 'info': information}
    return temp


def downloadImageBasedOnDimensions(ID, width, height):
    '''Downloads a random image and saves it as temp-ID.jpg'''
    url = 'https://picsum.photos/{}/{}'.format(str(width), str(height))
    fname = 'temp-'+str(ID)+'.jpg'
    r = requests.get(url, allow_redirects=True)
    open(fname, 'wb').write(r.content)
    return fname


def translate(phrase, languageCode):
    '''Returns the Google translation of a phrase you insert in the language you specify, eg: languageCode='el' for Greek'''
    translator = Translator()
    return translator.translate(phrase, dest=languageCode).text


def createImage(baseImagePath, quote, author, opacity, destination, color):
    # wrap text to fit in image
    wrapper = textwrap.TextWrapper(width=32)
    WordList = wrapper.wrap(text=quote)
    newQuote = ''
    for ii in WordList[:-1]:
        newQuote = newQuote + ii + '\n'
    newQuote += WordList[-1]

    # open downloaded image
    img = Image.open(baseImagePath)

    # apply gaussian blur
    img = img.filter(ImageFilter.GaussianBlur(radius=1.4))

    # create new black image to darken the base image
    W, H = img.size
    solidColorImage = Image.new("RGB", (W, H), (0, 0, 0))

    # blend images with alpha 0.2
    img = Image.blend(img, solidColorImage, opacity)

    # download the font of your choice and replace the font with the font file.
    font = ImageFont.truetype("NotoSerif-Bold.ttf", 35)

    # calculate text positioning
    draw = ImageDraw.Draw(img)
    w, h = draw.textsize(newQuote, font=font)
    x, y = 0.5*(W-w), 0.50*H-h

    # create black text outlines
    draw.text((x-1, y-1), newQuote, font=font, fill='black')
    draw.text((x+1, y-1), newQuote, font=font, fill='black')
    draw.text((x-1, y+1), newQuote, font=font, fill='black')
    draw.text((x+1, y+1), newQuote, font=font, fill='black')

    # draw quote
    draw.text((x, y), newQuote, 'white', font=font)

    # repeat process for author
    if author != '':
        author = '-'+author
        font = ImageFont.truetype("NotoSerif-Regular.ttf", 28)
        w, h = draw.textsize(author, font=font)
        x, y = 0.9*(W-w), 0.96*H-h

        draw.text((x-1, y), author, font=font, fill='black')
        draw.text((x+1, y), author, font=font, fill='black')
        draw.text((x, y-1), author, font=font, fill='black')
        draw.text((x, y+1), author, font=font, fill='black')
        draw.text((x, y), author, 'white', font=font)

    # save created image
    img.save(destination,  optimize=True, quality=71)


def main():
    parser = argparse.ArgumentParser(
        description='''Random Quote Image Generator aka The easiest way to create random quotes' images in seconds!''', epilog='Have fun!')
    parser.add_argument("-x, --height", type=int, metavar='',
                        help="Specify picture height in pixels.If only one dimension is specified, the script will produce a square image.")
    parser.add_argument("-y, --width", type=int, metavar='',
                        help="Specify picture width in pixels. If no dimension is specified, the script will produce a 800x800px square image.")
    parser.add_argument("-q, --quality", default=70, type=int, metavar='',
                        help="Specify produced picture quality [0-100]. If quality is not specified, the script will produce an image with quality set to 70.")
    parser.add_argument("-p, --phrase", type=str, metavar='',
                        help="Specify the phrase you want to add to the picture. If phrase is not specidied, the script will download a random quote.")
    parser.add_argument("-a, --author", default='', type=str, metavar='',
                        help='''Specify the author of the phrase you want to add to the picture. If authos is not specified, the script will use the
                        random quote's author or
                        if you use a custom phrase, no author will not be written on the image.''')
    parser.add_argument("-d, --destination", default='', type=str, metavar='',
                        help='''Specify the file name of the created photo''')
    parser.add_argument("-t, --translate", default='None', type=str, metavar='',
                        help='''Specify the translation language. If not specified, the script will not translate the phrase.''')
    parser.add_argument("-c, --color", default='00,00,00', type=str, metavar='',
                        help='''Specify the RGB value (with commas) of solid color that will be blended with the original image. Default color is black.''')
    parser.add_argument("-o, --opacity", default=0.2, type=str, metavar='',
                        help='''Specify the opacity of the color that will be blended with the original image [0-1]. Default opacity is 0.2.''')
    args = parser.parse_args()
    print('Random Quote Image Creator Initialized. Analysing arguments...')
    sleep(0.1)
    res = vars(args)
    rand = randint(1, 15000)

    # Quote Stuff
    print('Calculating phrase...')
    sleep(0.1)
    quote = res["p, __phrase"]
    author = res["a, __author"]

    if quote == None:
        print("Ok. Let's download a random phrase. Please be patient...")
        quote = getQuote(rand)
        while 'ERROR:' in quote['quote']:
            sleep(0.5)
            quote = getQuote(rand)
        quote = {'quote': quote['quote'], 'author': quote['author']}
    else:
        quote = {'quote': quote, 'author': author}
    phraseMessage = 'Phrase: ' + quote['quote']
    if author != '':
        phraseMessage += ' by Author: '+quote['author']
    print(phraseMessage)

    # Translation stuff
    tr = res['t, __translate']
    if tr != 'None':
        try:
            quote['quote'] = translate(quote['quote'], tr)
            print('Translated phrase: '+quote['quote'])
        except ValueError:
            print('Invalid destination language. Please use a correct language code.')
            exit(-1)
        except:
            print(
                'Hmmm... Seems like Google banned your IP. Try using a VPN or try again in 20 minutes.')
            exit(-1)

    # Image Dimension stuff
    height = res['x, __height']
    width = res['y, __width']
    quality = res['q, __quality']
    dest = res['d, __destination']
    opacity = res['o, __opacity']
    try:
        if float(opacity) > 1 or float(opacity) < 0:
            print('Invalid opacity value. Falling back to 0.2.')
            opacity = 0.2
    except:
        print('Invalid opacity value. Falling back to 0.2.')
        opacity = 0.2

    if dest.replace('/', '') != dest or dest[-4:] != '.jpg':
        if dest != '':
            print('Invalid destination value. Falling back to default file name.')
        dest = 'quote-'+str(rand)+'.jpg'

    color = res['c, __color']
    colorlist = color.split(',')
    if len(colorlist) < 3:
        print('Invalid color value. Falling back to black color.')
        color = '00,00,00'
    else:
        cflag = 0
        try:
            for each in colorlist:
                if int(each) < 0 or int(each) > 255:
                    cflag = 1
                    break
            if cflag == 1:
                print('Invalid color value. Falling back to black color.')
                color = '00,00,00'
        except:
            print('Invalid color value. Falling back to black color.')
            color = '00,00,00'
    try:
        if quality < 0 or quality > 100:
            print('Invalid quality value. Falling back to black color.')
            quality = 71
    except:
        print('Invalid quality value. Falling back to black color.')
        quality = 71

    if height == None and width == None:
        height = 800
        width = 800
    elif height == None and width != None:
        height = width
    elif height != None and width == None:
        width = height

    try:
        if width <= 0 or height <= 0:
            print('Invalid dimensions detected. Falling back to 800x800px.')
            height = 800
            width = 800
        width = int(width)
        height = int(height)
    except:
        print('Invalid dimensions detected. Falling back to 800x800px.')
        height = 800
        width = 800

    print('Donwloading image with dimensions: ' +
          str(width)+'x'+str(height)+'px. Please be patient...')
    tempImage = downloadImageBasedOnDimensions(rand, width, height)
    print('Downloaded image: ', tempImage)
    print('Creating your text image. Please be patient...')

    rgb = (int(color.split(',')[0]), int(
        color.split(',')[1]), int(color.split(',')[2]))
    createImage(baseImagePath=tempImage, quote=quote['quote'],
                author=quote['author'], opacity=opacity, destination=dest, color=rgb)

    remove(tempImage)
    print('Done. Goodbye!')


if __name__ == "__main__":
    main()
