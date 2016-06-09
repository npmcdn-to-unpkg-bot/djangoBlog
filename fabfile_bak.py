#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'zhaochy'

'''
Deployment toolkit.
Need fabric first, pip install fabric
usage:
1. build dist package
compress local files for deployment:
>>> fab build

2. deploy dist package
fab deploy

3. rollback
fab rollback

4. backup remote database
If not exist, create a dir named database_backup at current path,
then run:
>>> fab backup
'''

import os, re

from datetime import datetime
from fabric.api import *

# set server username when making ssh connections
env.user = ''
# set password. If not set fabric will prompt you when necessary
env.password = ''
# set sudo user
env.sudo_user = ''
# The global host list used when composing per-task host lists.
env.hosts = ['']

# mysql username and password
db_user = ''
db_password = ''

_TAR_FILE = 'blog.tar.gz'

_REMOTE_TMP_TAR = '/tmp/%s' % _TAR_FILE

_REMOTE_BASE_DIR = '/srv/zhaochy_cn'


def _current_path():
    return os.path.abspath('.')


def _now():
    return datetime.now().strftime('%y-%m-%d_%H.%M.%S')


def backup():
    '''
    Dump entire database on server and backup to local.
    need to make dir 'database_backup' at current path first.
    '''
    dt = _now()
    f = 'backup-blog-%s.sql' % dt
    with cd('/tmp'):
        run(
            'mysqldump --user=%s --password=%s --skip-opt --add-drop-table --default-character-set=utf8 --quick zhaochy_cn > %s' % (
                db_user, db_password, f))
        run('tar -czvf %s.tar.gz %s' % (f, f))
        get(remote_path='/tmp/%s.tar.gz' % f, local_path='%s/database_backup' % _current_path())
        run('rm -f %s' % f)
        run('rm -f %s.tar.gz' % f)


def build():
    '''
    Build dist package.
    '''
    includes = ['api', 'blog', 'media', 'posts', 'templates',
                'zcy_md', 'zhaochy_cn', '*.py', 'requirements.txt', '*.md']
    excludes = ['.*', '*.pyc', '*.pyo']
    local('rm -f dist/%s' % _TAR_FILE)
    cmd = ['tar', '--dereference', '-czvf', 'dist/%s' % _TAR_FILE]
    cmd.extend(['--exclude=\'%s\'' % ex for ex in excludes])
    cmd.extend(includes)
    # print 'cmd'
    local(' '.join(cmd))


def deploy():
    newdir = 'djangoBlog-%s' % _now()
    run('rm -f %s' % _REMOTE_TMP_TAR)
    put('dist/%s' % _TAR_FILE, _REMOTE_TMP_TAR)
    with cd(_REMOTE_BASE_DIR):
        sudo('mkdir %s' % newdir)
    # extract files
    with cd('%s/%s' % (_REMOTE_BASE_DIR, newdir)):
        sudo('tar -xzvf %s' % _REMOTE_TMP_TAR)
        sudo('rm zhaochy_cn/custom.py')
        # set deploy env
        sudo('mv zhaochy_cn/custom_deploy.py zhaochy_cn/custom.py')
        sudo('python manage.py makemigrations')
        sudo('python manage.py migrate')
        sudo('python manage.py collectstatic --link')
    with cd('/srv'):
        sudo('rm -f djangoBlog')
        sudo('ln -s %s/%s djangoBlog' % (_REMOTE_BASE_DIR, newdir))
        sudo('chown -R www-data:www-data zhaochy_cn')
        sudo('chmod 755 -R zhaochy_cn')
        sudo('chown www-data:www-data djangoBlog')
        sudo('chown -R www-data:www-data %s/%s' % (_REMOTE_BASE_DIR, newdir))
        sudo('chmod 755 djangoBlog')
        sudo('chmod 755 -R %s/%s' % (_REMOTE_BASE_DIR, newdir))
    with settings(warn_only=True):
        sudo('service apache2 reload')


RE_FILES = re.compile('\r?\n')


def rollback():
    '''
    rollback to previous version
    '''
    with cd(_REMOTE_BASE_DIR):
        r = run('ls -p -1')
        files = [s[:-1] for s in RE_FILES.split(r) if s.startswith('djangoBlog-') and s.endswith('/')]
        files.sort(cmp=lambda s1, s2: 1 if s1 < s2 else -1)
        r = run('ls -l ../djangoBlog')
        ss = r.split(' -> ')
        if len(ss) != 2:
            print ('ERROR: \'djangoBlog\' is not a symbol link.')
            return
        current_fullpath = ss[1]
        current_filename = current_fullpath.split('/')[-1]
        print ('Found current symbol link points to: %s\n' % current_fullpath)
        try:
            index = files.index(current_filename)
        except ValueError, e:
            print ('ERROR: symbol link is invalid.')
            return
        if len(files) == index + 1:
            print ('ERROR: already the oldest version.')
        print ('==================================================')
        item = 0
        for f in files:
            if f == current_filename:
                print ('      Current ---> %d. %s' % (item, f))
            else:
                print ('                   %d. %s' % (item, f))
            item += 1
        print ('==================================================')

        version = raw_input('Please choose a version to rollback:')
        try:
            version = int(version)
        except Exception, e:
            print ('Please input a correct version.')
            print (e.message)
            return
        if version >= item or version <= 0:
            print ('Please input a correct version.')
            return

        print ('==================================================')
        item = 0
        old = files[version]
        for f in files:
            if f == current_filename:
                print ('      Current ---> 0. %s' % current_filename)
            elif f == old:
                item = item + 1
                print ('  Rollback to ---> %d. %s' % (item, old))
            else:
                item = item + 1
                print ('                   %d. %s' % (item, f))
        print ('==================================================')
        print ('')
        yn = raw_input('continue? y/N ')
        if yn != 'y' and yn != 'Y':
            print ('Rollback cancelled.')
            return
        print ('Start rollback...')
        old_fullpath = os.path.join('/srv/zhaochy_cn', old)
    with cd('/srv'):
        sudo('rm -f djangoBlog')
        sudo('ln -s %s djangoBlog' % old_fullpath)
        sudo('chown www-data:www-data djangoBlog')
        sudo('chmod 755 djangoBlog')
    with settings(warn_only=True):
        sudo('service apache2 reload')
    print ('ROLLBACKED OK.')


def restore2local():
    '''
    Restore db to local
    '''
    backup_dir = os.path.join(_current_path(), 'backup')
    fs = os.listdir(backup_dir)
    files = [f for f in fs if f.startswith('backup-') and f.endswith('.sql.tar.gz')]
    files.sort(cmp=lambda s1, s2: 1 if s1 < s2 else -1)
    if len(files) == 0:
        print 'No backup files found.'
        return
    print ('Found %s backup files:' % len(files))
    print ('==================================================')
    n = 0
    for f in files:
        print ('%s: %s' % (n, f))
        n = n + 1
    print ('==================================================')
    print ('')
    try:
        num = int(raw_input('Restore file: '))
    except ValueError:
        print ('Invalid file number.')
        return
    restore_file = files[num]
    yn = raw_input('Restore file %s: %s? y/N ' % (num, restore_file))
    if yn != 'y' and yn != 'Y':
        print ('Restore cancelled.')
        return
    print ('Start restore to local database...')
    p = raw_input('Input mysql root password: ')
    sqls = [
        'drop database if exists awesome;',
        'create database awesome;',
        'grant select, insert, update, delete on awesome.* to \'%s\'@\'localhost\' identified by \'%s\';' % (
            db_user, db_password)
    ]
    for sql in sqls:
        local(r'mysql -uroot -p%s -e "%s"' % (p, sql))
    with lcd(backup_dir):
        local('tar zxvf %s' % restore_file)
    local(r'mysql -uroot -p%s awesome < backup/%s' % (p, restore_file[:-7]))
    with lcd(backup_dir):
        local('rm -f %s' % restore_file[:-7])
