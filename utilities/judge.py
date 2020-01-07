"""All Judge/Code Running Utilities here"""
from app.models import Question, Assignment
import coderunner


def run_code(code, lang, question):
    expected_output = Question.objects.filter(
        question__id=question).get('sample_output')
    standard_input = Question.objects.filter(
        question__id=question).get('sample_input')

    if standard_input.exists():
        r = coderunner.code(code, lang, standard_input, expected_output, False)
    else:
        r = coderunner.code(code, lang, expected_output, False)

    r.run()

    submission_status = r.getStatus()
    standard_output = r.getOutput()

    if submission_status == "Accepted":
        content = {'status': 'Accepted', 'output': standard_output}
    elif submission_status == "Wrong Answer":
        content = {'status': 'Wrong Answer'}
    else:
        error = r.getError()
        content = {
            'status': 'Error Occured',
            'output': standard_output,
            'error': error
        }
    return content


def submit_code(question, assignment, code):
    expected_output = Question.objects.filter(id=question).values('sample_output')
    standard_input = Question.objects.filter(id=question).values('sample_input')
    lang = Assignment.objects.filter(id=assignment).values('language')
    lang = lang[0]['language']

    expected_output = expected_output[0]['sample_output']

    if standard_input.exists():
        standard_input = standard_input[0]['sample_input']
        r = coderunner.code(code, lang, standard_input, expected_output, False)
    else:
        r = coderunner.code(code, lang, expected_output, False)

    r.run()

    submission_status = r.getStatus()
    standard_output = r.getOutput()

    if submission_status == "Accepted":
        execution_status = "accepted"
    elif submission_status == "Wrong Answer":
        execution_status = "wrong"
    else:
        execution_status = "not-attempted"

    context = {"status": submission_status, "output": standard_output}

    return context, execution_status
