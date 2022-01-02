import t2q2tlib
import linecache

def main():

    lines = linecache.getlines(file)
    question_type = get_question_type(lines)

    if question_type == "mc": 
        question_body = get_question_body(lines)
        answers_raw = get_answers(lines)
        formated_answers, correct_answer_index = format_answers(answers_raw)

        write_txt_mc_file(question_body, formated_answers, correct_answer_index)


