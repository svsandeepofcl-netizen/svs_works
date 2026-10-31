from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        channel="chrome",  # use real installed Chrome
        args=[
            '--disable-blink-features=AutomationControlled',
            '--no-sandbox',
            '--disable-dev-shm-usage',
            '--disable-infobars',
        ]
    )
    context = browser.new_context(
        viewport={'width': 1366, 'height': 768},
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    )
    stealth = Stealth()
    page = context.new_page()
    stealth.apply_stealth_sync(page)
    
    # Try visiting homepage first or login page
    page.goto('https://www.naukri.com/nlogin/login', wait_until='networkidle', timeout=60000)
    page.wait_for_timeout(3000)
    print("Page URL:", page.url)
    print("Page Title:", page.title())
    
    username_el = page.query_selector("input#usernameField, input[placeholder*='Email'], input[placeholder*='Username']")
    password_el = page.query_selector("input#passwordField, input[type='password']")
    submit_btn = page.query_selector("button[type='submit'], .loginButton")
    
    print("Found username field:", bool(username_el))
    print("Found password field:", bool(password_el))
    print("Found submit button:", bool(submit_btn))
    
    page.screenshot(path="d:/Sandeep/Projects/Naukri/login_test2.png")
    browser.close()
