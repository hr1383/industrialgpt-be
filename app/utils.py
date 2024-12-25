def get_email_text(result):
    messages = (result['message']['artifact']['messages'])
    text = "Here is a transcript of the call \n"
    for m in messages:
        # print(m)
        if (m['role'] !='system'):
            text += m['role'] +":"+m['message'] +"\n"
    print(text)
    return text
