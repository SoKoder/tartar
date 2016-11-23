
def parse_command_line(command_line):
    import argparse
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()

    group.add_argument(
        '-a', '--aquire',          dest = 'aquire',        default = True, action='store_true',
        help    = 'aquire files'
    )
    group.add_argument(
        '-p', '--predeploy',       dest = 'predeploy',     default = None, action='store_true',
        help    = 'predeploy files'
    )
    group.add_argument(
        '-j', '--adjust',          dest = 'adjust',        default = None, action='store_true',
        help    = 'adjust ownership and perms of files'
    )
    group.add_argument(
        '-d', '--deploy',          dest = 'deploy',        default = None, action='store_true',
        help    = 'deploy files'
    )
    group.add_argument (
        '-r', '--revert',          dest = 'revert',        default = None, action='store_true',
        help    = 'revert files'
    )
    parser.add_argument(
        '-s', '--sanction',        dest = 'sanction',      default = 'unsanctioned', 
        help    = 'authorizing document id (CR/DR/Novo/etc)'
    )
    parser.add_argument(
        '-ad','--archive_dir',     dest = 'archive_dir',   default = 'default',
        help    = 'directory for archive and support files'
    )
    parser.add_argument(
        '-bd','--base_dir',        dest = 'base_dir',      default = '.',
        help    = 'base for relative paths where to cd to for tar operation'
    )
    parser.add_argument(
        '-td','--top-dir',         dest = 'top_dir',       default = '.',
        help    = 'path of top of tree to archive relative to BASE_DIR'
    )
    parser.add_argument(
        '-af','--file',            dest = 'archive_file',  default = 'default',
        help    = 'archive file'
    )
    parser.add_argument(
        '-if' ,'--include-file',    dest = 'include_file',  default = None, nargs='*',
        help    = 'files(s) to include in processing'
    )
    parser.add_argument(
        '-xf', '--exclude-file',    dest = 'exclude_file',  default = None, nargs='*', 
        help    = 'file(s) to exclude from processing'
    )
    parser.add_argument(
        '-il','--includes-lists',  dest = 'includes_file', default = None, nargs='*',
        help    = 'file(s) with list of files to include in archive'
    )
    parser.add_argument(
        '-xl','--excludes-lists',  dest = 'excludes_file', default = None, nargs='*', 
        help    = 'file(s) with lists of files to exclude from processing'
    )
    parser.add_argument(
        '-m' ,'--machines',        dest = 'host',          default = None, nargs='*',
        help    = 'machine(s) to aquire from, adjust on, (pre)deploy to or revert'
    )
    parser.add_argument(
        '-u', '--userid',          dest = 'userid',        default = None,
        help    = 'Userid to sudo to when aquiring/adjusting/deploying/reverting'
    )
    parser.add_argument(
        '-pl','--pandos-lists',    dest = 'pandos_file',   default = None, nargs='*',
        help    = 'file(s) with permissions and ownerships of files to deploy'
    )

    args    = parser.parse_args(command_line)
    parsed  = {}
    for a in args.__dict__.keys():
        parsed[a] = args.__dict__[a]
    return parsed

def create_predeployment_archive(tree,args):
    import os
    # create temporary links to be tarred
    sanction = parsed['sanction']
    for leaf in tree.descend():
        # create a temporary .SANCTION directory under each leaf
        os.mkdir(leaf.path + '/.' + sanction)
        # link all files from each directory into its .SANCTION
        for f in leaf.files.keys():
            os.link(leaf.path + '/' + f, leaf.path + '/.' + sanction + '/' + f)

    # build list of all files to tar
    file_of_files = parsed['archive_dir'] + '/' + parsed['archive_file'] +'.' + parsed['sanction'] +'.list'
    tar_file      = parsed['archive_dir'] + '/' + parsed['archive_file'] +'.' + parsed['sanction'] + '.tar'
    with open(file_of_files,'w') as fd:
       for leaf in tree.descend():
           for f in leaf.files.keys():
               fd.write(leaf.path+'/.'+sanction+'/'+f+'\n')

    # create tar of listed files
    tar_output = check_output(
         '/usr/bin/tar -T ' + file_of_files + ' -cvf ' + tar_file + ' 2>&1',
         shell=True
    )
    print('results of tar:',file=stderr)
    print(tar_output.decode(),file=stderr)

    # remove the tarred files from the .SANCTION directories
    print('temp files removed:',file=stderr)
    with open(file_of_files,'r') as fd:
        for file in fd.readlines():
            file = file[:-1]                 # removing line-end character (assuming UNIX)
            print( '- ' + file,file=stderr)
            os.remove(file)

    # remove the now empty '.SANCTION' temporary directories
    # using 'ascend()' would be necessary were they nested,
    # but since they are not, I used ascend() just for fun
    for leaf in tree.ascend():
        os.rmdir(leaf.path+'/.'+parsed['sanction'])

    return

if __name__ == '__main__':
    # import os
    from   leafer     import Leaf
    from   subprocess import check_output
    from   sys        import argv,stderr

    parsed    =  parse_command_line(argv[1:]) # skip argv[0] (program name)
    # populate tree with directory to be tarred up
    tree      = Leaf.tree_of_folder(base=parsed['base_dir'],top=parsed['top_dir'])

    create_predeployment_archive(tree,parsed)


