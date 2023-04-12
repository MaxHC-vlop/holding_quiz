import os
import re

from environs import Env


def open_quiz_file(filename: str) -> str:
    with open(filename, "r", encoding='KOI8-R') as file:
        file_content = file.read()

    return file_content


def parse_file_contents(element: str) -> dict:
    question_key = r'\bВопрос'
    answer_key = r'\bОтвет'

    title, content = re.split(r':', element, maxsplit=1)
    content = content.strip().replace('\n', '')

    if re.search(question_key, title):
        return {'question': content}

    elif re.search(answer_key, title):
        return {'answer': content}


def fetch_questions() -> dict:
    env = Env()
    env.read_env()

    folder = env.str('FOLDER', 'quiz-questions')
    files = os.listdir(folder)
    number_questions = 1
    questions = {}
    for filename in files:
        filepath = f'{folder}{os.sep}{filename}'
        file_contents = open_quiz_file(filepath)

        file_contents = file_contents.split('\n\n')
        for content in file_contents:
            content = content.strip()
            element_content = parse_file_contents(content)
            if 'question' in element_content:
                questions[number_questions] = element_content
            elif 'answer' in element_content:
                questions[number_questions].update(element_content)
                number_questions += 1

    return questions


fetch_questions()
