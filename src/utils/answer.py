import re

import re

def convert_answer_list(answer_text, qtype="radio"):
    answer_text = re.sub(r'[^\d,]', '', answer_text.strip())

    if qtype == "radio":
        if re.match(r'^\d$', answer_text):
            return [int(answer_text) - 1]
        else:
            return [3]  # fallback if invalid
    elif qtype == "checkbox":
        if re.match(r'^\d(,\d)*$', answer_text):
            return [int(x) - 1 for x in answer_text.split(',')]
        else:
            return [3]  # fallback if invalid


def parse_answer(output, type):
    if type == "radio":
        m = re.match(r'^\d$', output)
        return int(output) if m else 3
    else:  # checkbox
        m = re.match(r'^\d(,\d)*$', output)
        return [int(x) for x in output.split(',')] if m else [3]