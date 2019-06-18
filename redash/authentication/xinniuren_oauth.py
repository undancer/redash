import logging
import requests
from flask import redirect, url_for, Blueprint, flash, request, session
from flask_oauthlib.client import OAuth

from redash import models, settings
from redash.authentication import create_and_login_user, logout_and_redirect_to_index, get_next_path
from redash.authentication.org_resolving import current_org

logger = logging.getLogger('xinniuren_oauth')

oauth = OAuth()
blueprint = Blueprint('xinniuren_oauth', __name__)


def xinniuren_remote_app():
    if 'xinniuren' not in oauth.remote_apps:
        oauth.remote_app('xinniuren',
                         base_url='http://x6pro.xinniuren.cn/api/OAuth/',
                         authorize_url='http://x6pro.xinniuren.cn/api/OAuth/authorize',
                         request_token_url=None,
                         request_token_params={
                             'scope': 'base',
                         },
                         access_token_url='http://x6pro.xinniuren.cn/api/OAuth/access_token',
                         access_token_method='POST',
                         consumer_key=settings.XINNIUREN_CLIENT_ID,
                         consumer_secret=settings.XINNIUREN_CLIENT_SECRET)

    return oauth.xinniuren


def get_user_profile(access_token):
    headers = {'Authorization': 'OAuth {}'.format(access_token)}
    # response = requests.get('http://x6pro.xinniuren.cn/api/OAuth/userinfo', headers=headers)
    response = requests.get('http://x6pro.xinniuren.cn/api/OAuth/userinfo', params={
        'access_token': access_token
    })

    if response.status_code == 401:
        logger.warning("Failed getting user profile (response code 401).")
        return None

    return response.json()


def verify_profile(org, profile):
    # if org.is_public:
    #     return True
    #
    # email = profile['Email']
    # domain = email.split('@')[-1]

    # if domain in org.google_apps_domains:
    #     return True
    #
    # if org.has_user(email) == 1:
    #     return True

    # return False
    return True


@blueprint.route('/<org_slug>/oauth/xinniuren', endpoint="authorize_org")
def org_login(org_slug):
    session['org_slug'] = current_org.slug
    return redirect(url_for(".authorize", next=request.args.get('next', None)))


@blueprint.route('/oauth/xinniuren', endpoint="authorize")
def login():
    callback = url_for('.callback', _external=True)
    next_path = request.args.get('next', url_for("redash.index", org_slug=session.get('org_slug')))
    logger.debug("Callback url: %s", callback)
    logger.debug("Next is: %s", next_path)
    return xinniuren_remote_app().authorize(callback=callback, state=next_path)


@blueprint.route('/oauth/xinniuren_callback', endpoint="callback")
def authorized():
    app = xinniuren_remote_app()
    resp = app.authorized_response()
    access_token = resp['access_token']

    if access_token is None:
        logger.warning("Access token missing in call back request.")
        flash("Validation error. Please retry.")
        return redirect(url_for('redash.login'))

    profile = get_user_profile(access_token)
    if profile is None:
        flash("Validation error. Please retry.")
        return redirect(url_for('redash.login'))

    if 'org_slug' in session:
        org = models.Organization.get_by_slug(session.pop('org_slug'))
    else:
        org = current_org

    if not verify_profile(org, profile):
        logger.warning("User tried to login with unauthorized domain name: %s (org: %s)", profile['Email'], org)
        flash("Your Google Apps account ({}) isn't allowed.".format(profile['Email']))
        return redirect(url_for('redash.login', org_slug=org.slug))

    # picture_url = "%s?sz=40" % profile['picture']
    picture_url = "/static/images/avatar.svg"
    user = create_and_login_user(org, profile['UserName'], profile['Email'], picture_url)
    if user is None:
        return logout_and_redirect_to_index()

    unsafe_next_path = request.args.get('state') or url_for("redash.index", org_slug=org.slug)
    next_path = get_next_path(unsafe_next_path)

    return redirect(next_path)
