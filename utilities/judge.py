"""All Judge/Code Running Utilities here"""
from app.models import Question, Assignment
import coderunner


def run_code(code, lang, question):
    execution_status = {}

    expected_output = Question.objects.only(
        'sample_output').get(pk=question).sample_output
    standard_input = Question.objects.only(
        'sample_input').get(pk=question).sample_input

    if standard_input != "":
        r = coderunner.code(code, lang, standard_input, expected_output, False)
    else:
        r = coderunner.code(code, lang, expected_output, False)

    r.run()

    execution_status["status"] = r.getStatus()
    execution_status["output"] = r.getOutput()
    execution_status["error"] = r.getError()

    return execution_status


def submit_code(question, assignment, code):

    lang = Assignment.objects.only('language').get(pk=assignment).language

    program_status = run_code(code, lang, question)

    if program_status["status"] == "Accepted":
        execution_status = "accepted"
    elif program_status["status"] == "Wrong Answer":
        execution_status = "wrong"
    else:
        execution_status = "not-attempted"

    return program_status, execution_status
