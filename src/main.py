import random

from groq import Groq
from google import genai
from playwright.sync_api import sync_playwright

from src.config import GROQ_API_KEYS, GOOGLE_API_KEYS

from src.browser.playwright import init_page, javascript_load
from src.browser.google_login import google_login

from src.quiz.questions import *
from src.quiz.answer import *

from src.ai.text_solver import request_answer
from src.ai.image_solver import request_picture_answer

from src.quiz.util.question_util import stack_images, delete_images_directory, make_images_directory
from src.browser.utils.user_agents import USER_AGENTS

# Getting Initial URL
INIT_URL = str(input("[I] Enter URL: "))
print(f"[+] Using URL: {INIT_URL}")

# User Agent Selection
random_ua = random.choice(USER_AGENTS)
print(f"[+] Using User-Agent: {random_ua}")

# Playwright Initialization
playwright = sync_playwright().start()
print(f"[+] Playwright Synced")

# Initializing Page
browser, context, page = init_page(playwright, random_ua)
print(f"[+] Page Initialized")

# Opening Page, Waiting for First Question
print(f"[+] Opening Webpage")
page.goto(INIT_URL)

# Logging In via Google SSO
print(f"[+] Logging In...")
google_login(page)
print(f"[+] Logged In. Get the code.")
page.wait_for_selector(".question_text", timeout=300000)

# Start Process
print(f"[+] Ready to begin. Press Enter to Start")
input()
print(f"[+] Starting Program")

while True:
    try:
        # Clear Images Directory
        delete_images_directory()
        print("[+] Images Directory Cleared")

        # Groq Initialization (New Client Per Question)
        groq_api_key = random.choice(GROQ_API_KEYS)
        google_api_key = random.choice(GOOGLE_API_KEYS)
        text_client = Groq(api_key=groq_api_key)
        image_client = genai.Client(api_key=google_api_key)
        print(f"[+] AI Clients Initialized")
        print(f"[+] Groq API KEY: {GROQ_API_KEYS.index(groq_api_key) + 1}")
        print(f"[+] Gemini API KEY: {GOOGLE_API_KEYS.index(google_api_key) + 1}")

        # Waits for JS to load
        javascript_load(page)
        print(f"[+] Javascript Loaded")

        # Reading Question
        print(f"[+] Reading Question...")
        # page.wait_for_timeout(random.randint(4000, 7000))
        print(f"[+] Finished Reading Question")

        # Gets Question Information
        q_type = get_question_type(page)
        print(f"[+] Question Type: {q_type}")
        q = get_question(page)
        print(f"[+] Question: {q} \n")

        # Gets Answer Information
        a_type = get_answer_type(page)
        print(f"[+] Answer Type: {a_type}")
        if a_type == "radio" or a_type == "checkbox":
            a = get_answers(page)
            print(f"[+] Answer Choices: {a}")
        elif a_type == "text":
            a = ["Text Input Required"]
            print(f"[+] Text Input Required")

        if q_type:
            print(f"[+] Image found")
            image_dir = make_images_directory()
            print(f"[+] Made Image Directory")
            get_question_image(page)
            print(f"[+] Downloaded Images")
            stacked_path = stack_images(image_dir=image_dir, output="question.png")
            print(f"[+] Stacked Images")
            print(f"[+] Sending Google Gemini API Query with Image")
            out = request_picture_answer(image_client, q, a, a_type, stacked_path)
        else:
            print(f"[+] Sending Groq API Query")
            out = request_answer(text_client, q, a, a_type)

        print(f"[+] Correct Answer(s): {out}")
        if a_type == "text":
            print(f"[+] Typing Answer...")
            type_answer(page,(out[0]))
            print(f"[+] Answer Successfully Typed")
        else:
            print(f"[+] Clicking Answer...")
            click_answer(page,out)
            print(f"[+] Answer Successfully Clicked")

        print(f"[+] Clicking Next Button...")
        click_next(page)
        print(f"[+] Next Button Successfully Clicked")

    except ButtonNotFound:
        print(f"[+] Next Button Not Found")
        print(f"[+] Prepare to Submit")
        print(f"[+] Thank You! Submit and Press Enter to End the Program!")
        break

    except Exception as e:
        print("[-] Loop stopped")
        print(e)
        break

input()