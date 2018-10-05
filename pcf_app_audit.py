#!/usr/local/opt/python/libexec/bin/python
import sys
import os.path
import json

def main():
    if len(sys.argv) != 2:
        print "Too many arguments: " + str(len(sys.argv))
        sys.exit()
    filename = sys.argv[1]
    if os.path.isfile(filename) != True:
        print "File does not exist in local directory."
        sys.exit()
    file = open(filename,"r")
    if file.mode == "r":
        contents = file.read()
        json_contents = json.loads(contents)
        apps = {}
        for i in json_contents["app_usages"]:
            org_name = i["organization_name"]
            space_name = i["space_name"]
            app_name = i["app_name"]
            inst_count = i["instance_count"]
            if org_name not in apps:
                apps[org_name] = {space_name:{app_name:{"instances":inst_count}}}
            elif space_name not in apps[org_name]:
                apps[org_name][space_name] = {app_name:{"instances":inst_count}}
            elif app_name not in apps[org_name][space_name]:
                apps[org_name][space_name][app_name] = {"instances":inst_count}

        for org in apps:
            print "Org: "+org
            for space in apps[org]:
                print "Space: "+space
                print "Number of apps: " +str(len(apps[org][space]))
                instances=0
                for app in apps[org][space]:
                    instances += apps[org][space][app]["instances"]
                print "Number of instances: "+str(instances)
            print ""

main()