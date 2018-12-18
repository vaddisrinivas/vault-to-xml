import traceback
import sys

try:
    import datetime
    import json
    from yaml import load, dump
    import lxml
    import yaml
    import warnings
    import logging

    warnings.simplefilter('ignore')
    try:
        from yaml import CLoader as Loader, CDumper as Dumper
    except ImportError:
        from yaml import Loader, Dumper
    import xml.etree.ElementTree as ET
    import os
    from lxml import etree

    from configparser import ConfigParser
    import hvac


    class plug:
        config = {}
        str_new_line = "----------------------------------------------------------"

        # logging.debug(x)
        # the below method just gets the values from config file
        # it takes the tag and variable name to get the value.
        # it takes the variable from Environment "VAULT_CONFIG"

        def config_yml(self, tag, var=''):
            try:
                config = yaml.load(open(os.environ["VAULT_CONFIG"], 'r'))
                if str(var) == '':
                    return config[tag]
                else:
                    return config[tag][var]
            except yaml.YAMLError as exc:
                print_to_log("Error in configuration file:", exc)

        def config_json(self, tag, var=''):
            try:
                config = json.load(open(os.environ["VAULT_CONFIG"], "r"))
                if str(var) == '':
                    return config[tag]
                else:
                    return config[tag][var]
            except:
                print_to_log("Error with json")

        # THIS METHOD GETS THE HVAC CLIENT AND RETURNS IT FOR FURTHER USE
        def client_hvac(self):
            client = hvac.Client(url=self.config_yml("default", "url"), verify=False,
                                 token=self.config_yml("default", "token"))
            return client

        # THE BELOW METHOD IS USED FOR  CHECKING AUTHENTICATION

        def is_authed(self):
            print_to_log("Checking Authentication")
            client = self.client_hvac()
            return client.is_authenticated()

        # THE BELOW METHOD IS FOR WRITING TO VAULT
        # 1 CHECKS FOR AUTH
        # 2 WRITES
        # 3 CHECKS AND REASSURES THE WRITE

        def vwrite(self, path, name, params):
            try:
                client = self.client_hvac()
                if self.is_authed():
                    print_to_log("Authentication Successful")
                    client.write(path + name, data=params)
                    if client.read(path + name)["data"] == params:
                        print_to_log("Successfully updated values")
                    else:
                        print_to_log(" curse the fate, Nothing will come of nothing")
                else:
                    print_to_log("Not Authenticated properly")
            except Exception as e:
                print_to_log("Error Occured, due to ", e)

        # this method is for reading the vault secrets
        def vread(self, params):
            path = params["path"]
            name = params["name_of_secret"]
            print_to_log("Checking for " + name)
            client = self.client_hvac()
            if self.vlist(path) != []:
                return client.read(path + name)["data"]
            else:
                print_to_log(" There is some error with path, nothing exists there")

        # this method is to delete
        # it checks for availibility and then deletes
        def vdelete(self, path, name):
            client = self.client_hvac()
            if self.vlist(path) != []:
                return client.delete(path + name)
            else:
                print_to_log(" There is some error with path, nothing exists there")

        # this method is to list the stuff available under this path
        # it checks for auth and sends back
        def vlist(self, path):

            client = self.client_hvac()
            if self.is_authed():
                print_to_log("Authentication looks good")
                return client.list(path)["data"]
            else:
                print_to_log("Not Authenticated  well")

        # this is a  method to xml file. You may tweak as it pleases
        def write_to_xml(self, params, res):
            try:
                print_to_log("Trying to Write to XML")
                tree = ET.parse(params["xml_file_path"])
                root = tree.getroot()
                flag = 0
                for elem in root.findall('.//' + params["parenting"]):
                    if elem.attrib.get('name') == params["name_of_tag"]:
                        flag = 1
                        print_to_log("Match for name of tag found....checking attributes")
                        for i in params["attribute_mapping"].keys():
                            if i == 0:
                                print_to_log("Please Enter values in attributelist of config file")
                            else:
                                try:
                                    if elem.get(i):
                                        print_to_log("Attribute " + i + "  Exists, over writing")
                                        elem.set(i, res[params["attribute_mapping"][i]])
                                    else:
                                        print_to_log("Attribute " + i + " Doesnt Exists, Creating one")
                                        elem.set(i, res[params["attribute_mapping"][i]])
                                except:
                                    print_to_log("There has been a error parsing")
                if flag == 0:
                    print_to_log("There is a issue with parenting, or, "
                          "the name of tag doesnt match to anything available\n\n exiting")
                    exit(0)
                tree.write(params["xml_file_path"])
                print_to_log("Rechecking the writes")
                fl = 0
                for elem in root.findall('.//' + params["parenting"]):
                    if elem.attrib.get('name') == params["name_of_tag"]:
                        for i in params["attribute_mapping"].keys():
                            if elem.get(i) == res[params["attribute_mapping"][i]]:
                                print_to_log("" + i + " is verified")
                            else:
                                fl = 1
                                print_to_log("Doesnt match for " + i)
                                print_to_log("Please rerun, if it persists, please contact the repo owner")
                                exit(0)

                if fl == 1:
                    print_to_log("Write to XML incomplete")
                else:
                    print_to_log("Write successful.............")
            except Exception:
                print_to_log("Error in Xml Parsing, check the file and hit back")
                traceback.print_exc(file=sys.stdout)


    play = plug()
    # logging.basicConfig(level=logging.DEBUG, filename=play.config_yml("default", "log_file_path"), filemode="a+")
    f = open(file=play.config_yml("default", "log_file_path"), mode="a")
    def print_to_log(x):
        try:
            f.write(x + "\n")
        except:
            print_to_log("Failed to write to logs")
        # logging.debug(x)


    print_to_log(plug.str_new_line)

    vals_from_config = play.config_yml("changes")
    for i in range(0, len(vals_from_config)):
        print_to_log(str(datetime.datetime.utcnow()))
        print_to_log("Starting to read congig file")
        print_to_log("Getting Keys from Vault")
        print_to_log("Fetching Secrets....")
        res = play.vread(vals_from_config[i])
        print_to_log("The Available parameters from Vault are " + str(res.keys()))
        play.write_to_xml(params=vals_from_config[i], res=res)
    print_to_log(plug.str_new_line)

# exceptions couldnt be caught much specifically, had to generalize it. :P sorry
except Exception as e:
    traceback.print_exc(file=sys.stdout)
