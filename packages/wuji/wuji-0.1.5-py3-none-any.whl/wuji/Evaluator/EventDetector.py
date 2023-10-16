#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   EventDetector 
@Time        :   2023/9/25 17:14
@Author      :   Xuesong Chen
@Description :   
"""

import pandas as pd
import dcase_util
from wuji import sed_eval


def compute_metrics(ref: pd.DataFrame, pred: pd.DataFrame, print_logs=True):
    '''
    :param pred and ref:
    :return:
    '''
    pred_event_list = dcase_util.containers.MetaDataContainer(
        pred.to_dict(orient='records')
    )
    ref_event_list = dcase_util.containers.MetaDataContainer(
        ref.to_dict(orient='records')
    )

    event_based_metrics = sed_eval.sound_event.EventBasedMetrics(
        event_label_list=ref_event_list.unique_event_labels,
        t_collar=5.,
        evaluate_onset=True,
        evaluate_offset=True,
        percentage_of_length=0.5,  # offset可容忍的误差，即offset误差在percentage_of_length*duration内都算正确，越接近于1，越宽松
        onset_offset_op='or'
    )

    for filename in ref_event_list.unique_files:
        reference_event_list_for_current_file = ref_event_list.filter(
            filename=filename
        )

        estimated_event_list_for_current_file = pred_event_list.filter(
            filename=filename
        )

        event_based_metrics.evaluate(
            reference_event_list=reference_event_list_for_current_file,
            estimated_event_list=estimated_event_list_for_current_file
        )

    if print_logs:
        print(event_based_metrics)
    else:
        return event_based_metrics


def convert_df_to_sed_type(df, file, scene_label):
    df['event_offset'] = df['Start'] + df['Duration']
    df.rename(columns={
        'Type': 'event_label',
        'Start': 'event_onset',
    }, inplace=True
    )
    df['file'] = file
    df['scene_label'] = scene_label
    df.drop(labels='Duration', axis=1, inplace=True)
    return df


class EventDetectorEvaluator:
    def __init__(self, gt_df, pred_df, file='pseudo_file', scene_label='pseudo_scene'):
        self.gt_df = convert_df_to_sed_type(gt_df, file, scene_label)
        self.pred_df = convert_df_to_sed_type(pred_df, file, scene_label)
        self.metrics = compute_metrics(self.gt_df, self.pred_df, print_logs=False).results()

    def _get_metric(self, metric, label='overall', average='macro'):
        if label == 'overall':
            if average == 'macro':
                if metric in ['f_measure', 'precision', 'recall']:
                    return self.metrics['class_wise_average']['f_measure'][metric]
            elif average == 'micro':
                if metric in ['f_measure', 'precision', 'recall']:
                    return self.metrics['overall']['f_measure'][metric]
        else:
            assert label in self.metrics['class_wise'], 'label not in class_wise'
            if metric in ['f_measure', 'precision', 'recall']:
                return self.metrics['class_wise'][label]['f_measure'][metric]

    def recall(self, label='overall', average='macro'):
        return self._get_metric('recall', label, average)

    def precision(self, label='overall', average='macro'):
        return self._get_metric('precision', label, average)

    def f1_score(self, label='overall', average='macro'):
        return self._get_metric('f_measure', label, average)


