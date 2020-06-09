### Modified version of https://github.com/sarumont/py-trello/blob/master/trello/util.py

import os
import urllib.parse as urlparse
import codecs
import json

import oauth2 as oauth

CON_FILE = '.trello-vim'
configs = {'key': None, 'token': None, 'url': False, 'label':False, 'done_cards': False}

def create_oauth_token():
    """
    Script to obtain an OAuth token from Trello.

    More info on token scope here:
        https://trello.com/docs/gettingstarted/#getting-a-token-from-a-user
    """
    request_token_url = 'https://trello.com/1/OAuthGetRequestToken'
    authorize_url = 'https://trello.com/1/OAuthAuthorizeToken'
    access_token_url = 'https://trello.com/1/OAuthGetAccessToken'


    print("Visit https://trello.com/1/appKey/generate to obtain API keys")
    expiration = 'never'
    scope = 'read'
    trello_key = str(input('API KEY >'))
    trello_secret = str(input('API SECRET >'))

    consumer = oauth.Consumer(trello_key, trello_secret)
    client = oauth.Client(consumer)

    # Step 1: Get a request token. This is a temporary token that is used for
    # having the user authorize an access token and to sign the request to obtain
    # said access token.

    resp, content = client.request(request_token_url, "GET")
    if resp['status'] != '200':
        raise Exception("Invalid response %s." % resp['status'])
    request_token = dict(urlparse.parse_qsl(content))

    # print("request sin dict: %s" % urlparse.parse_qsl(content))

    # print("request_token: %s" % request_token)

    key, value = list(request_token.items())[0]
    #print(key)
    #print(value)
    oauth_token = str(value)
    oauth_token = oauth_token[2:]
    oauth_token = oauth_token[:-1]

    key, value = list(request_token.items())[1]
    #print(key)
    #print(value)
    oauth_token_secret = str(value)
    oauth_token_secret = oauth_token_secret[2:]
    oauth_token_secret = oauth_token_secret[:-1]

    #print(oauth_token)
    #print(oauth_token_secret)

    print("Request Token:")
    print("    - oauth_token        = %s" % oauth_token)
    print("    - oauth_token_secret = %s" % oauth_token_secret)
    print()

    # Step 2: Redirect to the provider. Since this is a CLI script we do not
    # redirect. In a web application you would redirect the user to the URL
    # below.

    print("Go to the following link in your browser: ")
    print("{authorize_url}?oauth_token={oauth_token}&scope={scope}&expiration={expiration}".format(
        authorize_url=authorize_url,
        oauth_token=oauth_token,
        expiration=expiration,
        scope=scope,
    ))

    # After the user has granted access to you, the consumer, the provider will
    # redirect you to whatever URL you have told them to redirect to. You can
    # usually define this in the oauth_callback argument as well.
    accepted = 'n'
    while accepted.lower() == 'n':
        accepted = input('Have you authorized me? (y/n) ')
    oauth_verifier = input('What is the PIN? ')

    # Step 3: Once the consumer has redirected the user back to the oauth_callback
    # URL you can request the access token the user has approved. You use the
    # request token to sign this request. After this is done you throw away the
    # request token and use the access token returned. You should store this
    # access token somewhere safe, like a database, for future use.
    token = oauth.Token(oauth_token,
                        oauth_token_secret)
    token.set_verifier(oauth_verifier)
    client = oauth.Client(consumer, token)

    resp, content = client.request(access_token_url, "POST")
    access_token = dict(urlparse.parse_qsl(content))

    configs['key'] = trello_key
    configs['token'] = oauth_token
    show_url = input('Do you want to show card urls?(y/n)')
    if show_url.lower() == 'y':
        configs['url'] = True

    show_label = input('Do you want to show card labels?(y/n)')
    if show_label.lower() == 'y':
        configs['label'] = True

    show_done_cards = input('Do you want to show done cards?(y/n)')
    if show_done_cards.lower() == 'y':
        configs['done_cards'] = True

    f = codecs.open(os.path.expanduser('~') + '/' + CON_FILE, 'w', encoding='utf8')
    json.dump(configs, f)

    print("Access Token:")
    print("    - oauth_token        = %s" % oauth_token)
    print()
    print("Configurations are now saved in .trello-vim file in home directory.")
    print("You are ready to use the plugin")

if __name__ == '__main__':
    create_oauth_token()
