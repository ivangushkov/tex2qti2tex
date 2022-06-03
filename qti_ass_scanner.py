import xml.etree.ElementTree as ET

tree_own = ET.parse('./tests/sample_assesment/text2qti_sample_assesment/text2qti_sample_assessment.xml')
root_own = tree_own.getroot()

c = '{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}'

#k = 0
#for matadata in root_own.findall(f"./{c}item/{c}qtimetadata"):
#    print(k)
#    k += 1

item_attribs = [item.attrib for item in root_own.iter(f'{c}item')]
#item_metadata = [metadata.iter() for metadata in root_own.iter(f'{c}qtimetadata')]
item_metadata = [metadata.iter() for metadata in root_own.iter(f'./{c}item/{c}qtimetadata')]

items_iterables = [item.iter() for item in root_own.iter(f'{c}item')]
#items_metadata_iters = [metadata.iter() for metadata in root_own.iter(f'{c}qtimetadata')]

#test = root_own.findall(f"./{c}item/{c}qtimetadata/")
item_1 = items_iterables[0]

#item_1_elems = [elem for elem in item_1]
field_labels = []
field_entries = []

#for i,elem in enumerate(item_1):
#    tag_n = elem.tag
#    if tag_n == f"{c}fieldlabel":
#        field_labels.append(elem.text)
#    elif tag_n == f"{c}fieldentry":
#        field_entries.append(elem.text)
#    elif tag_n == f"{c}mattext":
#        question_body = elem.text


####################################################################################
file = "./data/items/composition_of_water_qti3.xml"
version = "qti_v3.0"

class QTI_ASS_SCANNER():
    """
    Generic class for scanning a qti assesment. Takes in a file and a specified config which will depend on the qti version
    """

    def __init__(self, file, qti_version):
        self.tree = ET.parse(file)
        self.root = self.tree.getroot()
        self.qti_version = qti_version

    def v3_interactions_init(self):
        """
        Initiates a bunch of look up values which are valid for qti v3.0
        """
        # At the start of each element tag there is this constant string which is there for no real reason.
        # Represented here with c, which stands for cursed
        self.c = "{http://www.imsglobal.org/xsd/imsqtiasi_v3p0}"
        
        # Possible interactions in a qti-item-body. TODO: put the rest of the interations in (21 in total)
        possible_interactions = ["qti-choice-interaction", "qti-text-entry-interaction", "qti-extended-text-interaction"
                                , "qti-gap-match-interaction", "qti-hotspot-interaction", "qti-hot-text-interaction",
                                "qti-inline-choice-interaction", "qti-match-interaction", "qti-order-interaction"]
        self.possible_interactions_tags = [f"{self.c}{possible_interaction}" for possible_interaction in possible_interactions]

    def scan_that_qti_3_ass(self):
        """
        Scans the xml assuming the qti 3.0 structure of the file. This method is question type, question number
        and test structure agnostic. It simply scans an item file and finds how many questions there are, what
        the different question types are and returns iterables for those things to be determined in a different
        place.

        Returns:
            question_types: list of strings containing the question types
            question_iterables: list of iterable items, one for each of the subprompts in the item body
            response_declaration_iterable: an iterable of the response declaration
        """

        response_declaration_iterables = []

        for elem in self.root.iter():
            tag_n = elem.tag
            if tag_n == f"{self.c}qti-response-declaration":
                response_declaration_iterables.append(elem.iter())
            elif tag_n == f"{self.c}qti-item-body":
                body_iterable = elem.iter()
            else:
                pass
        
        return body_iterable, response_declaration_iterables

    def get_interaction_types(self, body_iterable):
        """
        Goes through a body_iterable variable and records all the interations in there
        Inputs:
            body_iterable - an iterable object containing the item body of the item file
        Outputs:
            interaction_types - a list of strings with all the interactions in this item
        """
        interaction_types = []
        for elem in body_iterable:
            tag_n = elem.tag
            if tag_n in self.possible_interactions_tags:
                interaction_types.append(tag_n)
        return interaction_types
        
    def scan_that_ass(self):
        if self.qti_version == "qti_v3.0":
            self.v3_interactions_init()
            body_iterable, response_declaration_iterables = self.scan_that_qti_3_ass()
            interaction_types = self.get_interaction_types(body_iterable)
            return response_declaration_iterables, body_iterable, interaction_types

        elif self.qti_version == "qti_v2.2":
            #TODO: implement assesment scan for version 2.2
            stuff = self.scan_that_qti_22_ass()

        return body_iterable, response_declaration_iterables


asser = QTI_ASS_SCANNER(file=file, qti_version=version)
asser.scan_that_ass()
