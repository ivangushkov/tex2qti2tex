from qti_ass_scanner import QTI_ASS_SCANNER
from qti_content_extraction import QTI_3_CONTENT_EXTRACTOR

file = "./data/items/composition_of_water_qti3.xml"
version = "qti_v3.0"

write_file = "faceit_quiz.tex"


asser = QTI_ASS_SCANNER(file=file, qti_version=version)
response_declaration_iterables, body_iterable, = asser.scan_that_ass()

extractor = QTI_3_CONTENT_EXTRACTOR(response_declaration_iterables=response_declaration_iterables,
                                    body_iterable=body_iterable)


questions = extractor.extract_contents()

f = open(write_file, "a")

for i,question in enumerate(questions):
    question.write_question(f, course="ez_course", content_units="ez_units", author_mail="ivanig@stud.ntnu.no", nq=int(i+1))

f.close()