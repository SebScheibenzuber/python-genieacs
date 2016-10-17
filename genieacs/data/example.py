#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Usage examples for python-genieacs
import genieacs
import time
# set a device_id for the following methods
device_id = "000149-c1500-000149014AF8"

# Create a Connection object to interact with a GenieACS server
acs = genieacs.Connection("tr069.tdt.de", ssl=True, auth=True, user="tdt", passwd="tdt")

# refresh some device parameters
acs.task_refresh_object(device_id, "InternetGatewayDevice.DeviceInfo.")
# set a device parameter
acs.task_set_parameter_values(device_id, [["InternetGatewayDevice.BackupConfiguration.FileList", "backup.cfg"]])
# get a device parameter
acs.task_get_parameter_values(device_id, [["InternetGatewayDevice.BackupConfiguration.FileList"]])
# factory reset a device
acs.task_factory_reset(device_id)
# reboot a device
acs.task_reboot(device_id)
# add an object to a device
acs.task_add_object(device_id, "VPNObject", [["InternetGatewayDevice.X_TDT-DE_OpenVPN"]])
# download a file
acs.task_download(device_id, "9823de165bb983f24f782951", "Firmware.img")
# retry a faulty task
acs.task_retry("9h4769svl789kjf984ll")

# print all tasks of a given device
print(acs.task_get_all(device_id))
# search a device by its ID and print all corresponding data
print(acs.device_get_by_id(device_id))
# search a device by its MAC address and print all corresponding data
print(acs.device_get_by_MAC("00:01:49:ff:0f:01"))
# print 2 given parameters of a given device
print(acs.device_get_parameters(device_id, "InternetGatewayDevice.DeviceInfo.SoftwareVersion,InternetGatewayDevice.X_TDT-DE_Interface.2.ProtoStatic.Ipv4.Address"))
# delete a task
acs.task_delete("9h4769svl789kjf984ll")

# create preconditions for a new preset
preconditionOne = genieacs.Precondition("summary.productClass", "", "NewProduct")
preconditionTwo = genieacs.Precondition("summary.softwareVersion", "gte", "1.3.2")
preconditionThree = genieacs.Precondition("_tag", "ne", "tagged")
preconditions = [preconditionOne, preconditionTwo, preconditionThree]
# create configurations for a new preset
configurationOne = genieacs.AddTag("tagged")
configurationTwo = genieacs.Refresh("InternetGatewayDevice", "43200")
configurationThree = genieacs.AddTag("refreshed")
configurations = [configurationOne, configurationTwo, configurationThree]
# create a new preset
createdPreset = genieacs.Preset("TagAndRefresh", "0", preconditions, configurations)
acs.preset_create(createdPreset)
# write all existing presets to a file and store them in a json object
preset_data = acs.preset_get_all('presets.json')
# delete all presets
for preset in preset_data:
    acs.preset_delete(preset["_id"])
# create all presets from the file
acs.preset_create_all_from_file('presets.json')

# create parameters for a new object
createdParameterOne = genieacs.Parameter("Param1", "Value1", True)
createdParameterTwo = genieacs.Parameter("Param2", "Value2")
createdParameterThree = genieacs.Parameter("Param3", "Value3", True)
createdParameters = [createdParameterOne, createdParameterTwo, createdParameterThree]
# create a new object
createdObject = genieacs.Object("CreatedObject", createdParameters)
acs.object_create(createdObject)
# write all existing objects to a file and store them in a json object
object_data = acs.object_get_all('objects.json')
# delete all objects
for gobject in object_data:
    acs.object_delete(gobject["_id"])
# create all objects from the file
acs.object_create_all_from_file('objects.json')

# assign a tag to a device
#acs.tag_assign(device_id, "tagged")
# remove a tag from a device
#acs.tag_remove(device_id, "tagged")

# print all existing files in the database
#print(acs.file_get_all())
# upload a new or modified file
#acs.file_upload("Firmware.img", "1 Firmware Upgrade Image", "123456", "r4500", "2.0")
# delete a file from the database
#acs.file_delete("Firmware.img")

# delete the device from the database
acs.device_delete(device_id)
