import os
import re
import subprocess

hash_re = re.compile("\w{40}")
def is_hash(name):
    return name if hash_re.findall(name) else False

def hash_names(dirname, fnames):
    return map(lambda f: dirname + f, fnames)

def sha_content(sha):
    return subprocess.check_output(['git', 'cat-file', '-p', sha])

def sha_type(sha):
    return subprocess.check_output(['git', 'cat-file', '-t', sha])

def walk():
    CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))

    N = 10
    i = 0
    for path, dirs, files in os.walk(CURRENT_PATH):
        # print("path: %s" % path)
        # print("dirs: %s" % dirs)
        # print("files: %s" % files)
        # find .git/objects -type f
        filtered = filter(is_hash, hash_names(path[-2:], files))
        for sha in filtered:
            print sha
            print sha_type(sha)
            print sha_content(sha)
            print("---")

def find_commit(commit, descend=True):
    assert is_hash(commit)
    assert sha_type(commit).strip() == 'commit'
    if descend:
        inspect_commit(commit, descend)

BLOB = re.compile('blob')
TREE = re.compile('tree')
def inspect_commit(commit, descend):
    print("commit: %s" % commit)
    lines = sha_content(commit).split('\n')
    walk_childs(lines)

def walk_childs(lines):
    for line in lines:
        print line
        split = line.split()
        if len(split) == 2:
            t, sha = split
        elif len(split) == 4:
            perm,t,sha,name = split
        else:
            pass

        if t == 'blob':
            inspect_blob(sha)
        elif t == 'tree':
            inspect_tree(sha)

def inspect_tree(tree):
    print("tree: %s" % tree)
    lines = sha_content(tree).split('\n')
    #print ''.join(lines)
    walk_childs(lines)

def inspect_blob(blob):
    print("blob: %s" % blob)
    lines = sha_content(blob)
    #print lines

if __name__ == '__main__':
    commit = "52c6898ce19fc4ccf0d6b781907a5e129d76835e"
    find_commit(commit)
