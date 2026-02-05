import os
import time
import random
import base64

from PIL import Image
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

def request_picture_answer(question, answer, type, image_path):
    if type == 'radio':
        system_content = (
            "Output ONLY the correct answer NUMBER.\n"
            "This should be the output structure (do not output curly brackets): {1-4}\n"
            "You are to only select ONE option."
        )
    elif type == 'checkbox':
        system_content = (
            "Output ONLY the correct answer NUMBER.\n"
            "This should be the output structure (do not output curly brackets): {1, 2, 3, 4}\n"
            "You are to only select ALL CORRECT options."
        )

    with open(image_path, "rb") as f:
        image_base64 = base64.b64encode(f.read()).decode("utf-8")

    output = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {
                "role": "system",
                "content": system_content
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"""
                            Question: {question}
                            Answer Choices: {answer}
                            """
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{image_base64}"
                        }
                    }
                ]
            }
        ],
        temperature=1,
        max_completion_tokens=256,
        top_p=1,
        stream=False
    )

    answer_text = output.choices[0].message.content.strip()

    if ',' in answer_text:
        answer_indices = [int(x.strip()) - 1 for x in answer_text.split(',')]
    else:
        answer_indices = [int(answer_text) - 1]

    return answer_indices


def request_answer(question, answer, type):
    if type == 'radio':
        system_content = """
        Output ONLY the correct answer NUMBER. If you are unsure, output 3.
        This should be the output structure (do not output curly brackets): {1-4}
        You are to only select ONE option"
        """
    elif type == 'checkbox':
        system_content = """
        Output ONLY the correct answer NUMBER. If you are unsure, output 3.
        This should be the output structure (do not output curly brackets): {1, 2, 3, 4}
        You are to only select ALL CORRECT options"
        """

    output = client.chat.completions.create(
        model="moonshotai/kimi-k2-instruct-0905",
        messages=[
            {
                "role": "system",
                "content": (
                    system_content
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
    answer_text = output.choices[0].message.content.strip()
    if ',' in answer_text:
        answer_indices = [int(x.strip()) - 1 for x in answer_text.split(',')]
    else:
        answer_indices = [int(answer_text) - 1]
    return answer_indices

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
    """, path="web_helper.js")
    return browser, context, page

def stack_images(image_dir="images", output="super_image.png"):
    files = sorted(
        f for f in os.listdir(image_dir)
        if f.lower().endswith((".png", ".jpg", ".jpeg"))
    )

    images = [Image.open(os.path.join(image_dir, f)) for f in files]

    max_width = max(img.width for img in images)
    resized = [
        img.resize((max_width, int(img.height * max_width / img.width)))
        for img in images
    ]

    total_height = sum(img.height for img in resized)
    final_img = Image.new("RGB", (max_width, total_height))

    y = 0
    for img in resized:
        final_img.paste(img, (0, y))
        y += img.height

    final_img.save(output)
    return output

def javascript_load():
    page.wait_for_selector(".question_text")

def get_question():
    return page.query_selector(".question_text").inner_text()

def get_question_type():
    return page.locator(".question_text img").count() > 0

def get_question_image():
    images = page.evaluate("() => window.quizHelpers.getQuestionImages()")
    for index, url in enumerate(images):
        response = context.request.get(url)
        with open(f"images/image{index}.png", "wb") as f:
            f.write(response.body())

def delete_images(image_dir="images"):
    if not os.path.exists(image_dir):
        return

    for filename in os.listdir(image_dir):
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            file_path = os.path.join(image_dir, filename)
            if filename != "question.png" and os.path.isfile(file_path):
                os.remove(file_path)

def get_answers():
    return page.evaluate("() => window.quizHelpers.getAnswers()")

def get_answer_type():
    return page.locator(".question_input").first.get_attribute("type")

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
input(f"[I] ")
print(f"[+] Starting Program")

while True:
    try:
        # Waits for JS to load
        javascript_load()

        # Gets Question Information
        q_type = get_question_type()
        q = get_question()
        print(f"[Q] Question: {q} \n")

        # Gets Answer Information
        a_type = get_answer_type()
        a = get_answers()
        print(f"[AL] Answer: {a} \n")

        if q_type:
            print("[+] Image found")
            get_question_image()
            stack_images("images", "question.png")
            out = request_picture_answer(q, a, a_type, "question.png")

        out = request_answer(q, a, a_type)

        print(f"[AC] Correct Answer(s): {out}")

        # Random Wait for Realism
        page.wait_for_timeout(random.randint(800, 1400))

        # Clicks Answer Button and Next
        page.evaluate("window.quizHelpers.clickAnswerAndNext", out)

        # Finishes Loop
        print(f"[+] Success")

        # 'Reading Question'
        page.wait_for_timeout(random.randint(4000, 7000))

    except Exception as e:
        print("[-] Loop stopped")
        print(e)
        break

time.sleep(600)
