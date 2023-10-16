#!/usr/bin/env python
# coding: utf-8
# 2292879219@qq.com
"""
Created on Mon Mar 17 17:35:12 2020

@author: xczcx
"""
import pandas as pd
import numpy as np
import time
import os
from sen2vec.util.utils import build_dataset_test, build_iterator
from sen2vec.util.tools import *

"""
This module provides functions to transform sentences to vectors.
There are two ways to employ sen2vec:
1.Use the default models we provide:
    from sen2vec import sen2vec_fi, sen2vec_download
    sen2vec_download() 
    new_df = sen2vec_fi(old_df, df_title)
2.Use the self-defined models:
    from sen2vec import sen2vec
    model_config = (model_name, vec_dim, num_class, model_path)  # (set your model config)
    s = sen2vec(model_config)  # (set your model config)
    new_df = s.sen2vec_fi(old_df, df_title)
"""


class CONFIG(object):
    def __init__(self):
        self.dataset = os.path.dirname(os.path.abspath(__file__)) + "/sampled"
        self.bert_config_path = self.dataset + "/bertwwm_pretrain/model_config.txt"
        self.mcl = [x.strip().split(':') for x in open(self.bert_config_path).readlines()]
        self.mcd = {idx: tag for idx, tag in self.mcl}
        self.model_config = (self.mcd['model_name'], int(self.mcd['vec_dim']), int(self.mcd['num_class']))
        self.model_path = None


class sen2vec(CONFIG):
    def __init__(self, model_config=None):
        CONFIG.__init__(self)
        if model_config is not None:
            self.model_config = model_config
            self.model_path = self.model_config[3] if len(model_config) == 4 else None
        self.model_name = self.model_config[0]
        self.vec_dim = self.model_config[1]
        self.num_class = self.model_config[2]
        _, self.utils = Model_Tools.utils_load_()

    def sen2vec_fi(self, data, title, by_sentence=False):
        """
        Use the self-defined models:
            from sen2vec import sen2vec
            model_config = (model_name, vec_dim, num_class, model_path)  # (set your model config)
            s = sen2vec(model_config)  # (set your model config)
            new_df = s.sen2vec_fi(old_df, df_title)
        """
        dataset = self.dataset
        model_name, vec_dim, num_class, model_path = self.model_name, self.vec_dim, self.num_class, self.model_path
        x, config = Model_Tools.config_load_(model_path, dataset, model_name, vec_dim, num_class)
        fa1, fa2 = Model_Tools.model_name_check_(config)
        fa = 0 if fa1 == False and fa2 == False else 1
        assert fa == 1, 'model_name {0} error'.format(model_name)
        data_ori, data = Data_Tools.data_clean_(data, title)
        config.seq_check = True
        if fa1:
            model = Model_Tools.model_load_(x, config)
            data['SEQ'] = None
            for i in range(len(data)):
                text = data[title][i]
                text_out = Seq_Tools.seq_predict(text, config, model, by_sentence)
                data.loc[i, 'SEQ'] = text_out
        config.seq_check = False
        if fa2:
            data_feature, len_data = Data_Tools.data_process_(data, title)
            config.test_path = data_feature
            model = Model_Tools.model_load_(x, config)
            exf = sen2vec_process_(model, config, len_data)
            data = Data_Tools.data_output_(data, exf, config)
        data = Data_Tools.data_post_process(data_ori, data, title)
        return data

    def sen2vec_load(self):
        dataset = self.dataset
        model_name, vec_dim, num_class, model_path = self.model_name, self.vec_dim, self.num_class, self.model_path
        x, config = Model_Tools.config_load_(model_path, dataset, model_name, vec_dim, num_class)
        config.seq_check = True if 'seq' in model_name else False
        model = Model_Tools.model_load_(x, config)
        self.config = config
        self.config.model = self.model = model
        return self.config

    def sen2vec_fa(self, data=None, title=None, by_sentence=False):
        """
        Use the default models we provide:
            from sen2vec import sen2vec
            ss=sen2vec()
            ss.model_name='cbertner'  # (set your model config)
            ss.model_path='cbertner.ckpt'
            ss.sen2vec_load()
            df_new = ss.sen2vec_fa(df_old, df_title)
        """
        model_name, config, model = self.config.model_name, self.config, self.model
        fa1, fa2 = Model_Tools.model_name_check_(config)
        assert fa1 != fa2, 'model_name {0} error'.format(model_name)
        data_ori, data = Data_Tools.data_clean_(data, title)
        if fa1:
            data['SEQ'] = None
            for i in range(len(data)):
                text = data[title][i]
                text_out = Seq_Tools.seq_predict(text, config, model, by_sentence)
                data.loc[i, 'SEQ'] = text_out
        if fa2:
            data_feature, len_data = Data_Tools.data_process_(data, title)
            config.test_path = data_feature
            exf = sen2vec_process_(model, config, len_data)
            data = Data_Tools.data_output_(data, exf, config)
        data = Data_Tools.data_post_process(data_ori, data, title)
        return data


def sen2vec_load(model_name=None, model_path=None, vec_dim=None, num_class=None):
    dataset = os.path.dirname(os.path.abspath(__file__)) + "/sampled"
    x, config = Model_Tools.config_load_(model_path, dataset, model_name, vec_dim, num_class)
    config.seq_check = True if 'seq' in model_name else False
    model = Model_Tools.model_load_(x, config)
    config.model = model
    return config


def sen2vec_fa(data=None, title=None, config=None, by_sentence=False):
    """
    Use the default models we provide:
        from sen2vec import sen2vec_fa, sen2vec_load
        config = sen2vec_load()
        new_df = sen2vec_fa(model, config, old_df, df_title)
    """
    model, model_name = config.model, config.model_name
    fa1, fa2 = Model_Tools.model_name_check_(config)
    assert fa1 != fa2, 'model_name {0} error'.format(model_name)
    data_ori, data = Data_Tools.data_clean_(data, title)
    if fa1:
        data['SEQ'] = None
        for i in range(len(data)):
            text = data[title][i]
            text_out = Seq_Tools.seq_predict(text, config, model, by_sentence)
            data.loc[i, 'SEQ'] = text_out
    if fa2:
        data_feature, len_data = Data_Tools.data_process_(data, title)
        config.test_path = data_feature
        exf = sen2vec_process_(model, config, len_data)
        data = Data_Tools.data_output_(data, exf, config)
    data = Data_Tools.data_post_process(data_ori, data, title)
    return data


def sen2vec_fi(data=None, title=None, model_name=None, vec_dim=None, num_class=None, model_path=None,
               by_sentence=False):
    """
    Use the default models we provide:
        from sen2vec import sen2vec_fi
        new_df = sen2vec_fi(old_df, df_title)
    """
    dataset = os.path.dirname(os.path.abspath(__file__)) + "/sampled"
    x, config = Model_Tools.config_load_(model_path, dataset, model_name, vec_dim, num_class)
    fa1, fa2 = Model_Tools.model_name_check_(config)
    fa = 0 if fa1 == False and fa2 == False else 1
    assert fa == 1, 'model_name {0} error'.format(model_name)
    data_ori, data = Data_Tools.data_clean_(data, title)
    config.seq_check = True
    if fa1:
        model = Model_Tools.model_load_(x, config)
        data['SEQ'] = None
        for i in range(len(data)):
            text = data[title][i]
            text_out = Seq_Tools.seq_predict(text, config, model, by_sentence)
            data.loc[i, 'SEQ'] = text_out
    config.seq_check = False
    if fa2:
        data_feature, len_data = Data_Tools.data_process_(data, title)
        config.test_path = data_feature
        model = Model_Tools.model_load_(x, config)
        exf = sen2vec_process_(model, config, len_data)
        data = Data_Tools.data_output_(data, exf, config)
    data = Data_Tools.data_post_process(data_ori, data, title)
    return data


def sen2vec_process_(model, config, len_data):
    model.eval()
    test_data = build_dataset_test(config)
    test_iter = build_iterator(test_data, config)
    time_start = time.time()
    n = 0
    for text, j in test_iter:
        outputs_0, outputs, outputs_classes, outputs_ner = model(text)
        if j == 0 and n == 0:
            vec_dim_0 = len(outputs_0[0])
            vec_dim = len(outputs[0])
            len_vecs = len(outputs_classes)
            len_vec_dims = []
            len_vec_dims_sum = 0
            for i in range(len_vecs):
                len_vec_dims.append(len(outputs_classes[i][0]))
                len_vec_dims_sum += len(outputs_classes[i][0])
            feature_0 = [np.zeros(vec_dim_0) for _ in range(len_data)]
            feature_2 = [np.zeros(vec_dim) for _ in range(len_data)]
            feature_3 = [np.zeros(len_vec_dims_sum) for _ in range(len_data)]
            feature_4 = ['' for _ in range(len_data)]
            feature_8 = ['' for _ in range(len_data)]
            feature_9 = ['' for _ in range(len_data)]
        j_index = j.cpu().data.numpy()[0]
        for i in range(len_vecs):
            if i == 0:
                outputs_1 = outputs_classes[i].cpu().data.numpy()[0]
            else:
                outputs_t = outputs_classes[i].cpu().data.numpy()[0]
                outputs_1 = np.concatenate((outputs_1, outputs_t), axis=0)
        feature_0[j_index] += outputs_0.cpu().data.numpy()[0]
        feature_2[j_index] += outputs.cpu().data.numpy()[0]
        feature_3[j_index] += outputs_1
        feature_4[j_index] = str(outputs_ner[0]) if \
            feature_4[j_index] == '' else feature_4[j_index] + Data_Tools.split_mark + str(outputs_ner[0])
        feature_8[j_index] = str(outputs_ner[1]) if \
            feature_8[j_index] == '' else feature_8[j_index] + Data_Tools.split_mark + str(outputs_ner[1])
        feature_9[j_index] = str(outputs_ner[2]) if \
            feature_9[j_index] == '' else feature_9[j_index] + Data_Tools.split_mark + str(outputs_ner[2])
        n += 1
        if j_index % 100 == 0:
            print("Cycle: ", j_index, 'totally cost', time.time() - time_start)
    out0 = pd.DataFrame(feature_0)
    out2 = pd.DataFrame(feature_2)
    out3 = pd.DataFrame(feature_3)
    out4 = pd.DataFrame(feature_4, columns=['NER_entity'])
    out8 = pd.DataFrame(feature_8, columns=['NER_simp'])
    out9 = pd.DataFrame(feature_9, columns=['QA'])
    len_vec_dims_cumsum = len_vec_dims.copy()
    for i in range(len_vecs):
        len_vec_dims_cumsum[i] = len_vec_dims_cumsum[i] + len_vec_dims_cumsum[i - 1] if i > 0 else len_vec_dims_cumsum[
            i]
    for i in range(len_vecs):
        listi = [ii for ii in range(len_vec_dims[i])]
        listi = [iii + len_vec_dims_cumsum[i - 1] for iii in listi] if i > 0 else listi
        out3['CLS' + str(i)] = np.argmax(np.array(out3[listi]), axis=1)
    for i in range(len_vec_dims_sum):
        out3.rename(columns={i: "out" + str(i)}, inplace=True)
    out3 = out3.loc[:, out3.columns.str.contains('CLS')]
    exf = (out0, out2, out3, (out4, out8, out9))
    return exf


def sen2vec_download(model_name=None, url_path=None, save_path=None):
    """
    Download the default models we provide:
        from sen2vec import sen2vec_download
        sen2vec_download()
    """
    fa = 0 if url_path is None and model_name is None else 1
    from sen2vec.sampled.downloader import Download_P
    dp = Download_P()
    if save_path is None:
        save_path = input('model save_path:')
    save_path = None if save_path == '' else os.path.normpath(save_path)
    save_path = dp.default_save_dir if save_path is None else save_path
    url_path = dp.default_url if url_path is None else url_path
    if fa == 0:
        dp.download_file(dp.default_bin_name, url_path, dp.default_save_dir)
        dp.download_file(dp.default_ckpt_name, url_path, save_path)
    elif fa == 1:
        model_name = dp.default_ckpt_name if model_name is None else model_name
        dp.download_file(model_name, url_path, save_path)
