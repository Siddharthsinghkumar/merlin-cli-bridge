from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir="/home/sidd/project/merlin-cli-bridge/playwright_profile",
            headless=False,
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-infobars",
                "--window-size=1920,1080"
            ],
            viewport={"width": 1920, "height": 1080}
        )
        page = browser.pages[0] if browser.pages else browser.new_page()
        Stealth().apply_stealth_sync(page)
        
        print("Opening browser...")
        page.goto("https://www.getmerlin.in/")
        
        print("\n========================================================")
        print("Browser opened! Please log in to Merlin AI now.")
        print("Close the browser window yourself when you are completely done.")
        print("========================================================\n")
        
        try:
            # Wait for the user to manually close the browser
            page.wait_for_event("close", timeout=0)
        except Exception:
            pass
        
        print("Browser closed. Verifying login session...")
        browser.close()
        
        # Re-launch context headlessly to verify session
        with p.chromium.launch_persistent_context(
            user_data_dir="/home/sidd/project/merlin-cli-bridge/playwright_profile",
            headless=True,
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            args=["--disable-blink-features=AutomationControlled"]
        ) as verify_browser:
            verify_page = verify_browser.pages[0] if verify_browser.pages else verify_browser.new_page()
            Stealth().apply_stealth_sync(verify_page)
            
            try:
                verify_page.goto("https://www.getmerlin.in/chat", timeout=20000)
                chat_box = verify_page.locator("[contenteditable='true'], textarea, div[role='textbox']")
                chat_box.wait_for(state="visible", timeout=10000)
                print("\n✅ LOGIN SUCCESSFUL: Chat input box detected! Your session is verified and active.\n")
            except Exception:
                print("\n❌ LOGIN FAILED or UNVERIFIED: Chat input box not detected. The session might be unauthenticated or blocked by Turnstile.\n")

if __name__ == "__main__":
    main()
