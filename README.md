# RandomQuoteImageGenerator
An automated way to create random images with random quotes on them.

## Installation
```
git clone https://github.com/gntouts/RandomQuoteImageGenerator.git
pip install -r requirements.txt
```

## Usage
```
python randomQuoteGenerator.py
```

## Known Issues
+ If the random quote is too long, it will not fit correclty. 
+ If you translate a lot of stuff, Google will ban your IP, which will raise a `JSONDecodeError`. Don't worry, just use a VPN, proxy or wait 20 minutes.
+ Some pages in the range of 1-12842 are empty, so expect some images with the quote 'Error: No quotation found'.
+ Automatic translation obviously produces funny results (if you think that sort of stuff funny).

## To be done
+ Spot 'Error: No quotation found' and reroll.
+ Create an SQLite DB with all the quotes for faster access and no need for spamming [Quotations Page's](http://www.quotationspage.com/) server.
+ Create a "responsive" way of determining font size etc to fit bigger quotes.


## Services Used
The services used are [Lorem Picsum](https://picsum.photos/) which is powered by [Unsplash](https://unsplash.com/), [Google Translate](https://translate.google.com/) and [The Quotations Page](http://www.quotationspage.com/).

<hr>


This was created during the Quarantine Lockdown to have some fun. Cheers!
