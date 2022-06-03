import xml.etree.ElementTree as ET


class QTI_ASS_SCANNER():
    """
    Generic class for scanning a qti assesment. Takes in a file and a specified config which will depend on the qti version
    """

    def __init__(self,
                file, 
                qti_version):

        self.tree = ET.parse(file)
        self.root = self.tree.getroot()
        self.qti_version = qti_version

    def scan_that_qti_3_ass(self):
        """
        Scans the xml assuming the qti 3.0 structure of the file. This method is question type, question number
        and test structure agnostic. It simply scans an item file and returns the qti-response-declaration-iterable
        and qti-item-body iterable

        Returns:
            body_iterable: iterable over the elements in the item body
            response_declaration_iterables: iterable over the elements in the response declaration

            question_types: list of strings containing the question types
            question_iterables: list of iterable items, one for each of the subprompts in the item body
            response_declaration_iterable: an iterable of the response declaration
        """
        c = "{http://www.imsglobal.org/xsd/imsqtiasi_v3p0}"
        response_declaration_iterables = []

        for elem in self.root.iter():
            tag_n = elem.tag
            if tag_n == f"{c}qti-response-declaration":
                response_declaration_iterables.append(elem.iter())
            elif tag_n == f"{c}qti-item-body":
                body_iterable = elem.iter()
            else:
                pass
        
        return body_iterable, response_declaration_iterables

        
    def scan_that_ass(self):
        if self.qti_version == "qti_v3.0":
            body_iterable, response_declaration_iterables = self.scan_that_qti_3_ass()
            return response_declaration_iterables, body_iterable

        elif self.qti_version == "qti_v2.2":
            #TODO: implement assesment scan for version 2.2
            stuff = self.scan_that_qti_22_ass()

