import pandas as pd

from ballon_dor.config import CSV_PATH, CSV_POSITIONS_PATH
from ballon_dor.get_positions import save_players_positions


DF_BALLON_DOR = pd.read_csv(CSV_PATH)
RELOAD_POSITIONS = False


def get_ranking_on_period(year_begin, year_end, df=DF_BALLON_DOR):
    assert year_begin <= year_end, 'year_begin must be <= year_end'
    assert year_begin >= df['Year'].min(), 'year_begin must be >= df["Year"]'
    assert year_end <= df['Year'].max(), 'year_end must be <= df["Year"].max()'
    df_period = df.query(f'Year >= {year_begin} and Year <= {year_end}')
    cumulative_share = df_period.groupby('Player')['Share'].sum()
    new_ranking = cumulative_share.sort_values(ascending=False)
    return new_ranking

def present_ranking(ranking):
    for i, (player, share) in enumerate(r.iteritems(), start=1):
        print(f'{i:3d}: {player:<50s} {share:.5f}')

if RELOAD_POSITIONS:
    df = save_players_positions(DF_BALLON_DOR)
else:
    df_positions = pd.read_csv(CSV_POSITIONS_PATH)
    df = pd.merge(DF_BALLON_DOR, df_positions, on='Player')
df_defenders = df.query('Vetted_position== "defender"')
r = get_ranking_on_period(1956, 2018, df=df_defenders)
present_ranking(r)

