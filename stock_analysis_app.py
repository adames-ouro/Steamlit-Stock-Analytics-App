import datetime as dt 
import pandas as pd
import numpy as np 
import warnings
import plotly.graph_objects as go
import streamlit as st

warnings.simplefilter(action='ignore', category=[FutureWarning,ValueError])


def Exponential_Moving_Average(stock_df, short_window,long_window):
    # column names for long and short moving average columns
    moving_avg = 'EMA'
    short_window_col = str(short_window) + '_' + moving_avg
    long_window_col = str(long_window) + '_' + moving_avg  

    # Create a short simple moving average column
    stock_df[short_window_col] = stock_df['Close'].ewm(span=short_window, adjust=True).mean()

    # Create a long simple moving average column
    stock_df[long_window_col] = stock_df['Close'].ewm(span=long_window, adjust=True).mean()

    # create a new column 'Signal' such that if faster moving average is greater than slower moving average 
    # then set Signal as 1 else 0.
    stock_df['Signal'] = 0.0  
    stock_df['Signal'] = np.where(stock_df[short_window_col] > stock_df[long_window_col], 1.0, 0.0) 

    # create a new column 'Position' which is a day-to-day difference of the 'Signal' column. 
    stock_df['Position'] = stock_df['Signal'].diff()

    # Create a dictionary to map values to labels
    label_map = {
        1: 'Sell',
        0: 'Hold',
        -1: 'Buy'
    }

    # Create new column with labels
    stock_df['Label'] = stock_df['Position'].fillna(0).map(label_map)

    # remove na
    stock_df = stock_df.fillna(0)

    return stock_df.drop(columns=['Signal'])

def visual(stock_df,stock_symbol,short_window,long_window):
    # column names for long and short moving average columns
    moving_avg = 'EMA'
    short_window_col = str(short_window) + '_' + moving_avg
    long_window_col = str(long_window) + '_' + moving_avg  

    # visualize data with buy/sell triggers
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=stock_df['Date'], y=stock_df['Close'],
                        mode='lines',
                        name='Close',
                        line=dict(color='black')))

    fig.add_trace(go.Scatter(x=stock_df['Date'], y=stock_df[short_window_col],
                        mode='lines',
                        name=short_window_col,
                        line=dict(color='blue')))

    fig.add_trace(go.Scatter(x=stock_df['Date'], y=stock_df[long_window_col],
                        mode='lines',
                        name=long_window_col,
                        line=dict(color='green')))

    # Add 'buy' signals
    buy_signals = stock_df[stock_df['Position'] == 1]
    fig.add_trace(go.Scatter(x=buy_signals['Date'], y=buy_signals[short_window_col],
                        mode='markers',
                        marker_symbol='triangle-up',
                        marker_size=15, marker_color='green',
                        name='Sell Signal'))

    # Add 'sell' signals
    sell_signals = stock_df[stock_df['Position'] == -1]
    fig.add_trace(go.Scatter(x=sell_signals['Date'], y=sell_signals[short_window_col],
                        mode='markers',
                        marker_symbol='triangle-down',
                        marker_size=15, marker_color='red',
                        name='Buy Signal'))

    # Update layout
    fig.update_layout(title=str(stock_symbol) + ' - ' + str(moving_avg) + ' Crossover',
                    xaxis_title='Date',
                    yaxis_title='Price in $',
                    template='plotly_white')

    return fig

# Set the app title and the app icon
# Create a blue rectangle using HTML inside Markdown
st.markdown(
        """
        <div style="background-color: blue; width: 100%; height: 25px; display: flex; align-items: center; justify-content: center;">
            <span style="color: black; font-weight: bold;"></span>
        </div>
        """,
        unsafe_allow_html=True)

st.title("Strategy Helper for stock analysis.")

# intention of tool
st.write(
    """
    This Streamlit application is designed to help users analyze stock data by visualizing Exponential Moving Averages (EMA) and identifying potential Buy/Sell signals based on the crossover of short and long-term EMA.
    """
        )

# Create a blue rectangle using HTML inside Markdown
st.markdown(
        """
        <div style="background-color: blue; width: 100%; height: 25px; display: flex; align-items: center; justify-content: center;">
            <span style="color: black; font-weight: bold;"></span>
        </div>
        """,
        unsafe_allow_html=True)

# Upload dataset
st.subheader('Please upload stock data.')

st.write(
    """
    Data must be in CSV format and contain the following columns: Date, Close.
    """
        )

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
if uploaded_file:
    data = pd.read_csv(uploaded_file)
    st.write("Got the uploaded cvs!")
    st.session_state.dataframe = data

# generates random data
else:
    data = pd.DataFrame({'Date': pd.Timestamp.now().date(),'Close':0.0})
    st.write("No data uploaded.")
    st.session_state.dataframe = data
    

# Create a blue rectangle using HTML inside Markdown
st.markdown(
        """
        <div style="background-color: blue; width: 100%; height: 25px; display: flex; align-items: center; justify-content: center;">
            <span style="color: black; font-weight: bold;"></span>
        </div>
        """,
        unsafe_allow_html=True)


st.subheader('Please Describe your stock data.')

# Create a blue rectangle using HTML inside Markdown
st.markdown(
        """
        <div style="background-color: blue; width: 100%; height: 50px; display: flex; align-items: center; justify-content: center;">
            <span style="color: black; font-weight: bold;"></span>
        </div>
        """,
        unsafe_allow_html=True)


# user inputs
st.session_state.stock_symbol = st.text_input("Enter specific stock symbol. For example, Apple stock symbol is APPL.",
                                             "Stock")

st.session_state.short_window = st.number_input("Enter number of consecutive days used for short-term analysis. Default is '7'.",7)

st.session_state.long_window = st.number_input("Enter number of consecutive days used for long-term analysis. Default is '90'.",90)

# Create a blue rectangle using HTML inside Markdown
st.markdown(
        """
        <div style="background-color: blue; width: 100%; height: 50px; display: flex; align-items: center; justify-content: center;">
            <span style="color: black; font-weight: bold;"></span>
        </div>
        """,
        unsafe_allow_html=True)

# Display a button that when clicked will "navigate" to visuals

st.title('Visuals of stock data.')

if st.checkbox('Explanation'):

    # Render HTML content
    st.markdown("""
    <p><strong>Exponential Moving Average (EMA)</strong></p>
    <p>The EMA is computed as:</p>
    """,
        unsafe_allow_html=True)

    # Render LaTeX content
    st.latex(r"\text{EMA}_t = (C_t \times \alpha) + (\text{EMA}_{t-1} \times (1-\alpha))")

    # Continue with HTML content
    st.markdown("""
    <p>Where:</p>
    """,
        unsafe_allow_html=True)

    # LaTeX with simple text
    st.latex(r"""
            \text{EMA}_t \text{: is Exponential Moving Average at time t }
             """)

    st.latex(r"""
            \text{C}_t \text{: is Closing price at time t }
             """)

    st.latex(r"""
            \text{EMA}_{t-1} \text{: is Exponential Moving Average at time t-1 }
             """)

    st.latex(r"""
            \alpha \text{: is Smoothing factor, calculated as}
             """)

    # Render the next LaTeX formula
    st.latex(r"\alpha = \frac{2}{N + 1}")

    # Finish with the remaining HTML
    st.markdown("""
    <p>Here, N is the number of days in the moving average period.</p>
    """,
        unsafe_allow_html=True)

    st.title("Benefits of Using Long and Short Time Window with EMA")

    st.write("""
    Using both a long and a short time window with Exponential Moving Averages (EMA) is a common strategy in technical analysis for identifying trends, especially in the context of trading. Here's why this approach is popular and beneficial:

    1. **Trend Identification:** 
    - When the short-term EMA crosses above the long-term EMA, it often indicates the beginning of an upward trend (bullish signal). 
    - Conversely, when the short-term EMA crosses below the long-term EMA, it can be a sign of a downward trend (bearish signal).

    2. **Sensitivity vs. Stability:**
    - **Short-term EMA** is more sensitive to recent price movements. When prices change, the short-term EMA will reflect this change more quickly than the long-term EMA.
    - **Long-term EMA** is less sensitive to daily price fluctuations and provides a more stable and smoother line that represents long-term trends. 

    3. **Reduction of False Signals:** 
    - While a short-term EMA might produce many signals (due to its sensitivity), not all of them are indicative of a sustained trend. By requiring confirmation from the long-term EMA (i.e., a crossover), the number of false signals can be reduced.

    4. **Confirmation and Strength of Trend:**
    - The divergence between the short-term and long-term EMA can give a sense of the strength of a trend. If the two averages are moving apart rapidly, it can indicate a strong trend, while if they start to converge, it might suggest the trend is weakening.

    5. **Versatility:** 
    - Different pairs of long and short windows can be used depending on the trading strategy, asset being traded, and the trader's time horizon. For instance, a day trader might use a 12-period short-term EMA with a 26-period long-term EMA on a minute chart, while a long-term trader might use the same averages on a daily or weekly chart.

    6. **Historical Success:** 
    - This approach of using dual EMAs for crossovers has historically been a part of many successful trading strategies, adding to its popularity.

    In summary, using both a long and a short EMA provides a balance between sensitivity to recent price changes and confirmation of longer-term trends, thereby aiding traders in making more informed decisions. However, like all technical indicators, it's important to use EMA crossovers in conjunction with other tools and methods for the best results.
    """)


else:
    st.subheader(str(st.session_state.stock_symbol) + 
                ' Exponential Moving Average Analysis'
                )
    
    if len(data) != 0:
        stock_df = Exponential_Moving_Average(stock_df = st.session_state.dataframe,
                                                short_window = st.session_state.short_window,
                                                long_window = st.session_state.long_window)

        st.plotly_chart(
            visual(stock_df = st.session_state.dataframe,
                    stock_symbol = str(st.session_state.stock_symbol),
                    short_window = st.session_state.short_window,
                    long_window = st.session_state.long_window),

            use_container_width=True,
            theme = None
            )
    else:
        st.write('Select data to visualize.')
