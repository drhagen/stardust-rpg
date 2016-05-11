import re

import requests
import bs4


class Roll20Login:
    def __init__(self, firebase_root: str, auth_token: str, campaign_path: str) -> None:
        self.firebase_root = firebase_root
        self.auth_token = auth_token
        self.campaign_path = campaign_path


def login(email: str, password: str) -> Roll20Login:
    session = requests.session()
    session.post(
        'https://app.roll20.net/sessions/create',
        data={'email': email, 'password': password}
    )

    campaigns_response = session.get('https://app.roll20.net/campaigns/search')
    campaigns = []
    document = bs4.BeautifulSoup(campaigns_response.text, 'html.parser')
    for div in document.find_all('div'):
        if 'class' in div.attrs and 'gameinfo' in div['class']:
            if 'Join Game' in div.text:
                campaigns.append({
                    'name': div.a.text,
                    'link': div.find_all('a')[1]['href']
                })

    if len(campaigns) == 0:
        raise RuntimeError('No campaigns found.')

    for campaign in campaigns:
        campaign_id = re.search(r'setcampaign/(\d+)', campaign['link']).group(1)
        print('Found campaign #{} {}'.format(campaign_id, campaign['name']))

    join_response = session.get(campaigns[0]['link'])
    startjs = None
    document = bs4.BeautifulSoup(join_response.text, 'html.parser')
    for script in document.find_all('script'):
        if 'src' in script.attrs and '/editor/startjs/' in script['src']:
            startjs = script['src']

    if startjs is None:
        raise RuntimeError('Could not find startjs.')

    js_response = session.get('https://app.roll20.net' + startjs)
    fb_root = re.search(r'window\.FIREBASE_ROOT\s+=\s+"(.*)"', js_response.text).group(1)
    auth_token = re.search(r'window\.GNTKN\s+=\s+"(.*)"', js_response.text).group(1)
    campaign_path = re.search(r'window\.campaign_storage_path\s+=\s+"(.*)"',
                              js_response.text).group(1)

    print('FIREBASE_ROOT: {}'.format(fb_root))
    print('GNTKN: {}'.format(auth_token))
    print('campaign_storage_path: {}'.format(campaign_path))

    return Roll20Login(firebase_root=fb_root, auth_token=auth_token, campaign_path=campaign_path)
