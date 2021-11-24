import time

from bs4 import BeautifulSoup
from joblib import Parallel, delayed
from numpy import vectorize
import pandas as pd
import requests
import wikipedia
import wikipediaapi

WIKI = wikipediaapi.Wikipedia('en')
VETTED_POSITIONS = {
    'second striker': 'forward',
    'right-back': 'defender',
    'wingback': 'defender',
    'outside right': 'forward',
    'goalkeeper': 'goalkeeper',
    'outside-left': 'forward',
    'left-half': 'midfielder',
    'right-half': 'midfielder',
    'centre midfielder': 'midfielder',
    'centre half': 'midfielder',
    'box-to-box midfielder': 'midfielder',
    'left midfielder': 'midfielder',
    'full-back': 'defender',
    'right wing-back': 'defender',
    'centre-back': 'defender',
    'striker': 'forward',
    'right winger': 'forward',
    'inside-forward': 'forward',
    'central defender': 'defender',
    'left-winger': 'forward',
    'winger': 'forward',
    'defensive midfielder': 'midfielder',
    'libero': 'defender',
    'inside forward': 'forward',
    'forward': 'forward',
    'inside right': 'forward',
    'centre-forward': 'forward',
    'attacking midfielder': 'midfielder',
    'wing forward': 'forward',
    'left back': 'defender',
    'midfielder': 'midfielder',
    'fullback': 'defender',
    'left half': 'midfielder',
    'central midfielder': 'midfielder',
    'right back': 'defender',
    'left winger': 'forward',
    'left wing-back': 'defender',
    'center back': 'defender',
    'left-back': 'defender',
    'centre forward': 'forward',
    'defender': 'defender',
    'centre back': 'defender',
    'right midfielder': 'midfielder',
    'sweeper': 'defender',
}
# VETTED_POSITIONS = list(set(p for ps in VETTED_POSITIONS for p in ps.lower().strip().replace(',', '/').split('/')))

def get_wikipedia_positions(player_name):
    search_results = wikipedia.search(f'{player_name} football')
    try:
        player_name_wiki = search_results[0]
    except IndexError:
        return None
    try:
        player = wikipedia.page(player_name_wiki)
    except (wikipedia.exceptions.PageError, wikipedia.exceptions.DisambiguationError):
        player = WIKI.page(player_name_wiki)
        url_player = player.fullurl
    else:
        url_player = player.url
    req = requests.get(url_player) 
    soup = BeautifulSoup(req.text, features="html.parser")
    table = soup.find('table', class_='infobox vcard')
    if table is None:
        table = soup.find('table', class_='infobox biography vcard')
    if table is None:
        return None
    positions = None
    for tr in table.find_all('tr'):
        if tr.find('th') and 'Position' in tr.find('th').text:
            positions = tr.find('td').text
            break
    return positions

def save_players_positions(df, name='players_positions'):
    s_players = pd.Series(df['Player'].unique(), name='Player')
    s_positions = Parallel(-1)(delayed(get_wikipedia_positions)(player) for player in s_players)
    s_positions = pd.Series(s_positions, name='Wikipedia_position')
    vetted_positions = Parallel(-1)(delayed(wikipedia_position_to_vetted_position)(p) for p in s_positions)
    s_vetted_positions = pd.Series(vetted_positions, name='Vetted_position')
    df_players = pd.concat([s_players, s_positions, s_vetted_positions], axis=1)
    csv_name = f'{name}_{int(time.time())}.csv'
    df_players.to_csv(csv_name)
    df = pd.merge(df, df_players, on='Player')
    return df

def wikipedia_position_to_vetted_position(wikipedia_position):
    if wikipedia_position is None:
        return None
    wikipedia_position = wikipedia_position.lower()
    vetted_position = []
    for vp, p_name in VETTED_POSITIONS.items():
        if vp in wikipedia_position:
            vetted_position.append(p_name)
    return vetted_position