import pandas as pd

from ballon_dor.config import CSV_PATH, CSV_POSITIONS_PATH
from ballon_dor.get_positions import save_players_positions


DF_BALLON_DOR = pd.read_csv(CSV_PATH)
RELOAD_POSITIONS = False


def get_ranking_on_period(year_begin, year_end):
    assert year_begin <= year_end, 'year_begin must be <= year_end'
    assert year_begin >= DF_BALLON_DOR['Year'].min(), 'year_begin must be >= DF_BALLON_DOR["Year"]'
    assert year_end <= DF_BALLON_DOR['Year'].max(), 'year_end must be <= DF_BALLON_DOR["Year"].max()'
    df_period = DF_BALLON_DOR.query(f'Year >= {year_begin} and Year <= {year_end}')
    cumulative_share = df_period.groupby('Player')['Share'].sum()
    new_ranking = cumulative_share.sort_values(ascending=False)
    return new_ranking


# r = get_ranking_on_period(2000, 2018)
# for i, (player, share) in enumerate(r.iteritems(), start=1):
#     print(f'{i:3d}: {player:<50s} {share:.5f}')

if RELOAD_POSITIONS:
    save_players_positions(DF_BALLON_DOR)
else:
    df_positions = pd.read_csv(CSV_POSITIONS_PATH)
    df = pd.merge(DF_BALLON_DOR, df_positions, on='Player')
    
