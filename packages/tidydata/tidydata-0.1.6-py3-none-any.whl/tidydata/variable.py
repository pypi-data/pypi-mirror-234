import pandas as pd
import numpy as np
import re
from typing import List,Literal,Optional,Callable, Dict,Tuple
from pandas.api.types import is_numeric_dtype, is_string_dtype, pandas_dtype, is_categorical_dtype
import functools

def datecount(data: Tuple[pd.Series, pd.Series], refs: Optional[Tuple[pd.Series, pd.Series]]=None, 
              unit: Literal['year','quarter','month','week','day']='day', ignore_interval_error: bool=True)->pd.Series:
    data_start, data_end = data
    ref_start, ref_end = refs if refs else data

    df = pd.DataFrame({
        'data_start': data_start,
        'data_end': data_end,
        'ref_start': ref_start,
        'ref_end': ref_end
    }).astype('datetime64[ns]')

    interval_errors = (df['data_start'] > df['data_end']) | (df['ref_start'] > df['ref_end'])
    
    if interval_errors.any():
        if ignore_interval_error:
            df[interval_errors] = pd.NaT
        else:
            raise ValueError("Start time cannot be after end time.")

    df['overlap_start'] = df[['data_start', 'ref_start']].max(axis=1,skipna=False)
    df['overlap_end'] = df[['data_end', 'ref_end']].min(axis=1,skipna=False)
    
    df.loc[df['overlap_end'] < df['overlap_start'], 'overlap_end'] = df['overlap_start']



    if unit == 'year':
        result = df['overlap_end'].dt.year - df['overlap_start'].dt.year
    elif unit == 'quarter':
        result = (df['overlap_end'].dt.year - df['overlap_start'].dt.year) * 4 + df['overlap_end'].dt.quarter - df['overlap_start'].dt.quarter
    elif unit == 'month':
        result = (df['overlap_end'].dt.year - df['overlap_start'].dt.year) * 12 + df['overlap_end'].dt.month - df['overlap_start'].dt.month
    elif unit == 'week':
        result = (df['overlap_end'] - df['overlap_start']).dt.days // 7
    else:  # day
        result = (df['overlap_end'] - df['overlap_start']).dt.days

    return result



def to_date(year, month, day=None):

    day = day if day is not None else pd.Series([1]*len(year))
    
    mask_missing = (year.isnull()) | (month.isnull()) | (day.isnull())
    
    date_series = pd.Series(pd.NaT, index=year.index)
    
    date_series[~mask_missing] = pd.to_datetime(pd.DataFrame({'year': year[~mask_missing], 
                                                              'month': month[~mask_missing], 
                                                              'day': day[~mask_missing]}))
    return date_series

def back1year(date_series):
    return date_series - pd.DateOffset(years=1)






def namax(series_list):
    df = pd.concat(series_list, axis=1).convert_dtypes()
    return df.max(axis=1, skipna=True)

def namin(series_list):
    df = pd.concat(series_list, axis=1).convert_dtypes()
    return df.min(axis=1, skipna=True)

def namean(series_list):
    df = pd.concat(series_list, axis=1).convert_dtypes()
    return df.mean(axis=1, skipna=True)

def nasum(data: List[pd.Series]):

    use_df = pd.concat(data, axis=1)
    sum_series = use_df.sum(axis=1)
    sum_series[(sum_series == 0) & use_df.isnull().all(axis=1)] = pd.NA

    return sum_series

def leftsum(series_list):
    df = pd.concat(series_list, axis=1)

    result = df.sum(axis=1)

    result[df.iloc[:, 0].isnull()] = pd.NA

    return result

def naprod(series_list):
    df = pd.concat(series_list, axis=1).convert_dtypes()
    print(df)
    return df.product(axis=1, skipna=False)

def where(condition, x, y):
    if pd.isna(condition).any():  # check if there are any missing values
        return np.where(condition.fillna(False), x, y)
    else:
        return np.where(condition, x, y)
    

def replace(series, mapping_dict):

    if "NA" in mapping_dict:
        series = series.fillna(mapping_dict["NA"])

    mapping_dict.pop("NA", None)

    cross_type_replace = False
    same_type_replace_dict = {}
    cross_type_replace_dict = {}

    for k, v in mapping_dict.items():
        if isinstance(k, tuple):
            if any(type(elem) != type(v) for elem in k):
                cross_type_replace = True
                cross_type_replace_dict[k] = v
            else:
                same_type_replace_dict[k] = v
        else:
            if type(k) != type(v):
                cross_type_replace = True
                cross_type_replace_dict[k] = v
            else:
                same_type_replace_dict[k] = v

    if cross_type_replace:
        series = series.astype('object')
        series = series.replace(cross_type_replace_dict)

    series = series.replace(same_type_replace_dict)
    
    return series


def fill(target_s, source_s):
    """
    使用 source_s 来填充 target_s 中的缺失值。

    参数:
        target_s (pd.Series): 需要填充缺失值的 Series
        source_s (pd.Series): 用来填充缺失值的 Series

    返回:
        pd.Series: 更新后的 Series
    """
    return target_s.fillna(source_s)


def nalog(arr):
    # 将pd.NA转换为np.nan
    arr = arr.replace({pd.NA: np.nan})


    # 尝试计算对数
    try:
        result = arr.apply(np.log)
    except ValueError as err:
        # 打印错误信息和无效的输入值
        print(f"Error: {err}")

    return result
    


    


    
# transform函数
def transformer(func: Callable):
    @functools.wraps(func)
    def wrapper(df: pd.DataFrame, *args, **kwargs) -> pd.DataFrame:
        groupby = kwargs.pop('groupby', None)
        ascendby = kwargs.pop('ascendby', None)
        gascendby = kwargs.pop('gascendby', None)
        to_nullable_dtypes = kwargs.pop('to_nullable_dtypes', False)
        columns = kwargs.pop('columns',df.columns.values)
        

        if groupby and ascendby and groupby == ascendby:
            raise ValueError("groupby and ascendby cannot have the same value")

        df = df.copy()

        if gascendby:
            df.sort_values(by=gascendby, kind='mergesort', inplace=True) # 有些数据类型如混合类型无法排序
            
        if groupby:
            if ascendby:
                df.sort_values(by=ascendby, kind='mergesort', inplace=True) # 有些数据类型如混合类型无法排序
            df[columns] = df.groupby(groupby)[columns].transform(lambda x: func(x, *args, **kwargs))
        else:
            df[columns] = df[columns].transform(lambda x: func(x, *args, **kwargs))

        if to_nullable_dtypes:
            df[columns] = df[columns].convert_dtypes()
        return df
    return wrapper


## 以下除装饰器函数外，均为df.transform可以使用的关于pd.Series的函数

def boardcast_to_series(include_dtypes: Literal['number','all','string','category'], to_numpy_nan: bool = False):
    def decorator(func: Callable):
        @functools.wraps(func)  
        def wrapper(s: pd.Series, *args, **kwargs):
            dtype_map = {
                'number': is_numeric_dtype,
                'string': is_string_dtype,
                'category': is_categorical_dtype,
                'all': pandas_dtype
            }
            
            if dtype_map[include_dtypes](s.dtype):
                if to_numpy_nan:
                    s = s.fillna(np.nan)
                return pd.Series(np.repeat(func(s, *args, **kwargs), len(s)), index=s.index)
            else:
                return s
        return wrapper
    return decorator


# 非缺失数值统计
@transformer
@boardcast_to_series(include_dtypes='number', to_numpy_nan= True)
def cmean(s: pd.Series):
    return s.mean()

@transformer
@boardcast_to_series(include_dtypes='number', to_numpy_nan= True)
def cmin(s: pd.Series):
    return s.min()

@transformer
@boardcast_to_series(include_dtypes='number', to_numpy_nan= True)
def cmax(s: pd.Series):
    return s.max()


@transformer
@boardcast_to_series(include_dtypes='number', to_numpy_nan= True)
def cstd(s: pd.Series):
    return s.std()

@transformer
@boardcast_to_series(include_dtypes='number', to_numpy_nan= True)
def csum(s: pd.Series):
    return s.sum()

@transformer
@boardcast_to_series(include_dtypes='number', to_numpy_nan= True)
def cmedian(s: pd.Series):
    return s.median()

@transformer
@boardcast_to_series(include_dtypes='number', to_numpy_nan= True)
def cvar(s: pd.Series):
    return s.var()

# 独特非缺失值统计
@transformer
@boardcast_to_series(include_dtypes='all')
def cnunique(s: pd.Series):
    return s.nunique()

# 缺失值统计
@transformer
@boardcast_to_series(include_dtypes='all')
def cfirst_notna(s: pd.Series):
    index = s.first_valid_index()
    return s.loc[index] if index else np.nan

@transformer
@boardcast_to_series(include_dtypes='all')
def clast_notna(s: pd.Series):
    index = s.last_valid_index()
    return s.loc[index] if index else np.nan

@transformer
@boardcast_to_series(include_dtypes='all')
def ccount_notna(s: pd.Series):
    return s.count()

@transformer
@boardcast_to_series(include_dtypes='all')
def ccount_all(s: pd.Series):
    return s.size

@transformer
@boardcast_to_series(include_dtypes='all')
def ccount_na(s: pd.Series):
    return s.size-s.count()

@transformer
@boardcast_to_series(include_dtypes='all')
def ccount_na_pct(s: pd.Series):
    return (s.size-s.count())/s.size

@transformer
@boardcast_to_series(include_dtypes='all')
def ciloc(s: pd.Series, index: int):
    return s.iloc[index]

@transformer
def cffillna(s:pd.Series):
    return s.ffill()

@transformer
def cbfillna(s:pd.Series):
    return s.bfill()

# 以下除装饰器函数外，均为对df应该transform操作的函数， df->df
## 装饰器
def reval(df: pd.DataFrame, exprs: List[str]):
    
    expr = '\n'.join(exprs)
    return df.eval(expr)



def rassign(df: pd.DataFrame, exprs: Dict[str, str]):
    lambda_exprs = {k: eval('lambda x: ' + v) for k, v in exprs.items()}
    return df.assign(**lambda_exprs)

    
