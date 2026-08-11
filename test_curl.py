import urllib.request
import re

url = "http://127.0.0.1:8899/posts/picoctf-writeups/"
req = urllib.request.urlopen(url)
html = req.read().decode('utf-8')

print("Title check:", "<title>picoCTF — Récapitulatif & Progression</title>" in html or "picoCTF" in html)
print("Challenges check:", "Les challenges résolus" in html or "StegoRSA" in html)
print("Roadmap check:", "Progression à venir" in html)

# Let's check sidebar
# Look for sidebar or nav links
links = re.findall(r'<a[^>]*>(.*?)</a>', html, re.DOTALL)
print("Links found in html:", links[:20])

