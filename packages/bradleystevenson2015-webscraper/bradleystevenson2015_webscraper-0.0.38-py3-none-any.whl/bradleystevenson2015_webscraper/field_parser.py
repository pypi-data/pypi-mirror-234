from .common_webscraper_functions import get_value_from_element, does_html_object_exist

class FieldParserFactory:

    def __init__(self, field_dict):
        self.field_dict = field_dict

    def get_field_parser(self):
        if self.field_dict['parse_type'] == 'static':
            return StaticFieldParser(self.field_dict['field_name'], self.field_dict['static_value'])
        elif self.field_dict['parse_type'] == 'input_dict':
            return InputDictFieldParser(self.field_dict['field_name'], self.field_dict['dict_key'])
        elif self.field_dict['parse_type'] == 'dynamic':
            if 'html_object' in self.field_dict.keys():
                return ChildElementParser(self.field_dict['field_name'], self.field_dict)
            return DynamicFieldParser(self.field_dict['field_name'], self.field_dict)
        raise Exception("No Match for parse type " + self.field_dict['parse_type'])

class FieldParser:

    def __init__(self, field_name):
        self.field_name = field_name

    def parse(self, html_object, data_dict, webscraperObject):
        pass

class InputDictFieldParser(FieldParser): 

    def __init__(self, field_name, input_dict_field):
        super().__init__(field_name)
        self.input_dict_field = input_dict_field

    def parse(self, html_object, data_dict, webscraperObject):
        return data_dict[self.input_dict_field]

class StaticFieldParser(FieldParser):

    def __init__(self, field_name, static_value):
        super().__init__(field_name)
        self.static_value = static_value


    def parse(self, html_object, data_dict, webscraperObject):
        return self.static_value
    
class DynamicFieldParser(FieldParser):

    def __init__(self, field_name, field_dict):
        super().__init__(field_name)
        self.field_dict = field_dict
        self.function = get_value_from_element(field_dict)

    def parse(self, html_object, data_dict, webscraperObject):
        return_value = self.function(html_object)
        if 'object_name' in self.field_dict.keys():
            try:
                return webscraperObject.databaseObject.tables[self.field_dict['object_name']].get_primary_key_by_search_dict(return_value)
            except:
                return webscraperObject.get_webscraper_object_with_name(self.field_dict['object_name']).create_from_page(return_value, webscraperObject)
        return return_value
    
class ChildElementParser(FieldParser):

    def __init__(self, field_name, field_dict):
        super().__init__(field_name)
        self.function = does_html_object_exist(field_dict)

    def parse(self, html_object, data_dict, webscraperObject):
        return self.function(html_object)