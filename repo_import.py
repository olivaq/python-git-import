#!/usr/bin/python
import git

import __builtin__
import imp
real_import = __builtin__.__import__

repo = git.Repo('.')


global dtree
dtree = repo.commit('TBA').tree


def walk_repo(tree, name, fromlist, lname = None):
    if not name:
        lookfor = '__init__'
    else:
        lookfor = name[0]
    
    for k in tree.blobs:
        if k.name.split(".")[0] == lookfor:
            if lookfor == '__init__':
                lookfor = lname
            m = imp.new_module(lookfor)
            global dtree
            tmp, dtree = dtree, tree
            
            exec k.data_stream.read() in m.__dict__
            dtree = tmp
            return m

    for k in tree.trees:
        if k.name == lookfor:
            return walk_repo(k, name[1:], fromlist, lookfor)

def import_from_repo(*args):
    name = args[0]
    fromlist = args[2]

    global dtree

    result = walk_repo(dtree, name.split("."), fromlist)
    
    if result:
        return result

    return real_import(*args)

__builtin__.__import__ = import_from_repo

import foo

foo.bar()

dtree = repo.commit('TBA').tree

import foo

foo.bar()