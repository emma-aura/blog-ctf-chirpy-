import requests
from bs4 import BeautifulSoup

resp = requests.get("http://127.0.0.1:8899/picoctf/")
print("--- PICOCTF PAGE STATUS ---", resp.status_code)
soup = BeautifulSoup(resp.text, "html.parser")

print("Page Title:", soup.title.string if soup.title else "")
h1 = soup.find("h1")
print("H1 Heading:", h1.get_text(strip=True) if h1 else "None")

text = soup.get_text()
print("Contains picoCTF:", "picoCTF" in text)
print("Contains Writeups picoCTF:", "Writeups picoCTF" in text)
print("Contains 1 writeup:", "1 writeup" in text)
print("Contains StegoRSA:", "StegoRSA" in text)

print("Images:", [img.get("src") for img in soup.find_all("img")])

# Sidebar check
sidebar = soup.find("aside", id="sidebar") or soup.find(class_="site-sidebar") or soup.find("nav")
if sidebar:
    print("Sidebar links:")
    for a in sidebar.find_all("a"):
        print(" -", a.get_text(strip=True), a.get("href"), [i.get("class") for i in a.find_all("i")])

resp_home = requests.get("http://127.0.0.1:8899/")
print("\n--- HOMEPAGE STATUS ---", resp_home.status_code)
soup_home = BeautifulSoup(resp_home.text, "html.parser")
home_sidebar = soup_home.find("aside", id="sidebar") or soup_home.find(class_="site-sidebar") or soup_home.find("nav")
if home_sidebar:
    print("Homepage sidebar links in order:")
    for a in home_sidebar.find_all("a"):
        print(" -", a.get_text(strip=True), a.get("href"))
