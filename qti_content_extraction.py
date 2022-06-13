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
                body_iterable,
                filename=None):

        self.response_declaration_iterables = response_declaration_iterables
        self.body_iterable                  = body_iterable
        self.filename=filename

        # Initiate some lookup values which are valid for v3.0
        # At the start of each element tag there is this constant string which is there for no real reason.
        # Represented here with c, which stands for cursed
        self.c = "{http://www.imsglobal.org/xsd/imsqtiasi_v3p0}"
        
        # Possible interactions in a qti-item-body. TODO: put the rest of the interations in (21 in total)
        self.possible_interactions =    ["qti-choice-interaction", "qti-text-entry-interaction", "qti-extended-text-interaction", 
                                        "qti-gap-match-interaction", "qti-hotspot-interaction", "qti-hot-text-interaction",
                                        "qti-inline-choice-interaction", "qti-match-interaction", "qti-order-interaction"]
        self.possible_interactions_tags = [f"{self.c}{possible_interaction}" for possible_interaction in self.possible_interactions]
        
        self.possible_bodies = ["p"]
        self.possible_body_tags = [f"{self.c}{possible_body}" for possible_body in self.possible_bodies]
    
    def get_interactions(self):
        """
        Goes through a body_iterable variable and records all the interations in there
        Inputs:
            body_iterable - an iterable object containing the item body of the item file
        Outputs:
            interaction_types_inds - indices in the list of possible interaction types, see constructor
            interaction_iterables  - iterable objects for all the different interactions(questions) found
            body_text              - any common body text, which is not a question specific prompt
        """

        interaction_types_inds = []
        interaction_iterables  = []
        body_text = None

        for i,elem in enumerate(self.body_iterable):
            tag_n = elem.tag
            if tag_n in self.possible_bodies: # This might not be a good solution TODO: change this to dynamically count outter bodies (??)
                body_text = elem.text
            elif tag_n in self.possible_interactions_tags:
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
        if body_text == None:
            body_text = ""
        
        ans_list            = []
        ans_identifiers     = []
        corr_ans_list       = []
        corr_inds           = []
        interaction_bodies  = []

        for elem in interaction_iterable:
            if elem.tag == f"{self.c}qti-prompt":
                prompt_text_lst = []
                prompt_iter = elem.iter()
                for subelem in prompt_iter:
                    prompt_text_lst.append(subelem.text)
                interaction_bodies.append("".join(prompt_text_lst))

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
        
        mc_question_text = body_text + interaction_bodies[0]
        if len(corr_inds) == 1:
            mc_object = faceit_question_classes.multiple_choice(question_body=mc_question_text, 
                                                                ans_list=ans_list,
                                                                corr_ind=corr_inds[0])
        elif len(corr_inds) > 1:
            mc_object = faceit_question_classes.multiple_choice(question_body=mc_question_text, 
                                                    ans_list=ans_list,
                                                    corr_ind=corr_inds) 
            #TODO: figure out if this should be different
        elif len(corr_inds) == 0:
            mc_object = faceit_question_classes.multiple_choice(question_body=mc_question_text, 
                                                    ans_list=ans_list,
                                                    corr_ind=None) 
        return mc_object
    def extract_contents(self):

        interaction_types_inds, interaction_iterables, body_text = self.get_interactions()
        questions = []
        for ind,interaction_iterable in enumerate(interaction_iterables):
            if interaction_types_inds[ind] == 0:
                question_object = self.extract_choice_interaction_content(self.response_declaration_iterables[ind], 
                                                                        interaction_iterable,
                                                                        body_text)
                questions.append(question_object)
            elif ind == 1:
                # TODO: add other extractions for different interactions
                content = self.extract_text_entry_interaction()

        return questions