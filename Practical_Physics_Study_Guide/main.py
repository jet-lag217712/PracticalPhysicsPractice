import os
import time
import random

from groq import Groq
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv()
API_KEY = os.getenv("API_KEY")

USER_AGENTS = [
    # Chrome - Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",

    # Chrome - macOS
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",

    # Firefox - Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) "
    "Gecko/20100101 Firefox/122.0",

    # Edge - Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",

    # Chrome - Linux
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
]

def request_answer(question, answer):
    output = client.chat.completions.create(
        model="moonshotai/kimi-k2-instruct-0905",
        messages=[
            {
                "role": "system",
                "content": (
                    "Output ONLY the correct answer NUMBER. "
                    "This should be the output structure (do not output curly brackets): {1-4}"
                )
            },
            {
                "role": "user",
                "content": f"""
                Question: {question}
                Answer Choices: {answer}
                """
            }
        ],
        temperature=1,
        max_completion_tokens=256,
        top_p=1,
        stream=False
    )
    answer_index = int(output.choices[0].message.content)
    return answer_index - 1

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

    page.add_init_script(path="web_helper.js")

    return browser, context, page

def get_question():
    page.wait_for_selector(".question_text")
    return page.query_selector(".question_text").inner_text()

def get_answers():
    return page.evaluate("() => window.quizHelpers.getAnswers()")

INIT_URL = str(input("[I] Enter URL: "))

# Groq Initialization
client = Groq(api_key=API_KEY)

# User Agent Selection
random_ua = random.choice(USER_AGENTS)

# Playwright Initialization
playwright = sync_playwright().start()
browser, context, page = init_page(playwright, random_ua)

print(f"[+] Using URL: {INIT_URL}")
print(f"[+] Using User-Agent: {random_ua}")

print(f"[+] Opening Webpage, Waiting for Start")
page.goto(INIT_URL)

page.wait_for_selector(".question_text", timeout=300000)

print(f"[+] Ready to begin. Press Enter to Start")
input("[I] ")

print(f"[+] Starting Program")

while True:
    try:
        q = get_question()
        print(f"[Q] Question: {q} \n")
        a = get_answers()
        print(f"[AL] Answer: {a} \n")

        out = request_answer(q, a)
        print(f"[AC] Correct Answer: {a[out]}")

        page.wait_for_timeout(random.randint(800, 1400))

        page.evaluate("(out) => window.quizHelpers.clickAnswerAndNext(out)", out)

        print(f"[+] Success")
        page.wait_for_timeout(random.randint(8000, 14000))

    except Exception as e:
        print("[-] Loop stopped")
        print(e)
        break

time.sleep(600)
