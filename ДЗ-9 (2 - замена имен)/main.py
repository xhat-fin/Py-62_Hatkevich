import re

regex = r"[А-ЯЁ][а-яё]+(?:-[А-ЯЁ][а-яё]+)?\s+[А-ЯЁ][а-яё]+\s+[А-ЯЁ][а-яё]+"

with open('file.txt', 'r+') as f:
    text = f.read()
    new_text = re.sub(regex, 'N', text, count=1)

with open('file.txt', "w") as f:
    f.write(new_text)