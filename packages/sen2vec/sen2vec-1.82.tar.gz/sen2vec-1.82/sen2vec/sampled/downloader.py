#!/usr/bin/env python
# coding: utf-8
# 2292879219@qq.com
"""
Created on Mon Mar 17 17:35:12 2020

@author: xczcx
"""
from six.moves import urllib
import os
import sys
import time
import requests


class Download_P(object):
    def __init__(self):
        self.defult_path = os.path.dirname(os.path.abspath(__file__))
        self.default_bin_name = 'pytorch_model.bin'
        self.default_ckpt_name = 'bert.ckpt'
        self.default_save_dir = self.defult_path + "/bertwwm_pretrain"
        self.default_txt = self.default_save_dir + '/model_url.txt'
        self.default_url = [x.strip() for x in open(self.default_txt).readlines()][0]
        self.chunk_size = 512
        self.secs_check = 2

    def download_and_extract(self, file_path, save_dir):
        """
        Parameter:
            filepath: list file_URL_path
            save_dir: str
        Return:
            None
        """
        for url, index in zip(file_path, range(len(file_path))):
            filename = url.split('/')[-1]
            filename = str(index) + '.jpg'
            save_path = os.path.join(save_dir, filename)
            urllib.request.urlretrieve(url, save_path)
            sys.stdout.write('\r>> Downloading %.1f%%' % (float(index + 1) / float(len(file_path)) * 100.0))
            sys.stdout.flush()
        print('\nSuccessfully downloaded')

    def _get_file_urls(self, file_url_txt):
        """
        Parameter:
            file_url_txt: str  txt
        Return:
            filepath: list  URL
        """
        file_path = []
        file = open(file_url_txt, 'r')
        for line in file.readlines():
            line = line.strip()
            file_path.append(line)
        file.close()
        return file_path

    def download_model(self, model_name, url_path, save_dir):
        """
        """
        filename = model_name + '.jpg'
        save_path = os.path.join(save_dir, filename)
        url_path = self.default_url if url_path is None else url_path
        urllib.request.urlretrieve(url_path, save_path)
        sys.stdout.write('\r>> Downloading %.1f%%' % (1.0 * 100.0))
        sys.stdout.flush()

    def formatFloat(self, num):
        return '{:.2f}'.format(num)

    def download_file(self, model_name=None, url_path=None, save_path=None):
        """
        Parameter:
            model_name: ckpt
            save_path: str
        Return:
            None
        """
        s = requests.session()
        save_path = os.path.join(save_path, model_name)
        url_path = url_path + "/" if url_path[-1] != '/' else url_path
        if os.path.exists(save_path):
            print('Model exists, download schedule canceled.')
            print(f"Save: {save_path}")
        else:
            url_path = url_path + model_name if url_path == self.default_url else url_path
            with s.get(url_path, stream=True) as fget:
                file_size = int(fget.headers["Content-Length"])
                print('-' * 32)
                print(f"Save: {save_path}")
                print(f"Size: {file_size / (1000 ** 2)}Mb")
                print(f"Link: {url_path}")
                print('-' * 32)
                file_done = 0
                percent_tmp = 0
                time1 = time.time()
                with open(save_path, "wb") as fw:
                    for chunk in fget.iter_content(self.chunk_size):
                        fw.write(chunk)
                        file_done = file_done + self.chunk_size
                        percent = file_done / file_size
                        if time.time() - time1 > self.secs_check:
                            speed = (percent - percent_tmp) * file_size / (1000 ** 2 * self.secs_check)
                            print(f'Download: {percent:.2%}', f' Speed: {self.formatFloat(speed)}M/S', end='\r')
                            percent_tmp = percent
                            time1 = time.time()
                print('Download: 100.0%')
        s.close()

