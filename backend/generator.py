from lxml import etree
import json
import os.path
import textwrap

header = textwrap.dedent("""
    package ai.aitia.demo.car_provider.controller;

    import java.util.*;
    import java.lang.*;
    import org.json.JSONObject;
    import org.json.JSONArray;

    /**
    * This plain JAVA class is a template, which will be replaced by a generated class.
    * It provides access to equipment data and an interface description.
    *
    * @author  Mario Thron (ifak e.V. Magdeburg, Germany)
    */
    public class GenericEquipmentInterface {

        private int dummy_int8 = 0;
        private int dummy_int16 = 0;
        private int dummy_int32 = 0;
        private long dummy_int64 = 0l;

        // unsigned data types are not supported by Java
        // we propose a data type, which can hold all values, but has different bit-structures
        private int dummy_uint8 = 0;
        private int dummy_uint16 = 0;
        private long dummy_uint32 = 0;

        // mapping uint64 to long looses a part of the value range
        // use BigInteger if really necessary
        private long dummy_uint64 = 0l;

        // org.json don't support float 32, so we use double as default
        private double dummy_float32 = 0.0d;
        private double dummy_float64 = 0.0d;
        private String dummy_string = "String";

        // we use an ArrayList to represent arrays in general
        private List dummyArray = new ArrayList();

        public GenericEquipmentInterface() {
            // two test entries for the dummyArray
            dummyArray.add("dummyValue");
            dummyArray.add("dummyValue");
        }

""")

footer = textwrap.dedent("""
    }
""")

def lib_elements(name):
    """Returns a dictionary of XML elements defined in library files in 'data_structures'.

    The 'name' parameter can be 'Struct' or 'DataBlock'.
    Keys are defined as strings according to the following pattern: <libID>::<libVersion>::<ID>.
    Values are XML elements out of those XML files with tag name specified by the 'name' parameter.
    So we hold all XML files in the working memory of the computer (memory consumption will be high).
    """
    xs = {}
    a = '../data/data_structures'
    for r in [os.path.join(a, b) for b in os.listdir(a) if os.path.isdir(os.path.join(a, b))]:
        for l in [os.path.join(r, b) for b in os.listdir(r) if os.path.isfile(os.path.join(r, b))]:
            lx = etree.parse(l)
            lib = lx.getroot().attrib['ID']
            ver = lx.getroot().attrib['Version']
            for s in lx.xpath('/Library/' + name):
                x = s.attrib['ID']
                k = '{0}::{1}::{2}'.format(lib, ver, x)
                xs[k] = s
    return xs

structs = {}
data_blocks = {}

object_index = 0
def ox():
    """Returns object names like 'o1', 'o2', ...  with increasing index
    """
    global object_index
    object_index += 1
    return 'o' + str(object_index)

def shift(x, s):
    """Returns multi-lline string s, where each line is shiftet x times four spaces.
    """
    v = ''
    for l in textwrap.dedent(s).splitlines():
        v += x * '    ' + l + '\n'
    return v


def generate_interface(x, block_instances, repo_name, equipment_description):
    """Generates a Java method for data access out of the XML tree x, which is an equipment description.
    """

    def code(name, parent, level, e):
        
        def scalar_code(name, parent, level, e):
            """Return the source code for a scalar value represented by an XML element 'e'.
            """
            xt = e.attrib['ScalarType']
            t = "String"
            types = {
                'int': ['int8', 'int16', 'int32', 'uint8', 'uint16'],
                'long': ['int64', 'uint32', 'uint64'],
                'double': ['float32', 'float64'],
                'String': ['string']
            }
            for x in types:
                if xt in types[x]:
                    t = x
            c = '{0}.put("{1}", ({2}) dummy_{3});\n'.format(parent, name, t, xt)
            return shift(level, c)

        def list_code(name, parent, level, e):
            """Returns the source code for a scalar value represented by an XML element 'e'.
            """
            oindex = ox()
            c = ''
            c += 'JSONArray {0} = new JSONArray();\n'.format(oindex)    # JSONArray o3 = new JSONArray();
            c += '{0}.put("{1}", {2});\n'.format(parent, name, oindex)  # o1.put("anArray", o3);
            c += 'for (Object x : dummyArray) {'
            c += code(None, oindex, level+1, e.getchildren()[0])
            c += '}'
            return shift(level, c)

        def struct_code(name, parent, level, e):
            """Returns the source code of a struct represented by an XML element 'e'.
            """
            oindex = ox()
            c = ''
            c += 'JSONObject {0} = new JSONObject();\n'.format(oindex)
            c += '{0}.put("{1}", {2});\n'.format(parent, name, oindex)

            # dereference the struct definition 's' from the given StructReference element 'e'
            k = '{0}::{1}::{2}'.format(e.attrib['LibraryID'], e.attrib['LibraryVersion'], e.attrib['StructID'])
            s = structs[k]

            for entry in s.xpath('./StructElement'):
                entry_name = entry.attrib['Name']
                c += code(entry_name, oindex, 0, entry.getchildren()[0])
            return shift(level, c)

        # implementation of scalar_code:
        if e.tag == 'Scalar':
            return scalar_code(name, parent, level, e)
        elif e.tag == 'List':
            return list_code(name, parent, level, e)
        elif e.tag == 'StructReference':
            return struct_code(name, parent, level, e)

    # implementation of generate_interface:
    c = textwrap.dedent("""
    public String getData(String blockName, String entryName) {
        String retval;
        JSONObject o = new JSONObject();

        // Please call the necessary communication functions of your equipment.
        // Then replace in the following all the 'dummy_' values by the communication response values.
    """)
    for bi in block_instances:
        k = '{0}::{1}::{2}'.format(bi.attrib['LibraryID'], bi.attrib['LibraryVersion'], bi.attrib['BlockID'])
        bd = data_blocks[k]
        for de in bd.xpath('./DataEntry'):
            c += '\n    if (blockName.equals("{0}") && entryName.equals("{1}")) {{\n'.format(bi.attrib['Name'], de.attrib['Name'])
            c += '        o = new JSONObject();\n'
            c += code(de.attrib['Name'], 'o', 2, de.getchildren()[0])
            c += '    }\n'
    c += '    return o.toString();\n'
    c += '}\n'
    return c

def generate_interface_description(x, block_instances, epo_name, equipment_description):
    """Generates a Java method for data access out of the XML tree x, which is an equipment description.
    """
    def type_description(target_dict, e):
        def scalar_description(target_dict, e):
            target_dict['type'] = e.attrib['ScalarType']
        def list_description(target_dict, e):
            target_dict['type'] = 'array'
            target_dict['items'] = {}
            type_description(target_dict['items'], e.getchildren[0])
        def struct_description(target_dict, e):
            target_dict['type'] = 'object'
            target_dict['properties'] = {}
            k = '{0}::{1}::{2}'.format(e.attrib['LibraryID'], e.attrib['LibraryVersion'], e.attrib['StructID'])
            s = structs[k]
            for entry in s.xpath('./StructElement'):
                entry_dict = {}
                target_dict['properties'][entry.attrib['Name']] = entry_dict
                type_description(entry_dict, entry.getchildren()[0])

        # implementation of type_description
        if e.tag == 'Scalar':
            return scalar_description(target_dict, e)
        elif e.tag == 'List':
            return list_description(target_dict, e)
        elif e.tag == 'StructReference':
            return struct_description(target_dict, e)

    # implementation of generate_interface_description
    d = {}
    d['type'] = 'EquipmentDescription'
    d['description'] = 'Generated description of interface {0}'.format(x.getroot().attrib['Name'])
    d['properties'] = {}
    for bi in block_instances:
        k = '{0}::{1}::{2}'.format(bi.attrib['LibraryID'], bi.attrib['LibraryVersion'], bi.attrib['BlockID'])
        bd = data_blocks[k]
        d['properties'][bi.attrib['Name']] = {}
        for de in bd.xpath('./DataEntry'):
            de_dict = {}
            d['properties'][bi.attrib['Name']][de.attrib['Name']] = de_dict
            type_description(de_dict, de.getchildren()[0])
    s = json.dumps(d, indent=4, sort_keys=True)
    g = ''
    for line in s.splitlines():
        g += '    c.append("' + line.replace('"', '\\"') + '");\n'

    # TODO: for efficiency, the description should better be created in the constructor
    c = textwrap.dedent("""
    public String getInterfaceDescription() {{
        StringBuilder c = new StringBuilder("");
    {0}
        return c.toString();
    }}
    """).format(g)
    return c

def generate_test_html(x, block_instances, repo_name, equipment_description):

    def t(name, attrib=None, content=None):
        s = '<{0}'.format(name)
        if attrib:
            for x in attrib:
                s += ' {0}="{1}"'.format(x, attrib[x])
        s += '>'
        if content:
            for x in content:
                s += '\n' + x
        s += '\n</{0}>'.format(name)
        return s

    def html_base(x):
        s = t('html', None, [
            t('head', None, [
                t('title', None, ['Test interface for an Arrowhead Device'])
            ]),
            t('body', None, [
                t('p', None, [
                    'The JSON-based ',
                    t('a', {'href': 'http://127.0.0.1:8888/data/interfaceDescription'}, ['self description']),
                    ' describes blocks and block members of the Arrowhead application service.'
                ]),
                t('p', None, [
                    'The following list contains items of the form BLOCK/BLOCK_MEMBER. Each item links to the respective value data sets.',
                    t('br'),
                    x
                ]),
            ])
        ])
        return s

    # implementation of generate_test_html
    g = ''
    for bi in block_instances:
        k = '{0}::{1}::{2}'.format(bi.attrib['LibraryID'], bi.attrib['LibraryVersion'], bi.attrib['BlockID'])
        bd = data_blocks[k]
        block_instance_name = bi.attrib['Name']
        for de in bd.xpath('./DataEntry'):
            entry_name = de.attrib['Name']
            be = '{0}/{1}'.format(block_instance_name, entry_name)
            url = 'http://127.0.0.1:8888/data/' + be
            g += t('a', {'href': url}, [be])
            g += t('p')
    g = html_base(g)

    s = ''
    for line in g.splitlines():
        s += '    c.append("' + line.replace('"', '\\"') + '");\n'

    # TODO: for efficiency, the HTML string should better be created in the constructor
    c = textwrap.dedent("""
    public String test() {{
        StringBuilder c = new StringBuilder("");
    {0}
        return c.toString();
    }}
    """).format(s)
    return c

def generate(repo_name, equipment_description):
    global structs
    global data_blocks
    structs = lib_elements('Struct')
    data_blocks = lib_elements('DataBlock')
    x = etree.parse(os.path.join('../data/equipment_interfaces', repo_name, equipment_description))
    block_instances = x.xpath('/EquipmentDescription/BlockInstance')
    c = generate_interface(x, block_instances, repo_name, equipment_description)
    c += generate_interface_description(x, block_instances, repo_name, equipment_description)
    c += generate_test_html(x, block_instances, repo_name, equipment_description)
    c = header + shift(1, c) + footer
    with open('data/GenericEquipmentInterface.java', 'w') as f:
        f.write(c)
    # print(c)
