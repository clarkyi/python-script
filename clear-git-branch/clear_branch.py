#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2017 Clarkyi clarkywq@gmail.com
#
# Distributed under terms of the MIT license.
import os, re
import sys, getopt

class ClearBranch :

  def clear_branch(self, skip_branch, src):
    k_branchs = self.skip_branchs()
    print(k_branchs)
    if not skip_branch in k_branchs :
      k_branchs.append(skip_branch)
    if src == "local" :
      self.clear_local(k_branchs)
    else :
      self.clear_origin(k_branchs)      

  def clear_local(self, skip_branch):
    local_branchs = self.get_local_branchs()
    branchs = local_branchs - skip_branch
    for branch in branchs :
      # os.system("git branch -d " + branch)
      print("deleted local ", branch)

  def clear_origin(self, skip_branch):
    origin_branchs = self.get_origin_branchs()
    branchs = origin_branchs - skip_branch
    for branch in branchs :
      # os.system("git branch -d origin " + branch)
      print("deleted origin ", branch)    

  def get_local_branchs(self):
    os.popen("git branch").readlines()

  def get_origin_branchs(self):
    result = os.popen("git branch -a | grep remotes").readlines()
    branchs = []
    for branch in result:
      branchs.append(branch.replace("remotes/origin/", ""))
    return branchs

  def valid_clear_env(self, arg):
    arg in ["local", "origin"]

  def skip_branchs(self):
    current_branch = self.get_current()
    branchs = ["develop", "master"]
    if not current_branch in branchs :
      branchs.append(current_branch)
    return branchs

  def get_current(self):
    result = os.popen("git name-rev --name-only HEAD").readlines()[0]
    return result.strip('\n')

  def in_project(self):
    result = os.popen("git branch").readlines()[0]
    count = result.find("master")
    if(count == -1):
      print "not in project directory"
      sys.exit()

  def help(self):
    print '≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈'
    print 'python clear_branch.py help show method'
    print 'python clear_branch.py clear --src=(local/origin, default: local)' +\
          '--skip=(skip branch name default:current branch) not clear develop master'
    sys.exit()

  def clear(self, argv):
    self.in_project()
    src = "local"
    skip_branch = self.get_current()
    try:
      opts, args = getopt.getopt(argv,"hi:o:",["src=","skip="])
    except getopt.GetoptError:
      self.help()
      sys.exit(2)
    for opt, arg in opts :
      if opt == '-src' and self.valid_clear_env(arg) :
        src == arg 
      elif opt == "skip" :
        skip_branch == arg
      elif opt == "help" :
        self.help()
        sys.exit()
    self.clear_branch(skip_branch, src)


cb = ClearBranch()
cb.clear(sys.argv[1:])