#!/usr/bin/env python
# coding: utf-8
# 2292879219@qq.com
"""
Created on Mon Mar 17 17:35:12 2020

@author: xczcx
"""
from importlib import import_module
import torch, re
from sen2vec.models.file_utils import sample_generate
import pandas as pd


class Model_Tools(object):
    @classmethod
    def config_load_(cls, model_path=None, *args, **kwargs):
        x = import_module('sen2vec.models.bert')
        config = x.Config(*args, **kwargs)
        config.model_path = model_path
        return x, config

    @classmethod
    def model_load_(cls, x, config):
        model = x.Model(config).to(config.device)
        model.load_state_dict(torch.load(config.model_path, config.device)) if config.model_path else None
        return model

    @classmethod
    def model_name_check_(cls, config):
        fa1 = True if 'seq' in config.model_name else False
        fa2 = True if 'ner' in config.model_name or 'simp' in config.model_name or 'qa' in config.model_name or \
                      'cls' in config.model_name or 'ori' in config.model_name or \
                      any(nd in config.model_name for nd in config.ver_list) else False
        return fa1, fa2

    @classmethod
    def utils_load_(cls, *args, **kwargs):
        x = import_module('sen2vec.models.bert')
        utils = x.Utils(*args, **kwargs)
        return x, utils


class Data_Tools(object):
    split_mark = ';;'

    def data_pre_process_(self, data, title):
        sen2vec_index_ = data[[title]].reset_index()['index'].to_list()
        data['sen2vec_index_'] = sen2vec_index_
        data_sen2vec_index_ = data[[title] + ['sen2vec_index_']].copy()
        return data, data_sen2vec_index_

    @classmethod
    def data_post_process(cls, data_ori, data, title):
        data = data.drop([title], axis=1)
        data_ori = pd.merge(data_ori, data, how='left', on=['sen2vec_index_'])
        data_ori = data_ori.drop(['sen2vec_index_'], axis=1)
        return data_ori

    @classmethod
    def data_clean_(cls, data, title):
        data_ori, data = cls.data_pre_process_(cls, data, title)
        data = data.dropna(subset=[title], axis=0).reset_index(drop=True)
        data[title] = data[title].apply(lambda x: x.replace('\t', ''))
        data[title] = data[title].apply(lambda x: x.strip().strip(cls.split_mark))
        data[title] = data[title].apply(lambda x: None if len(x) == 0 else x)
        data = data.dropna(subset=[title], axis=0).reset_index(drop=True)
        return data_ori, data

    @classmethod
    def data_process_(cls, data, title):
        data_feature = []
        for i, line in enumerate(data[title]):
            for ll in line.split(cls.split_mark):
                data_feature.append(ll + "\t" + str(i)) if ll != '' else None
        len_data = len(data)
        return data_feature, len_data

    @classmethod
    def data_output_(cls, data, exf, config):
        data = pd.concat([data, exf[3][0]], axis=1) if 'ner' in config.model_name else data.copy()
        data = pd.concat([data, exf[3][1]], axis=1) if 'simp' in config.model_name else data
        data = pd.concat([data, exf[3][2]], axis=1) if 'qa' in config.model_name else data
        data = pd.concat([data, exf[2]], axis=1) if 'cls' in config.model_name else data
        data = pd.concat([data, exf[1]], axis=1) if any(nd in config.model_name for nd in config.ver_list) else data
        data = pd.concat([data, exf[0]], axis=1) if 'ori' in config.model_name else data
        return data


class Seq_Tools(object):
    @classmethod
    def seq_predict(cls, text, config, model, by_sentence=False):
        model.eval()
        pattern_s = re.compile(r'\s')
        text_out = []
        for texts in text.split('\n'):
            texts = re.sub(pattern_s, '', texts)
            t_out = []
            if by_sentence:
                len_t_out = 0
                for t in texts.split('。'):
                    if t is '':
                        continue
                    if len(t) <= 20:
                        summary = t
                    else:
                        t = t + '。'
                        summary = sample_generate(t, config, model, top_k=5, top_p=0.95)
                        summary = re.sub(pattern_s, '', summary)
                    t_out.append(summary)
                    len_t_out = len(t_out)
                t_out = '。'.join(t_out)
                if len_t_out > 20:
                    t_out = t_out + '。' if t_out[-1] != '。' else t_out
            else:
                t = texts
                if t is '':
                    continue
                if len(t) <= 20:
                    summary = t
                else:
                    summary = sample_generate(t, config, model, top_k=5, top_p=0.95)
                    summary = re.sub(pattern_s, '', summary)
                    if len(summary) > 20:
                        summary = summary + '。' if summary[-1] != '。' else summary
                t_out = summary
            t_out = cls.seq_out_clean(t_out)
            text_out.append(t_out)
        text_out = '\n'.join(text_out)
        return text_out

    @classmethod
    def seq_out_clean(cls, x):
        pattern_1 = re.compile('！。|!。')
        pattern_2 = re.compile('？。|\?。')
        pattern_3 = re.compile('\.。|。。|。\.')
        x = re.sub(pattern_1, '！', x)
        x = re.sub(pattern_2, '？', x)
        x = re.sub(pattern_3, '。', x)
        return x
