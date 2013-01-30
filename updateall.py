#!/usr/bin/python
'''
Recursively updates Git and SVN repositories in a specified directory.
Assumes there's one SVN or Git repository per project.
'''
import os
import subprocess
import os.path
import sys

def updateAllProjectDirectories(overall_proj_dir):
    os.chdir(overall_proj_dir)
    proj_files = os.listdir(overall_proj_dir)
    [updateProject(proj_dir, overall_proj_dir) for proj_dir in proj_files if os.path.isdir(proj_dir)]

def updateProject(repo_dir, proj_dir):
    files = os.listdir(repo_dir)
    
    print "Project: " + repo_dir
    if '.git' in files:
        print "git pull: " + repo_dir
        updateGit(repo_dir)
        return
    elif '.svn' in files:
        print "SVN update: " + repo_dir
        updateSvn(repo_dir)
        return
    else:
        print "No top level repository found in " + repo_dir + ". Will walk through now..."
        for root, dirs, files in os.walk(repo_dir):
            if '.git' in dirs:
                print "git pull: " + root
                updateGit(root)
                return
            elif '.svn' in dirs:
                print "SVN update: " + root
                updateSvn(root)
                return
        print "No repository found in " + repo_dir

def updateGit(repo_dir):
    cur_dir = os.getcwd()
    os.chdir(repo_dir)
    subprocess.call(['git', 'pull'])
    os.chdir(cur_dir)
    
def updateSvn(repo_dir):
    cur_dir = os.getcwd()
    os.chdir(repo_dir)
    subprocess.call(['svn', 'up'])
    os.chdir(cur_dir)

def main():
    proj_dir = ""
    if len(sys.argv) > 1: 
        proj_dir = str(sys.argv[1])
    else:
        proj_dir = '.'
    updateAllProjectDirectories(proj_dir)
                                  
if __name__ == "__main__":
    main()

#proj_dir = os.getenv('PROJ', os.getenv('HOME') + '/proj')
