import time
import random

from groq import Groq
from playwright.sync_api import sync_playwright

from config import API_KEYS
from utils.user_agents import USER_AGENTS
from browser.playwright import init_page, javascript_load
from quiz.questions import *
from quiz.images import *
from ai.text_solver import request_answer
from ai.image_solver import request_picture_answer
from utils.images import stack_images, delete_images, make_images

INIT_URL = str(input("[I] Enter URL: "))

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
        # Groq Initialization (New Client Per Question)
        api_key = random.choice(API_KEYS)
        client = Groq(api_key=api_key)
        print(f"Using API KEY: {api_key}")

        # Waits for JS to load
        javascript_load(page)

        # Gets Question Information
        q_type = get_question_type(page)
        q = get_question(page)
        print(f"[Q] Question: {q} \n")

        # Gets Answer Information
        a_type = get_answer_type(page)
        a = get_answers(page)
        print(f"[AL] Answer: {a} \n")

        if q_type:
            print("[+] Image found")
            image_dir = make_images()
            get_question_image(page, context)
            stacked_path = stack_images(image_dir=image_dir, output="question.png")
            out = request_picture_answer(client, q, a, a_type, stacked_path)
            delete_images()

        out = request_answer(client, q, a, a_type)

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
