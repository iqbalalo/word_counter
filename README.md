# Word Counter

Objective is to count specified word in a given URL page. It is considered that no nested link will be checked but only the given URL page.

It is also assumed that word is case sensitive and only given word will be considered. For an example `fit` will be counted but not `Fitting` or `Fit`.

For this project `django` framework has been chosen.

## Installation procedure below

### Prerequisite:
- Mac or Linux
- Python >= 3.7

### Clone repository

```
git clone https://github.com/iqbalalo/word_counter.git
cd word_counter
```
### Active virtual environment and Install packages
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
### DB Migration
```
cd src
python manage.py makemigrations
python manage.py migrate
```

### Run local server

```
python manage.py runserver
```

## REST API

### Request (With all correct input params)
```
POST /wordcount/
```

```
curl -i -H 'Accept: application/json' http://localhost:8000/wordcount/ -d '{"word":"fit","url":"https://www.virtusize.jp/"}'
```


### Response:
```
HTTP/1.1 200 OK
Date: Mon, 20 Dec 2021 08:50:40 GMT
Content-Type: application/json
Content-Length: 29

{"status": "ok", "count": 13}
```

### Request (Missing param or param value)
```
POST /wordcount/
```

```
curl -i -H 'Accept: application/json' http://localhost:8000/wordcount/ -d '{"word":"fit","url":""}'
```


### Response:
```
HTTP/1.1 400 Bad Request
Date: Mon, 20 Dec 2021 08:53:26 GMT
Server: WSGIServer/0.2 CPython/3.8.10
Content-Type: application/json
X-Frame-Options: DENY
Content-Length: 44
X-Content-Type-Options: nosniff
Referrer-Policy: same-origin
Cross-Origin-Opener-Policy: same-origin

{"status": "error", "msg": "Invalid Params"}

```

## Unit Test
```
python manage.py test
```

## Author Comment
1. Django framework has been chosen to build quick prototype.
2. To scrap the URL a popular library `BeautifulSoup` has been selected.
3. There are multiple ways to extract the word from scrapped data. It may require manual extraction process. However a popular library `NLTK` has been chosen which can tokenize accurately.