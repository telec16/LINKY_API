#https://github.com/outadoc/linkindle

import base64
import requests
import html

LOGIN_BASE_URI = 'https://espace-client-connexion.enedis.fr'
API_BASE_URI = 'https://espace-client-particuliers.enedis.fr/group/espace-particuliers'

API_ENDPOINT_LOGIN = '/auth/UI/Login'
API_ENDPOINT_HOME = '/home'
API_ENDPOINT_DATA = '/suivi-de-consommation'

R_ID_HOUR = 'urlCdcHeure';
R_ID_DAY = 'urlCdcJour';
R_ID_MONTH = 'urlCdcMois';
R_ID_YEAR = 'urlCdcAn';

DATA_NOT_REQUESTED = -1
DATA_NOT_AVAILABLE = -2


def login(username, password):
    session = requests.Session()

    payload = {'IDToken1': username,
               'IDToken2': password,
               'SunQueryParamsString': base64.b64encode(b'realm=particuliers'),
               'encoded': 'true',
               'gx_charset': 'UTF-8'}

    req = session.post(LOGIN_BASE_URI + API_ENDPOINT_LOGIN, allow_redirects=False, data=payload)

    if not 'iPlanetDirectoryPro' in session.cookies:
        print("Login unsuccessful. Check your credentials.")

    return session



def _get_data(session, resource_id, start_date=None, end_date=None):
    req_part = 'lincspartdisplaycdc_WAR_lincspartcdcportlet'

    payload = {
        '_' + req_part + '_dateDebut': start_date,
        '_' + req_part + '_dateFin': end_date
    }

    params = {
        'p_p_id': req_part,
        'p_p_lifecycle': 2,
        'p_p_state': 'normal',
        'p_p_mode': 'view',
        'p_p_resource_id': resource_id,
        'p_p_cacheability': 'cacheLevelPage',
        'p_p_col_id': 'column-1',
        'p_p_col_pos': 1,
        'p_p_col_count': 3
    }

    req = session.post(API_BASE_URI + API_ENDPOINT_DATA, allow_redirects=False, data=payload, params=params)

    if 300 <= req.status_code < 400:
        req = session.post(API_BASE_URI + API_ENDPOINT_DATA, allow_redirects=False, data=payload, params=params)

    if req.status_code == 200 and req.text is not None and "Conditions d'utilisation" in req.text:
        print("You need to accept the latest Terms of Use. Please manually log into the website, then come back.")

    res = req.json()

    if res['etat'] and res['etat']['valeur'] == 'erreur' and res['etat']['erreurText']:
        print(html.unescape(res['etat']['erreurText']))

    return res
