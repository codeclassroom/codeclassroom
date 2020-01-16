"""All Moss Services here"""
import plagcheck
from app.models import Assignment, Professor, Solution, Question, Classroom
import os


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


def plagiarism(assignment):
    """TODO:
    - Get all solutions with speified assignent id
    - Order Soluions based on questions
    - Submit seggregated results one-by-one (all soltuions for 1 question)
    - Obtain Moss results and insert them into PlagResult Table.
    - Return a nested JSON in response
    """
    classroom = Assignment.objects.filter(pk=assignment).values('classroom')[0]
    lang = Assignment.objects.only(
        'language').get(pk=assignment).language
    professor = Classroom.objects.filter(
        pk=classroom['classroom']).values('professor')[0]
    moss_user_id = Professor.objects.only(
        'moss_id').get(pk=professor['professor']).moss_id

    if moss_user_id != "":
        moss = plagcheck.check(format_lang(lang), moss_user_id)
    else:
        # if progessor has no moss_id, use from env
        moss_user_id = os.environ['MOSS_ID']
        moss = plagcheck.check(format_lang(lang), moss_user_id)

    submissions = Solution.objects.filter(assignment__id=assignment)

    for code in submissions['submissions']:
        moss.addFile(code)

    moss.submit()

    results = moss.getResults()

    return results
