import linecache

def get_nr_of_questions(lines):
    nq = 0
    for element in lines:
        if "\begin{IndexedQuestion}" in element:
            nq += 1

    return nq


def get_question_type(lines):
    start = len("\QuestionType ")

    for element in lines:
        if "\QuestionType" in element:
            element.strip()
            q_type = element[start:len(element)] #TODO format the element
            return q_type


def get_question_body(lines):

    # Returns a string which is the body of the question
    start_slice = len("\QuestionBody{")
    
    for element in lines:
        if "\QuestionBody" in element:
            element.strip()
            del element[0:start_slice]
            del element[-1]

            return element

            
    # TODO get the body from the lines of the file


def get_answers(lines):
    # Input: question on standard form
    # Returns: list of strings which are the answers of the question
    
    ans_lst = []
    k = 0

    for element in lines:
        if "\QuestionPotentialAnswers" in element:
            while lines[k+1].strip() != "}":
                ans_lst.append(lines[k+1].strip())
                k += 1
        k += 1

    return ans_lst
    
    # TODO returns answers


def format_answers(ans_lst):
    # TODO returns formated_answers, correct_answer_index


def write_txt_mc_file(write_to_filename ,question_body, answers, correct_index):
    # TODO figure out from the text2qti parsers how one does this