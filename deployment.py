import os
from leafer import Leaf

if __name__ == '__main__':
    tree = Leaf('deploy_test')
    for d,ds,fs in os.walk('deploy_test'):
        leaf = Leaf(d)
        leaf.leaf_update(d,files=fs,dirs=ds)

    for leaf in tree.climb():
        print(__name__,leaf.path)

    sanction = 'CR_12345'
    for leaf in tree.climb():

        os.mkdir(leaf.path+'/.'+sanction)
        for f in leaf.files.keys():
            os.link(leaf.path+'/'+f,leaf.path+'/.'+sanction+'/'+f)

    with open('deployment_tar/list','w') as fd:
       for leaf in tree.climb():
           for f in leaf.files.keys():
               fd.write(leaf.path+'/.'+sanction+'/'+f+'\n')

    os.system('/usr/bin/tar -T deployment_tar/list -cvf deployment_tar/sanctioned.tar')






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


