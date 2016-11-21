
def parse_command_line(command_line):
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-s', '--sanction--',
        dest    = 'sanction',
        default = 'CR_000000',
        help    = 'authorizing document (CR/DR/Novo/etc)'
    )
    parser.add_argument(
        '-t', '--top-dir--',
        dest    = 'top_dir',
        default = 'deploy_test',
        help    = 'path at top of relative deployment tree'
    )
    parser.add_argument(
        '-a', '--archive-dir--',
        dest    = 'archive_dir',
        default = 'deploy_tars',
        help    = 'location of archive'
    )
    return parser.parse_args(command_line)


if __name__ == '__main__':
    import os
    from   leafer     import Leaf
    from   subprocess import check_output
    from   sys        import argv,stderr
    args = parse_command_line(argv[1:])

    # populate tree with directory to be tarred up
    tree = Leaf(args.top_dir)
    for d,ds,fs in os.walk(args.top_dir):
        leaf = Leaf(d)
        leaf.leaf_update(d,files=fs,dirs=ds)

    # create temporary links to be tarred
    sanction = args.sanction
    for leaf in tree.descend():
        # create a temporary .SANCTION directory under each leaf
        os.mkdir(leaf.path+'/.'+sanction)
        # link all files from each directory into its .SANCTION
        for f in leaf.files.keys():
            os.link(leaf.path+'/'+f,leaf.path+'/.'+sanction+'/'+f)

    # build list of all files to tar
    file_of_files = args.archive_dir + '/sanctioned.' + args.sanction +'.list'
    tar_file      = args.archive_dir + '/sanctioned.' + args.sanction + '.tar'
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

