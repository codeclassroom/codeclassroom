"""All Plagiarism Utilities"""
import os
from typing import List

import plagcheck

from app.models import Assignment, Classroom, Professor, Question, Solution


class moss_data_dict(dict):
    """Typing for Moss Data"""

    submission1: int
    submission2: int
    question: int
    percentage_sub1: int
    percentage_sub2: int
    no_of_lines_matched: int
    lines_matched: List[List[str]]


def format_lang(language: str):
    if language in ['Python2', 'Python3', 'python']:
        return "python"
    elif language in ['C++', 'c++', 'cpp']:
        return "cc"
    elif language in ['Java', 'java']:
        return "java"
    elif language in ['c', 'C']:
        return "c"
    return None


def extract_ids(path1, path2):
    """Extract Solution & Quesiton IDs from submission file paths"""
    solution1 = int(os.path.basename(path1).split('_')[1])
    solution2 = int(os.path.basename(path2).split('_')[1])
    question = int(os.path.basename(path1).split('_')[0])

    return solution1, solution2, question


def codesim(assignment):
    """The CodeClassroom Plagiarism Detector"""
    classroom = Assignment.objects.filter(pk=assignment).values('classroom')[0]
    lang = Assignment.objects.only(
        'language').get(pk=assignment).language
    professor = Classroom.objects.filter(
        pk=classroom['classroom']).values('professor')[0]
    moss_user_id = Professor.objects.only(
        'moss_id').get(pk=professor['professor']).moss_id
    questions = Question.objects.filter(check_plagiarism=True)

    if moss_user_id != "":
        moss = plagcheck.check(format_lang(lang), moss_user_id)
    else:
        # if professor has no moss_id, use from env
        moss_user_id = os.environ['MOSS_ID']
        moss = plagcheck.check(format_lang(lang), moss_user_id)

    submissions = Solution.objects.filter(
        assignment__id=assignment, question__in=questions
    )

    for submission in submissions:
        moss.addFile(submission.submission.path)

    moss.submit()

    results = moss.getResults()

    moss_data = []

    for result in results:
        path1 = result['file1']
        path2 = result['file2']
        sub1, sub2, question = extract_ids(path1, path2)
        question_title = Question.objects.get(pk=question).title

        result_dict = moss_data_dict(
            submission1=sub1,
            submission2=sub2,
            question_id=question,
            question_title=question_title,
            percentage_sub1=result['percentage_file1'],
            percentage_sub2=result['percentage_file2'],
            no_of_lines_matched=result['no_of_lines_matched'],
            lines_matched=result['lines_matched'],
        )

        moss_data.append(result_dict)

    return moss_data
