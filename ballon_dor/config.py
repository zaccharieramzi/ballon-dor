import os
from pathlib import Path


CSV_PATH = Path(os.environ.get('CSV_BALLON_DOR_PATH', 'BallonDOr.csv'))
POSITIONS_CSV_PATH = Path(os.environ.get('CSV_POSITIONS_PATH', 'players_positions.csv'))