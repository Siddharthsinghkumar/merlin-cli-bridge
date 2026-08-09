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
        
        print("Going to Chat interface...")
        page.goto("https://www.getmerlin.in/chat") # Try direct chat URL
        page.wait_for_timeout(5000)
        
        # If we are still on the landing page or get a 404, try clicking the Chat link
        if "chat" not in page.url:
            print("Direct URL failed, clicking 'Chat' from top nav...")
            page.goto("https://www.getmerlin.in/")
            page.wait_for_timeout(3000)
            page.get_by_role("link", name="Chat").click()
            page.wait_for_timeout(5000)

        print("Taking screenshot of Chat UI...")
        page.screenshot(path="chat_ui.png", full_page=True)
        
        # Also dump HTML to find selectors precisely
        with open("chat_ui.html", "w", encoding="utf-8") as f:
            f.write(page.content())
            
        browser.close()
        print("Done.")

if __name__ == "__main__":
    main()
