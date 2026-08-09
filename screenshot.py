import time
from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir="/home/sidd/project/merlin-cli-bridge/playwright_profile",
            headless=False,
            args=["--disable-blink-features=AutomationControlled"]
        )
        page = browser.pages[0] if browser.pages else browser.new_page()
        page.goto("https://www.getmerlin.in/")
        
        print("Waiting 10 seconds for the app to load fully...")
        page.wait_for_timeout(10000)
        
        print("Taking screenshot...")
        page.screenshot(path="ui_screenshot.png", full_page=True)
            
        browser.close()
        print("Done.")

if __name__ == "__main__":
    main()
