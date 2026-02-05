import os
import shutil

from PIL import Image

def make_images(question_dir="images"):
    os.makedirs(question_dir, exist_ok=True)
    return question_dir

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

def delete_images():
    if os.path.exists("images"):
        shutil.rmtree("images")
    os.remove("question.png")