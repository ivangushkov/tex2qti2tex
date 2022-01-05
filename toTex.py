
import linecache

def write_toTex_MC(writing_file, content_units, q_course, q_body, ans_lst, author_mail, nq):

    #### Writes to a .tex file a multiple choice in the faceIt format ####
    # Inputs: file name, list of content units, question course, question body in plain latex,
    #         a formated list of answers, author mail, question number

    f = open(writing_file, "a")
    string = (f"%question {nq}\n"
    "\\begin{IndexedQuestion}\n"
    "   \QuestionContentUnits{" f"{content_units.strip()}""}\n"
    "   \QuestionCourses{" f"{q_course.strip()}""}\n"
    "   \QuestionType{multiple choice}\n"
    "   \QuestionBody{\n"
    "       "f"{q_body}" "\n"
    "       }% DO NOT INCLUDE FIGURES HERE\n"
    "       \QuestionPotentialAnswers{\n")
    "f"
    for i in range(len(ans_lst)):
        string += "            " + ans_lst[i]

    string += ("       } % ONLY IF TYPE = MULTIPLE CHOICE\n"
    "       \QuestionAuthorsEmails{" f"{author_mail}" "}\n"
    "       \QuestionLanguage{English}\n"
    "       %\\begin{IndexedSolution}\n"
    "           %\SolutionContentUnits{" f"{content_units.strip()}""}\n"
    "           %\SolutionBody{\n"
    "% \n"
    "%           }\n"
    "           %\SolutionAuthorsEmail{" f"f{author_mail}" "}\n"
    "       %\end{IndexedSolution}\n"
    "\end{IndexedQuestion}\n"
    "\n\n")
    f.write(string)
    f.close()

def call_writing_function(question_type, writing_file, content_units, q_course, q_body, ans_lst, author_mail, nq):
    
    if question_type.casefold() == "multiple choice":
        write_toTex_MC(writing_file, content_units, q_course, q_body, ans_lst, author_mail, nq)

