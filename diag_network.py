import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(
            user_data_dir="/home/sidd/project/merlin-cli-bridge/chrome_profile",
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
            ]
        )
        
        page = await browser.new_page()
        
        # Inject fetch override to capture stream chunks
        js_override = """
        const originalFetch = window.fetch;
        window.fetch = async function(...args) {
            const url = typeof args[0] === 'string' ? args[0] : args[0].url;
            if (url && url.includes('arcane/api/v2/thread/unified')) {
                const response = await originalFetch(...args);
                const clone = response.clone();
                const reader = clone.body.getReader();
                const decoder = new TextDecoder("utf-8");
                (async function readStream() {
                    while (true) {
                        const { done, value } = await reader.read();
                        if (done) break;
                        const chunkStr = decoder.decode(value, { stream: true });
                        console.log("MERLIN_CHUNK: " + chunkStr);
                    }
                })();
                return response;
            }
            return originalFetch(...args);
        };
        """
        await page.add_init_script(js_override)
        page.on("console", lambda msg: print(f"{msg.text}") if "MERLIN_CHUNK" in msg.text else None)
        
        await page.goto("https://www.getmerlin.in/chat")
        await page.wait_for_timeout(5000)
        
        # Auto-fill and send a prompt
        print("Sending prompt...")
        textbox = page.locator("[contenteditable='true']").first
        if await textbox.is_visible():
            await textbox.fill("Write a long poem about the ocean.")
            # Wait for button to be enabled
            await page.wait_for_timeout(1000)
            
            # Find send button by role or aria-label
            send_btn = page.locator("button[type='submit'], button[aria-label='Send message'], button:has-text('Send')").first
            if await send_btn.count() > 0 and await send_btn.is_visible():
                await send_btn.click(force=True)
                print("Clicked Send button.")
            else:
                await page.keyboard.press("Enter")
                print("Pressed Enter.")
            
        print("Waiting 15 seconds for stream to finish...")
        await page.wait_for_timeout(15000)
        
        await page.screenshot(path="diag_screenshot.png")
        print("Screenshot saved to diag_screenshot.png")
        
        await browser.close()

async def handle_request(request):
    try:
        if request.method == "POST":
            print(f"[POST] -> {request.url}")
    except Exception:
        pass

async def handle_response(response):
    try:
        content_type = response.headers.get("content-type", "")
        if "text/event-stream" in content_type:
            print(f"[STREAM] Intercepted {content_type} from {response.url}")
    except Exception as e:
        pass

if __name__ == "__main__":
    asyncio.run(main())
