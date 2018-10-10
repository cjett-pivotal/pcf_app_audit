#!/usr/local/opt/python/libexec/bin/python
import sys
import os.path
import json
import ssl
import getpass
import urllib2
import csv

def get_usage_payload(url, username='', password=''):
    if username and password:
        auth_handler = urllib2.HTTPBasicAuthHandler()
        auth_handler.add_password(realm='CF Orgs Usage',
                                uri=url,
                                user=username,
                                passwd=password)
        opener = urllib2.build_opener(auth_handler)
        # ...and install it globally so it can be used with urlopen.
        urllib2.install_opener(opener)
        contents = urllib2.urlopen(url+"/app-usage/today",context=ssl._create_unverified_context()).read()
        return contents
    else:
        contents = urllib2.urlopen(url+"/app-usage/today",context=ssl._create_unverified_context()).read()
        return contents
        

def main():
    url = ''
    while url is '':
        url = raw_input("Usage API URL? <http(s)://usage-api.example.com>: ")
        if len(url.split("/")) != 3:
            print "Invalid input."
            url = ''

    isBasic = ''
    while isBasic != 'n' and isBasic != 'y':
        isBasic = raw_input("Using basic auth? <y/n>").lower()

    username = ''
    password = ''

    if isBasic == 'y':
        while username is '':
            username = raw_input("Username: ")
        while password is '':
            password = getpass.getpass(prompt="Password: ")

    contents = get_usage_payload(url, username, password)

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

    with open('app_usage.csv', 'wb') as csvfile:
        fieldnames = ['Org', 'Space', '# Apps', '# Instances']
        csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        csvwriter.writeheader()
        for org in apps:
            print "Org: "+org
            for space in apps[org]:
                print "Space: "+space
                print "Number of apps: " +str(len(apps[org][space]))
                instances=0
                for app in apps[org][space]:
                    instances += apps[org][space][app]["instances"]
                print "Number of instances: "+str(instances)
                csvwriter.writerow({'Org': org, 'Space': space, '# Apps': str(len(apps[org][space])), '# Instances': str(instances)})
            print ""

main()