import pandas as pd
import numpy as np

import pandas as pd

def linear_multi_filter(df, columns, filters, operations, values):
    result_rows = []

    for _, row in df.iterrows():

        col = columns[0]
        flt = filters[0]
        val = str(values[0])
        row_val = str(row[col])

        if flt == "contains":
            cond_result = val.lower() in row_val.lower()
        elif flt == "endswith":
            cond_result = row_val.lower().endswith(val.lower())
        elif flt == "startswith":
            cond_result = row_val.lower().startswith(val.lower())
        elif flt == "=":
            cond_result = row_val == val
        elif flt == "!=":
            cond_result = row_val != val
        elif flt == ">":
            try:
                cond_result = float(row_val) > float(val)
            except:
                cond_result = False
        elif flt == "<":
            try:
                cond_result = float(row_val) < float(val)
            except:
                cond_result = False
        else:
            cond_result = False

        for i in range(1, len(columns)):
            col2 = columns[i]
            flt2 = filters[i]
            val2 = str(values[i])
            row_val2 = str(row[col2])

            if flt2 == "contains":
                cond2 = val2.lower() in row_val2.lower()
            elif flt2 == "endswith":
                cond2 = row_val2.lower().endswith(val2.lower())
            elif flt2 == "startswith":
                cond2 = row_val2.lower().startswith(val2.lower())
            elif flt2 == "=":
                cond2 = row_val2 == val2
            elif flt2 == ">":
                try:
                    cond2 = float(row_val2) > float(val2)
                except:
                    cond2 = False
            elif flt2 == "<":
                try:
                    cond2 = float(row_val2) < float(val2)
                except:
                    cond2 = False
            else:
                cond2 = False

            op = operations[i - 1].upper() if i - 1 < len(operations) else "AND"

            if op == "AND":
                cond_result = cond_result and cond2
            elif op == "OR":
                cond_result = cond_result or cond2
            elif op == "NOT":
                cond_result = cond_result and not cond2

        if cond_result:
            result_rows.append(row)

    return pd.DataFrame(result_rows)


import pandas as pd

def binary_multi_search(df, columns, filters, operations, values):
    if not columns or not values:
        return df.copy()

    mask = pd.Series([True] * len(df), index=df.index)

    for i, col in enumerate(columns):
        if col not in df.columns:
            continue
        
        val = values[i]
        flt = filters[i] if i < len(filters) else "="

        col_data = df[col]

        if flt == "contains":
            current_mask = col_data.astype(str).str.contains(str(val), case=False, na=False)
        elif flt == "startswith":
            current_mask = col_data.astype(str).str.startswith(str(val), na=False)
        elif flt == "endswith":
            current_mask = col_data.astype(str).str.endswith(str(val), na=False)
        elif flt == ">":
            current_mask = pd.to_numeric(col_data, errors='coerce') > pd.to_numeric(val, errors='coerce')
        elif flt == "<":
            current_mask = pd.to_numeric(col_data, errors='coerce') < pd.to_numeric(val, errors='coerce')
        elif flt == "!=":
            current_mask = col_data != val
        else:
            col_sorted = col_data.sort_values()
            left, right = 0, len(col_sorted) - 1
            found_indices = []

            while left <= right:
                mid = (left + right) // 2
                mid_val = col_sorted.iloc[mid]
                try:
                    cmp_val = type(mid_val)(val)
                except:
                    cmp_val = val

                if mid_val == cmp_val:
                    l, r = mid, mid + 1
                    while l >= 0 and col_sorted.iloc[l] == cmp_val:
                        found_indices.append(col_sorted.index[l])
                        l -= 1
                    while r < len(col_sorted) and col_sorted.iloc[r] == cmp_val:
                        found_indices.append(col_sorted.index[r])
                        r += 1
                    break
                elif mid_val < cmp_val:
                    left = mid + 1
                else:
                    right = mid - 1

            current_mask = pd.Series(False, index=df.index)
            if found_indices:
                current_mask.loc[found_indices] = True

        if i == 0:
            mask = current_mask
        else:
            op = operations[i - 1].upper() if i - 1 < len(operations) else "AND"
            if op == "AND":
                mask = mask & current_mask
            elif op == "OR":
                mask = mask | current_mask
            elif op == "NOT":
                mask = mask & (~current_mask)

    return df[mask].reset_index(drop=True)
