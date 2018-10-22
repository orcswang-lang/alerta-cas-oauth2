
import requests
from flask import jsonify, request, current_app
from flask_cors import cross_origin

from alerta.auth.utils import create_token, get_customers, not_authorized
from alerta.exceptions import ApiError

from . import auth


@auth.route('/auth/cas', methods=['OPTIONS', 'POST'])
@cross_origin(supports_credentials=True)
def cas():
    access_token_url = current_app.config['CAS_URL'] +  '/cas/oauth2.0/accessToken'
    userinfo_url = current_app.config['CAS_URL'] + "/cas/oauth2.0/profile"

    # 获取accessToken（plain-text或者JSON，默认plain-text）
    payload = {
        'client_id': request.json['clientId'],
        'client_secret': current_app.config['OAUTH2_CLIENT_SECRET'],
        'redirect_uri': request.json['redirectUri'],
        'grant_type': 'authorization_code',
        'code': request.json['code'],
    }
    try:
        r = requests.post(access_token_url, data=payload)
    except Exception:
        return jsonify(status='error', message='Failed to call CAS API over HTTPS')
    token =r.text.split("&")[0].split("=")[1]

    # 返回用户相关属性(json格式,见 用户属性格式以及字段 ）
    r = requests.get(userinfo_url, params={'access_token':token})
    profile = r.json()

    if not_authorized('ALLOWED_CAS_GROUPS', profile.get('Groups')):
        raise ApiError('User %s is not authorized' % profile.get('Name'), 403)

    customers = get_customers(profile.get('Mail'), profile.get('Groups'))

    token = create_token(profile['id'], profile['Name'], profile.get('Mail'),
                         provider='cas', customers=customers,
                         groups=profile.get('Groups'), email=profile.get('Mail', None),
                         email_verified=True if 'Mail' in profile else False)
    return jsonify(token=token.tokenize)
