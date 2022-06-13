import glob
from qti_ass_scanner import QTI_ASS_SCANNER
from qti_content_extraction import QTI_3_CONTENT_EXTRACTOR

version = "qti_v3.0"

path = "./data/items/data_to_faceit/"

for filename in glob.glob("./data/items/*.xml"):

    pure_name = filename.split("\\")[-1][:-4]
    write_file = pure_name + ".tex"
    write_path = path + write_file

    asser = QTI_ASS_SCANNER(file=filename, qti_version=version)
    response_declaration_iterables, body_iterable, = asser.scan_that_ass()
    extractor = QTI_3_CONTENT_EXTRACTOR(response_declaration_iterables=response_declaration_iterables,
                                    body_iterable=body_iterable, filename=pure_name)

    questions = extractor.extract_contents()

    f = open(write_path, "a")

    for i,question in enumerate(questions):
        question.write_question(f, course="ez_course", content_units="ez_units", author_mail="ivanig@stud.ntnu.no", nq=int(i+1))
    
    f.close()
    bruh = 1