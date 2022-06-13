

class multiple_choice():
    """
    Creates an object that stores all the data needed to write a multiple choice
    question on the faceit format
    """

    def __init__(self, 
                question_body,
                ans_list,
                corr_ind):
        
        self.question_type = 'multiple choice'

        self.question_bod = question_body
        self.ans_list     = ans_list
        self.corr_ind     = corr_ind
    
    def write_question(self, file, course, content_units, author_mail, nq):
        """
        Writes to an open file. Assume file opened with "a" option
        """
        if self.corr_ind == None:
            self.ans_list.append("Please provide correct answer")
            self.corr_ind = [len(self.ans_list) - 1]

        to_write = (f"%question {nq}\n"
        "\\begin{IndexedQuestion}\n"
        "   \QuestionContentUnits{" f"{content_units.strip()}""}\n"
        "   \QuestionCourses{" f"{course.strip()}""}\n"
        "   \QuestionType{multiple choice}\n"
        "   \QuestionBody{\n"
        "       "f"{self.question_bod}" "\n"
        "       }% DO NOT INCLUDE FIGURES HERE\n"
        "       \QuestionPotentialAnswers{\n")
        "f"
        for i in range(len(self.ans_list)):
            if i in self.corr_ind:
                to_write += "\t\t\t\correctanswer " + self.ans_list[i] + "\n"
            else:
                to_write += "\t\t\t\\answer " + self.ans_list[i] + "\n"

        to_write += ("       } % ONLY IF TYPE = MULTIPLE CHOICE\n"
        "       \QuestionAuthorsEmails{" f"{author_mail}" "}\n"
        "       \QuestionLanguage{English}\n"
        "       %\\begin{IndexedSolution}\n"
        "           %\SolutionContentUnits{" f"{content_units.strip()}""}\n"
        "           %\SolutionBody{\n"
        "% \n"
        "%           }\n"
        "           %\SolutionAuthorsEmail{" f"{author_mail}" "}\n"
        "       %\end{IndexedSolution}\n"
        "\end{IndexedQuestion}\n"
        "\n\n")
        file.write(to_write)
        