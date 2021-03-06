#!/usr/bin/env python 
#-*- coding:utf-8 -*- 

import traceback 
import sys
import json
from sets import Set
import ldap
from ldap.controls import SimplePagedResultsControl
from collections import defaultdict

try:
    from lib import __meta__
    sys.path = __meta__.PATHS.values() + sys.path
except Exception, e:
    print e
    sys.exit(-1)

import rest
import streams
import entity_types
import users
import perspectives
import nodes
import node_entities
import holmes_admin_conf

def handle_remove_perspectives_option():
    print 'Remove perspectives option yet not implemented.'

def handle_remove_node_entities_option():
    print 'Remove node entities option yet not implemented.'
    
def handle_remove_nodes_option():
    print 'Remove nodes option yet not implemented.'
    
def handle_remove_users_option():
    print 'Remove users option yet not implemented.'

def handle_remove_entity_types_option():
    print 'Remove entity-types option yet not implemented.'

def handle_remove_streams_option():
    print 'Remove streams option yet not implemented.'

def handle_get_node_entities_option():
    print 'Get node entities option yet not implemented.'
     
def handle_get_nodes_option():
    cookie = rest.login_holmes()
    rest.get_all_nodes(cookie, verbose=True)
           
def handle_get_nodes_from_file_option():
    cookie = rest.login_holmes()
    parentNodeIdSet = Set()
    for data in nodes.DATA:
        if data['parentNodeId'] not in parentNodeIdSet:
            parentNodeIdSet.add(data['parentNodeId'])
            nodeList = rest.get_nodes_from_parent(data['perspectiveId'], data['parentNodeId'], 'root', cookie)
            print 'Total nodes: %s' % len(nodeList)
            if len(nodeList) > 0:
                print 'Nodes list:',
            for item in nodeList:
                print '"%s"' % item['text'], 
            print
    
def handle_get_users_option():
    print 'Get users option yet not implemented.'

def handle_get_entity_types_option():
    print 'Get entity-types option yet not implemented.'
    
def handle_get_perspectives_option():
    cookie = rest.login_holmes()
    perspectivesList = rest.get_perspectives(cookie)
    print 'Total perspectives: %s' % len(perspectivesList)
    if len(perspectivesList) > 0:
        print 'Perspectives list:',
        for item in perspectivesList:
            perspective = '"' + item['name'] + '"' 
            print perspective,

def handle_get_streams_option():
    cookie = rest.login_holmes()
    rest.get_streams(cookie)

def handle_get_stats_option():
    cookie = rest.login_holmes()
    rest.get_stats(cookie)
    
def handle_insert_perspectives_option():
    cookie = rest.login_holmes()
    for data in perspectives.DATA:
        rest.insert_perspective(data, cookie)    

def handle_insert_node_entities_option():
    cookie = rest.login_holmes()
    for data in node_entities.DATA:
        rest.insert_node_entity(data['entityId'], data['nodeId'], cookie)

def handle_insert_nodes_option():
    cookie = rest.login_holmes()
    for data in nodes.DATA:
        print 'Inserting node: %s ' % data['name']
        rest.insert_node(json.dumps(data), cookie)
       
def handle_insert_entity_type_option():
    cookie = rest.login_holmes()
    for data in entity_types.DATA:
        rest.insert_entity_type(data, cookie)

def handle_insert_streams_option():
    cookie = rest.login_holmes()
    stream_list = streams.STREAM_LIST
    stream_dir  = streams.STREAM_DIR
    for stream in stream_list:
        exec('from %s import %s' % (stream_dir, stream))
        exec('stream_conf = %s' % stream)
        rest.insert_stream(stream_conf, cookie)
       
def handle_insert_users_from_file_option():
    cookie = rest.login_holmes()
    for data in users.DATA:
        rest.insert_user(data, cookie)

def handle_insert_users_from_ldap_option():
    try:
        l = ldap.initialize(holmes_admin_conf.LDAP_SERVER_URI)
        l.set_option(ldap.OPT_REFERRALS, 0)
        l.simple_bind(holmes_admin_conf.LDAP_USERNAME, holmes_admin_conf.LDAP_PASSWORD)
    except ldap.LDAPError, e:
        print e
        sys.exit(-1)
    try:
        result_set = []
        for search_filter in holmes_admin_conf.LDAP_SEARCH_FILTERS:
            ldap_result_id = l.search(holmes_admin_conf.LDAP_BASE_DN, holmes_admin_conf.LDAP_SEARCH_SCOPE, search_filter, holmes_admin_conf.LDAP_RETRIEVE_ATTRIBUTES)
            
            while 1:
                result_type, result_data = l.result(ldap_result_id, 0)
                if (result_data == []):
                    break
                else:
                    if result_type == ldap.RES_SEARCH_ENTRY:
                        print result_data
                        result_set.append(result_data)
    except ldap.LDAPError, e:
        print e
        sys.exit(-1)
    cookie = rest.login_holmes()
    groups = defaultdict(lambda: [])
    for result in result_set:
        data = holmes_admin_conf.LDAP_USER_FACTORY(lambda s: result[0][1][s][0])
        inserted = rest.insert_user(data, cookie)
        print inserted
        if inserted and 'data' in inserted:
            for group in holmes_admin_conf.LDAP_USER_GROUPS(lambda s: result[0][1][s]):
                groups[group].append(inserted['data']['id'])
                
    for name, users in groups.items():
        rest.insert_group({'name':name, 'users': ','.join(str(v) for v in users), 'allPerspectivesAllowed':False}, cookie)
        
    print data, groups

#Import users from ldap using paged queries strategy
def handle_insert_users_from_ldap_paged_option():

    #Initialing ldap connection parameters
    try:        
        ldap.set_option(ldap.OPT_REFERRALS, 0)
        l = ldap.initialize(holmes_admin_conf.LDAP_SERVER_URI)
        l.protocol_version = 3
        l.simple_bind_s(holmes_admin_conf.LDAP_USERNAME, holmes_admin_conf.LDAP_PASSWORD)
        lc = SimplePagedResultsControl(ldap.LDAP_CONTROL_PAGE_OID,True,(holmes_admin_conf.LDAP_PAGE_SEARCH_PAGE_SIZE,''))
    except ldap.LDAPError, e:
        print e
        sys.exit(-1)

    #Performing searches, one for each given search filter
    try:
        result_list = []
        for search_filter in holmes_admin_conf.LDAP_SEARCH_FILTERS:

            ldap_result_id = l.search_ext(holmes_admin_conf.LDAP_BASE_DN, holmes_admin_conf.LDAP_SEARCH_SCOPE, search_filter, serverctrls=[lc])
            pages = 0
            while True:
                pages += 1
                print "Getting page %d" % (pages,)
                rtype, rdata, rmsgid, serverctrls = l.result3(ldap_result_id)

                #Recovering valid user entries
                for rdata_element in rdata:
                    dn, result = rdata_element
                    #if (('name' in result.keys()) and ('sAMAccountName' in result.keys())):
                    result_list.append(result)       


                pctrls = [c for c in serverctrls if c.controlType == ldap.LDAP_CONTROL_PAGE_OID]
            
                if pctrls:
                    est, cookie = pctrls[0].controlValue
                    if cookie:
                        lc.controlValue = (holmes_admin_conf.LDAP_PAGE_SEARCH_PAGE_SIZE, cookie)
                        ldap_result_id = l.search_ext(holmes_admin_conf.LDAP_BASE_DN, holmes_admin_conf.LDAP_SEARCH_SCOPE, search_filter, serverctrls=[lc])
                    else:
                        break
                else:
                    print "Warning:  Server ignores RFC 2696 control."
                    break                                    

    except ldap.LDAPError, e:
        print e
        print traceback.format_exc()
        sys.exit(-1)
    
    #Debug
    print "\n\nTotal users: " + str(len(result_list)) + '\n\n'
    cookie = rest.login_holmes()

    groups = defaultdict(lambda: [])
    for result in result_list:
        data = holmes_admin_conf.LDAP_USER_FACTORY(lambda s: result[s][0])
        inserted = rest.insert_user(data, cookie)
        print inserted
        if inserted and 'data' in inserted:
            for group in holmes_admin_conf.LDAP_USER_GROUPS(lambda s: result[s]):
                groups[group].append(inserted['data']['id'])
                
    for name, users in groups.items():
        rest.insert_group({'name':name, 'users': ','.join(str(v) for v in users), 'allPerspectivesAllowed':False}, cookie)


insert_users_options = {
    'from_file': handle_insert_users_from_file_option,
    'from_ldap': handle_insert_users_from_ldap_option,
    'from_ldap_paged': handle_insert_users_from_ldap_paged_option
}

insert_options = {
    'perspectives': handle_insert_perspectives_option,                  
    'streams': handle_insert_streams_option,
    'entity-types': handle_insert_entity_type_option,
    'users': insert_users_options,
    'nodes': handle_insert_nodes_option,
    'node-entities': handle_insert_node_entities_option,
}

get_options = {
    'perspectives': handle_get_perspectives_option,
    'streams': handle_get_streams_option,
    'stats': handle_get_stats_option, 
    'entity-types': handle_get_entity_types_option,
    'users': handle_get_users_option,
    'nodes': handle_get_nodes_option,
    'node-entities': handle_get_node_entities_option,
}

remove_options = {
    'perspectives': handle_remove_perspectives_option,                  
    'streams': handle_remove_streams_option,
    'entity-types': handle_remove_entity_types_option,
    'users': handle_remove_users_option,
    'nodes': handle_remove_nodes_option,
    'node-entities': handle_remove_node_entities_option
}


options = {
    'insert': insert_options,
    'get': get_options,
    'remove': remove_options
}

