from datetime import datetime
from flask import Blueprint, request, session, url_for, redirect, flash
from src.helper.common import twitter, kakao, map_auth_response_key
from src.models.model import User, db_session
import logging

logger = logging.getLogger()
logger.setLevel('DEBUG')

login = Blueprint(
    name='login',
    import_name=__name__
)

@login.route('/twitter-login', methods=['POST', 'GET'])
def twitter_login():
    url_for_res = url_for(
        '.oauth_authorized',
        next=request.args.get('next') or request.referrer or None
    )
    session['platform'] = 'twitter'
    return twitter.authorize(callback=url_for_res)

@login.route('/kakao-login')
def kakao_login():
    url_for_res = url_for(
        '.oauth_authorized',
        _external=True
    )
    session['platform'] = 'kakao'
    return kakao.authorize(callback=url_for_res)

@login.route('/oauth-authorized', methods=['GET'])
def oauth_authorized():
    if session['platform'] == 'twitter':
        resp = twitter.authorized_response()
    elif session['platform'] == 'kakao':
        resp = kakao.authorized_response()

    resp = map_auth_response_key(resp, session['platform'])
    next_url = request.args.get('next') or url_for('main.index')
    if resp is None:
        flash(u'로그인 권한 없음')
        return redirect(next_url)

    user = db_session.query(User).filter_by(user_id=resp['user_id']).first()
    if user is None:
        user = User(
            platform=session['platform'],
            screen_name=resp['screen_name'],
            user_id=resp['user_id']
        )
        db_session.add(user)
    else:
        user.screen_name = resp['screen_name']
        user.update_date = datetime.now()
        db_session.merge(user)

    db_session.commit()

    session['user_id'] = user.user_id
    session['oauth_token'] = resp['oauth_token']
    session['oauth_token_secret'] = resp['oauth_token_secret']

    logger.debug(f'authorized session: {session}')
    flash('로그인되었습니다.')

    return redirect(next_url)
