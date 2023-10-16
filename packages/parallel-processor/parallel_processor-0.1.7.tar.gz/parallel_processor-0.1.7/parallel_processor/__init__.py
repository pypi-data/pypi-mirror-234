"""
# 介绍
我们提供了一个可快速处理大量数据的多进程数据处理模块
此模块可以处理list、numpy、pandas等数据，并且可以以tuple的形式输入，以tuple的形式输出
中间的处理过程可以让用户来决定，只要传入一个自定义函数即可
可设置进程数
----------------------------
# 作者
连晓磊 lian222@foxmail.com
王岳   wangyue29@tal.com
----------------------------

"""

import numpy as np
import math
import multiprocessing
import copy


def _process_data_subprocessing(idx, manager_dict, data, op_func, kwargs):
    manager_dict[idx] = op_func(data, **kwargs)


def process_data(data, op_func, num_workers=1, data_type='list', **kwargs):
    """
        多进程处理数据
    Args:
        data: 输入数据（可以是一个ndarray、list以及一个tuple(e.g. (X, Y)，当输入数据为tuple时，需要设置参数is_tuple_data为True )）
        op_func: 处理函数，用于操作数据
        num_workers: 进程数
        data_type: 数据类型（'array'|'list', default 'list'）
        **kwargs: 其它参数

    Returns:
        处理完成的数据
    """

    def throw_error(e):
        raise e

    func_kwargs = kwargs.get('func_kwargs')
    is_tuple_data = kwargs.get('is_tuple_data')
    if func_kwargs is None:
        func_kwargs = {}
    if num_workers < 2:
        data = op_func(data, **func_kwargs)
    else:
        # 计算每个进程处理的数据量
        if is_tuple_data:
            data_len = len(data[0])
        else:
            data_len = len(data)

        batch_size = math.ceil(data_len / num_workers)
        # 按照单进程数据量对数据集进行切分，当数据量不能被进程数整除时，最后一个进程会和其它进程处理的数据量不同
        batch_idxs = [list(range(batch_size * idx, min(batch_size * (idx + 1), data_len))) for idx in
                      range(num_workers)]

        # 定义进程池
        pool = multiprocessing.Pool(num_workers)
        # 定义数据共享管理器
        manager = multiprocessing.Manager()
        manager_dict = manager.dict()

        # 向进程池分发任务
        for idx in range(len(batch_idxs)):
            # 分批将数据放入进程
            if data_type == 'array':
                _ = pool.apply_async(_process_data_subprocessing,
                                     (idx, manager_dict,
                                      data[batch_idxs[idx]] if not is_tuple_data else [item[batch_idxs[idx]] for item in
                                                                                       data],
                                      op_func, func_kwargs), error_callback=throw_error)
            elif data_type == 'list':
                _ = pool.apply_async(_process_data_subprocessing,
                                     (idx, manager_dict,
                                      [data[j] for j in batch_idxs[idx]] if not is_tuple_data else [
                                          [item[j] for j in batch_idxs[idx]] for item in data],
                                      op_func, func_kwargs), error_callback=throw_error)

        pool.close()
        pool.join()

        # 获取每个进程的结果数据
        sub_data = [manager_dict.get(idx) for idx in range(len(batch_idxs))]

        data = copy.copy(sub_data[0])

        low_memory = kwargs.get('low_memory')

        # 低内存模式，不使用np进行数据组装
        if low_memory:
            # 判断数据的格式
            if is_tuple_data:
                # [(d1, d2), (d1, d2), ...]
                [[data[j].extend(jtem) for j, jtem in enumerate(item)] for item in sub_data]
            else:
                [data.extend(item) for item in sub_data]
        else:  # 使用np进行数据组装，速度快，内存占用高
            data = []
            seg_locale = [0]  # 当数据为tuple时，用于记录合并后再分割时的index
            subprocess_result = None
            for idx in range(len(batch_idxs)):
                subprocess_result = manager_dict.get(idx)
                # 判断自定义函数返回的数据是否为tuple，如果是tuple，则此函数也会返回多个值
                # 例如自定义函数最后是`return (input_ids_batch, segment_ids_batch, input_mask_batch)`，
                # 则此函数最终返回结果是(input_ids_all, segment_ids_all, input_mask_all)
                if isinstance(subprocess_result, tuple):
                    if idx == 0:
                        for item in subprocess_result[:-1]:
                            if len(item.shape) == 1:
                                item_shape = (item.shape[0], 1)
                            else:
                                item_shape = item.shape
                            seg_locale.append(item_shape + seg_locale[-1])
                        seg_locale = seg_locale[1:]
                    # 将tuple数据拼接成一个大ndarray
                    tmp_data = np.concatenate(subprocess_result, axis=1)
                else:
                    tmp_data = subprocess_result
                data.append(tmp_data)
            # 将最后一个batch的拼接起来
            data = np.concatenate(data, axis=0)

            if isinstance(subprocess_result, tuple):
                # 将拼接后的ndarray再拆分成tuple
                data = np.split(data, seg_locale, axis=1)
    return data
