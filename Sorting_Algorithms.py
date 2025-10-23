import pandas as pd
import numpy as np


def bubble_sort_df(df, column):
    arr = df.values.copy()
    col_idx = df.columns.get_loc(column)
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j, col_idx] > arr[j + 1, col_idx]:
                arr[[j, j + 1]] = arr[[j + 1, j]]
    return pd.DataFrame(arr, columns=df.columns)


def insertion_sort_df(df, column):
    arr = df.values.copy()
    col_idx = df.columns.get_loc(column)
    n = len(arr)
    for i in range(1, n):
        key_row = arr[i].copy()
        j = i - 1
        while j >= 0 and arr[j, col_idx] > key_row[col_idx]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key_row
    return pd.DataFrame(arr, columns=df.columns)

def selection_sort_df(df, column):
    arr = df.values.copy()
    col_idx = df.columns.get_loc(column)
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j, col_idx] < arr[min_idx, col_idx]:
                min_idx = j
        min_row = arr[min_idx].copy()
        arr[i+1:min_idx+1] = arr[i:min_idx]
        arr[i] = min_row
    return pd.DataFrame(arr, columns=df.columns)

def merge_sort_df(df, column):
    arr = df.values.copy()
    col_idx = df.columns.get_loc(column)

    def merge(arr):
        if len(arr) <= 1:
            return arr
        mid = len(arr) // 2
        left = merge(arr[:mid])
        right = merge(arr[mid:])
        merged = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i][col_idx] <= right[j][col_idx]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
        merged.extend(left[i:])
        merged.extend(right[j:])
        if merged:
            return np.array(merged)
        else:
            return np.empty((0, arr.shape[1]))
    sorted_arr = merge(arr)
    return pd.DataFrame(sorted_arr, columns=df.columns)

def quick_sort_df(df, column):
    arr = df.values.copy()
    col_idx = df.columns.get_loc(column)

    def quick(arr):
        if len(arr) <= 1:
            return arr
        pivot = arr[len(arr) // 2, col_idx]
        left = np.array([row for row in arr if row[col_idx] < pivot])
        middle = np.array([row for row in arr if row[col_idx] == pivot])
        right = np.array([row for row in arr if row[col_idx] > pivot])
        arrays_to_stack = [a for a in [quick(left), middle, quick(right)] if a.size > 0]
        if arrays_to_stack:
            return np.vstack(arrays_to_stack)
        else:
            return np.empty((0, arr.shape[1]))
    sorted_arr = quick(arr)
    return pd.DataFrame(sorted_arr, columns=df.columns)


def counting_sort_df(df, column):
    arr = df.values.copy()
    col_idx = df.columns.get_loc(column)
    values = arr[:, col_idx].astype(int)
    min_val, max_val = values.min(), values.max()
    count = [0] * (max_val - min_val + 1)
    output = np.zeros_like(arr)
    for v in values:
        count[v - min_val] += 1
    for i in range(1, len(count)):
        count[i] += count[i - 1]
    for i in reversed(range(len(arr))):
        v = values[i]
        count[v - min_val] -= 1
        output[count[v - min_val]] = arr[i]
    return pd.DataFrame(output, columns=df.columns)

def radix_sort_df(df, column):
    arr = df.values.copy()
    col_idx = df.columns.get_loc(column)
    values = arr[:, col_idx].astype(int)
    max_val = values.max()
    exp = 1
    n = len(arr)
    output = np.zeros_like(arr)
    while max_val // exp > 0:
        count = [0] * 10
        for i in range(n):
            index = (values[i] // exp) % 10
            count[index] += 1
        for i in range(1, 10):
            count[i] += count[i - 1]
        for i in reversed(range(n)):
            index = (values[i] // exp) % 10
            count[index] -= 1
            output[count[index]] = arr[i]
        arr = output.copy()
        values = arr[:, col_idx].astype(int)
        exp *= 10
    return pd.DataFrame(arr, columns=df.columns)

def bucket_sort_df(df, column):
    arr = df.values.copy()
    col_idx = df.columns.get_loc(column)
    values = arr[:, col_idx].astype(float)
    n = len(arr)
    vmin, vmax = values.min(), values.max()
    if vmax == vmin:
        return df.copy()

    buckets = [[] for _ in range(n)]
    for i in range(n):
        idx = int((values[i] - vmin) / (vmax - vmin) * (n - 1))
        buckets[idx].append(arr[i])

    sorted_arr_list = [np.array(sorted(b, key=lambda x: x[col_idx])) for b in buckets if b]
    if sorted_arr_list:
        sorted_arr = np.vstack(sorted_arr_list)
    else:
        sorted_arr = np.empty((0, arr.shape[1]))
    return pd.DataFrame(sorted_arr, columns=df.columns)
