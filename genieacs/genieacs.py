# -*- coding: utf-8 -*-
#
# python-genieacs
# A Python API to interact with the GenieACS REST API
# https://github.com/TDT-GmbH/python-genieacs

import requests
import json

class InvalidOperatorError(Exception):
    """Raised when an invalid operator has been entered"""
    def __init__ (self, operator):
        self.operator = operator
        self.msg = ("InvalidOperatorError: Precondition has an invalid operator. Given: \"" + self.operator + "\" Expected: =, !=, <, >, <=, >=")

class Parameter(object):

    def __init__(self, name, value, key = False):
        self.name = name
        self.value = value
        self.key = key

    def name(self):
        return self.name

    def value(self):
        return self.value

    def key(self):
        return self.key

class Object(object):

    def __init__(self, name, parameters):
        self.name = name
        self.parameters = parameters

    def name(self):
        return self.name

    def parameters(self):
        return self.parameters

class Precondition(object):

    def __init__(self, name, operator, value):
        self.name = name
        self.operator = operator
        self.value = value

    def name(self):
        return self.name

    def operator(self):
        return self.operator

    def value (self):
        return self.value

class Configuration(object):
    pass

class AddObject(Configuration):

    def __init__(self, name, object):
        self.type = "add_object"
        self.name = name
        self.object = object

class AddTag(Configuration):

    def __init__(self, tag):
        self.type = "add_tag"
        self.tag = tag

class Command(Configuration):

    def __init__(self, command, value):
        self.type = "custom_command_value"
        self.command = command
        self.value = value

class Execute(Configuration):

    def __init__(self, command, age):
        self.type = "custom_command_age"
        self.command = command
        self.age = age

class Refresh(Configuration):

    def __init__(self, name, age):
        self.type = "age"
        self.name = name
        self.age = age

class RemoveObject(Configuration):

    def __init__(self, name, object):
        self.type = "delete_object"
        self.name = name
        self.object = object

class RemoveTag(Configuration):

    def __init__(self, tag):
        self.type = "delete_tag"
        self.tag = tag

class Set(Configuration):

    def __init__(self, name, value):
        self.type = "value"
        self.name = name
        self.value = value

class SoftwareVersion(Configuration):

    def __init__(self, software_version):
        self.type = "software_version"
        self.software_version = software_version

class Preset(object):

    def __init__(self, name, weight, preconditions, configurations):
        self.name = name
        self.weight = weight
        self.preconditions = preconditions
        self.configurations = configurations

    def name(self):
        return self.name

    def weight(self):
        return self.weight

    def precondition(self):
        return self.precondition

    def configurations(self):
        return self.configurations

class Connection(object):
    """Connection object to interact with the GenieACS server."""
    def __init__(self, ip, port=7557, ssl=False, verify=False, auth=False, user="", passwd="", url=""):
        self.server_ip = ip
        self.server_port = port
        self.use_ssl = ssl
        self.ssl_verify = verify
        self.use_auth = auth
        self.username = user
        self.password = passwd
        self.server_url = url
        self.base_url = ""
        self.session = None
        self.__set_base_url()
        self.__create_session()

    def __del__(self):
        if self.session is not None:
            self.session.close()

    def __set_base_url(self):
        if not self.use_ssl:
            self.base_url = "http://"
        else:
            self.base_url = "https://"
        self.base_url += self.server_ip + ":" + str(self.server_port) + self.server_url

    def __create_session(self):
        if self.session is None:
            self.session = requests.Session()
            if self.use_auth:
                self.session.auth = (self.username, self.password)
            if self.use_ssl:
                self.session.verify = self.ssl_verify
        try:
            # do a request to test the connection
            self.file_get_all()
        except requests.exceptions.ConnectionError as err:
            print("Connection:\nConnectionError: " + str(err) + "\nCould not connect to server.\n")
        except requests.exceptions.HTTPError as err:
            print("Connection:\nHTTPError: " + str(err) + "\n")

    def __request_post(self, url, data, conn_request=True):
        if conn_request:
            request_url = self.base_url + url + "?connection_request"
        else:
            request_url = self.base_url + url
        r = self.session.post(request_url, json=data)
        r.raise_for_status()

    def __request_put(self, url, data):
        request_url = self.base_url + url
        r = self.session.put(request_url, data)
        r.raise_for_status()

    ##### methods for devices #####

    def device_get_by_id(self, device_id):
        """Get all data of a device identified by its ID"""
        quoted_id = requests.utils.quote("{\"_id\":\"" + device_id + "\"}", safe = '')
        r = self.session.get(self.base_url + "/devices/" + "?query=" + quoted_id)
        r.raise_for_status()
        data = r.json()
        return data

    def device_get_by_MAC(self, device_MAC):
        """Get all data of a device identified by its MAC address"""
        quoted_MAC = requests.utils.quote("{\"summary.mac\":\"" + device_MAC + "\"}", safe = '')
        r = self.session.get(self.base_url + "/devices/" + "?query=" + quoted_MAC)
        r.raise_for_status()
        data = r.json()
        return data

    def device_get_parameters(self, device_id, parameter_names):
        """Get a defined list of parameters from a given device"""
        quoted_id = requests.utils.quote("{\"_id\":\"" + device_id + "\"}", safe = '')
        r = self.session.get(self.base_url + "/devices" + "?query=" + quoted_id + "&projection=" + parameter_names)
        r.raise_for_status()
        data = r.json()
        return data

    def device_delete(self, device_id):
        """Delete a given device from the database"""
        r = self.session.delete(self.base_url + "/devices/" + device_id)
        r.raise_for_status()

    ##### methods for tasks #####

    def task_get_all(self, device_id):
        """Get all existing tasks of a given device"""
        quoted_id = requests.utils.quote("{\"device\":\"" + device_id + "\"}", safe = '')
        r = self.session.get(self.base_url + "/tasks/" + "?query=" + quoted_id)
        r.raise_for_status()
        data = r.json()
        return data

    def task_refresh_object(self, device_id, object_name, conn_request=True):
        """Create a refreshObject task for a given device"""
        data = { "name": "refreshObject",
                 "objectName": object_name }
        try:
            self.__request_post("/devices/" + device_id + "/tasks", data, conn_request)
        except requests.exceptions.HTTPError:
            print("task_refresh_object:\nHTTPError: device_id might be incorrect\n")

    def task_set_parameter_values(self, device_id, parameter_values, conn_request=True):
        """Create a setParameterValues task for a given device"""
        data = { "name": "setParameterValues",
                 "parameterValues": parameter_values }
        try:
            self.__request_post("/devices/" + device_id + "/tasks", data, conn_request)
        except requests.exceptions.HTTPError:
            print("task_set_parameter_values:\nHTTPError: device_id might be incorrect\n")

    def task_get_parameter_values(self, device_id, parameter_names, conn_request = True):
        """Create a getParameterValues task for a given device"""
        data = { "name": "getParameterValues",
                "parameterNames": parameter_names}
        try:
            self.__request_post("/devices/" + device_id + "/tasks", data, conn_request)
        except requests.exceptions.HTTPError:
            print("task_get_parameter_values:\nHTTPError: device_id might be incorrect\n")

    def task_add_object(self, device_id, object_name, object_path, conn_request=True):
        """Create an addObject task for a given device"""
        data = { "name": "addObject", object_name : object_path}
        try:
            self.__request_post("/devices/" + device_id + "/tasks", data, conn_request)
        except requests.exceptions.HTTPError:
            print("task_add_object:\nHTTPError: device_id might be incorrect\n")

    def task_reboot(self, device_id, conn_request=True):
        """Create a reboot task for a given device"""
        data = { "name": "reboot"}
        try:
            self.__request_post("/devices/" + device_id + "/tasks", data, conn_request)
        except requests.exceptions.HTTPError:
            print("task_reboot:\nHTTPError: device_id might be incorrect\n")

    def task_factory_reset(self, device_id, conn_request=True):
        """Create a factoryReset task for a given device"""
        data = { "name": "factoryReset"}
        try:
            self.__request_post("/devices/" + device_id + "/tasks", data, conn_request)
        except requests.exceptions.HTTPError:
            print("task_factory_reset:\nHTTPError: device_id might be incorrect\n")

    def task_download(self, device_id, file_id, filename, conn_request=True):
        """Create a download task for a given device"""
        data = { "name": "download", "file": file_id, "filename": filename}
        try:
            self.__request_post("/devices/" + device_id + "/tasks", data, conn_request)
        except requests.exceptions.HTTPError:
            print("task_download:\nHTTPError: device_id might be incorrect\n")

    def task_retry(self, task_id):
        """Retry a faulty task at the next inform"""
        try:
            r = self.session.post(self.base_url + "/tasks/" + task_id + "/retry")
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            print("task_retry:\nHTTPError: task_id might be incorrect\n")

    def task_delete(self, task_id):
        """Delete a Task for a given device"""
        try:
            r = self.session.delete(self.base_url + "/tasks/" + task_id)
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            print("task_delete:\nHTTPError: task_id might be incorrect\n")

    ##### methods for tags ######

    def tag_assign(self, device_id, tag_name):
        """Assign a tag to a device"""
        try:
            self.__request_post("/devices/" + device_id + "/tags/" + tag_name, None, False)
        except requests.exceptions.HTTPError:
            print("tag_assign:\nHTTPError: device_id might be incorrect\n")

    def tag_remove(self, device_id, tag_name):
        """Remove a tag from a device"""
        try:
            r = self.session.delete(self.base_url + "/devices/" + device_id + "/tags/" + tag_name)
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            print("tag_remove:\nHTTPError: device_id might be incorrect\n")

    ##### methods for presets #####

    def preset_get_all(self, filename=None):
        """Get all existing presets as a json object, optionally write them to a file"""
        r = self.session.get(self.base_url + "/presets")
        r.raise_for_status()
        data = r.json()
        try:
            if filename is not None:
                f = open(filename, 'w')
                json.dump(data, f)
                f.close()
        except IOError as err:
            print("preset_get_all:\nIOError: " + str(err) + "\n")
        finally:
            return data

    def preset_create(self, preset):
        """Create a new preset or update a preset with a given name"""
        try:
            data = str({"weight" : preset.weight, "precondition" : "{}", "configurations" : []})
            data = data.replace("\'", "\"")
            if precondition.operator == "=":
                operator = "e"
            elif precondition.operator == "!=":
                operator = "ne"
            elif precondition.operator == "<":
                operator = "lt"
            elif precondition.operator == ">":
                operator = "gt"
            elif precondition.operator == "<=":
                operator = "lte"
            elif precondition.operator == ">=":
                operator = "gte"
            for precondition in preset.preconditions:
                if "{}" in data:
                    if operator == "e":
                        precons = ("{\"%(n)s\":\"%(v)s\"}" % {"n" : precondition.name,"v" : precondition.value})
                        precons = json.dumps(precons)
                        data = data.replace("\"{}\"", "%s" % precons)
                    elif operator in ("ne", "lt", "gt", "lte", "gte"):
                        precons = "{\"%(n)s\":{\"$%(o)s\":\"%(v)s\"}}" % {"n" : precondition.name,"o" : operator,"v" : precondition.value}
                        precons = json.dumps(precons)
                        data = data.replace("\"{}\"", "%s" % precons)
                    else:
                        raise InvalidOperatorError(operator)
                elif ", \\\"" not in data:
                    if operator == "e":
                        precons = (", \"%(n)s\":\"%(v)s\"}" % {"n" : precondition.name,"v" : precondition.value})
                        precons = json.dumps(precons)
                        precons = precons.replace("\",", ",")
                        if "\"}\", \"weight\"" in data:
                            data = data.replace("}\", \"weight\"", "%s, \"weight\"" % precons)
                        elif "}}\", \"weight\"" in data:
                            precons = ("}" + precons)
                            data = data.replace("}}\", \"weight\"", "%s, \"weight\"" % precons)
                    elif operator in ("ne", "lt", "gt", "lte", "gte"):
                        precons = ", \"%(n)s\":{\"$%(o)s\":\"%(v)s\"}}" % {"n" : precondition.name,"o" : operator,"v" : precondition.value}
                        precons = json.dumps(precons)
                        precons = precons.replace("\",", ",")
                        if "\"}\", \"weight\"" in data:
                            data = data.replace("}\", \"weight\"", "%s, \"weight\"" % precons)
                        elif "\"}}\", \"weight\"" in data:
                            precons = ("}" + precons)
                            data = data.replace("}}\", \"weight\"", "%s, \"weight\"" % precons)
                    else:
                        raise InvalidOperatorError(operator)
                else:
                    if operator == "e":
                        precons = (", \"%(n)s\":\"%(v)s\"}" % {"n" : precondition.name,"v" : precondition.value})
                        precons = json.dumps(precons)
                        precons = precons.replace("\",", ",")
                        if "\"}\", \"weight\"" in data:
                            data = data.replace("}\", \"weight\"", "%s, \"weight\"" % precons)
                        elif "\"}}\", \"weight\"" in data:
                            precons = ("}" + precons)
                            data = data.replace("}}\", \"weight\"", "%s, \"weight\"" % precons)
                    elif operator in ("ne", "lt", "gt", "lte", "gte"):
                        precons = ", \"%(n)s\":{\"$%(o)s\":\"%(v)s\"}}" % {"n" : precondition.name,"o" : operator,"v" : precondition.value}
                        precons = json.dumps(precons)
                        precons = precons.replace("\",", ",")
                        if "\"}\", \"weight\"" in data:
                            data = data.replace("}\", \"weight\"", "%s, \"weight\"" % precons)
                        elif "\"}}\", \"weight\"" in data:
                            precons = ("}" + precons)
                            data = data.replace("}}\", \"weight\"", "%s, \"weight\"" % precons)
                    else:
                        raise InvalidOperatorError(operator)
            for configuration in preset.configurations:
                if "}]" in data:
                    config = str(vars(configuration))
                    config = config.replace("\'", "\"")
                    data = data.replace("}]", "}, %s]" % config)
                if "[]" in data:
                    config = str(vars(configuration))
                    config = config.replace("\'", "\"")
                    data = data.replace("[]", "[%s]" % config)
            self.__request_put("/presets/" + preset.name, data)
        except requests.exceptions.HTTPError:
            print("preset_create:\nHTTPError: given parameters might be incorrect\n")
        except InvalidOperatorError as err:
            print("preset_create:\n" + err.msg)

    def preset_create_all_from_file(self, filename):
        """Create all presets contained in a json file"""
        try:
            f = open(filename, 'r')
            data = json.load(f)
            f.close()
            for preset in data:
                preset_name = preset["_id"]
                del preset["_id"]
                self.__request_put("/presets/" + preset_name, json.dumps(preset))
        except IOError as err:
            print("preset_create_all_from_file:\nIOError: " + str(err) + "\n")
        except ValueError:
            print("preset_create_all_from_file:\nValueError: File contains faulty values\n")
        except KeyError:
            print("preset_create_all_from_file:\nKeyError: File contains faulty keys\n")

    def preset_delete(self, preset_name):
        """Delete a given preset"""
        r = self.session.delete(self.base_url + "/presets/" + preset_name)
        r.raise_for_status()

    ##### methods for objects #####

    def object_get_all(self, filename=None):
        """Get all existing objects as a json object, optionally write them to a file"""
        r = self.session.get(self.base_url + "/objects")
        r.raise_for_status()
        data = r.json()
        try:
            if filename is not None:
                f = open(filename, 'w')
                json.dump(data, f)
                f.close()
        except IOError as err:
            print("object_get_all:\nIOError: " + str(err) + "\n")
        finally:
            return data

    def object_create(self, object):
        """Create a new object or update an object with a given name"""
        try:
            data = str({parameter.name: parameter.value for parameter in object.parameters})
            data = data.replace("\'", "\"")
            for param in object.parameters:
                if param.key == True:
                    if "keys" not in data:
                        data = data.replace("}", ", \"_keys\":[\"%s\"]}" % param.name)
                    else:
                        data = data.replace("]}", ", \"%s\"]}" % param.name)
            self.__request_put("/objects/" + object.name, data)
        except requests.exceptions.HTTPError:
                print("object_create:\nA HTTPError accured, given parameters might be incorrect\n")

    def object_create_all_from_file(self, filename):
        """Create all objects contained in a json file"""
        try:
            f = open(filename, 'r')
            data = json.load(f)
            f.close()
            for gobject in data:
                object_name = gobject["_id"]
                del gobject["_id"]
                self.__request_put("/objects/" + object_name, json.dumps(gobject))
        except IOError as err:
            print("object_create_all_from_file:\nIOError: " + str(err) + "\n")
        except ValueError:
            print("object_create_all_from_file:\nValueError: File contains faulty values\n")
        except KeyError:
            print("object_create_all_from_file:\nKeyError: File contains faulty keys\n")

    def object_delete(self, object_name):
        """Delete a given object"""
        r = self.session.delete(self.base_url + "/objects/" + object_name)
        r.raise_for_status()

    ##### methods for files #####

    def file_upload(self, filename, fileType, oui, productClass, version):
        """Upload or update a file"""
        try:
            r = self.session.request("PUT", self.base_url + "/files/" + filename, data = open( filename,"rb"), headers = {"fileType": fileType, "oui": oui, "productClass": productClass, "version" : version})
            r.raise_for_status()
        except IOError as err:
            print("file_upload:\nIOError: " + str(err) + "\n")

    def file_delete(self, filename):
        """Delete a given file"""
        r = self.session.delete(self.base_url + "/files/" + filename)
        r.raise_for_status()

    def file_get_all(self):
        """Get all files as a json object"""
        r = self.session.get(self.base_url + "/files")
        r.raise_for_status()
        data = r.json()
        return data
