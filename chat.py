import time
from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        print("Launching browser using saved profile...")
        browser = p.chromium.launch_persistent_context(
            user_data_dir="/home/sidd/project/merlin-cli-bridge/playwright_profile",
            headless=False, # Use headful since Cloudflare blocked headless
            args=["--disable-blink-features=AutomationControlled"]
        )
        page = browser.pages[0] if browser.pages else browser.new_page()
        page.goto("https://www.getmerlin.in/")
        
        print("Waiting 8 seconds for Cloudflare/Auth to load...")
        page.wait_for_timeout(8000)
        
        # Attempt to select Opus model
        print("Attempting to select Opus...")
        try:
            # Often it's in a dropdown. Let's look for "Opus" or "Claude 3 Opus"
            # It might require opening a menu first, but let's try a broad text search
            opus_locator = page.get_by_text("Opus", exact=False).first
            if opus_locator.is_visible():
                opus_locator.click()
                print("Clicked Opus option!")
            else:
                print("Opus option not visibly found, might already be selected or hidden.")
        except Exception as e:
            print(f"Could not select Opus: {e}")

        # Wait a moment after potential click
        page.wait_for_timeout(2000)

        print("Looking for chat input...")
        # Common locators for modern chat UI
        input_locators = [
            page.get_by_role("textbox"),
            page.locator("textarea"),
            page.locator("[contenteditable='true']")
        ]
        
        textbox = None
        for loc in input_locators:
            if loc.first.is_visible():
                textbox = loc.first
                break
                
        if textbox:
            print("Found input! Sending 'hi'...")
            textbox.fill("hi")
            page.keyboard.press("Enter")
            
            # Wait for response (hardcoded wait to ensure it finishes generating)
            print("Waiting 15 seconds for a valid answer to finish generating...")
            page.wait_for_timeout(15000)
            
            print("Sending 'which model are you'...")
            textbox.fill("which model are you")
            page.keyboard.press("Enter")
            
            print("Waiting 20 seconds for the second answer...")
            page.wait_for_timeout(20000)
            
            print("Done! Chat interaction finished.")
        else:
            print("Could not find the chat input box! Dumping HTML for debugging.")
            with open("failed_chat.html", "w", encoding="utf-8") as f:
                f.write(page.content())
                
        browser.close()

if __name__ == "__main__":
    main()
