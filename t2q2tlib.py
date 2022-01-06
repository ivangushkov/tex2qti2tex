import linecache

def get_nr_of_questions(lines): 
    nq = 0

    for element in lines:
        if "begin""{""IndexedQuestion}" in element:
            nq += 1

    return nq # works


def get_question_type(lines):
    start = len("\QuestionType{")

    for element in lines:
        if "\QuestionType" in element:
            q_type = element.strip().strip("}")[start:len(element)] #TODO format the element
            return q_type # works


def get_question_body(lines):
    # Input: the lines of a single question on standard form
    # Returns: list of strings which is the body of the question
    start_slice = 0
    end_slice = 0
    
    for element in lines:
        if "\QuestionBody" in element:
            start_slice = lines.index(element)+1
        elif "\QuestionPotentialAnswers{" in element:
            end_slice = lines.index(element)-2

    return lines[start_slice:end_slice] # works
    


def get_answers(lines): 
    # Input: the lines of a single question on standard form
    # Returns: list of strings which are the answers of the question
    
    start_slice = 0
    end_slice = 0

    for element in lines:
        if "\QuestionPotentialAnswers" in element:
            start_slice = lines.index(element)+1
        elif "\QuestionAuthorsEmails{" in element:
            end_slice = lines.index(element)-1

    return lines[start_slice:end_slice] # works


def format_answers(ans_lst):

    # Input: list of answers as they appear in the standard format
    # Output: list of simply the answers and a correct answer index

    correct_index = 0
    remove_correct = len("\correctanswer")
    remove = len("\\answer")

    for element in ans_lst:

        i = ans_lst.index(element)
        element = element.strip()
        line_len = len(element)

        if "correctanswer" in element:
            correct_index = i
            ans_lst[i] = element[remove_correct:line_len].strip()
        else:
            ans_lst[i] = element[remove:line_len].strip()
    return ans_lst, correct_index # works


def test_function(file):
    
    f = open(file, "r")
    lines = f.readlines()
    
    result_file = open("test_result.txt", "w")

    result_file.close()
    f.close()

test_function("test.txt")

#def write_txt_mc_file(write_to_filename ,question_body, answers, correct_index):
    # TODO figure out from the text2qti parsers how one does this