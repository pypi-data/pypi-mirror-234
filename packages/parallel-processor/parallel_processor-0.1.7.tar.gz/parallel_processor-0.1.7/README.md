# 介绍

我们提供了一个可快速处理大量数据的多进程数据处理模块

此模块可以处理list、numpy、pandas等数据，并且可以以tuple的形式输入，以tuple的形式输出

中间的处理过程可以让用户来决定，只要传入一个自定义函数即可

可设置进程数

----------------------------

# 样例

引入：
```python
from parallel_processor import process_data

# 注意在向进程池传入处理函数时，不能使用lambda的方式，否则会报错
from functools import partial
```

样例1：分词
```python
def seg(x):
    result = []
    for i in tqdm_notebook(x):
        result.append(list(jieba.cut(i)))
    return result

data = process_data(data, seg, num_workers=16)
```

-------------

样例2：text2ids
```python
def convert_example(x, f_token, max_seq_len, return_raw_data=False, mask_rate=0, x1=None, avg_split=False):
    input_ids_list = []
    input_mask_list = []
    segment_ids_list = []
    input_ids_gt_list = []
    contents = []

    if x1 is not None:
        if "JPY_PARENT_PID" in os.environ:
            bar = tqdm_notebook(zip(x, x1))
        else:
            bar = tqdm(zip(x, x1))
    else:
        if "JPY_PARENT_PID" in os.environ:
            bar = tqdm_notebook(x)
        else:
            bar = tqdm(x)

    for line in bar:
        if x1 is not None:
            line, line1 = line[0], line[1]
        else:
            line1 = ''
        if mask_rate <= 0:
            input_ids, input_mask, segment_ids = convert_single_example(max_seq_len, f_token, line, line1,
                                                                        avg_split=avg_split)
        else:
            input_ids, input_mask, segment_ids, input_ids_gt = convert_single_example_with_mlm(
                max_seq_len, f_token, line, line1, avg_split=avg_split)

        input_ids = np.array(input_ids)
        input_mask = np.array(input_mask)
        segment_ids = np.array(segment_ids)
        input_ids_list.append(input_ids)
        input_mask_list.append(input_mask)
        segment_ids_list.append(segment_ids)
        if mask_rate > 0:
            input_ids_gt = np.array(input_ids_gt)
            input_ids_gt_list.append(input_ids_gt)

        if return_raw_data:
            contents.append(list(line.replace('\n', '')))

    if mask_rate > 0:
        if return_raw_data:
            return np.array(input_ids_list), np.array(input_mask_list), np.array(segment_ids_list), \
                   np.array(input_ids_gt_list), np.array(contents)
        return np.array(input_ids_list), np.array(input_mask_list), np.array(segment_ids_list), \
               np.array(input_ids_gt_list)
    else:
        if return_raw_data:
            return np.array(input_ids_list), np.array(input_mask_list), np.array(segment_ids_list), np.array(contents)
        return np.array(input_ids_list), np.array(input_mask_list), np.array(segment_ids_list)

def _process(text, **kwargs):
    f_token = kwargs.get('f_token')
    max_seq_len = kwargs.get('max_seq_len', 128)
    return_raw_data = kwargs.get('return_raw_data', False)
    mask_rate = kwargs.get('mask_rate', 0)
    avg_split = kwargs.get('avg_split', False)
    if len(text.shape) > 1:
        text_a, text_b = text[:, 0], text[:, 1]
        return convert_example(text_a, f_token, max_seq_len, return_raw_data, mask_rate, text_b, avg_split=avg_split)
    else:
        return convert_example(text, f_token, max_seq_len, return_raw_data, mask_rate, avg_split=avg_split)

vocab_file = os.path.join(bert_model_dir, "vocab.txt")
f_token = FullTokenizer(vocab_file)

text = data[text_cols].values
func_kwargs = {'f_token': f_token, 'max_seq_len': max_seq_len, 'return_raw_data': return_raw_data,
               'mask_rate': mask_rate, 'avg_split': avg_split}

result = process_data(text, _process, num_workers=16, is_tuple_data=False, func_kwargs=func_kwargs)
input_ids = result[0]
input_mask = result[1]
segment_ids = result[2]
```
