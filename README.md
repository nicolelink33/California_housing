# California Housing
## Dashboard URLs
Stable Dashboard: https://019c91e4-9ae2-9f80-d307-5b31052f2781.share.connect.posit.cloud/   
Preview Dashboard: https://019c91ed-c71c-d6a8-76fc-1417d4c15a89.share.connect.posit.cloud/

## About
This repository contains a data dashboard project that enables investigation of California housing data from 1990. At present, we include the raw dataset from Kaggle, initial exploratory data analysis, and an overall proposal for the dashboard. We intend to include visualizations such as an interactive map to investigate house prices and features by location, as well as both scatter plots to investigate house prices by the age of the house, median income of the households on the same block, proximity to the ocean, and bar plots to investigate house prices by number of bedrooms, number of total rooms, the number of households on the block etc. The intent is both to enable user-directed investigation of California housing prices in the year 1990, and to provide proof of concept of this type of dashboard, which could be adapted for datasets with wider or more modern time ranges.

## Usage

To run the dashboard locally:

1. Clone this repository:

Using HTTPS:

```bash
git clone https://github.com/UBC-MDS/DSCI-532_2026_5_california_housing.git
```

Or, using SSH:

```bash
git clone git@github.com:UBC-MDS/DSCI-532_2026_5_california_housing.git
```

Navigate to the project root:

```bash
cd DSCI-532_2026_5_california_housing
```

2. Create the environment:

```bash
conda env create -f environment.yml
conda activate dsci-532-dashboard
```

3. Launch the dashboard:

```bash
shiny run --reload src/app.py
```

4. Open `http://127.0.0.1:8000` in browser.

## Authors

Ali Boloor Foroosh, Fu Hung (Teem) Kwong, Nicole Link, Shrabanti Bala Joya 

## Attribution

Gen AI tools (Google Gemini, OpenAI ChatGPT, and GitHub Copilot) were used to assist in code generation and documentation drafting. All generated content was reviewed and edited by the human authors to ensure accuracy and quality.
