from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir="./playwright_profile",
            headless=True,
            args=["--disable-blink-features=AutomationControlled"]
        )
        page = browser.pages[0] if browser.pages else browser.new_page()
        page.goto("https://www.getmerlin.in/")
        
        # Wait for the page to fully load
        page.wait_for_timeout(8000)
        
        page.screenshot(path="./screenshot1.png", full_page=True)
        with open("./page.html", "w") as f:
            f.write(page.content())
            
        print("Exploration complete.")
        browser.close()

if __name__ == "__main__":
    main()
