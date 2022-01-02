import linecache

def get_question_type(lines):
    
    for element in lines:
        if "\QuestionType" in element:
            type = element #TODO format the element


def get_question_body(lines):
    # TODO get the body from the lines of the file


def get_answers(lines):
    # TODO returns answers


def format_answers():
    # TODO returns formated_answers, correct_answer_index


def write_txt_mc_file(write_to_filename ,question_body, answers, correct_index):
    # TODO figure out from the text2qti parsers how one does this