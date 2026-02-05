def get_question_image(page, context):
    images = page.evaluate("() => window.quizHelpers.getQuestionImages()")
    for index, url in enumerate(images):
        response = context.request.get(url)
        with open(f"images/image{index}.png", "wb") as f:
            f.write(response.body())
