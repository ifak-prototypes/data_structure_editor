import convert
import exc
from lxml import etree
import json
import os
import shutil
import time


script_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = os.path.abspath(os.path.join(script_dir, "..", "data"))


def ensure_data_path(path):
    path = os.path.join(data_dir, path)
    if not os.path.isdir(path):
        os.makedirs(path)
    return path


class WebApplication(object):

    def __init__(self, session_manager):
        self.sm = session_manager
        self.data_structures_dir = ensure_data_path("data_structures")
        self.equipment_interfaces_dir = ensure_data_path("equipment_interfaces")
        self.comm_profiles_dir = ensure_data_path("comm_profiles")
        self.config_dir = ensure_data_path("config")

    def get_error_response(self, sid):
        """ This is an example, which should be removed in the final version."""
        raise(exc.Error(404, "file XXX not found."))


    def repository_list_all(self, sid, ctype):
        """ Returns a list of repositories within the ctype-directory."""
        if self.sm.check(sid, 'admin'):
            result = []
            nonsense = [".", ".."]
            base_path = os.path.join("../data/", ctype)
            for x in os.listdir("../data/" + ctype):
                path = os.path.join(base_path, x)
                if os.path.isdir(path) and x not in nonsense:
                    result.append(x)
            return result

    def repository_clone(self, sid, ctype, name, url):
        """ clones a repository from a given url """
        if not os.path.isdir(os.path.join("../data/", ctype, name)):
            os.system("cd '../data/{0}' && git clone '{1}' '{2}'".format(ctype, url, name))
        return "Repository cloned"

    def repository_create(self, sid, ctype, name):
        """ creates a repository of its own """
        if not os.path.isdir(os.path.join("../data/", ctype, name)):
            os.system("cd '../data/{0}' && mkdir '{1}'".format(ctype, name))
        if not os.path.isdir(os.path.join("../data/", ctype, name, ".git")):
            os.system("cd '../data/{0}/{1}' && git init".format(ctype, name))
        return "Repository created"

    def repository_push(self, sid, ctype, name):
        """ pushes a repository to its origin """
        pass

    def repository_rename(self, sid, ctype, old_name, new_name):
        """ edits the description file in the repository """
        source_path = os.path.join("../data/", ctype, old_name)
        target_path = os.path.join("../data/", ctype, new_name)
        if not os.path.isdir(target_path):
            shutil.move(source_path, target_path)
        else:
            raise Exception("Can not move repository. The destination repository already exists.")
        return "Repository renamed"

    def repository_delete(self, sid, ctype, name):
        """ deletes a repository from the file system """
        d = os.path.join(data_dir, ctype, name)
        if os.path.isdir(d):
            shutil.rmtree(d, ignore_errors=True)


    def file_list_all(self, sid, ctype, repo):
        """ Returns a list of file names within a repository folder within a ctype directory.
        
        Within this draft implementation we assume all files to be valid files.
        """
        if self.sm.check(sid, 'admin'):
            result = []
            base_path = os.path.join("../data/", ctype, repo)
            for x in os.listdir(base_path):
                path = os.path.join(base_path, x)
                if os.path.isfile(path):
                    result.append(x)
            return result

    def file_create(self, sid, ctype, repo, name):
        """ This method creates a new file.
        """
        if self.sm.check(sid, 'admin'):
            dst = os.path.join(data_dir, ctype, repo, name)
            if not os.path.isfile(dst):
                src = os.path.join(script_dir, "data", ctype + '.xml')
                shutil.copyfile(src, dst)
                return "File created."
            else:
                raise(exc.Error(404, "Can not create file {dst}. It already exists.".format(dst=dst)))

    def file_read(self, sid, ctype, repo, name):
        """ This method returns the content of an XML file as JSON.
        """
        if self.sm.check(sid, 'admin'):
            dst = os.path.join(data_dir, ctype, repo, name)
            if not os.path.isfile(dst):
                raise(exc.Error(404, "The file {dst} does not exists.".format(dst=dst)))
            else:
                jsonstr = convert.xmlfile_to_jsonstr(dst)
                return jsonstr

    def file_write(self, sid, ctype, repo, name, data):
        """ This method writes the data (a dict) into a file.
        """
        if self.sm.check(sid, 'admin'):
            dst = os.path.join(data_dir, ctype, repo, name)
            convert.jsonstr_to_xmlfile(data, dst)
            return "Wrote file '{0}'.".format(dst)

    def file_read_template(self, sid, ctype):
        """ This method returns the content of an XML file as JSON.
        """
        if self.sm.check(sid, 'admin'):
            dst = os.path.join(script_dir, 'data', ctype + '.xml')
            if not os.path.isfile(dst):
                raise(exc.Error(404, "The file {dst} does not exists.".format(dst=dst)))
            else:
                jsonstr = convert.xmlfile_to_jsonstr(dst)
                return jsonstr

    def file_rename(self, sid, ctype, repo, old_name, new_name, data):
        """ This method renames a file.
        """
        if self.sm.check(sid, 'admin'):
            source_path = os.path.join("../data/", ctype, repo, old_name)
            target_path = os.path.join("../data/", ctype, repo, new_name)
            if source_path == target_path or not os.path.isfile(target_path):
                if not source_path == target_path:
                    shutil.move(source_path, target_path)
                self.file_write(sid, ctype, repo, new_name, data)
            else:
                raise Exception("Can not rename file. The target file already exists.")
            return "File renamed."

    def file_delete(self, sid, ctype, repo, name):
        """ This method deletes a file.
        """
        if self.sm.check(sid, 'admin'):
            dst = os.path.join(data_dir, ctype, repo, name)
            if not os.path.isfile(dst):
                raise(exc.Error(404, "The file {dst} does not exists.".format(dst=dst)))
            else:
                os.remove(dst)
                return "File deleted."


    def struct_rename(self, sid, ctype, repo, name, jsonstr):
        """ This method updates an XML file by a given JSON string.
        """
        if self.sm.check(sid, 'admin'):
            dst = os.path.join(data_dir, repo, name)
            if not os.path.isfile(dst):
                raise(exc.Error(404, "The file {dst} does not exists.".format(dst=dst)))
            else:
                jsonstr = convert.jsonstr_to_xmlfile(jsonstr, dst)
                return "XML file updated."

    def struct_list_all(self, sid, ctype):
        """ This function returns a list of all repositories,
            including all struct libraries including all structs
        """
        if self.sm.check(sid, 'admin'):
            dst = os.path.join(data_dir, ctype)
            result = []

            # evaluate each repository within ctype (currently 'data_structures')
            for r in sorted(os.listdir(dst)):
                if os.path.isdir(os.path.join(dst, r)):
                    repo = {}
                    result.append(repo)
                    repo['RepoName'] = r
                    repo['Libraries'] = []

                    # evaluate each structure library XML file of the repository
                    for l in sorted(os.listdir(os.path.join(dst, r))):
                        if os.path.isfile(os.path.join(dst, r, l)):
                            lib = {}
                            repo['Libraries'].append(lib)
                            lib['LibraryName'] = l
                            lib['Structs'] = []

                            # parse a struct library XML file
                            with open(os.path.join(dst, r, l), 'r') as f:
                                tree = etree.parse(f)

                                lib['LibraryID'] = tree.getroot().attrib['ID']
                                lib['LibraryVersion'] = tree.getroot().attrib['Version']

                                struct_els = tree.xpath('/Library/Struct')

                                # sort the 'Struct' elements by name:
                                d = {}
                                for v in struct_els:
                                    k = v.attrib['Name']
                                    d[k] = v
                                slist = []
                                for k in sorted(d.keys()):
                                    slist.append(d[k])
                                
                                # evaluate each 'Struct' element of the XML file
                                for e in slist:
                                    struct = {}
                                    lib['Structs'].append(struct)
                                    struct['Name'] = e.attrib['Name']
                                    struct['ID'] = e.attrib['ID']
                                    struct['Comment'] = e.attrib['Comment']
            return result

    def block_list_all(self, sid, ctype):
        """ This function returns a list of all repositories,
            including all block libraries including all blocks
        """
        if self.sm.check(sid, 'admin'):
            dst = os.path.join(data_dir, ctype)
            result = []

            # evaluate each repository within ctype (currently 'data_structures')
            for r in sorted(os.listdir(dst)):
                if os.path.isdir(os.path.join(dst, r)):
                    repo = {}
                    result.append(repo)
                    repo['RepoName'] = r
                    repo['Libraries'] = []

                    # evaluate each library XML file of the repository
                    for l in sorted(os.listdir(os.path.join(dst, r))):
                        if os.path.isfile(os.path.join(dst, r, l)):
                            lib = {}
                            repo['Libraries'].append(lib)
                            lib['LibraryName'] = l
                            lib['Blocks'] = []

                            # parse a library XML file
                            with open(os.path.join(dst, r, l), 'r') as f:
                                tree = etree.parse(f)

                                lib['LibraryID'] = tree.getroot().attrib['ID']
                                lib['LibraryVersion'] = tree.getroot().attrib['Version']

                                block_els = tree.xpath('/Library/DataBlock')

                                # sort the 'DataBlock' elements by name:
                                d = {}
                                for v in block_els:
                                    k = v.attrib['Name']
                                    d[k] = v
                                slist = []
                                for k in sorted(d.keys()):
                                    slist.append(d[k])
                                
                                # evaluate each 'DataBlock' element of the XML file
                                for e in slist:
                                    block = {}
                                    lib['Blocks'].append(block)
                                    block['Name'] = e.attrib['Name']
                                    block['ID'] = e.attrib['ID']
                                    block['Comment'] = e.attrib['Comment']
            return result


if __name__ == "__main__":
    pass