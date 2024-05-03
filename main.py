from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import requests
from bs4 import BeautifulSoup


app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def modify_response_html(html):
    soup = BeautifulSoup(html, "html.parser")
    # removing the top bar
    top_bar = soup.find(id="top-bar")
    if top_bar:
        top_bar.decompose()
    # remove the second tr after #sheets-viewport
    css_selector = "#sheets-viewport table tr:nth-child(2)"
    second_tr = soup.select_one(css_selector)
    if second_tr:
        second_tr.decompose()
    # convert the soup back to string
    new_html = str(soup)
    return new_html


@app.get("/", response_class=HTMLResponse)
def modify_embed(google_url: str):
    res = requests.get(google_url)
    new_html = modify_response_html(res.text)
    return new_html
