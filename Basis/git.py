# -*- coding: utf-8 -*-

import os

def git_add_commit_push(date, filename):
	cmd_git_add = 'git add .'
	cmd_git_commit = 'git commit -m "{date}"'.format(date=date)
	cmd_git_push = 'git push -u origin master'

	os.system(cmd_git_add)
	os.system(cmd_git_commit)
	os.system(cmd_git_push)