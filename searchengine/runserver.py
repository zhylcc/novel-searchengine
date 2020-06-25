import os

if __name__ == '__main__':
    path = os.path.dirname(__file__) + '/manage.py'
    res = os.popen('python ' + path + ' runserver 127.0.0.1:8000').read()
    for line in res.splitlines():
        print(line)