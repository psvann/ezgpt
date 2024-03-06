# streamlit app

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from ragchain import ChainQA
from scraper import Scraper
from utils import create_database, clear_files

# start streamlit app
st.title('ChainScrape')


url = st.text_input("Enter a URL to scrape: ")

if st.button("Scrape"): 
    scraper = Scraper()
    if url == "":
        st.write("Please enter a URL.")
    else:
        st.spinner("Getting links from URL...")
        links = scraper.scrape_links(url)
        st.status("Links scraped: %s" % len(links))

    
if st.button("Enter Chat"): 
    chain = ChainQA()
    chain.set_llm()
    chain.vectorize()

    session = chain.get_qa_session()
    question = ""
    while question != "X": 
        question = st.chat_input("Enter a message")
        response = session.run(question)
        st.chat_message(response)    
    
    # scrape page

    # get links and store in db
    # for l in links -> scrape page, get text, and put in vector storage
    # do so in a progress bar
    # let user know when done 



if st.button("Clear Files"): 
    clear_files()
    st.status("Files cleared.")







