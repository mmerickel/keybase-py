import base64
import binascii
import hashlib
import hmac
import json
from urllib.parse import urlencode

import requests
import scrypt

CMD_URL = 'https://keybase.io/_/api/1.0/%s.json'

def make_url(cmd, params=None):
    if params is not None:
        qs = '?' + urlencode(params, doseq=True)
    else:
        qs = ''
    return CMD_URL % cmd + qs

def make_session():
    session = requests.Session()
    return session

def _do_getsalt(session, username):
    url = make_url('getsalt', {'email_or_username': username})
    r = session.get(url)
    assert r.status_code == 200

    content = r.json()
    assert content['status']['code'] == 0

    csrf = content['csrf_token']
    salt = content['salt']
    login_session = content['login_session']

    session.headers['X-CSRF-Token'] = csrf

    return {
        'salt': salt,
        'login_session': login_session,
        'username': username,
        'csrf': csrf,
    }

def _do_login(session, salt_info, password):
    salt = salt_info['salt']
    login_session = salt_info['login_session']

    if isinstance(password, str):
        password = password.encode('utf8')
    if isinstance(salt, str):
        salt = salt.encode('utf8')

    rs = binascii.unhexlify(salt)
    pwh = scrypt.hash(password, rs, N=2**15, r=8, p=1, buflen=224)[192:224]

    content = base64.b64decode(login_session)
    hmac_pwh = hmac.new(pwh, content, hashlib.sha512).hexdigest()

    url = make_url('login')
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    params = {
        'email_or_username': salt_info['username'],
        'hmac_pwh': hmac_pwh,
        'login_session': salt_info['login_session'],
    }
    r = session.post(url, json.dumps(params), headers=headers)
    assert r.status_code == 200

    content = r.json()
    assert content['status']['code'] == 0

    session.cookies['session'] = content['session']
    return content['me']

def login(session, username, password):
    salt_info = _do_getsalt(session, username)
    profile = _do_login(session, salt_info, password)

    return profile

def add_pubkey(session, pubkey):
    url = make_url('key/add')
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    params = {
        'public_key': pubkey,
        'is_primary': True,
    }
    r = session.post(url, json.dumps(params), headers=headers)
    assert r.status_code == 200

    content = r.json()
    assert content['status']['code'] == 0

    return True

def parse_args(argv=None):
    import argparse
    import sys
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser()
    parser.add_argument('--pubkey-file')
    parser.add_argument('-l', '--login', required=True)
    parser.add_argument('-p', '--password')
    return parser.parse_args(argv)

def main(argv=None):
    from getpass import getpass

    args = parse_args()

    username = args.login
    if args.password is None:
        password = getpass('Password: ')
    else:
        password = args.password

    session = make_session()
    user_info = login(session, username, password)

    if args.pubkey_file is not None:
        with open(args.pubkey_file, 'r', encoding='utf8') as fp:
            pubkey = fp.read()
        add_pubkey(session, pubkey)

if __name__ == '__main__':
    sys.exit(main() or 0)
