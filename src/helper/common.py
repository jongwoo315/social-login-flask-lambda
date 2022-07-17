import json
from flask_oauthlib.client import OAuth
import requests
from config import DevelopmentConfig
import logging

logger = logging.getLogger()
logger.setLevel('DEBUG')

def map_auth_response_key(resp, platform):
    user_info = {}
    
    if not platform:
        raise ValueError('incorrect platform parameter')
    elif platform == 'twitter':
        user_info = resp
    elif platform == 'kakao':
        with requests.Session() as session:
            session.headers.update({
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': f'Bearer {resp["access_token"]}'
            })
            response = session.post('https://kapi.kakao.com/v2/user/me')

        response_data = json.loads(response.content)
        user_info['user_id'] = response_data.get('id')
        user_info['screen_name'] = response_data.get('kakao_account').get('profile').get('nickname')
        user_info['oauth_token'] = resp['access_token']
        user_info['oauth_token_secret'] = ''

    return user_info


oauth = OAuth()
twitter = oauth.remote_app(
    'twitter',
    base_url='https://api.twitter.com/1.1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    authorize_url='https://api.twitter.com/oauth/authorize',
    access_token_url='https://api.twitter.com/oauth/access_token',
    consumer_key=DevelopmentConfig.TWITTER_CONSUMER_KEY,
    consumer_secret=DevelopmentConfig.TWITTER_CONSUMER_SECRET
)

kakao = oauth.remote_app(
    'kakao',
    base_url='https://kapi.kakao.com/v2/',
    authorize_url='https://kauth.kakao.com/oauth/authorize',
    access_token_url='https://kauth.kakao.com/oauth/token',
    consumer_key=DevelopmentConfig.KAKAO_CONSUMER_KEY,
    consumer_secret=DevelopmentConfig.KAKAO_CONSUMER_SECRET
)