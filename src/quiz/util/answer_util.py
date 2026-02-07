import re

def convert_answer_list(answer_text, qtype="radio"):
    answer_text = answer_text.strip()
    if qtype == "radio":
        answer_text = re.sub(r'[^\d]', '', answer_text)
        if re.match(r'^\d$', answer_text):
            return [int(answer_text) - 1]
        else:
            return [0]
    elif qtype == "checkbox":
        answer_text = re.sub(r'[^\d,]', '', answer_text)
        if re.match(r'^\d(,\d)*$', answer_text):
            return [int(x) - 1 for x in answer_text.split(',')]
        else:
            return [0]
    elif qtype == "text":
        return [answer_text] if answer_text else [""]
    else:
        raise ValueError(f"Unknown question type: {qtype}")


def parse_answer(output, qtype):
    output = output.strip()
    if qtype == "radio":
        m = re.match(r'^\d$', output)
        return [int(output) - 1] if m else [0]
    elif qtype == "checkbox":
        m = re.match(r'^\d(,\d)*$', output)
        return [int(x) - 1 for x in output.split(',')] if m else [0]
    elif qtype == "text":
        return [output]
    else:
        raise ValueError(f"Unknown question type: {qtype}")