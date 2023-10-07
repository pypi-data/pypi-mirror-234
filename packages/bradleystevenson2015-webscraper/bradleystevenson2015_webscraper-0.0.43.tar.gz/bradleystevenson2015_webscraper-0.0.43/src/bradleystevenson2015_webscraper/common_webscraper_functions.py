from bs4 import BeautifulSoup
from selenium import webdriver
import selenium
import logging

def get_element(field_dict):
    element_type = None
    attributes = {}
    if 'element_type' in field_dict.keys():
        element_type = field_dict['element_type']
    if 'attributes' in field_dict.keys():
        attributes = field_dict['attributes']
    if element_type is None:
        def return_function(html_object):
            return html_object.find(attrs=attributes)
        return return_function
    def return_function(html_object):
        return html_object.find(element_type, attrs=attributes)
    return return_function

def get_rough_value_from_element(field_dict):
    logging.info("[GET_ROUGH_VALUE_FROM_ELEMENT] " + str(field_dict))
    if field_dict['html_field_value'] == 'url':
        def return_function(html_object):
            return get_element(field_dict)(html_object).find('a')['href']
        return return_function
    elif field_dict['html_field_value'] == 'text':
        def return_function(html_object):
            return get_element(field_dict)(html_object).text
        return return_function
    else:
        raise Exception(f"No match for html field value {field_dict['html_field_value']}")

def get_value_from_element(field_dict):
    def return_function(html_object):
        return_value = get_rough_value_from_element(field_dict)(html_object)
        if 'remove_strings' in field_dict.keys():
            for remove_string in field_dict['remove_strings']:
                return_value = return_value.replace(remove_string, '')
        return return_value
    return return_function

def does_html_object_exist(field_dict):
    def return_function(html_object):
        if get_element(field_dict)(html_object).find(field_dict['html_object']) is not None:
            return 1
        return 0
    return return_function

def get_element_with_attributes(attributes):
    def return_function(html_object):
        return html_object.find(attrs=attributes)
    return return_function

def get_tr_of_table_with_id(table_id):
    def return_function(soup):
        return soup.find(id=table_id).find("tbody").find_all("tr")
    return return_function

def get_tr_of_stats_table():
    def return_function(soup):
        return soup.find(attrs={'class': 'stats_table'}).find('tbody').find_all('tr')
    return return_function

def row_has_link(html_object):
    return html_object.find("a") is not None

def true(html_object):
    return True

def fetch_soup_from_page(url):
    while True:
        try:
            options = webdriver.ChromeOptions()
            options.add_argument('headless')
            options.add_argument('window-size=1200x600')
            driver = webdriver.Chrome(options=options)
            driver.get(url)
            page = driver.page_source
            driver.quit()
            soup = BeautifulSoup(page, 'html.parser')
            return soup
        except selenium.common.exceptions.TimeoutException:
            print("Failing url: url")
            print("Timed out loading page, trying again")
        except selenium.common.exceptions.WebDriverException:
            print("failing url: " + str(url))
            print("Web Driver Error, trying again")
