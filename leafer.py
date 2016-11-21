from os          import stat
from collections import OrderedDict

class Leaf:
    ''' Leaf(foo) acts as a factory, creating one and only one bar object (Leaf) for each foo (path)'''
    leaf_pile = dict();

    @classmethod
    def tree_of_folder(cls,base='.',top='.'):
        # populate tree with directory to be tarred up
        import os
        os.chdir(base)
        tree = Leaf(top)
        for d, ds, fs in os.walk(top):
            leaf = Leaf(d)
            leaf.leaf_update(d, files=fs, dirs=ds)
        return tree

    def __new__(cls,path):
        if path in Leaf.leaf_pile:          # create but one leaf for any one path
            return(Leaf.leaf_pile[path])    # return already in-service leaf
        return super(Leaf,cls).__new__(cls) # create new leaf

    def __init__(self,path):
        if path in Leaf.leaf_pile: # don't reinitialize already existing object
           return None
        # if we get here, we are initializing a new Leaf object
        Leaf.leaf_pile[path] = self
        self._path           = path                      # relative path to current directory
        self._files          = OrderedDict() # attributes for each file in current directory
        self._dirs           = OrderedDict() # link to subdir leafs and attributes for each subdir

    @property
    def path(self):    return self._path

    @path.setter
    def path(self,*args,**kwargs):
        raise (TypeError,'You mustn\'t alter path')

    @property
    def files(self):   return self._files

    def file(self,name,**kwargs):
        ''' file(self,name,**kwargs) lets you create an entry for file named name
            and optionally set or update values of path, size, uname, gname and perms
        '''
        if name not in self._files: # allows for first call
            self._files[name]={}
        if kwargs:                  # set any new attributes or override old ones
            self._files[name].update(kwargs)

    @property
    def dirs(self):
        return self._dirs;

    def dire(self, name, **kwargs):
        ''' dire(self,name,**kwargs) lets you create an entry for directory named name
            and optionally set or update values of uname, gname and perms and leaf
        '''
        if name not in self._dirs:
            self._dirs[name]={}
        if kwargs:
            self._dirs[name].update(kwargs)

    def leaf_update(self,path,files=None,dirs=None):
        for f in files:
            s  = stat(path+'/'+f)
            self.file(f,gname=s.st_gid,uname=s.st_uid,size=s.st_size)
        for d in dirs:
            s  = stat(path+'/'+d)
            self.dire(d, leaf=Leaf(path + '/' + d), uname=s.st_uid, gname=s.st_gid)

    def descend(self):
        ''' climb() recursively does a top-down traverse of the tree of leaves below
        the starting point.
        climb() should be called from a generator or other contruct that will
        read one leaf at a time
        '''
        yield self;
        for v in self._dirs.values():
            yield from v['leaf'].descend()

    def ascend(self):
        for v in self._dirs.values():
            yield from v['leaf'].ascend()
        yield self;




