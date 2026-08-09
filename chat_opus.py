import time
from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir="./playwright_profile",
            headless=False,
            args=["--disable-blink-features=AutomationControlled"]
        )
        page = browser.pages[0] if browser.pages else browser.new_page()
        
        print("Navigating directly to chat interface...")
        page.goto("https://www.getmerlin.in/chat")
        
        print("Waiting 8 seconds for page to load...")
        page.wait_for_timeout(8000)
        
        # Click the model dropdown (currently showing GPT 5.5 based on screenshot)
        print("Looking for model selector dropdown (GPT 5.5)...")
        try:
            model_dropdown = page.get_by_text("GPT 5.5", exact=False).first
            if model_dropdown.is_visible():
                model_dropdown.click()
                print("Clicked model dropdown!")
                page.wait_for_timeout(2000)
                
                # Now select Opus
                opus_option = page.get_by_text("Opus", exact=False).first
                if opus_option.is_visible():
                    opus_option.click()
                    print("Successfully clicked Opus option!")
                else:
                    print("Could not find Opus in the dropdown menu.")
            else:
                print("Could not find 'GPT 5.5' button.")
        except Exception as e:
            print(f"Error selecting model: {e}")

        page.wait_for_timeout(2000)

        print("Finding chat input...")
        # Common locators
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
            
            print("Waiting 15 seconds for Opus to finish generating...")
            page.wait_for_timeout(15000)
            
            print("Sending 'which model are you'...")
            textbox.fill("which model are you")
            page.keyboard.press("Enter")
            
            print("Waiting 20 seconds for final answer...")
            page.wait_for_timeout(20000)
            
            print("Done! Interaction complete.")
        else:
            print("Could not find chat input.")
            
        browser.close()

if __name__ == "__main__":
    main()
