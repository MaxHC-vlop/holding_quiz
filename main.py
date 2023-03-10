import os
import re


def open_quiz_file(filename: str) -> str:
    with open(filename, "r", encoding='KOI8-R') as my_file:
        file_contents = my_file.read()

    return file_contents


def parse_file_contents(file_contents: str) -> dict:
    file_contents = file_contents.split('\n\n')

    number_questions = 1
    questions = {}

    for content in file_contents:
        content = content.strip()
        if not content:
            continue

        title, content = re.split(r':', content, maxsplit=1)
        content = content.strip().replace('\n', '')

        if re.search(r'\bВопрос', title):
            questions[number_questions] = {
                'question': content
            }

        elif re.search(r'\bОтвет', title):
            answer = {'answer': content}
            questions[number_questions].update(answer)

            number_questions += 1

    return questions


def main() -> None:
    folder = 'quiz-questions'
    files = os.listdir(folder)
    for filename in files:
        filepath = f'{folder}{os.sep}{filename}'
        file_contents = open_quiz_file(filepath)
        parse_file_contents(file_contents)


if __name__ == main():
    main()
