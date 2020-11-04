# -*- coding: utf-8 -*-
"""
@author: Matheus Stauffer (matheusvostauffer@gmail.com) 10/06/2020

@description: PyDash Project

A mpd parser implementation to store and extract MDP information used
during the simulation
"""

from xml.etree.ElementTree import fromstring, ElementTree

class mpd_node:
    def __init__(self):
        self.mpd_dict = {}
        self.period_dict = {}
        self.program_info_dict = {}
        self.adaptation_set_list = []
        self.adaptation_set_dict = {}
        self.title = ""
        self.segment_template = {}
        self.first_level_adp_set = {}
            
    def add_mpd_info(self, data):
        self.mpd_dict = data
    
    # return mpd_info dict
    def get_mpd_info(self):
        return self.mpd_dict
    
    def add_period_info(self, data):
        self.period_dict = data
        
    # return period_info dict
    def get_period_info(self):
        return self.period_dict
    
    def add_program_info(self, data):
        self.program_info_dict = data
    
    # return program_info dict
    def get_program_info(self):
        return self.program_info_dict
    
    def add_adaptation_set_info(self, data):
        self.adaptation_set_list = data
    
    # return adaptation set
    def get_adaptation_set_info(self):
        return self.adaptation_set_list
    
    def add_title(self, data):
        self.title = data
    
    # return title
    def get_title(self):
        return self.title
    
    def add_segment_template(self, data):
        self.segment_template = data
    
    # return segment template
    def get_segment_template(self):
        return self.segment_template
    
    def add_first_level_adp_set(self, data):
        self.first_level_adp_set = data
    
    # return first level adp set
    def get_first_level_adp_set(self):
        return self.first_level_adp_set

    def get_qi(self):
        handle_list = self.get_adaptation_set_info()
        qi = [int(i['bandwidth']) for i in handle_list]
        qi.sort()
        return qi

# mpd file parsing.
def parse_mpd(file_path):
    node = mpd_node()
    adaptation_set = []

    #tree = ET.parse(file_path)
    tree = ElementTree(fromstring(file_path))

    root = tree.getroot()

    node.add_mpd_info(root.attrib)

    # inside mpd
    for child in root:
        if child.tag == "{urn:mpeg:dash:schema:mpd:2011}ProgramInformation":
            node.add_program_info(child.attrib)
        elif child.tag == "{urn:mpeg:dash:schema:mpd:2011}Period":
            node.add_period_info(child.attrib)
        # inside program_information and period
        for inside in child:
            if inside.tag == "{urn:mpeg:dash:schema:mpd:2011}Title":
                node.add_title(inside.text)
            elif inside.tag == "{urn:mpeg:dash:schema:mpd:2011}AdaptationSet":
                node.add_first_level_adp_set(inside.attrib)
            # inside adaptation_set
            for adp_set in inside:
                if adp_set.tag == "{urn:mpeg:dash:schema:mpd:2011}SegmentTemplate":
                    node.add_segment_template(adp_set.attrib)
                else:
                    adaptation_set.append(adp_set.attrib)
    
    node.add_adaptation_set_info(adaptation_set)
        
    return node

# return the specific attribute value. 
# if representation_id is passed, returns the correspondent dict.
def navigate_mpd(mpd_node, attribute = None, representation_id = None):
    handle_dict = {}
    handle_list = []
    
    if representation_id:
        handle_list = mpd_node.get_adaptation_set_info()
        for i, item in enumerate(handle_list):
            if item['id'] == representation_id:
                return item
            
    else:
        handle_dict = mpd_node.get_mpd_info()
        for key in handle_dict:
            if attribute == key:
                return(attribute, handle_dict[key])

        handle_dict = mpd_node.get_period_info()
        for key in handle_dict:
            if attribute == key:
                return(attribute, handle_dict[key])

        handle_dict = mpd_node.get_program_info()
        for key in handle_dict:
            if attribute == key:
                return(attribute, handle_dict[key])

        handle_dict = mpd_node.get_segment_template()
        for key in handle_dict:
            if attribute == key:
                return(attribute, handle_dict[key])

        handle_dict = mpd_node.get_first_level_adp_set()
        for key in handle_dict:
            if attribute == key:
                return(attribute, handle_dict[key])

'''
exemplo = mpd_node()
exemplo = parse_mpd('file.mpd')

print(exemplo.get_mpd_info())
print(navigate_mpd(exemplo, 'timescale'))
print(navigate_mpd(exemplo, 'blah', '480x360 182.0kbps'))
'''