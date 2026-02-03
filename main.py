import os
import time
import random

from groq import Groq
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv()
API_KEY = os.getenv("API_KEY")
INIT_URL = os.getenv("INIT_URL")
DEST_URL = os.getenv("DEST_URL")

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

random_ua = random.choice(USER_AGENTS)
print(f"[+] Using User-Agent: {random_ua}")

client = Groq(api_key=API_KEY)

playwright = sync_playwright().start()
browser = playwright.chromium.launch(headless=False)

context = browser.new_context(
    user_agent=random_ua,
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

def get_question():
    page.wait_for_selector(".question_text")
    return page.query_selector(".question_text").inner_text()

def get_answers():
    answers_list = page.evaluate("""
        () => {
            let answers = document.querySelectorAll(".answer");
            let answerlist = [];
            for (let i = 0; i < answers.length; i++) {
                answerlist[i] = answers[i].children[0].children[1];
            }
            return answerlist.map(el => el.textContent);
        }
    """)
    return [ans.strip() for ans in answers_list]

page.goto(INIT_URL)
page.wait_for_selector(".question_text", timeout=300000)

print("ready, on countdown")
page.wait_for_timeout(15000)
print("ready, hide the chrome tab")

while True:
    try:
        q = get_question()
        print(q)
        a = get_answers()
        print(a)

        out = request_answer(q, a)
        print(a[out])

        page.wait_for_timeout(random.randint(800, 1400))

        page.evaluate("""
        (out) => {
            let answers = document.querySelectorAll(".answer");
            let nextButton = document.querySelector(".submit_button.next-question");
            let answerlist = [];
            
            for (let i = 0; i < answers.length; i++) {
                let el = answers[i].children[0]?.children[1];
                if (el) answerlist.push(el);
            }

            if (out < 0 || out >= answerlist.length) {
                throw new Error(`Invalid answer index: ${out}`);
            }
            
            answerlist[out].click();

            if (!nextButton) {
                throw new Error("Next button not found");
            }

            nextButton.click();
        }
        """, out)

        print("success, next page")
        page.wait_for_timeout(random.randint(8000, 14000))

    except Exception as e:
        print("Loop stopped")
        print(e)
        break

time.sleep(600)
