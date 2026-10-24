import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9223")
        context = browser.contexts[0]
        
        # Fast URL match without calling await page.title()
        pin_page = None
        for page in context.pages:
            if "pinterest" in page.url.lower():
                pin_page = page
                break
                
        if not pin_page:
            print("No existing Pinterest page found by URL, opening new tab...")
            pin_page = await context.new_page()
            await pin_page.goto("https://www.pinterest.co.uk/", wait_until="domcontentloaded")
            await asyncio.sleep(3)

        print(f"Pinterest Page URL: {pin_page.url}")
        title = await pin_page.title()
        print(f"Pinterest Page Title: {title}")
        
        # Check login state
        is_logged_in = await pin_page.evaluate("""() => {
            const hasProfile = !!document.querySelector('div[data-test-id="header-profile"], a[href*="/cctv_services"], [aria-label*="Profile"]');
            const hasLogin = !!document.querySelector('div[data-test-id="simple-login-button"], button[aria-label="Log in"]');
            return { hasProfile, hasLogin, bodySnippet: document.body.innerText.slice(0, 200) };
        }""")
        print("Login status:", is_logged_in)
        
        await pin_page.screenshot(path="pinterest_live_screen.png")
        print("Screenshot saved to pinterest_live_screen.png")

if __name__ == "__main__":
    asyncio.run(main())
