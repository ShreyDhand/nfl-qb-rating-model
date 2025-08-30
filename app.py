import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import streamlit as st

# streamlit run main.py

# Load data
pbp_2024 = pd.read_csv('pbp_data/play_by_play_2024.csv', low_memory=False)

# Filter valid QB plays
qb_plays = pbp_2024[(pbp_2024['passer_player_name'].notna()) & (pbp_2024['epa'].notna())]

# Aggregate stats
qb_stats = qb_plays.groupby('passer_player_name').agg(
    team=('posteam', lambda x: x.mode()[0]),
    total_plays=('play_id', 'count'),
    total_epa=('epa', 'sum'),
    epa_per_play=('epa', 'mean'),
    avg_cpoe=('cpoe', 'mean'),
    total_yards=('yards_gained', 'sum'),
    pass_tds=('pass_touchdown', 'sum'),
    ints=('interception', 'sum')
).reset_index()

# Filters (150 plays - 5 games)
qb_stats = qb_stats[qb_stats['total_plays'] >= 150]

# Rating calculation
qb_stats['neg_ints'] = qb_stats['ints'] * -1
features = ['epa_per_play', 'avg_cpoe', 'total_yards', 'pass_tds', 'neg_ints']
weights = np.array([0.30, 0.20, 0.15, 0.25, 0.10])
z = StandardScaler().fit_transform(qb_stats[features])
qb_stats['raw_score'] = z @ weights
qb_stats['qb_rating'] = MinMaxScaler((50, 99)).fit_transform(qb_stats[['raw_score']])
qb_stats['rank'] = qb_stats['qb_rating'].rank(ascending=False).astype(int)
qb_stats = qb_stats.sort_values('qb_rating', ascending=False).reset_index(drop=True)

# Streamlit UI 
st.title("NFL QB Ratings (2024)")

qb_names = qb_stats['passer_player_name'].sort_values().tolist()
selected_qb = st.selectbox("Search for a QB:", qb_names)

qb = qb_stats[qb_stats['passer_player_name'] == selected_qb].iloc[0]


# Load image mapping
qb_images = pd.read_csv('pbp_data/qb_images.csv')
img_dict = dict(zip(qb_images.qb_name, qb_images.image_url))

# Display image if found
# Normalize QB name for lookup
normalized_name = selected_qb.replace('.', '').replace(' ', '')

img_url = img_dict.get(normalized_name)

if img_url:
    st.image(img_url, caption=selected_qb, width=150)
else:
    st.text("Image not available")


st.markdown(f"**Team**: {qb['team']}")
# QB Overview Section
st.markdown(f"**Team**: {qb['team']}")
st.markdown(f"**Rating**: {qb['qb_rating']:.2f}")
st.markdown(f"**Rank**: {qb['rank']}")

# --- Full Rankings Section ---
st.markdown("---")
st.subheader("Full QB Rankings")

sort_order = st.selectbox("Sort by Rating:", ["Highest Overall", "Lowest Overall"])
sorted_qbs = qb_stats.sort_values("qb_rating", ascending=(sort_order == "Lowest Overall"))

st.dataframe(
    sorted_qbs[[
        'rank', 'passer_player_name', 'team', 'qb_rating', 'epa_per_play',
        'avg_cpoe', 'total_yards', 'pass_tds', 'ints'
    ]].style.format({
        'qb_rating': "{:.2f}", 
        'epa_per_play': "{:.2f}", 
        'avg_cpoe': "{:.2f}"
    }),
    use_container_width=True
)
