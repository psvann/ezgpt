# streamlit app

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from ragchain import ChainQA
from scraper import Scraper
from utils import create_database, clear_files



# create chromadb instance and collection
if st.button("Create Database"):
    chain = ChainQA()

# start streamlit app
st.title(':chain: ChainScrape')


url = st.text_input("Enter a URL to scrape: ")

if st.button("Scrape"): 
    progress_text = "Scraping in Progress. Please wait."
    progress_bar = st.progress(0, text=progress_text)
    scraper = Scraper()
    if url == "":
        st.write("Please enter a URL.")
    else:
        p = 0
        links = scraper.scrape_links(url)
        links = links[:100]
        t = len(links)

        for i in range(t):
            text = scraper.scrape_and_get_text(links[i])
            chain.add_document(text)
            p = int(i/t*100)
            progress_bar.progress(p, text=f"Processing site: {i} of {t} pages processed.")
        
        st.status("Links scraped: %s" % len(links))

    
if st.button("Enter Chat"): 
    
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







