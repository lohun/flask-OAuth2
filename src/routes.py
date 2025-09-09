from flask import Blueprint, request, render_template, flash, session, redirect, url_for
from .flasklogin import login_manager
from flask_login import login_required
from .models import Client, Grant, Token, User
from src.db import db
from .utility import oauth
from functools import wraps
from datetime import datetime, timedelta
import google.oauth2.credentials
import google_auth_oauthlib.flow


routes = Blueprint('routes', __name__)

flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file('client_secret.json',
    scopes=['https://www.googleapis.com/auth/drive.metadata.readonly',
            'https://www.googleapis.com/auth/calendar.readonly'])

flow.redirect_uri = 'http://127.0.0.1:5000/oauth/authorize'

authorization_url, state = flow.authorization_url(
    access_type='offline',
    include_granted_scopes='true',
    login_hint='hint@example.com',
    prompt='consent'
)
print(flow)




def get_current_user():
    user = Client.query.filter(Client.client_id == request.client.client_id).first()
    print(user)
    pass


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



@oauth.clientgetter
def load_client(client_id):
    return Client.query.filter_by(client_id=client_id).first()



@oauth.grantgetter
def load_grant(client_id, code):
    return Grant.query.filter_by(client_id=client_id, code=code).first()


@oauth.grantsetter
def save_grant(client_id, code, request, *args, **kwargs):
    expires = datetime.now() + timedelta(minutes=10)
    grant = Grant(
        client_id=client_id,
        code=code['code'],
        redirect_uri=request.redirect_uri,
        _scopes=' '.join(request.scopes),
        user=get_current_user,
        expires=expires
    )
    db.session.add(grant)
    db.session.commit()
    print(Grant)

    return grant


@oauth.tokengetter
def load_token(access_token=None, refresh_token=None):
    if access_token:
        return Token.query.filter_by(access_token=access_token).first()
    elif refresh_token:
        return Token.query.filter_by(refresh_token=refresh_token).first()


@oauth.tokensetter
def save_token(token, request, *args, **kwargs):
    toks = Token.query.filter_by(client_id=request.client.client_id, user_id=request.user.id).first()

    for t in toks:
        db.session.delete(t)
        print("toks", toks)

    expires_in = token.get('expires_in')
    expires = datetime.now() + timedelta(seconds=expires_in)

    tok = Token(
        access_token=token['access_token'],
        refresh_token=token['refresh_token'],
        token_type=token['token_type'],
        _scopes=token['scope'],
        expires=expires,
        client_id=request.client.client_id,
        user_id=request.user.id
    )
    db.session.add(tok)
    db.session.commit()
    print("tok", tok)
    return tok


@routes.route('/')
def oauthorize_login():
    return render_template('home.html')


@routes.route('/oauth/authorize', methods=['GET', 'POST'])
@login_required
@oauth.authorize_handler
def authorize(*args, **kwargs):
    if request.method == 'GET':
        client_id = kwargs.get('client_id')
        client = Client.query.filter_by(client_id=client_id).first()
        kwargs['client'] = client
        return render_template('home.html', **kwargs)
    
    confirm = request.form.get('confirm', 'no')
    return confirm == 'yes'


@routes.route('/google_auth')
def google_auth():
    print(authorization_url)
    return redirect(authorization_url)


@routes.route('/oauth/token')
@oauth.token_handler
def access_token():
    return {'version': '0.1.0'}


@routes.route('/oauth/revoke', methods=['POST'])
@oauth.revoke_handler
def revoke_token(): pass
