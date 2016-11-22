#tartar
is to be a deployment script (or collection of scripts) for the office. Mostly I'm just trying to learn python, so ...
you might as well just move along, nothing to see here... ;)
```
usage: deployment.py [-h] [-a | -p | -j | -d | -r] [-s SANCTION]
                     [-f ARCHIVE_FILE] [-bd BASE_DIR] [-td TOP_DIR]
                     [-ad ARCHIVE_DIR] [-u USERID] [-m [HOST [HOST ...]]]
                     [-pf [PANDO_FILE [PANDO_FILE ...]]]
                     [-xf [EXCLUDES_FILE [EXCLUDES_FILE ...]]]

optional arguments:
  -h, --help            show this help message and exit
  -a, --aquire          aquire files
  -p, --predeploy       predeploy files
  -j, --adjust          adjust ownership and perms of files
  -d, --deploy          deploy files
  -r, --revert          revert files
  -s SANCTION, --sanction SANCTION
                        authorizing document id (CR/DR/Novo/etc)
  -f ARCHIVE_FILE, --file ARCHIVE_FILE
                        archive file
  -bd BASE_DIR, --base_dir BASE_DIR
                        base for relative paths where to cd to for tar
                        operation
  -td TOP_DIR, --top-dir TOP_DIR
                        path of top of tree to archive relative to BASE_DIR
  -ad ARCHIVE_DIR, --archive_dir ARCHIVE_DIR
                        directory for archive and support files
  -u USERID, --userid USERID
                        Userid to sudo to when
                        aquiring/adjusting/deploying/reverting
  -m [HOST [HOST ...]], --machines [HOST [HOST ...]]
                        machine(s) to aquire from, adjust on, (pre)deploy to
                        or revert
  -pf [PANDO_FILE [PANDO_FILE ...]], --pando-files [PANDO_FILE [PANDO_FILE ...]]
                        file(s) with permissions and ownerships of files to
                        deploy
  -xf [EXCLUDES_FILE [EXCLUDES_FILE ...]], --excludes-files [EXCLUDES_FILE [EXCLUDES_FILE ...]]
                        file(s) with lists of files to exclude from processing
```
