import os
import glob
from html.parser import HTMLParser

class V10Parser(HTMLParser):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        self.hotel_entry_depth = 0
        self.in_ul = False
        self.nested_hotel_entry = 0
        self.invalid_ul_children = 0
        
        self.in_pros_cons = False
        self.pros_count = 0
        self.cons_count = 0
        self.in_pros_section = False
        self.in_cons_section = False
        self.in_li = False

        self.blocks = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        classes = attrs_dict.get('class', '').split()
        
        if 'hotel-entry' in classes:
            if self.hotel_entry_depth > 0:
                self.nested_hotel_entry += 1
            self.hotel_entry_depth += 1
            
        if tag == 'ul':
            self.in_ul = True
            
        if self.in_ul:
            if tag == 'table' or tag == 'figure' or 'hotel-entry' in classes or 'facts' in classes:
                self.invalid_ul_children += 1
                
        if 'pros-cons' in classes:
            self.in_pros_cons = True
            self.pros_count = 0
            self.cons_count = 0
            
        if self.in_pros_cons:
            if 'pros--section' in classes:
                self.in_pros_section = True
            if 'cons--section' in classes:
                self.in_cons_section = True
                
            if tag == 'li':
                if self.in_pros_section: self.pros_count += 1
                if self.in_cons_section: self.cons_count += 1

    def handle_endtag(self, tag):
        if tag == 'div':
            # This is a bit naive for tracking div depths without a full stack, 
            # but standard html.parser doesn't auto-build the tree.
            # A true DOM parser is better.
            pass
        if tag == 'ul':
            self.in_ul = False
            
        if self.in_pros_cons and tag == 'div':
            # We can't properly track end of pros-cons without a stack.
            pass

def main():
    pass
