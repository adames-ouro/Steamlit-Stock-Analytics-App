# Strategy Helper for Stock Analysis

![EMA_vis](./EMA_vis.png)


## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation & Usage](#installation--usage)
- [Acknowledgements](#acknowledgements)

## Overview

This application is designed to assist users in analyzing stock data. Using Streamlit, the application visualizes Exponential Moving Averages (EMA) and identifies potential Buy/Sell signals based on the crossover of short and long-term EMA.

## Features
1. **Exponential Moving Average (EMA) Computation**: Helps in identifying stock price trends by comparing the short-term and long-term moving averages.
2. **Visual Representation**: Displays stock prices, EMA, and Buy/Sell signals on an interactive plot.
3. **Stock Data Insights**: Provides date-specific information, along with a summary of the closing value.
4. **User Interactivity**: Allows users to specify stock symbol, short-term, and long-term window periods.
5. **Educational**: Offers an in-depth explanation of the EMA and the significance of using dual EMAs.

## Requirements

- Python 3.6 or newer.
- Libraries: `yfinance`, `datetime`, `pandas`, `numpy`, `plotly`, `streamlit`.

## Installation & Usage

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/your-github-username/Steamlit-Stock-Analytics.git
    cd Steamlit-Stock-Analytics
    ```

2. **Setup a Virtual Environment (optional but recommended)**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Required Libraries**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the Streamlit App**:
    ```bash
    streamlit run stock_analysis_app.py 
    ```

## Acknowledgements

- Data visualization powered by [Plotly](https://plotly.com/).
- Built with [Streamlit](https://www.streamlit.io/).
- Data transformations are power by [Pandas](https://pandas.pydata.org/).

