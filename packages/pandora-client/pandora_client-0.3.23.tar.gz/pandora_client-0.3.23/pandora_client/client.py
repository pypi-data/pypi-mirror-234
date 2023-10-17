# encoding: utf-8
# vi:si:et:sw=4:sts=4:ts=4

import json
import os
import socket
import subprocess
import sys
import threading
import time

import requests

from . import extract

class Encoding:

    def worker(self):
        while True:
            if not self.client.next():
                return

    def __init__(self, client, threads=1):
        self.client = client
        self.threads = []
        for i in range(threads):
            t = threading.Thread(target=self.worker)
            t.start()
            self.threads.append(t)

    def join(self):
        for t in self.threads:
            t.join()


class DistributedClient:

    interrupted = False

    def __init__(self, url, name, threads):
        self.url = url
        while self.url and self.url[-1] == '/':
            self.url = self.url[:-1]
        self.name = name
        self.threads = threads
        self.supported_formats = extract.supported_formats()

    def ping(self, oshash):
        try:
            url = '%s/ping/%s/%s' % (self.url, oshash, self.name)
            requests.get(url)
        except:
            print('cound not ping server')

    def status(self, oshash, status):
        url = '%s/status/%s' % (self.url, oshash)
        requests.post(url, {'error': status})

    def upload(self, oshash, path):
        url = '%s/upload/%s' % (self.url, oshash)
        with open(path, 'rb') as f:
            requests.put(url, f)

    def next(self):
        url = '%s/next' % self.url
        data = requests.get(url).json()
        if 'oshash' in data:
            return self.encode(data['oshash'], data['cmd'], data['output'])
        return False

    def encode(self, oshash, cmds, output):
        if not isinstance(cmds[0], list):
            cmds = [cmds]
        for cmd in cmds:
            cmd[0] = extract.command('ffmpeg')
            if self.threads > 1:
                cmd = cmd[:1] + ['-nostats', '-loglevel', 'error'] + cmd[1:]
            if 'webm' in cmd and not self.supported_formats['webm']:
                print("ffmpeg is compiled without WebM support")
                return
            elif cmd[-1].endswith('.mp4') and not self.supported_formats['webm']:
                print("ffmpeg is compiled without H.264 support")
                return
            try:
                if self.threads > 1:
                    print('encode', oshash)
                p = subprocess.Popen(cmd)
                r = None
                n = 0
                while True:
                    r = p.poll()
                    if r is None:
                        if n % 60 == 0:
                            self.ping(oshash)
                            n = 0
                        time.sleep(2)
                        n += 2
                    else:
                        break
            except KeyboardInterrupt:
                p.kill()
                #encoding was stopped, put back in queue
                self.status(oshash, '')
                if os.path.exists(output):
                    os.unlink(output)
                if self.threads > 1:
                    self.interrupted = True
                    return False
                sys.exit(1)
            if r != 0:
                break
        if r == 0:
            if self.threads > 1:
                print('ok', oshash)
            self.upload(oshash, output)
        else:
            if self.threads > 1:
                print('error', oshash)
            self.status(oshash, 'failed')
        if os.path.exists(output):
            os.unlink(output)
        return True

    def run(self):
        if self.threads > 1:
            enc = Encoding(self, self.threads)
            enc.join()
        else:
            self.run_single()

    def run_single(self):
        new = True
        while True:
            if not self.next():
                if new:
                    new = False
                    print("currently no more files to encode, ctrl-c to quit")
                try:
                    time.sleep(60)
                except KeyboardInterrupt:
                    return
            else:
                new = True


if __name__ == '__main__':
    url = 'http://127.0.0.1:8789'
    if len(sys.args) == 0:
        name = socket.gethostname()
    else:
        name = sys.argv[1]
    c = DistributedClient(url, name)
    c.run()
