from src.utils.images import make_images, stack_images

def get_question(page):
    return page.query_selector(".question_text").inner_text()

def get_question_image(page):
    images = page.evaluate("() => window.quizHelpers.getQuestionImages()")
    for index, url in enumerate(images):
        response = page.context.request.get(url)
        with open(f"images/image{index}.png", "wb") as f:
            f.write(response.body())

def get_question_type(page):
    return page.locator(".question_text img").count() > 0