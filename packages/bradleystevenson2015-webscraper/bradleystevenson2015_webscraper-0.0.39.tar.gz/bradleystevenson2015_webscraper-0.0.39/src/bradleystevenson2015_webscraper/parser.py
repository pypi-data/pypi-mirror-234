from .common_webscraper_functions import fetch_soup_from_page, row_has_link, get_tr_of_stats_table, get_tr_of_table_with_id, true
from .field_parser import FieldParserFactory
import logging

class CreateFromPageParserFactory:

    def __init__(self, create_from_page_parser_dict) -> None:
        self.create_from_page_parser = CreateFromPageParser(create_from_page_parser_dict['base_url'], DataDictParserFactory(create_from_page_parser_dict['parser']).data_dict_parser)


class CreateFromPageParser:

    def __init__(self, base_url, data_dict_parser) -> None:
        self.base_url = base_url
        self.data_dict_parser = data_dict_parser

    def parse(self, url, webscraperObjectCollection):
        soup = fetch_soup_from_page(self.base_url + url)
        data_dict = self.data_dict_parser.parse(soup, {}, webscraperObjectCollection)
        data_dict['url'] = url
        return data_dict

class TableParserObject:

    def __init__(self, all_object_selection_function, narrow_down_function, data_dict_parser):
        self.all_object_selection_function = all_object_selection_function
        self.narrow_down_function = narrow_down_function
        self.data_dict_parser = data_dict_parser

    def parse_page(self, soup, data_dict, webscraperObjectCollection):
        return_array = []
        for eligible_element in self.all_object_selection_function(soup):
            if self.narrow_down_function(eligible_element):
                return_array.append(self.data_dict_parser.parse(eligible_element, data_dict, webscraperObjectCollection))
        return return_array

class ParserObjectFactory:

    def _get_narrow_down_function(self, function_name):
        if function_name == 'row_has_link':
            return row_has_link
        elif function_name == 'true':
            return true
        else:
            raise Exception("No match for narrow down function")


    def __init__(self, parser_dict):
        self.parser_dict = parser_dict
        if parser_dict['parser_type'] == 'table':
            if 'table_id' in parser_dict.keys():
                self.parser = TableParserObject(get_tr_of_table_with_id(parser_dict['table_id']), self._get_narrow_down_function(parser_dict['narrow_down_function']), DataDictParserFactory(parser_dict['data_dict_parser']).data_dict_parser)
            else:
                self.parser = TableParserObject(get_tr_of_stats_table(), self._get_narrow_down_function(parser_dict['narrow_down_function']), DataDictParserFactory(parser_dict['data_dict_parser']).data_dict_parser)
        else:
            raise Exception("No match for parser type")


class DataDictParserFactory:

    def __init__(self, data_dict_parser_dict):
        logging.info('[DataDictParserFactory] [Init] ' + str(data_dict_parser_dict))
        field_parsers = []
        for field_dict in data_dict_parser_dict:
            field_parsers.append(FieldParserFactory(field_dict).get_field_parser())
        self.data_dict_parser = DataDictParser(field_parsers)

class DataDictParser:

    def __init__(self, field_parsers):
        self.field_parsers = field_parsers

    def parse(self, html_object, data_dict, webscraperObject):
        return_dict = {}
        for field_parser in self.field_parsers:
            return_dict[field_parser.field_name] = field_parser.parse(html_object, data_dict, webscraperObject)
        return return_dict