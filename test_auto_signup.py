import asyncio
import os
from playwright.async_api import async_playwright

agent_profile = os.path.expanduser(r"~\\.chrome_agent_profile")

async def signup_platform(page, name, start_url, github_btn_selector):
    print(f"\n[AUTO-SIGNUP] Starting {name}...")
    try:
        await page.goto(start_url, wait_until="networkidle", timeout=30000)
        print(f"[{name}] Landed on: {page.url}")
        
        # Click GitHub sign-in button if present
        btn = page.locator(github_btn_selector).first
        if await btn.count() > 0:
            print(f"[{name}] Clicking GitHub button...")
            await btn.click()
            await page.wait_for_timeout(5000)
        
        # Handle GitHub Authorize screen if it pops up
        auth_btn = page.locator("button:has-text('Authorize'), input[value*='Authorize'], button[name='authorize']").first
        if await auth_btn.count() > 0 and await auth_btn.is_visible():
            print(f"[{name}] Authorize button found! Clicking Authorize...")
            await auth_btn.click()
            await page.wait_for_timeout(8000)
            
        print(f"[{name}] Final URL: {page.url}")
        screenshot_path = os.path.join(os.getcwd(), f"auto_signup_{name}.png")
        await page.screenshot(path=screenshot_path)
        print(f"[{name}] Screenshot saved to {screenshot_path}")
        return True
    except Exception as e:
        print(f"[{name}] Error: {e}")
        return False

async def main():
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir=agent_profile,
            headless=False,
            channel="chrome"
        )
        page = context.pages[0] if context.pages else await context.new_page()
        
        # 1. Deno Deploy
        await signup_platform(
            page,
            "deno_deploy",
            "https://dash.deno.com/signin",
            "button:has-text('GitHub'), a:has-text('GitHub')"
        )
        
        # 2. Supabase
        await signup_platform(
            page,
            "supabase",
            "https://supabase.com/dashboard/sign-in",
            "button:has-text('GitHub'), a:has-text('GitHub')"
        )

        # 3. Render
        await signup_platform(
            page,
            "render",
            "https://dashboard.render.com/register",
            "button:has-text('GitHub'), a:has-text('GitHub')"
        )

        await context.close()

if __name__ == "__main__":
    asyncio.run(main())
