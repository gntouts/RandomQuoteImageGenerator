# RandomQuoteImageGenerator
An automated way to create random images with random automatically translated quotes on them.

## Installation
```
git clone https://github.com/gntouts/RandomQuoteImageGenerator.git
pip install -r requirements.txt
```

## Usage
```
usage: randomQuoteGenerator.py [-h] [-x, --height] [-y, --width]
                               [-q, --quality] [-p, --phrase] [-a, --author]
                               [-d, --destination] [-t, --translate]
                               [-c, --color] [-o, --opacity]

Random Quote Image Generator aka The easiest way to create random quotes'
images in seconds!

optional arguments:
  -h, --help          show this help message and exit
  -x, --height        Specify picture height in pixels.If only one dimension
                      is specified, the script will produce a square image.
  -y, --width         Specify picture width in pixels. If no dimension is
                      specified, the script will produce a 800x800px square
                      image.
  -q, --quality       Specify produced picture quality [0-100]. If quality is
                      not specified, the script will produce an image with
                      quality set to 70.
  -p, --phrase        Specify the phrase you want to add to the picture. If
                      phrase is not specidied, the script will download a
                      random quote.
  -a, --author        Specify the author of the phrase you want to add to the
                      picture. If authos is not specified, the script will use
                      the random quote's author or if you use a custom phrase,
                      no author will not be written on the image.
  -d, --destination   Specify the file name of the created photo
  -t, --translate     Specify the translation language. If not specified, the
                      script will not translate the phrase.
  -c, --color         Specify the RGB value (with commas) of solid color that
                      will be blended with the original image. Default color
                      is black.
  -o, --opacity       Specify the opacity of the color that will be blended
                      with the original image [0-1]. Default opacity is 0.2.
```
Have fun!




## Known Issues
+ If the random quote is too long, or the image too small it will not fit correclty. 
+ If you translate a lot of stuff, Google will ban your IP, which will raise a `JSONDecodeError`. Don't worry, just use a VPN, proxy or wait 20 minutes.
+ Automatic translation obviously produces funny results (if you think that sort of stuff funny).

## To be done
+ Create an SQLite DB with all the quotes for faster access and no need for spamming [Quotations Page's](http://www.quotationspage.com/) server.
+ Create a "responsive" way of determining font size and text wrapping to fit all quotes regardless of image size


## Services Used
The services used are [Lorem Picsum](https://picsum.photos/) which is powered by [Unsplash](https://unsplash.com/), [Google Translate](https://translate.google.com/) and [The Quotations Page](http://www.quotationspage.com/).

<hr>


This was created during the Covid19 Lockdown to have some fun. Cheers!
