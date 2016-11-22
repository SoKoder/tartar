#tartar
is to be a deployment script (or collection of scripts) for the office. Mostly I'm just trying to learn python, so ...
you might as well just move along, nothing to see here... ;)
```
usage: deployment.py [-h] [-a | -p | -j | -d | -r] [-s SANCTION]
                     [-ad ARCHIVE_DIR] [-bd BASE_DIR] [-td TOP_DIR]
                     [-af ARCHIVE_FILE]
                     [-if [INCLUDE_FILE [INCLUDE_FILE ...]]]
                     [-xf [EXCLUDE_FILE [EXCLUDE_FILE ...]]]
                     [-il [INCLUDES_FILE [INCLUDES_FILE ...]]]
                     [-xl [EXCLUDES_FILE [EXCLUDES_FILE ...]]]
                     [-m [HOST [HOST ...]]] [-u USERID]
                     [-pl [PANDOS_FILE [PANDOS_FILE ...]]]

optional arguments:
  -h, --help            show this help message and exit
  -a, --aquire          aquire files
  -p, --predeploy       predeploy files
  -j, --adjust          adjust ownership and perms of files
  -d, --deploy          deploy files
  -r, --revert          revert files
  -s SANCTION, --sanction SANCTION
                        authorizing document id (CR/DR/Novo/etc)
  -ad ARCHIVE_DIR, --archive_dir ARCHIVE_DIR
                        directory for archive and support files
  -bd BASE_DIR, --base_dir BASE_DIR
                        base for relative paths where to cd to for tar
                        operation
  -td TOP_DIR, --top-dir TOP_DIR
                        path of top of tree to archive relative to BASE_DIR
  -af ARCHIVE_FILE, --file ARCHIVE_FILE
                        archive file
  -if [INCLUDE_FILE [INCLUDE_FILE ...]], --include-file [INCLUDE_FILE [INCLUDE_FILE ...]]
                        files(s) to include in processing
  -xf [EXCLUDE_FILE [EXCLUDE_FILE ...]], --exclude-file [EXCLUDE_FILE [EXCLUDE_FILE ...]]
                        file(s) to exclude from processing
  -il [INCLUDES_FILE [INCLUDES_FILE ...]], --includes-lists [INCLUDES_FILE [INCLUDES_FILE ...]]
                        file(s) with list of files to include in archive
  -xl [EXCLUDES_FILE [EXCLUDES_FILE ...]], --excludes-lists [EXCLUDES_FILE [EXCLUDES_FILE ...]]
                        file(s) with lists of files to exclude from processing
  -m [HOST [HOST ...]], --machines [HOST [HOST ...]]
                        machine(s) to aquire from, adjust on, (pre)deploy to
                        or revert
  -u USERID, --userid USERID
                        Userid to sudo to when
                        aquiring/adjusting/deploying/reverting
  -pl [PANDOS_FILE [PANDOS_FILE ...]], --pandos-lists [PANDOS_FILE [PANDOS_FILE ...]]
                        file(s) with permissions and ownerships of files to
                        deploy
```

