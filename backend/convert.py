# -*- coding: utf-8 -*-
"""Module for handling data conversions between XML, JSON and perspectively in YAML.

"""

import json
import lxml.etree as etree
import os
import re


NAMESPACES = {}
NAMESPACE_STRINGS = {}
REVERSE_NAMESPACE_STRINGS = {}


def update_namespaces(prefix, namespace):
    NAMESPACES[prefix] = namespace
    for key in NAMESPACES.keys():
        NAMESPACE_STRINGS[key] = "{{{0}}}".format(NAMESPACES[key])
    for key in NAMESPACE_STRINGS.keys():
        REVERSE_NAMESPACE_STRINGS[NAMESPACE_STRINGS[key]] = key
update_namespaces(None, "http://www.w3.org/XML/1998/namespace")
update_namespaces("xhtml", "http://www.w3.org/1999/xhtml")
update_namespaces("xs", "http://www.w3.org/2001/XMLSchema")


def load_xml(file_path, schema_path=None):
    """Load an XML file and validate it, if an XMLSchema is provided.

    Args:
        file_path (str): the path of the XML file
        schema_path (str): the path of the XML schema (usually the file suffix is ".xsd")
    
    Retusns:
        lxml.etree._ElementTree: the resulting tree of XML element representations

    """
    with open(file_path) as xml_file:
        xml_document = etree.parse(xml_file)
        if schema_path is not None:
            with open(schema_path) as schema_file:
                schema = etree.XMLSchema(etree.parse(schema_file))
                if schema.validate(xml_document):
                    raise Exception("File '{0}' is not valid against schema '{1}'."
                                    .format(file_path, schema_path))
    return xml_document

def xmlfile_to_jsonstr(file_path, schema_path=None, namespaces={}):
    """Transforms XML including namespaces into JSON.

    Args:
        file_path (str): The file path to an XML file.
        schema_path (str): The file path to an XML Schema for validation of the XML file.
        namespaces (dict<str, str>): A dict mapping namespaces to namespace shortcuts.
        A valid namespaces dict would be namespaces={"{http://www.w3.org/XML/1998/namespace}": "xml"}.
    
    Returns:
        str: Formatted JSON content.

    """
    def replace_namespaces(name):
        """Replace XML namespaces like {http://www.w3.org/XML/...} by prefixes.

        Args:
            name (str): The input string, which possibly contains namespaces to be replaced.

        Returns:
            str: The input string with replaced namespaces.

        """
        if not namespaces is None:
            for k in namespaces.keys():
                 if name.startswith(k):
                    return name.replace(k, namespaces[k] + "___")
        return name
        

    def append_element_dict(current_element, parent_dict):
        """Append a dictionary to the parent_dict for the sub-element tree and attributes of the current element.

        Args:
            current_element (etree.Element): The current XML-Element.
            parent_dict (dict): The parent dictionary.

        Returns:
            None: The parent_dict is modified.
        """
        r = {}
        if current_element.text and not current_element.text.isspace():
            r['_'] = current_element.text
        for att_name in sorted(current_element.attrib.keys()):
            r['_' + replace_namespaces(att_name)] = current_element.attrib[att_name]
        for child in current_element:
            append_element_dict(child, r)
        if current_element.tag not in parent_dict:
            parent_dict[current_element.tag] = []
        parent_dict[current_element.tag].append(r)

    retval = {}
    xml = load_xml(file_path, schema_path)
    root = xml.getroot()
    retval[root.tag] = {}
    append_element_dict(root, retval[root.tag])
    d = retval[root.tag][root.tag][0]
    for key in sorted(namespaces.keys()):
        shortcut = namespaces[key]
        if shortcut is None:
            shortcut = "NONE"
        abbrev = "_xmlns___" + shortcut
        d[abbrev] = key
    return json.dumps(retval[root.tag], indent=4, sort_keys=True)

def jsonstr_to_xmlfile(json_string, target_file_path):
    """Convert a JSON character string into an XML tree and writes it as file.

    Args:
        json_string (str): A character string containing JSON.
        target_file_path (str): The path of the target XML file.

    Returns:
        lxml.etree._Element: The root element of the target XML file.

    """

    def create_xml_element(parent_xml_element, namespace_prefix, tag_name, list_of_element_dictionaries):
        """Create an XML element from a Python list representing sub-elements.

        The Python list contains Python dictionaries with key-value pairs.
        If a value is of type 'list', then this key-value pair is considered as XML element representation.
        Otherwise the key-value pair is considered as XML attribute representation.

        The key within such a key-value can indicate whether it is:

            "_" : The value represents the element text.
            starting with "_" : The value represents an attribute value.
            otherwise : The value represents a list of elements.

        There is a special syntax for namespaces:
            "_<namespace_prefix>___<...>": An XML attribute name with a namespace prefix.
            "<namespace_prefix>___<...>": An XML element name with a namespace prefix.

        Args:
            tag_name (str): The tag name of the element to be constructed.
            list_of_element_dictionaries (list<dict>): A list of dictionaries, each representing
                an XML sub-element of the XML element to be constructed.
            parent_xml_element (lxml.etree._Element): The parent XML element of the sub-elements
                to be constructed.

        Returns:
            lxml.etree._Element: The constructed XML element.

        """
        xml_element = None
        attribute_regex = r"^_(\S+)___(\S+)$"
        element_regex = r"^(\S+)___(\S+)$"
        for attribute_and_element_dict in list_of_element_dictionaries:
            if parent_xml_element is None:
                # create the root element of the XML element tree
                xml_element = etree.Element(tag_name)
            else:
                xml_element = etree.SubElement(parent_xml_element, tag_name)

            for k in sorted(attribute_and_element_dict.keys()):
                if k == "_":
                    # create a text node
                    xml_element.text = attribute_and_element_dict[k]
                elif k.startswith("_"):
                    # create an attribute node
                    matches = re.search(attribute_regex, k)
                    if matches:
                        # attribute with namespace
                        matching_groups = matches.groups()
                        namespace_prefix = matching_groups[0]
                        if namespace_prefix == "NONE":
                            namespace_prefix = None
                        attribute_name = matching_groups[1]
                        if namespace_prefix == "xmlns":
                            update_namespaces(attribute_name, attribute_and_element_dict[k])
                        else:
                            xml_element.set(NAMESPACE_STRINGS[namespace_prefix] + attribute_name,
                                            attribute_and_element_dict[k])
                    else:
                        # attribute without namespace
                        xml_element.attrib[k[1:]] = attribute_and_element_dict[k]
                else:
                    # create an element node
                    matches = re.search(element_regex, k)
                    if matches:
                        matching_groups = matches.groups()
                        namespace_prefix = matching_groups[0]
                        if namespace_prefix == "NONE":
                            namespace_prefix = None
                        element_name = matching_groups[1]
                        create_xml_element(xml_element,
                                           namespace_prefix, element_name,
                                           attribute_and_element_dict[k])
                    else:
                        create_xml_element(xml_element, None, k, attribute_and_element_dict[k])
        return xml_element
    
    data = json.loads(json_string)
    root_key = data.keys()[0]
    root_xml_element = create_xml_element(None, None, root_key, data[root_key])
    xs = etree.tostring(root_xml_element, xml_declaration=True, encoding="UTF-8", pretty_print=True)
    # target_path = os.path.join(base_data_dir, target_file_path)
    with open(target_file_path, "w") as f:
        f.write(xs)
    return root_xml_element


if __name__ == "__main__":
    # define the path of this script
    script_path = os.path.dirname(os.path.abspath( __file__ ))

    # convert "test.xml" into a JSON string and convert this back into an XML file "test2.xml"
    source_file_path = os.path.join(script_path, "data", "test.xml")
    target_xml_file_path = os.path.join(script_path, "data", "test2.xml")
    target_json_file_path = os.path.join(script_path, "data", "test2.json")
    json_str = xmlfile_to_jsonstr(source_file_path, namespaces=REVERSE_NAMESPACE_STRINGS)
    with open(target_json_file_path, "w") as f:
        f.write(json_str)
    jsonstr_to_xmlfile(json_str, target_xml_file_path)

    # now apply the same procedure to create "test3.xml" from "test2.xml"
    source_file_path = os.path.join(script_path, "data", "test2.xml")
    target_xml_file_path = os.path.join(script_path, "data", "test3.xml")
    target_json_file_path = os.path.join(script_path, "data", "test3.json")
    json_str = xmlfile_to_jsonstr(source_file_path, namespaces=REVERSE_NAMESPACE_STRINGS)
    with open(target_json_file_path, "w") as f:
        f.write(json_str)
    jsonstr_to_xmlfile(json_str, target_xml_file_path)

    # when comparing "test2.xml" and "test3.xml" there should not be a difference
    import filecmp
    t2 = os.path.join(script_path, "data", "test2.xml")
    t3 = os.path.join(script_path, "data", "test3.xml")
    print(filecmp.cmp(t2, t3))
