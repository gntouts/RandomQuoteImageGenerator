import sqlite3
import requests
import textwrap
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageFilter
from random import randint
from bs4 import BeautifulSoup
from googletrans import Translator

'''If the random quote is too long, it will not fit correclty. If you translate a lot of stuff, Google will ban your IP,
which will raise a JSONDecodeError. Don't worry, just use a VPN, proxy or wait 20 minutes.
Some pages in the range of 1-12842 are empty, so expect some 'Error: No quotation found'.
Automatic translation obviously produces funny results (if you think that sort of stuff funny).
The services used are https://picsum.photos/, https://unsplash.com/, Google Translate and http://www.quotationspage.com/.
This was created during the Quarantine Lockdown to have some fun. Cheers!'''


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


def downloadImage(ID):
    '''Downloads a random image and saves it as ID.jpg'''
    url = 'https://picsum.photos/800/800'
    fname = str(ID)+'.jpg'
    r = requests.get(url, allow_redirects=True)
    open(fname, 'wb').write(r.content)


def translate(phrase, languageCode):
    '''Returns the Google translation of a phrase you insert in the language you specify, eg: languageCode='el' for Greek'''
    translator = Translator()
    return translator.translate(phrase, dest=languageCode).text


def createImage(baseImagePath, quote, author):
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
    black = Image.new("RGB", (800, 800), (0, 0, 0))

    # blend images with alpha 0.2
    img = Image.blend(img, black, 0.2)

    # download the font of your choice and replace the font with the font file.
    font = ImageFont.truetype("NotoSerif-Bold.ttf", 35)

    # calculate text positioning
    draw = ImageDraw.Draw(img)
    w, h = draw.textsize(newQuote, font=font)
    W, H = img.size
    x, y = 0.5*(W-w), 0.50*H-h

    # create black text outlines
    draw.text((x-1, y-1), newQuote, font=font, fill='black')
    draw.text((x+1, y-1), newQuote, font=font, fill='black')
    draw.text((x-1, y+1), newQuote, font=font, fill='black')
    draw.text((x+1, y+1), newQuote, font=font, fill='black')

    # draw quote
    draw.text((x, y), newQuote, 'white', font=font)

    # repeat process for author
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
    img.save("quote-"+baseImagePath, optimize=True, quality=81)


def main():
    ID = randint(1, 12842)
    quoteInfo = getQuote(ID)
    downloadImage(ID)
    # skip this step if you just want the english quote
    translatedQuote = translate(quoteInfo['quote'], 'el')
    createImage(str(ID)+'.jpg', translatedQuote, quoteInfo['author'])


if __name__ == "__main__":
    main()
