"""All Moss Services here"""
import plagcheck
from app.models import Assignment, Professor, Solution, Question, Classroom, PlagResult
import os
from typing import List


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
    """Extract Solution & Quesiton IDs from submission file path"""
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
        # if progessor has no moss_id, use from env
        moss_user_id = os.environ['MOSS_ID']
        moss = plagcheck.check(format_lang(lang), moss_user_id)

    submissions = Solution.objects.filter(assignment__id=assignment, question__in=questions)

    for submission in submissions:
        moss.addFile(submission.submission.path)

    moss.submit()

    results = moss.getResults()

    # the list contains the data that will be the response
    moss_data = []

    for result in results:
        path1 = result['file1']
        path2 = result['file2']
        sub1, sub2, question = extract_ids(path1, path2)

        result_dict = moss_data_dict(
            submission1=sub1,
            submission2=sub2,
            question=question,
            percentage_sub1=result['percentage_file1'],
            percentage_sub2=result['percentage_file2'],
            no_of_lines_matched=result['no_of_lines_matched'],
            lines_matched=result['lines_matched'],
        )

        moss_data.append(result_dict)

    return moss_data

    # plaglist = []

    # for result in moss.getResults():
    #     path1 = result['file1']
    #     path2 = result['file2']
    #     sub1, sub2, question = extract_ids(path1, path2)

    #     plaglist.append(PlagResult(
    #             question=question,
    #             solution_1=sub1,
    #             solution_2=sub2,
    #             perc1=result['precentage_file1'],
    #             perc2=result['precentage_File2'],
    #             lines_matched=result['lines_matched'],
    #             no_of_lines_matched=result['no_of_lines_matched']
    #         ))

    # PlagResult.objects.bulk_create(plaglist)
