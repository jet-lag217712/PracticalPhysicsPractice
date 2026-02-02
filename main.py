import os
import time

from groq import Groq
from dotenv import load_dotenv

from playwright.sync_api import sync_playwright

# Gets Environment Variables
load_dotenv()
API_KEY = os.getenv("API_KEY")
INIT_URL = os.getenv("INIT_URL")
DEST_URL = os.getenv("DEST_URL")

#Initalize Groq
client = Groq(api_key=API_KEY)

#Initalize Playwright
playwright = sync_playwright().start()
browser = playwright.chromium.launch(headless=False)
page = browser.new_page(viewport={"width": 1280, "height": 720})

def request_answer(question,answer):
    output = client.chat.completions.create(
        model="moonshotai/kimi-k2-instruct-0905",
        messages=[
            {
                "role": "system",
                "content": "Output ONLY the correct answer NUMBER. This should be the output structure (do not output curly brackets): {1-4}"
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
        max_completion_tokens=512,
        top_p=1,
        stream=False,
        stop=None
    )
    answer = output.choices[0].message.content
    answer = int(answer)
    return answer-1

def get_question():
    page.wait_for_selector(".question_text")
    question = page.query_selector(".question_text").inner_text()
    return question

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
    clean_answers = [ans.strip() for ans in answers_list]
    return clean_answers

page.goto(INIT_URL)
page.wait_for_selector(".question_text", timeout=120_000)
print("ready, on countdown")
page.wait_for_timeout(30000)
print('ready, hide the chrome tab')

while True:
    try:
        q = get_question()
        a = get_answers()
        out = request_answer(q, a)
        print(f'Answer Found! {a[out]}')

        page.wait_for_timeout(1000)

        page.evaluate("""
        (out) => {
            let answers = document.querySelectorAll(".answer");
            let nextButton = document.querySelector(".submit_button.next-question");
            
            let answerlist = [];
            for (let i = 0; i < answers.length; i++) {
                let el = answers[i].children[0]?.children[1];
                if (el) answerlist.push(el);
            }
            
            answerlist[out].click();

            if (out < 0 || out >= answerlist.length) {
                throw new Error(`Invalid answer index: ${out}, length: ${answerlist.length}`);
            }
            
            if (!nextButton) {
                throw new Error("Next button not found");
            }

            nextButton.click();
        }
        """, out)
    except Exception as e:
        print("Loop stopped")
        print(e)
        break

time.sleep(600)