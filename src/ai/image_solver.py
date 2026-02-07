from google.genai import types
from src.ai.prompts.sys_context import *
from src.quiz.util.answer_util import *


def request_picture_answer(client, question, answer, qtype, image_path):
    if qtype == "radio":
        context = system_context_radio
    elif qtype == "checkbox":
        context = system_context_checkbox
    elif qtype == "text":
        context = system_context_textbox
    else:
        raise ValueError(f"Unknown question type: {qtype}")

    with open(image_path, "rb") as f:
        image_bytes = f.read()

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=[
            types.Content(
                role="user",
                parts=[
                    types.Part(text=f"""
                        System Instructions: {context}
                        Question: {question}
                        Answer Choices: {answer}
                    """),
                    types.Part(
                        inline_data=types.Blob(
                            mime_type="image/png",
                            data=image_bytes,
                        )
                    ),
                ],
            )
        ],
    )
    answer_text = response.text.strip()
    if qtype == "text":
        return answer_text
    return convert_answer_list(answer_text, qtype=qtype)
