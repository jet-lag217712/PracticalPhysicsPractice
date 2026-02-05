def get_question(page):
    return page.query_selector(".question_text").inner_text()

def get_question_type(page):
    return page.locator(".question_text img").count() > 0

def get_answers(page):
    return page.evaluate("() => window.quizHelpers.getAnswers()")

def get_answer_type(page):
    return page.locator(".question_input").first.get_attribute("type")
