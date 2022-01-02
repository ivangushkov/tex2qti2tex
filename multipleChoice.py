import linecache

def formatCorrectIndexLst(line): # returns the indeces of multiple correct answers
    retLst = []
    for i in range(0, len(line), 2):
        retLst.append(int(line[i]))
    return retLst
def formatCorrectIndex(line): # returns only the part of the string where the correct answer indeces are contained
    for i in range(len("correctAnswer ")):
        line = line[1::]
    line.strip()
    return line
def getCorrectAnswerIndex(qLst): # gives where the answer starts, and the index of correct answer
    for i in range(len(qLst)):
        if "correctAnswer" in qLst[i]:
            indexLst = formatCorrectIndex(qLst[i])
            retlst = formatCorrectIndexLst(indexLst)
            return retlst, qLst.index(qLst[i])

def getBodyStartEnd(qLst): # gives where the body starts and ends
    for i in range(len(qLst)):
        if "questionBody" in qLst[i]:
            bodyStart = i
        elif "bodyEnd" in qLst[i]:
            bodyEnd = i
    return bodyStart, bodyEnd

def formatAnswerLine(aLine): # formats an answer line that is not the correct answer
    while aLine[0] != " ":
        aLine = aLine[1::]
    aLine.strip()
    return str('\\answer ' + aLine)

def formatCorrectAnswerLine(aLine): # formats an answer line that is the correct answer
    while aLine[0] != " ":
        aLine = aLine[1 : :]
    aLine.strip()
    return "\\correctanswer " + aLine

def getAnswerLst(aLst, correctIndexLst): # gives a list with the answers formated correctly
    answerLst = []
    for i in range(1,len(aLst)):
        if i in correctIndexLst:
            answerLst.append(formatCorrectAnswerLine(aLst[i]))
        else:
            answerLst.append(formatAnswerLine(aLst[i]))
    return answerLst

def getQuestionBody(bLst): # gives one string with the question body
    questionBody = ""
    for i in range(len(bLst)):
        questionBody = str(questionBody) + str(bLst[i])
    return questionBody

def questionAsseser(qFile, qLine):
    #get all the lines from file, find range, define list we iterate over
    lns = linecache.getlines(qFile)
    qendLine = qLine
    while linecache.getline(qFile,qendLine) != "questionBruhEnd\n":
        qendLine += 1

    qLst = lns[qLine:qendLine]
    # The easy stuff: question units and course
    contentUnits = qLst[1]
    questionCourse = qLst[2]

    # figure out and format body
    bodyStart, bodyEnd = getBodyStartEnd(qLst)
    bLst = qLst[bodyStart + 1:bodyEnd]
    questionBody = getQuestionBody(bLst)

    #Figure out and format answers
    correctIndexLst, ansStart = getCorrectAnswerIndex(qLst)
    aLst = qLst[ansStart:len(qLst)-1]
    answerLst = getAnswerLst(aLst, correctIndexLst)

    return contentUnits, questionCourse, questionBody, answerLst


def writingFunction(formatedFile, contentUnits, questionCourse, questionBody, answerLst, authorMail, nq):
    f = open(formatedFile, "a")
    string = (f"%question {nq}\n"
    "\\begin{IndexedQuestion}\n"
    "   \QuestionContentUnits{" f"{contentUnits.strip()}""}\n"
    "   \QuestionCourses{" f"{questionCourse.strip()}""}\n"
    "   \QuestionType{multiple choice}\n"
    "   \QuestionBody{\n"
    "       "f"{questionBody}" "\n"
    "       }% DO NOT INCLUDE FIGURES HERE\n"
    "       \QuestionPotentialAnswers{\n")
    "f"
    for i in range(len(answerLst)):
        string += "            " + answerLst[i]

    string += ("       } % ONLY IF TYPE = MULTIPLE CHOICE\n"
    "       \QuestionAuthorsEmails{" f"{authorMail}" "}\n"
    "       \QuestionLanguage{English}\n"
    "       %\\begin{IndexedSolution}\n"
    "           %\SolutionContentUnits{" f"{contentUnits.strip()}""}\n"
    "           %\SolutionBody{\n"
    "% \n"
    "%           }\n"
    "           %\SolutionAuthorsEmail{" f"f{authorMail}" "}\n"
    "       %\end{IndexedSolution}\n"
    "\end{IndexedQuestion}\n"
    "\n\n")
    f.write(string)
    f.close()
#answers = str(input("Provide the answer list: "))
#correctIndex = int(input("The correct answer is on row: "))

fRaw = "questionsLinSys.txt"
fMC = "LinSys_MC.tex"

f = open(fMC, "w")
f.close()

authorMail = "ivanig@stud.ntnu.no" #string with mail here
#questionNumber = 0 # Somehow get it from Raw
# For loop over RAW to get question number

nq = 0
with open(fRaw,"r") as questionFile:
    k = 0
    for line in questionFile:
        if line == "questionBruh:\n":
            nq += 1
            contentUnits, questionCourse, questionBody, answerLst = questionAsseser(fRaw, k)
            writingFunction(fMC,contentUnits,questionCourse,questionBody,answerLst,authorMail, nq)
        k += 1
questionFile.close()