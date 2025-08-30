import pandas as pd

# Load the 2024 play-by-play data
pbp_2024 = pd.read_csv('pbp_data/play_by_play_2024.csv', low_memory=False)

# Preview QB-related columns
print(pbp_2024[['passer_player_name', 'epa', 'cpoe', 'yards_gained', 'play_type']].head())


# Filter plays where a QB is listed and EPA is valid
qb_plays = pbp_2024[
    (pbp_2024['passer_player_name'].notna()) &
    (pbp_2024['epa'].notna())
]

# Aggregate stats by QB
qb_stats = qb_plays.groupby('passer_player_name').agg(
    total_plays=('play_id', 'count'),
    total_epa=('epa', 'sum'),
    epa_per_play=('epa', 'mean'),
    avg_cpoe=('cpoe', 'mean'),
    total_yards=('yards_gained', 'sum'),
    pass_tds=('pass_touchdown', 'sum'),
    ints=('interception', 'sum')
).reset_index()

qb_stats = qb_stats[qb_stats['total_plays'] >= 150]


from sklearn.preprocessing import StandardScaler, MinMaxScaler
import numpy as np

# Metrics used in the rating
metrics = ['epa_per_play', 'avg_cpoe', 'total_yards', 'pass_tds', 'ints']

# Copy so dont mess with original
qb_scores = qb_stats.copy()

# Invert interceptions so fewer is better
qb_scores['neg_ints'] = qb_scores['ints'] * -1

# Re-select with "ints" replaced
features = ['epa_per_play', 'avg_cpoe', 'total_yards', 'pass_tds', 'neg_ints']

# Normalize using z-scores
scaler = StandardScaler()
qb_scores_z = scaler.fit_transform(qb_scores[features])

# Weight: EPA=30%, CPOE=20%, Yards=15%, TDs=25%, INTs=10%
weights = np.array([0.30, 0.20, 0.15, 0.25, 0.10])
qb_scores['raw_score'] = qb_scores_z @ weights

# Scale to Madden range (50–99)
minmax = MinMaxScaler(feature_range=(50, 99))
qb_scores['qb_rating'] = minmax.fit_transform(qb_scores[['raw_score']])

# Sort and show top 10 QBs
top_qbs = qb_scores[['passer_player_name', 'qb_rating']].sort_values(by='qb_rating', ascending=False)
print(top_qbs.head(32))  # Show top 30 QBs

