from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir="/home/sidd/project/merlin-cli-bridge/playwright_profile",
            headless=True,
            args=["--disable-blink-features=AutomationControlled"]
        )
        print("Exporting storage state (cookies/auth) to auth.json...")
        browser.storage_state(path="auth.json")
        browser.close()
        print("Done!")

if __name__ == "__main__":
    main()
