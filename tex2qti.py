import linecache
import text2qti
import os
import textwrap

def get_nr_of_questions(lines): 
    nq = 0

    index_pairs = []
    for i,element in enumerate(lines):
        if "begin""{""IndexedQuestion}" in element:
            nq += 1
            remaining_lines = lines[i:]
            for j,remaining_line in enumerate(remaining_lines):
                if "\end""{""IndexedQuestion""}" in remaining_line:
                    index_pair = [i,int(i+j+1)]
                    index_pairs.append(index_pair)
                    break

    return index_pairs,nq # works


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

def convert_md_and_cleanup(lines): #works
    temp_write = open("temp_write.tex", "w")
    temp_write.write("".join(lines))
    temp_write.close()

    # pandoc -s temp_write.tex -o bruh_result.md
    os.system("pandoc -s temp_write.tex -o temp_write_md.md")
    temp_md = open("temp_write_md.md", "r")
    lines_md = temp_md.readlines()
    temp_md.close()

    os.remove("temp_write.tex")
    os.remove("temp_write_md.md")
    return lines_md

def body_ans_to_md(q_body, q_ans): # works 
    """
    Converts the qeustion body and questions answers lists to markdown using pandoc
    """

    q_body_md = convert_md_and_cleanup(q_body)
    q_ans_md = []
    for answer in q_ans:
        answer_md = convert_md_and_cleanup(answer)
        q_ans_md.append(answer_md[0])

    return q_body_md, q_ans_md

def write_txt_mc_file(write_to_filename ,question_body, answers, correct_index, question_nr):
    f = open(write_to_filename, "a")
    wrapper = textwrap.TextWrapper(initial_indent='\t',subsequent_indent='\t\t')
    to_write = "\n"
    to_write += f"{question_nr}. " + wrapper.fill(question_body[0])
    to_write += "\t\t".join(question_body[1:])
    #wrapped = wrapper.fill(to_write)

    for i in range(len(answers)):
        if i == correct_index:
            to_write += f"[*] {answers[i]}" # might want to add back the newline here later
        else:
            to_write += f"[] {answers[i]}"

    f.write(to_write)
    f.close()

def tex2qti_pipeline(file, assesment_name):
    """
    Pipelines a .tex file in the format of the faceit portal to a qti assesment zip
    """
    f = open(file, "r")

    lines = f.readlines()
    index_pairs, nq = get_nr_of_questions(lines)

    for i,pair in enumerate(index_pairs):
        q_start, q_end = pair[0], pair[1]
        q_lines = lines[q_start:q_end]

        q_type , q_bod , ans , correct_i = extract_elements(q_lines)
        q_bod_md, ans_md = body_ans_to_md(q_bod, ans)
        write_txt_mc_file(f"{assesment_name}.txt", q_bod_md, ans_md, correct_i, (i+1))
    
    os.system(f"text2qti {assesment_name}.txt")

    f.close()
    os.remove(f"{assesment_name}.txt")

tex2qti_pipeline("LinSys_MC.tex", "sample_assesment")
