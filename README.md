## Personal Blog with Django, mysql and markdown

### Install
```bash
apt-get install python-imaging libmysqlclient-dev
```

```
pip install -r requirements.txt
```

### Deploy
rename fabfile_bak.py to fabfile.py
configure server ip and password, database username and password.
```bash
fab build
fab deploy
```
- Backup Database
```bash
fab backup
```
- Rollback to previous version
```bash
fab rollback
```