def get_question(page):
    question = page.query_selector(".question_text").inner_text()
    return question.strip()

def get_question_image(page):
    images = page.evaluate("""
        () => {
            const container = document.querySelector(".question_text");
            if (!container) return [];

            const images = container.querySelectorAll("img");
            return Array.from(images).map(img => img.src);
        }
    """)
    for index, url in enumerate(images):
        response = page.context.request.get(url)
        with open(f"images/image{index}.png", "wb") as f:
            f.write(response.body())

def get_question_type(page):
    return page.locator(".question_text img").count() > 0