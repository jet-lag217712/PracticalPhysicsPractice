system_context_radio = """
    Return one answer number only.
    Format: DIGIT
    No text, spaces, reasoning, or newlines
    If unsure, return 3. 
    """

system_context_checkbox = """
    Return all correct answer numbers.
    Format: DIGIT or DIGIT,DIGIT
    Numbers only. No spaces, reasoning, newlines or text.
    If unsure, return 3.
    """

system_context_textbox = """
    Return the correct answer. It should be formatable as a string.
    Format: STRING STRING STRING
    No reasoning, or newlines. Return only the correct answer, as text
    If unsure, return 3.
    """