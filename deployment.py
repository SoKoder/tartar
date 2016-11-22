
def parse_command_line(command_line):
    import argparse
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()

    group.add_argument(
        '-a', '--aquire',
        dest='aquire',
        action='store_true',
        default=True,
        help='aquire files'
    )
    group.add_argument(
        '-p', '--predeploy',
        dest='predeploy',
        action='store_true',
        default=None,
        help='predeploy files'
    )
    group.add_argument(
        '-j', '--adjust',
        dest='adjust',
        action='store_true',
        default=None,
        help='adjust ownership and perms of files'
    )
    group.add_argument(
        '-d', '--deploy',
        dest='deploy',
        action='store_true',
        default=None,
        help='deploy files'
    )
    group.add_argument(
        '-r', '--revert',
        dest='revert',
        action='store_true',
        default=None,
        help='revert files'
    )
    parser.add_argument(
        '-s', '--sanction',
        dest    = 'sanction',
        default = 'CR_000000',
        help    = 'authorizing document id (CR/DR/Novo/etc)'
    )
    parser.add_argument(
        '-td', '--top-dir',
        dest    = 'top_dir',
        default = 'deploy_test',
        help    = 'path of top of tree to archive'
    )
    parser.add_argument(
        '-f','--file',
        dest    = 'archive_file',
        default = 'sanction',
        help    = 'archive file'
    )
    parser.add_argument(
        '-bd','--base_dir',
        dest    = 'base_dir',
        default = '.',
        help    = 'base for relative paths'
    )
    parser.add_argument(
        '-dd','--deploy_dir',
        dest    = 'deploy_dir',
        default = 'deploy_tars',
        help    = 'directory for archive and support files'
    )
    parser.add_argument(
        '-u','--userid',
        dest    = 'userid',
        default = None,
        help    = 'Userid to sudo to when archiving/adjusting/deploying'
    )
    parser.add_argument(
        '-m','--machines',
        dest    ='host',
        nargs   = '*',
        default = None,
        help    = 'machine(s) to archive from, adjust on or (pre)deploy to'
    )
    parser.add_argument(
        '-pf', '--pando-files',
        dest='pando_file',
        nargs='*',
        default=None,
        help='file(s) with permissions and ownerships of files to deploy'
    )
    parser.add_argument(
        '-xf', '--excluded-files',
        dest='excluded_file',
        nargs='*',
        default=None,
        help='file(s) with lists of files to exclude from processing'
    )

    return parser.parse_args(command_line)


if __name__ == '__main__':
    import os
    from   leafer     import Leaf
    from   subprocess import check_output
    from   sys        import argv,stderr
    args = parse_command_line(argv[1:]) # skip argv[0] (program name)

    # populate tree with directory to be tarred up
    tree = Leaf.tree_of_folder(base=args.base_dir,top=args.top_dir)

    # create temporary links to be tarred
    sanction = args.sanction
    for leaf in tree.descend():
        # create a temporary .SANCTION directory under each leaf
        os.mkdir(leaf.path+'/.'+sanction)
        # link all files from each directory into its .SANCTION
        for f in leaf.files.keys():
            os.link(leaf.path+'/'+f,leaf.path+'/.'+sanction+'/'+f)

    # build list of all files to tar
    file_of_files = args.deploy_dir + '/' + args.archive_file +'.' + args.sanction +'.list'
    tar_file      = args.deploy_dir + '/' + args.archive_file +'.' + args.sanction + '.tar'
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
        os.rmdir(leaf.path+'/.'+args.sanction)

