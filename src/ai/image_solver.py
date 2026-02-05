import base64

from src.utils.sys_context import system_context_radio, system_context_checkbox
from src.utils.answer import *

def request_picture_answer(client, question, answer, type, image_path):
    if type == 'radio':
        context = system_context_radio
    elif type == 'checkbox':
        context = system_context_checkbox

    with open(image_path, "rb") as f:
        image_base64 = base64.b64encode(f.read()).decode("utf-8")

    output = client.chat.completions.create(
        model="meta-llama/llama-4-maverick-17b-128e-instruct",
        messages=[
            {
                "role": "system",
                "content": context
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"""
                            Question: {question}
                            Answer Choices: {answer}
                            """
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{image_base64}"
                        }
                    }
                ]
            }
        ],
        temperature=1,
        max_completion_tokens=256,
        top_p=1,
        stream=False
    )

    answer_text = output.choices[0].message.content.strip()
    return convert_answer_list(answer_text, qtype=type)
