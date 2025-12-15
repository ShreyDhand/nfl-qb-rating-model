# NFL QB Performance Ratings (2024)

A data-driven quarterback rating model built from 2024 NFL play-by-play data. The project aggregates advanced efficiency metrics and volume stats to produce a single **QB performance score**, presented in an interactive Streamlit app with rankings and player lookup.



## What This Project Does

* Aggregates 2024 NFL play-by-play data at the quarterback level
* Uses advanced metrics such as **EPA/play** and **CPOE** alongside traditional stats
* Combines metrics using weighted, standardized scoring
* Produces a QB rating scaled to a familiar **50–99 range**
* Displays full rankings and individual QB profiles in a Streamlit interface



## Data & Methodology

* Source: 2024 NFL play-by-play data
* Minimum threshold applied to exclude low-sample QBs
* Features used in the model:

  * EPA per play
  * Average CPOE
  * Total passing yards
  * Passing touchdowns
  * Interceptions (penalized)
* Metrics are standardized (z-scores), weighted, and scaled using MinMax normalization



## Tech Stack

* Python
* Pandas / NumPy
* scikit-learn
* Streamlit



## How to Run

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Run the app:

   ```bash
   streamlit run main.py
   ```



## Data Notes

Raw play-by-play data and image mapping files are not included in this repository. The app expects:

* 2024 NFL play-by-play CSV data
* A QB image mapping CSV (optional)

Paths and column usage are documented directly in the source code.



## Use Case

This project is intended for exploratory analysis and portfolio demonstration of sports analytics concepts, including feature engineering, normalization, and metric weighting using real NFL data.



## Author

Built as a sports analytics portfolio project focused on quarterback performance evaluation.
