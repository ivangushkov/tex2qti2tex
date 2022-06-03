import xml.etree.ElementTree as ET
import faceit_question_classes

class QTI_3_CONTENT_EXTRACTOR():
    """
    qti content extractor class. Receives response-declaration iterables, item-body iterable and a list of interaction
    types. First locates the interactions of the quiz and determines their types. Then for each type of interation, calls
    a special function which extracts the specific contents of the interaction.

    Interactions implemented so far: qti-choice-interaction
    """

    def __init__(self, 
                response_declaration_iterables,
                body_iterable):

        self.response_declaration_iterables = response_declaration_iterables
        self.body_iterable                  = body_iterable

        # Initiate some lookup values which are valid for v3.0
        # At the start of each element tag there is this constant string which is there for no real reason.
        # Represented here with c, which stands for cursed
        self.c = "{http://www.imsglobal.org/xsd/imsqtiasi_v3p0}"
        
        # Possible interactions in a qti-item-body. TODO: put the rest of the interations in (21 in total)
        self.possible_interactions =    ["qti-choice-interaction", "qti-text-entry-interaction", "qti-extended-text-interaction", 
                                        "qti-gap-match-interaction", "qti-hotspot-interaction", "qti-hot-text-interaction",
                                        "qti-inline-choice-interaction", "qti-match-interaction", "qti-order-interaction"]
        self.possible_interactions_tags = [f"{self.c}{possible_interaction}" for possible_interaction in self.possible_interactions]
        
    
    def get_interactions(self):
        """
        Goes through a body_iterable variable and records all the interations in there
        Inputs:
            body_iterable - an iterable object containing the item body of the item file
        Outputs:
            interaction_types - a list of strings with all the interactions in this item
        """

        interaction_types_inds = []
        interaction_iterables  = []

        for i,elem in enumerate(self.body_iterable):
            if i == 0:
                body_text = elem.text
            tag_n = elem.tag
            if tag_n in self.possible_interactions_tags:
                interaction_ind = self.possible_interactions_tags.index(tag_n)
                interaction_types_inds.append(interaction_ind)
                interaction_iterables.append(elem.iter())

        return interaction_types_inds, interaction_iterables, body_text
    
    def extract_choice_interaction_content(self, 
                                        response_declaration_iterable, 
                                        interaction_iterable,
                                        body_text):
        """

        """
        
        ans_list            = []
        ans_identifiers     = []
        corr_ans_list       = []
        corr_inds           = []

        for elem in interaction_iterable:
            if elem.tag == f"{self.c}qti-prompt":
                interaction_body = elem.text
            elif elem.tag == f"{self.c}qti-simple-choice":
                ans_list.append(elem.text)
                ans_identifiers.append(elem.attrib['identifier'])

        for elem in response_declaration_iterable:
            if elem.tag == f"{self.c}qti-correct-response":
                corr_response_iter = elem.iter()
                for elem2 in corr_response_iter:
                    if elem2.tag == f"{self.c}qti-value":
                        corr_ans_list.append(elem2.text)
        
        for corr_ans in corr_ans_list:
            corr_inds.append(ans_identifiers.index(corr_ans))
        
        mc_question_text = body_text + interaction_body
        if len(corr_inds) == 1:
            mc_object = faceit_question_classes.multiple_choice(question_body=mc_question_text, 
                                                                ans_list=ans_list,
                                                                corr_ind=corr_inds[0])
        elif len(corr_inds) > 1:
            mc_object = faceit_question_classes.multiple_choice(question_body=mc_question_text, 
                                                    ans_list=ans_list,
                                                    corr_ind=corr_inds) 
            #TODO: figure out if this should be different
        return mc_object
    def extract_contents(self):

        interaction_types_inds, interaction_iterables, body_text = self.get_interactions()
        questions = []
        for ind in interaction_types_inds:
            if ind == 0:
                question_object = self.extract_choice_interaction_content(self.response_declaration_iterables[ind], 
                                                                        interaction_iterables[ind],
                                                                        body_text)
                questions.append(question_object)
            elif ind == 1:
                # TODO: add other extractions for different interactions
                content = self.extract_text_entry_interaction()
        
        beruh = 1
        return questions