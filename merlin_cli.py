import sys
import argparse
import time
from playwright.sync_api import sync_playwright

def login():
    print("[*] Booting Merlin Auth Window...")
    print("[*] Please log in with your Google account. Do NOT close the browser manually.")
    print("[*] The browser will automatically save your session and close once authenticated.")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=["--disable-blink-features=AutomationControlled"]
        )
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()
        page.goto("https://www.getmerlin.in/chat")
        
        print("[*] Waiting for successful authentication (detecting chat box)...")
        try:
            # Wait until the text input box is visible, meaning login succeeded
            page.wait_for_selector("[contenteditable='true'], textarea", timeout=300000) # 5 min timeout
            print("[+] Authentication detected!")
            
            # Save the state to auth.json
            context.storage_state(path="/home/sidd/project/merlin-cli-bridge/auth.json")
            print("[+] Saved auth state to auth.json.")
        except Exception as e:
            print(f"[-] Authentication timed out or failed: {e}")
        
        browser.close()

def main():
    parser = argparse.ArgumentParser(description="Merlin AI CLI Helper")
    subparsers = parser.add_subparsers(dest="command")
    
    login_parser = subparsers.add_parser("login", help="Log into Merlin and save session cookies")
    
    args = parser.parse_args()
    
    if args.command == "login":
        login()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
