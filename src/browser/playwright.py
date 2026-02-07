def init_page(playwright, user_agent: str):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(
        user_agent=user_agent,
        viewport={"width": 1280, "height": 720},
        locale="en-US",
        timezone_id="America/Los_Angeles"
    )
    page = context.new_page()
    page.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });
    """)
    return browser, context, page

def javascript_load(page):
    page.wait_for_selector(".question_text")
