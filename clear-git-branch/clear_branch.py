#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2017 Clarkyi clarkywq@gmail.com
#
# Distributed under terms of the MIT license.
import os, sys
import re, getopt

class ClearBranch :

  def clear_branch(self, skip_branch, src):
    k_branchs = self.skip_branchs()
    k_branchs = list(set(k_branchs).union(set(skip_branch)))
    if src == "local" :
      self.clear_local(k_branchs)
    else :
      self.clear_origin(k_branchs)      

  def clear_local(self, skip_branch):
    local_branchs = self.get_local_branchs()
    branchs = list(set(local_branchs) - set(skip_branch))
    for branch in branchs :
      os.system("git branch -d " + branch)

  def clear_origin(self, skip_branch):
    origin_branchs = self.get_origin_branchs()
    branchs = list(set(origin_branchs) - set(skip_branch))
    for branch in branchs :
      os.system("git branch -d origin " + branch)

  def get_local_branchs(self):
    result = os.popen("git branch").readlines()
    branchs = []
    for item in result:
      branch = item.strip(' ').strip('* ').strip('\n')
      branchs.append(branch)
    return branchs


  def get_origin_branchs(self):
    result = os.popen("git branch -a | grep remotes").readlines()
    branchs = []
    for item in result:
      branch = item.replace("remotes/origin/", "")
      branch = branch.strip(' ').strip('* ').strip('\n')
      branchs.append(branch)
    return branchs

  def valid_clear_env(self, arg):
    return arg in ["local", "origin"]

  def skip_branchs(self):
    current_branch = self.get_current()
    branchs = ["develop", "master"]
    if not current_branch in branchs :
      branchs.append(current_branch)
    return branchs

  def get_current(self):
    branch = os.popen("git branch | grep \* | cut -d ' ' -f2").readlines()[0]
    return branch.strip('\n')

  def in_project(self):
    result = os.popen("git branch").readlines()[0]
    count = result.find("Not a git repository")
    if(count >= 0):
      print "not in project directory"
      sys.exit()

  def help(self):
    print '-h          show help'
    print '-src        local/origin, default: local'
    print '-skip       skip branch name default:current branch not clear develop master more than one split comma'
    sys.exit()

  def clear(self, argv):
    self.in_project()
    src = "local"
    skip_branch = [self.get_current()]
    try:
      opts, args = getopt.getopt(argv,"ho:",["src=","skip=", "help"])
    except getopt.GetoptError, e:
      print("python args Illegal")
      self.help()
    for opt, arg in opts :
      if opt == '--src':
        if self.valid_clear_env(arg):
          src = arg
        else:
          print("args not unsupport:" + arg)
          self.help()
      elif opt == "--skip" :
        skip_branch = arg.split(",")
      elif opt == "--help" :
        self.help()
      elif(opt == "-h"):
        self.help()
    self.clear_branch(skip_branch, src)

  def union_array(self, source, elems):
    for elem in elems:
      if not elem in source:
        source.append(elem)
    return source



cb = ClearBranch()
cb.clear(sys.argv[1:])