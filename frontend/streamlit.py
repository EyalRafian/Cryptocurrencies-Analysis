import streamlit as st
import requests
import json
import sys
import yfinance as yf
import pandas as pd
import altair as alt

st.set_page_config(page_title="Crypto Analysis")

# FastAPI endpoints for add and delete coins
backend = "http://fastapi:8000/"

def post_request(ticker, backend):
    json_data = json.dumps({"ticker": ticker})
    response = requests.post(
        backend, data=json_data
    )

st.title("Cryptocurrencies Analysis")

st.sidebar.image("https://miro.medium.com/max/1000/1*B_R11J_9G4U3lac0omktLQ.png", width=100,
                channels='BGR', output_format='PNG')

st.sidebar.header("Cryptocurrencies Analysis")
with st.sidebar.expander("Info"):
    st.info(f"""
        Click [here](https://finance.yahoo.com/cryptocurrencies/)
        for a list of cryptocurrencies symbols on Yahoo Finance.
        """)

# User options to add and delete coins in the table
input_ticker = st.sidebar.text_input("Add coin by symbol")
remove_ticker = st.sidebar.text_input("Remove coin by symbol")

# for adding coins
if input_ticker:
    try:
        post_request(input_ticker, f"{backend}add")
    except:
        st.sidebar.write("Ticker isn't correct. Try again.")

if remove_ticker:

    try:
        post_request(remove_ticker, f"{backend}delete")
    except:
        st.sidebar.write("Ticker isn't correct. Try again.")

# response = requests.post(f"{backend}table").json()
response = requests.get(backend).json()
coins = json.loads(response)['coins']


df = pd.DataFrame(coins, columns=[
                  'Ticker', 'Name', 'Price', '50 Days MA', '200 Days MA'])

if st.sidebar.checkbox("Above 50 Days Moving Average"):
    df = df[df['Price'] > df['50 Days MA']]

if st.sidebar.checkbox("Above 200 Days Moving Average"):
    df = df[df['Price'] > df['200 Days MA']]

# Update table to show the latest data from yFinance
if st.sidebar.button("Update table"):
    ticker_list = str(list(df['Ticker'])).strip() # store existing ticker in list
    response = post_request(ticker_list, f"{backend}update")


st.write(df)

if df.shape[0]!=0:
    if st.sidebar.checkbox("Show historical prices chart", value=True):

        # user options to select coin ticker and historical period
        user_hist_ticker = st.selectbox(
            "Select a ticker", list(df['Ticker']))
        user_hist_period = st.selectbox(
        "Select a period", ['1mo', '3mo', '6mo', '1y']
        )

        # call yfinance API for historical data of selected ticker
        hist = yf.Ticker(user_hist_ticker).history(period=user_hist_period)
        hist_mini = hist[['Close', 'Volume']].reset_index()
        hist_mini['Volume'] = hist_mini['Volume'].apply(lambda x : x/1000000)

        # build due-axis chart showing volume and price history
        base = alt.Chart(hist_mini).encode(x='Date')
        bar = base.mark_bar(color='#5276A7').encode(
                    alt.Y('Volume', axis=alt.Axis(title='Volume (million)',
                            titleColor='#5276A7')))

        line = base.mark_line(color='red').encode(
                     alt.Y('Close', axis=alt.Axis(title='Price (USD)',
                            titleColor='red')))

        c1 = alt.layer(bar, line).resolve_scale(y = 'independent')
        st.altair_chart(c1, use_container_width=True)

