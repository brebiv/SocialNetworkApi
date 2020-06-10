# Social Network API

API for twitter like social network.

## Installation

```bash
pip install -r requirements.txt
git clone https://github.com/brebiv/SocialNetworkApi
cd SocialNetworkApi
python manage.py makemigrations && python manage.py migrate
python manage.py runserver
```

Go ahead, it's on http://localhost:8000

You can delete db.sqlite3, if you don't need examples or demo.

## Usage
You can send requests data as json or as form data. I'll use form.
1. Register: \
curl --location --request POST 'http://localhost:8000/api/register/' \
--form 'username=Bill' \
--form 'password=321' \
--form 'email=bill@genius.com'
2. Obtain token: \
curl --location --request POST 'http://localhost:8000/api/token/' \
--form 'username=Bill' \
--form 'password=321'
3. With that token you can make request to any url you see in api/urls.py, just set request header like: Authorization: Bearer {your access token here}.

If you want to know what fields are avaliable for urls, check api/serializers.py.

### Admin panel
Visit http://localhost:8000/admin to open admin panel. (user:root, password:1089)

