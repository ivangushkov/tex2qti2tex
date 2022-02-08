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
            q_type = element.strip().strip("}")[start:len(element)]
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


def extract_elements(lines):
    # Input: the lines of a question
    # Output: all the principle elements of a question
    q_type = get_question_type(lines)
    q_body = get_question_body(lines)
    ans = get_answers(lines)
    ans, correct_i = format_answers(ans)

    return q_type, q_body, ans, correct_i

def write_txt_mc_file(write_to_filename ,question_body, answers, correct_index):
    f = open(write_to_filename, "w")

    string = f"{question_body}\n"

    for i in range(len(answers)):
        if i == correct_index:
            string += f"*{answers[i]}\n"
        else:
            string += f"{answers[i]}\n"

    f.write(string)
    f.close()

def test_function(file):
    
    f = open(file, "r")

    lines = f.readlines()
    q_type , q_bod , ans , correct_i = extract_elements(lines)
    write_txt_mc_file("test_result.txt", q_bod, ans, correct_i)

    f.close()

test_function("test.txt")
