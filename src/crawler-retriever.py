import os
import json
import re

def removecomments(s):
    inCommentSingle = False
    inCommentMulti = False
    inString = False

    t = []
    l = len(s)

    i = 0
    fromIndex = 0
    while i < l:
        c = s[i]

        if not inCommentMulti and not inCommentSingle:
            if c == '"':
                slashes = 0
                for j in range(i - 1, 0, -1):
                    if s[j] != '\\':
                        break

                    slashes += 1

                if slashes % 2 == 0:
                    inString = not inString

            elif not inString:
                if c == '#':
                    inCommentSingle = True
                    t.append(s[fromIndex:i])
                elif c == '/' and i + 1 < l:
                    cn = s[i + 1]
                    if cn == '/':
                        inCommentSingle = True
                        t.append(s[fromIndex:i])
                        i += 1
                    elif cn == '*':
                        inCommentMulti = True
                        t.append(s[fromIndex:i])
                        i += 1

        elif inCommentSingle and (c == '\n' or c == '\r'):
            inCommentSingle = False
            fromIndex = i

        elif inCommentMulti and c == '*' and i + 1 < l and s[i + 1] == '/':
            inCommentMulti = False
            i += 1
            fromIndex = i + 1

        i += 1

    if not inCommentSingle and not inCommentMulti:
        t.append(s[fromIndex:len(s)])

    return "".join(t)

common_prefix = os.getcwd()+'\\'

p_list = []

for path, dirs, files in os.walk(os.getcwd()):
    for file in files :
        if '.object' in file:
            t_file = open(os.path.join(path,file))
            t_string = t_file.read()
            t_json = json.loads(removecomments(t_string))
            if 'description' in t_json:
                t_desc = t_json['description']
            else:
                t_desc = "__no description__"
            p_list.append(dict(path = os.path.relpath(path,common_prefix),file = file, name = t_json['shortdescription'], desc = t_desc))

t_file.close()

t_file = open(os.path.join(common_prefix,'namedump.json'),'w')

json.dump(p_list,t_file,indent = 2, sort_keys = True)

t_file.close()
