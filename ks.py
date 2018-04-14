from mycrypt import MyCrypt
from mylog import newlogger
from subprocess import Popen
from time import time, asctime
from random import choice
import getpass
import os
import re

log = newlogger()

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def genk(bit):
    dig = '0123456789'
    low = 'abcdefghijklmnopqrstuvwxyz'
    up = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    char = dig + low + up

    output = ''
    while True:
        output = ''.join([choice(char) for i in range(bit)])
        condition = re.search('[0-9]', output) and re.search('[a-z]', output) and re.search('[A-Z]', output)
        if condition:
            break
    return output


class Bins:

    @classmethod
    def delold(cls, critial=5):
        for order, name in enumerate(sorted([i for i in os.listdir('.') if i.endswith('.bin')], reverse=True)):
            if order >= critial:
                log.debug('DEL %s', name)
                os.remove(name)

    @classmethod
    def readlast(cls):
        names = sorted([i for i in os.listdir('.') if i.endswith('.bin')])
        if len(names) == 0:
            filename = '%d.bin' % time()
            f = open(filename, 'wb')
            f.close()
            names.append(filename)

        with open(names[-1], 'rb') as f:
            return f.read()


class Mode:
    try:
        ky = getpass.getpass()
    except:
        import sys
        print('EXIT!')
        sys.exit()
    cry = MyCrypt(ky)

    @classmethod
    def decry(cls):
        return cls.cry.decrypt(Bins.readlast())

    @classmethod
    def vim(cls):
        Popen('vim cache', shell=True).wait()

    @classmethod
    def encry(cls, text):
        content = cls.cry.encrypt(text)
        filename = '%d.bin' % time()
        with open(filename, 'wb') as f:
            f.write(content)
        log.debug('WRITE %s', filename)


class ModeNew(Mode):

    @classmethod
    def run(cls, bit=None):

        k = genk(bit)
        text = cls.decry()

        with open('cache', 'w') as f:
            f.write('# \n')
            f.write('Time: %s\n' % asctime())
            f.write(bytes.fromhex('4163636f756e743a200a50617373776f72643a20').decode())
            f.write('%s\n' % k)

        cls.vim()

        with open('cache', 'r') as f:
            added = f.read()
        if not added.startswith('del'):
            cls.encry('%s%s' % (added, text))
        with open('cache', 'w') as f:
            pass


class ModeAll(Mode):

    @classmethod
    def run(cls):
        text = cls.decry()
        with open('cache', 'w') as f:
            f.write(text)
        cls.vim()
        with open('cache', 'r') as f:
            cls.encry(f.read())
        with open('cache', 'w') as f:
            pass


class ModeFind(Mode):

    @classmethod
    def split(cls, text):

        output = {}
        for lino, l in enumerate(text.splitlines(keepends=True)):
            if l == '\n':
                continue
            m = re.match('(# .*?)\n', l)
            if m:
                title = m.group(1)
                output[title] = []
            else:
                output[title].append(l)
        return output

    @classmethod
    def run(cls, kw):
        text = cls.decry()
        for title, content in cls.split(text).items():
            if kw in title or kw in content:
                print(title)
                print(''.join(content))


if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-n', '--new', nargs='?', const=12, default=False, type=int)
    group.add_argument('-a', '--all', action='store_true')
    group.add_argument('-f', '--find', type=str, default=False)
    args = parser.parse_args()

    if args.new:
        ModeNew.run(args.new)
    elif args.all == args.find == 0:
        ModeNew.run(12)
    elif args.all:
        ModeAll.run()
    elif args.find:
        ModeFind.run(args.find)

    Bins.delold()
