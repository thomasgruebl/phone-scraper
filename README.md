# phone-scraper
Anonymously scrapes onlinesim.ru for new usable phone numbers.

![GitHub last commit](https://img.shields.io/github/last-commit/thomasgruebl/phone-scraper?style=plastic) ![GitHub](https://img.shields.io/github/license/thomasgruebl/phone-scraper?style=plastic) <a style="text-decoration: none" href="https://github.com/thomasgruebl/phone-scraper/stargazers">
<img src="https://img.shields.io/github/stars/thomasgruebl/phone-scraper.svg?style=plastic" alt="Stars">
</a>
<a style="text-decoration: none" href="https://github.com/thomasgruebl/phone-scraper/fork">
<img src="https://img.shields.io/github/forks/thomasgruebl/phone-scraper.svg?style=plastic" alt="Forks">
</a>
<a style="text-decoration: none" href="https://github.com/thomasgruebl/phone-scraper/issues">
<img src="https://img.shields.io/github/issues/thomasgruebl/phone-scraper.svg?style=plastic" alt="Issues">
</a>


**Usage**
---

### Clone the repository
```bash
$ git clone https://github.com/thomasgruebl/phone-scraper.git
```

### Install requirements
```bash
$ pip3 install -r requirements.txt
```

### Run
```bash
$  python3 scraper.py [OPTIONS]

Options:
  [1]	-e | --email	Add your email address to receive a notification when a brand new phone number is available.
  [2]	-m | --maxage	Pull only phone numbers that are younger than the specified maximum age value in minutes.
  [3]	-r | --repeat	Specify the repeat interval in minutes for fetching phone numbers.
  [4]	-h | --help	Shows brief help.
```

### Run in the background

#### Windows
```powershell
pythonw3.exe scraper.py [OPTIONS]
```

#### Linux
```bash
$ chmod +x scraper.py
$ nohup python3 scraper.py [OPTIONS] &
```


**Description**
---

This repo uses the torpy (pure python Tor client implementation) in order to anonymously scrape phone numbers from onlinesim.ru. The numbers are automatically filtered by recency and can be used for SMS verification purposes. Since it often is quite unclear which phone numbers have been added recently and thus might still be usable, this program scrapes the website in a given time interval (repeat argument) and outputs all new phone numbers (maxage argument). You can optionally set the email flag to receive a notification when new phone numbers have been added.

Note: Since the getFreeMessageList API call is currently unavailble, you still need to look up the SMS verification codes manually on onlinesim.ru. To continue to maintain your anonymity, don't forget to use TOR.

