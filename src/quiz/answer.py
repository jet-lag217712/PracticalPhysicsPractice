from playwright.sync_api import TimeoutError
from src.utils.exceptions import *

def get_answers(page):
    answers = page.locator(".answer").all()
    answer_list = []
    for a in answers:
        text = a.inner_text().strip()
        answer_list.append(text)
    return answer_list


def get_answer_type(page):
    return page.locator(".question_input").first.get_attribute("type")

def click_answer(page, out):
    answers = page.locator(".answer").all()
    if not answers:
        raise AnswersNotFound()
    for index in out:
        if index < 0 or index >= len(answers):
            raise InvalidAnswerIndex()
        ans = answers[index]
        input_el = ans.locator("input[type=checkbox], input[type=radio]")
        label_el = ans.locator(".answer_label")
        if input_el.count() == 0 or label_el.count() == 0:
            raise AnswerElementNotFound()
        try:
            checked = input_el.is_checked()
        except TimeoutError:
            raise AnswerStateReadFailed()
        if not checked:
            try:
                label_el.click(timeout=1500)
            except TimeoutError:
                raise AnswerClickFailed()

def type_answer(page, out):
    page.locator(".question_input").fill(out)

def click_next(page):
    try:
        page.locator(".submit_button.next-question").click(timeout=1000)
    except:
        raise ButtonNotFound()   # Exception