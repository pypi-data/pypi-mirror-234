from .utils import *

class Node(object):
    def __init__(self, data, internal=True):
        self.data = data
        self.parent = None
        self.children = Set(lambda a,b: a.data == b.data)
        self.internal = internal

    def __str__(self):
        def strip_empty(l):
            return [e for e in l if len(l) > 0]
        if len(self.children) == 0:
            return self.data
        ret=self.data + ('/' if self.internal else '') + CHARS.NEW_LINE
        for c in self.children:
            ch_repr = strip_empty(c.__str__().strip().split(CHARS.NEW_LINE))
           # ret += CHARS.PIPE_VERT+CHARS.NEW_LINE
            ret += CHARS.T_END if c == self.children[-1] else CHARS.T_MID
            ret += CHARS.PIPE_HORIZ\
                    +ch_repr[0]+CHARS.NEW_LINE
            for l in ch_repr[1:]:
                ret += (' ' if c == self.children[-1] else CHARS.PIPE_VERT)+' '
                ret += l+CHARS.NEW_LINE
        return ret


def getDirectChildren(l):
    directChildren=dict()
    for c in l:
        if len(c) == 0:
            continue
        if c[0] not in directChildren:
            directChildren[c[0]] = list()
        directChildren[c[0]].append(c)
    return directChildren


def Tree(name, lst, recursive=True, collapsePaths=False, commonBase=False):
    if collapsePaths:
        tpl = getCommonPrefix(collapse(lst))
        if tpl and tpl[0] != '':
            name = (name+'/' if recursive else '')+tpl[0]
            lst = tpl[1]
            recursive = True
    children = list()
    directChildren = getDirectChildren(lst)
    for c in directChildren:
        n = Tree(c, [e[1:] for e in directChildren[c]], collapsePaths=collapsePaths)[0]
        children.append(n)
    if not recursive and not commonBase:
        return children
    ret = Node(name, internal=len(children) != 0)
    for n in children:
        n.parent = ret
        ret.children.add(n)
    return [ret]
