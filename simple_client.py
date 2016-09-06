import json
import ipdb
import requests
import gzip
import base64
from secrets import twitter_secrets

class SimpleTwitter:
    def __init__(self, config):
        self.config = config
        self.headers = self.init_headers()

    def get_user_timeline(self, username="cslinkyrun"):
        url = "https://api.twitter.com/1.1/statuses/user_timeline.json?count=100&screen_name=%s" % username
        response = requests.get(url, headers=self.headers)
        return response

    def encoded_token(self):
      key = self.config['key']
      secret = self.config['secret']
      bearer_token_credentials = key+":"+secret
      encoded = bearer_token_credentials.encode('ascii')
      base_encoded = base64.b64encode(encoded)
      return base_encoded

    def authorization_headers(self):
      token = self.encoded_token().decode('ascii')
      return {
        'Authorization':'Basic %s' % token,
        'Content-Type':'application/x-www-form-urlencoded;charset=UTF-8'
      }

    def get_bearer_token(self):
      url = "https://api.twitter.com/oauth2/token"
      res = requests.post(url, data={'grant_type':'client_credentials'}, headers=self.authorization_headers())
      bearer_token = json.loads(res.content.decode())['access_token']
      return bearer_token

    def init_headers(self):
      access_token = self.get_bearer_token()
      return {
        'User-Agent':'Connor S',
        'Authorization':'Bearer %s' % access_token,
        'Accept-Encoding':'gzip'
      }

t = SimpleTwitter(twitter_secrets)
ipdb.set_trace()
