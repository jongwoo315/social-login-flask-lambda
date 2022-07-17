from flask import Blueprint, flash, render_template, session, g
from src.helper.common import twitter, kakao

main = Blueprint(
    name='main',
    import_name=__name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/main/static'
)

@main.route('/')
def index():
    tweets = None
    kakao_user_info = None

    if g.user is not None:
        resp = twitter.get('statuses/home_timeline.json')
        kakao_resp = kakao.get('user/me')

        if resp.status == 200 and session['platform'] == 'twitter':
            tweets = resp.data
        elif kakao_resp.status == 200 and session['platform'] == 'kakao':
            kakao_user_info = kakao_resp.data
        else:
            flash('소셜 플랫폼에서 데이터 로드가 불가능합니다.')

    return render_template('index.html', tweets=tweets, kakao_user_info=kakao_user_info)
