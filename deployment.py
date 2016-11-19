import os
import collections
import queue

q = queue.Queue()

class Leaf:
    ''' Leaf(foo) acts as a factory, creating one and only one bar object (Leaf) for each foo (path)'''
    leaf_pile = dict();

    def __new__(cls,path):
        if path in Leaf.leaf_pile:
            return(Leaf.leaf_pile[path])
        return super(Leaf,cls).__new__(cls)

    def __init__(self,path):
        if path in Leaf.leaf_pile:
           return None
        Leaf.leaf_pile[path] = self
        self._path           = path
        self._files          = collections.OrderedDict()
        self._dirs           = collections.OrderedDict()
    @property
    def path(self):
        return self._path
    @property
    def files(self):
        return self._files;

    def file(self,name,**kwargs):
        ''' file(self,name,**kwargs) lets you create an entry for file named name
            and optionally set or update values of path, size, uname, gname and perms
        '''
        if name not in self._files:
            self._files[name]={}
        if kwargs:
            self._files[name].update(kwargs)

    @property
    def dirs(self):
        return self._dirs;

    def dire(self, name, **kwargs):
        ''' dir(self,name,**kwargs) lets you create an entry for dir named name
            and optionally set or update values of uname, gname and perms and leaf
        '''
        if name not in self._dirs:
            self._dirs[name]={}
        if kwargs:
            self._dirs[name].update(kwargs)

    def leaf_update(self,path,files=None,dirs=None):
        for f in files:
            ff = path +'/'+f
            s  = os.stat(ff)
            self.file(f,gname=s.st_gid,uname=s.st_uid,size=s.st_size)
        for d in dirs:
            dd = path + '/' + d
            s  = os.stat(dd)
            self.dire(d, leaf=Leaf(path + '/' + d), uname=s.st_uid, gname=s.st_gid)
    def climb(self):
        yield self
        for v in self._dirs.values():
             yield from v['leaf'].climb()

if __name__ == '__main__':
    tree = Leaf('deploy_test')
    for d,ds,fs in os.walk('deploy_test'):
        leaf = Leaf(d)
        leaf.leaf_update(d,files=fs,dirs=ds)

    for leaf in tree.climb():
        print(__name__,leaf.path)








# print(l1,'\n',l2,'\n',l3)
#     def __init__(self,location,dirs,files):
#         self.location = location
#         self.files    = files
#         if dirs == None:
#             self.dirs[dir] = k
#         for dir in dirs:
#             self.dirs[dir] = Leaf(dir,None,None)
# class Deployment:
#     # A deployment
#     def __init__(self,sanction=None,local_base=None):
#         self.sanction   = sanction
#         self.local_base =local_base
#         self.tree       = dict()
#     def tree =
# class Tree:
#     pass
#
# class Leaf:
#     pass


