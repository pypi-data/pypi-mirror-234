#!/usr/bin/env python
# coding: utf-8
# 2292879219@qq.com
"""
Created on Mon Mar 17 17:35:12 2020

@author: xczcx
"""
import torch
from tqdm import tqdm


PAD, CLS, SEP = '[PAD]', '[CLS]', '[SEP]'


def build_dataset_test(config):

    def load_dataset(path, pad_size=32):
        contents = []
        f = path
        for line in tqdm(f):
            lin = line.strip()
            if not lin:
                continue
            try:
                content, label = lin.split("\t")
            except:
                print("error", lin)
            token = config.tokenizer.tokenize(content)
            if not token:
                token = [CLS]
            else:
                token = [CLS] + token if token[0] != CLS else token  # sep for seq
            seq_len = len(token)
            mask = []
            token_ids = config.tokenizer.convert_tokens_to_ids(token)

            first_token_type_ids = [0] * len(token_ids)  # x_type for seq
            first_token_type_ids_for_mask = [1] * len(token_ids)  # mask for seq

            if pad_size:
                if len(token) < pad_size:
                    mask = [1] * len(token_ids) + [0] * (pad_size - len(token))
                    token_ids += ([0] * (pad_size - len(token)))  # token_ids pad
                else:
                    mask = [1] * pad_size
                    token_ids = token_ids[:pad_size]
                    seq_len = pad_size
            contents.append((token_ids, int(label), seq_len, mask, first_token_type_ids, first_token_type_ids_for_mask))
        return contents
    test = load_dataset(config.test_path, config.pad_size)
    return test


class DatasetIterater(object):
    def __init__(self, batches, batch_size, device):
        self.batch_size = batch_size
        self.batches = batches
        self.n_batches = len(batches) // batch_size
        self.residue = False
        if len(batches) % self.n_batches != 0:
            self.residue = True
        self.index = 0
        self.device = device

    def _to_tensor(self, datas):
        x = torch.LongTensor([_[0] for _ in datas]).to(self.device)
        y = torch.LongTensor([_[1] for _ in datas]).to(self.device)

        seq_len = torch.LongTensor([_[2] for _ in datas]).to(self.device)
        mask = torch.LongTensor([_[3] for _ in datas]).to(self.device)

        x_type = torch.LongTensor([_[4] for _ in datas]).to(self.device)
        x_id_for_mask = torch.LongTensor([_[5] for _ in datas]).to(self.device)
        return (x, seq_len, mask, x_type, x_id_for_mask), y

    def __next__(self):
        if self.residue and self.index == self.n_batches:
            batches = self.batches[self.index * self.batch_size: len(self.batches)]
            self.index += 1
            batches = self._to_tensor(batches)
            return batches

        elif self.index >= self.n_batches:
            self.index = 0
            raise StopIteration
        else:
            batches = self.batches[self.index * self.batch_size: (self.index + 1) * self.batch_size]
            self.index += 1
            batches = self._to_tensor(batches)
            return batches

    def __iter__(self):
        return self

    def __len__(self):
        if self.residue:
            return self.n_batches + 1
        else:
            return self.n_batches


def build_iterator(dataset, config):
    iter = DatasetIterater(dataset, config.batch_size, config.device)
    return iter
