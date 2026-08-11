import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path='/usr/bin/chromium', headless=True)
        page = await browser.new_page()
        
        # 1. Navigate to picoctf-writeups
        await page.goto('http://127.0.0.1:8899/posts/picoctf-writeups/')
        title_1 = await page.title()
        print(f"Title 1: {title_1}")
        
        content = await page.content()
        has_challenges = '🏆 Les challenges résolus' in content or 'Les challenges résolus' in content
        has_stegorsa = 'StegoRSA' in content
        has_roadmap = 'Progression à venir' in content
        
        print(f"Has challenges section: {has_challenges}")
        print(f"Has StegoRSA: {has_stegorsa}")
        print(f"Has Progression à venir: {has_roadmap}")
        
        # Check sidebar tabs
        # Expected: Accueil, Catégories, Tags, Archives, À propos, Ressources. NOT PICOCTF.
        sidebar_text = await page.locator('aside, nav, .sidebar, .menu').all_inner_texts()
        print(f"Sidebar / Nav texts: {sidebar_text}")
        
        # Click prominent link to StegoRSA writeup
        # Let's find a link containing StegoRSA
        stegorsa_link = page.get_by_role("link", name=re.compile("StegoRSA", re.IGNORECASE)).first
        if await stegorsa_link.count() > 0:
            print("Found StegoRSA link, clicking...")
            await stegorsa_link.click()
            await page.wait_for_load_state('networkidle')
            title_2 = await page.title()
            url_2 = page.url
            print(f"Title 2: {title_2}, URL 2: {url_2}")
        else:
            print("Could not find StegoRSA link by role")
            
        await browser.close()

import re
asyncio.run(main())
