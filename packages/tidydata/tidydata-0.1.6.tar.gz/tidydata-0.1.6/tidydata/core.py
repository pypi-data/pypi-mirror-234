# 导入数据集
import pandas as pd
import numpy as np
import duckdb
from pathlib import Path
from typeguard import typechecked
from typing import List, Optional, Union, Dict, Tuple, Literal, Any
from collections import defaultdict
from tidydata.config import Config
import logging
from rich import print
import re
from tidydata.variable import (
    ciloc, clast_notna, cfirst_notna, reval
)


logging.basicConfig(level=logging.INFO)

Number = Union[int, float]
Scalar = Union[str, int, float, bool]
ScalarNA = Union[str, int, float, bool, pd.NA, np.nan, None, pd.NaT] 



PANDAS_TO_NUMPY = {
    pd.BooleanDtype(): np.bool_,
    pd.Int8Dtype(): np.int8,
    pd.Int16Dtype(): np.int16,
    pd.Int32Dtype(): np.int32,
    pd.Int64Dtype(): np.int64,
    pd.UInt8Dtype(): np.uint8,
    pd.UInt16Dtype(): np.uint16,
    pd.UInt32Dtype(): np.uint32,
    pd.UInt64Dtype(): np.uint64,
    pd.Float32Dtype(): np.float32,
    pd.Float64Dtype(): np.float64,
    pd.StringDtype(): np.str_
}

STATA_VERSION = {
    'Stata10': 114,
    'Stata13': 117,
    'Stata14': 118,
    'Stata14Max': 119
}






@typechecked
class Table:
    """Table类"""
  
    def __init__(self, name: str, df: pd.DataFrame):
        self.df = df
        self.name = name
        self._check_mixed_dtypes()


    def _check_mixed_dtypes(self):
        """检查并警告混合数据类型"""
        mixed_type_cols = []
        mixed_integer_float_cols = []
        mixed_integer_cols = []
        unknown_array_cols = []

        for col in self.df.columns:
            inferred_dtype = pd.api.types.infer_dtype(self.df[col])
            if inferred_dtype == 'mixed':
                mixed_type_cols.append(col)
            elif inferred_dtype == 'mixed-integer-float':
                mixed_integer_float_cols.append(col)
            elif inferred_dtype == 'mixed-integer':
                mixed_integer_cols.append(col)
            elif inferred_dtype == 'unknown-array':
                unknown_array_cols.append(col)

        if len(mixed_type_cols) > 0:
            logging.warning(f"The dataframe contains columns of type 'mixed': {mixed_type_cols}. "
                            "It is recommended to use the 'replace_values' method to replace non-null values with a consistent type.")
        if len(mixed_integer_float_cols) > 0:
            logging.warning(f"The dataframe contains columns of type 'mixed-integer-float': {mixed_integer_float_cols}. "
                            "It is recommended to use the 'replace_values' method to replace non-null values with a consistent type.")
        if len(mixed_integer_cols) > 0:
            logging.warning(f"The dataframe contains columns of type 'mixed-integer': {mixed_integer_cols}. "
                            "It is recommended to use the 'replace_values' method to replace non-null values with a consistent type.")
        if len(unknown_array_cols) > 0:
            logging.warning(f"The dataframe contains columns of type 'unknown-array': {unknown_array_cols}. "
                            "It is recommended to use the 'replace_values' method to replace non-null values with a consistent type.")
            
    @classmethod
    def from_stata(cls, name: str, file: Path | str, usecols: Optional[List[str]] = None, convert_categoricals: bool = False, fast_load_path: Optional[str | Path] = None):
        tbname = Path(file).stem
        if fast_load_path:
            fast_load_path = str(fast_load_path)
            with duckdb.connect(fast_load_path) as conn: 
                try:
                    columns = ", ".join(usecols) if usecols else "*"
                    df = conn.execute(f"SELECT {columns} FROM {tbname};").df()
                except Exception as e:
                    logging.warning(f"正在导入文件到DuckDB'{fast_load_path}'为表{tbname}")
                    df = pd.read_stata(file, convert_categoricals=convert_categoricals)
                    conn.execute(f"CREATE TABLE {tbname} AS SELECT * FROM df")

                    df = conn.execute(f"SELECT {columns} FROM {tbname};").df()
        else:
            df = pd.read_stata(file, columns=usecols, convert_categoricals=convert_categoricals)
            
        return cls(name, df.convert_dtypes())



    @classmethod
    def from_duckdb(cls, name: str, connect: Path | str, sql_statement: str):
    
        with duckdb.connect(str(connect)) as conn:
            return cls(name, conn.sql(sql_statement).df().convert_dtypes())



    @classmethod
    def from_csv(cls, name: str, file: Path | str, usecols: Optional[List[str]] = None, fast_load_path: Optional[str| Path] = None):
        
        tbname = Path(file).stem
        if fast_load_path:
            fast_load_path = str(fast_load_path)
            with duckdb.connect(fast_load_path) as conn:
                try:
                    columns = ", ".join(usecols) if usecols else "*"
                    df = conn.execute(f"SELECT {columns} FROM {tbname};").df()
                except Exception as e:
                    logging.info(f"正在导入文件到DuckDB'{fast_load_path}'为表{tbname}")
                    conn.execute("INSTALL httpfs;")
                    conn.execute(f"CREATE TABLE {tbname} AS SELECT * FROM read_csv_auto('{file}');")
                    df = conn.execute(f"SELECT {columns} FROM {tbname};").df()
        else:
            df = pd.read_csv(file, usecols=usecols, sep=',')
        return cls(name, df.convert_dtypes())


    @classmethod
    def from_tsv(cls, name: str, file: Path | str, usecols: Optional[List[str]] = None, fast_load_path: Optional[str|Path] = None):
        
        tbname = Path(file).stem
        if fast_load_path:
            fast_load_path = str(fast_load_path)
            with duckdb.connect(fast_load_path) as conn:
                try:
                    columns = ", ".join(usecols) if usecols else "*"
                    df = conn.execute(f"SELECT {columns} FROM {tbname};").df()
                except Exception as e:
                    logging.info(f"正在导入文件到DuckDB'{fast_load_path}'为表{tbname}")
                    conn.execute("INSTALL httpfs;")
                    conn.execute(f"CREATE TABLE {tbname} AS SELECT * FROM read_csv_auto('{str(file)}')")
                    df = conn.execute(f"SELECT {columns} FROM {tbname};").df()
        else:
            df = pd.read_csv(file, usecols=usecols, sep='\t')
        return cls(name, df.convert_dtypes())

    @classmethod
    def from_excel(cls, name: str, file: Path | str, usecols: Optional[List[str]] = None,  sheet_name: str = 'Sheet1', fast_load_path: Optional[str|Path] = None):
        tbname = Path(file).stem
        if fast_load_path:
            fast_load_path = str(fast_load_path)
            with duckdb.connect(fast_load_path) as conn:
                table_exists = conn.execute(f"SELECT name FROM tables WHERE name='{tbname}';").fetchone() is not None
                
                if not table_exists:
                    df = pd.read_excel(file, sheet_name=sheet_name)
                    conn.execute(f"CREATE TABLE {tbname} AS", df)

                columns = ", ".join(usecols) if usecols is not None else "*"
                df = conn.execute(f"SELECT {columns} FROM {tbname};").fetch_df()
        else:
            df = pd.read_excel(file, usecols=usecols, sheet_name=sheet_name)

        return cls(name, df.convert_dtypes())


    @classmethod
    def from_parquet(cls, name: str, file: Path | str, usecols: Optional[List[str]] = None, fast_load_path: Optional[str | Path] = None):
        tbname = Path(file).stem
        
        if fast_load_path:
            fast_load_path = str(fast_load_path)
            with duckdb.connect(fast_load_path) as conn:
                try:
                    columns = ", ".join(usecols) if usecols else "*"
                    df = conn.execute(f"SELECT {columns} FROM {tbname};").df()
                except Exception as e:
                    logging.info(f"正在导入文件到DuckDB'{fast_load_path}'为表{tbname}")
                    conn.execute("INSTALL httpfs;")
                    
                    conn.execute(f"CREATE TABLE {tbname} AS SELECT * FROM read_parquet('{str(file)}')")
                    df = conn.execute(f"SELECT {columns} FROM {tbname};").df()
        else:
            df = pd.read_parquet(file, columns=usecols, engine='pyarrow')

        return cls(name, df.convert_dtypes())



    def select_columns(self, cols: List[str]):
        filtered_df = self.df.filter(items=cols)
        return self.__class__(self.name, filtered_df)

    def select_rows(self, exprs: List[str]):
        exprs = [f'{expr.replace(" is not NA", " == " + expr.split()[0])}' for expr in exprs]
        query_expr = " & ".join(exprs)
        queried_df = self.df.query(query_expr)
        return self.__class__(self.name, queried_df)


    def downcast_pandas_dtypes(self, nocats: Optional[List[str]]=None):
        df = self.df.convert_dtypes()

        if nocats is None:
            nocats = []

        number_mapping = {
            'int': {
                'Int8': (np.iinfo(np.int8).min, np.iinfo(np.int8).max),
                'Int16': (np.iinfo(np.int16).min, np.iinfo(np.int16).max),
                'Int32': (np.iinfo(np.int32).min, np.iinfo(np.int32).max),
            },
            'uint': {
                'UInt8': (0, np.iinfo(np.uint8).max),
                'UInt16': (0, np.iinfo(np.uint16).max),
                'UInt32': (0, np.iinfo(np.uint32).max),
            },
        }

        dtype_mapping = defaultdict(dict)

        for col in df.columns:
            if pd.api.types.is_integer_dtype(df[col]):
                min_val, max_val = df[col].dropna().min(), df[col].dropna().max()
                dtype_class = 'int' if pd.api.types.is_signed_integer_dtype(df[col]) else 'uint'
                for dtype_type, (min_int, max_int) in number_mapping[dtype_class].items():
                    if min_val >= min_int and max_val <= max_int:
                        dtype_mapping[col] = dtype_type
                        break

            elif pd.api.types.is_float_dtype(df[col]):
                min_val, max_val = df[col].dropna().min(), df[col].dropna().max()
                if min_val >= np.finfo(np.float32).min and max_val <= np.finfo(np.float32).max:
                    dtype_mapping[col] = 'Float32'

            elif pd.api.types.is_string_dtype(df[col]) and col not in nocats:
                dtype_mapping[col] = 'category'

        if dtype_mapping:
            df = df.astype(dict(dtype_mapping))

        return self.__class__(self.name, df)



    def _check_float_to_int(self, dtype_mapper):

        df = self.df.convert_dtypes()
        for col, target_dtype in dtype_mapper.items():
            if pd.api.types.is_float_dtype(df[col]) and ('int' in target_dtype or 'uint' in target_dtype):
                logging.warning(f"Converting from float to integer for column '{col}' may cause data loss. "
                                "Please check your dtype_mapper and confirm.")
        return self.__class__(self.name, df)


    def convert_dtypes(self, dtype_mapper: Dict[str, str], downcast: bool=False, nocats: Optional[List[str]]=None):

        if not nocats:
            nocats = [key for key, value in dtype_mapper.items() if value == 'string']
    
        df = (self._check_float_to_int(dtype_mapper)
            .df.convert_dtypes()
            .astype(dtype_mapper))

        return self.__class__(self.name, df)

    def specify_valid_values(self, valid_values: Dict[str, List[Union[Scalar, Tuple[Number, Number]]]]):

        df = self.df.copy()

        for col, values in valid_values.items():
            if col in df.columns:
                scalar_values = [value for value in values if not isinstance(value, tuple)]
                tuple_values = [value for value in values if isinstance(value, tuple)]

                # Using mask for scalar_values
                if scalar_values:
                    df[col] = df[col].mask(~df[col].isin(scalar_values))

                # Using where for tuple_values
                for value_range in tuple_values:
                    min_val, max_val = value_range
                    df[col] = df[col].where(df[col].between(min_val, max_val).fillna(False), other=pd.NA)

        return self.__class__(self.name, df)



    def replace_values(self, value_mapper: Dict[str, Dict[ScalarNA | Tuple[ScalarNA], ScalarNA]] | Dict[ScalarNA | Tuple[ScalarNA], ScalarNA]):
        
        if not all(isinstance(val, dict) for val in value_mapper.values()):
            value_mapper = {col: value_mapper for col in self.df.columns}

        replace_dict = {}
        for col, mapper in value_mapper.items():
            replace_dict[col] = {k: v for key, v in mapper.items() for k in (key if isinstance(key, tuple) else [key])}

        replaced_df = self.df.replace(replace_dict)

        return self.__class__(self.name, replaced_df)

    def rename_columns(self, column_mapper: Dict[str, str]):
        renamed_df = self.df.rename(columns=column_mapper)
        return self.__class__(self.name, renamed_df)

    def add_columns(self, column_exprs: List[Dict[str, callable]]):
        new_df = self.df.copy().convert_dtypes() 
        for expr in column_exprs:
            new_df = new_df.assign(**expr).convert_dtypes()

        return self.__class__(self.name, new_df)

    def apply_functions(self, functions: List[Dict[str, Any]]) -> 'Table':
        
        df = self.df.copy()
        
        for func_dict in functions:
            df = df.pipe(func_dict['func'], **func_dict['kwargs'])

        return Table(self.name, df)
        

    def melt_columns(self, i: List[str], j: Dict[str, List[str]], prename_mapper: Optional[Dict[str, str]]=None, sep: str = '-'):
        df = self.df.copy()

        if prename_mapper:
            df.rename(columns=prename_mapper, inplace=True)

        for j_val, stubnames in j.items():
            df = pd.wide_to_long(df, stubnames, i=i, j=j_val, sep=sep, suffix=r'\d+').reset_index()
            
            df.loc[df[stubnames].isna().all(axis=1), j_val] = pd.NA
            df.drop_duplicates(subset=i+[j_val], inplace=True)
            
            subset_columns = df.columns.difference(i + [j_val])
            df.dropna(subset=subset_columns, how='all', inplace=True)
            
            df[j_val] = df[j_val].astype('Int64')
        return self.__class__(self.name, df)


    def _to_numpy_dtypes(self):
        """转换 pandas 扩展类型到相应的 numpy 类型"""
        df = self.df.copy()

        # 对于每一列
        for col, dtype in df.dtypes.items():
            # 如果列中有缺失值，则转为 'object'
            if df[col].isnull().any():
                df[col] = df[col].astype('object').fillna(np.nan)
            # 否则按照 PANDAS_TO_NUMPY 映射进行转换
            elif dtype in PANDAS_TO_NUMPY:
                df[col] = df[col].astype(PANDAS_TO_NUMPY[dtype])

        # 返回新的 TidyData 对象
        return self.__class__(self.name, df)

    def to_stata(self, 
                to_path: Path | str, 
                file_label: Optional[str]=None, 
                columns: Optional[List[str]]=None, 
                column_labels: Optional[Dict[str, str]]=None, 
                value_labels: Optional[Dict[str, Dict[int, str]]]=None,
                version: Literal['Stata10','Stata13','Stata14', 'Stata14Max'] = 'Stata14'):
        
        export_df = (self.select_columns(columns) if columns else self)._to_numpy_dtypes().df
        
        export_df.to_stata(to_path, write_index=False, version=STATA_VERSION[version], 
                        data_label=file_label, variable_labels=column_labels, value_labels=value_labels)
        
    def to_parquet(self, to_path: Path | str, columns: Optional[List[str]]= None, compression: bool = True):
        
        export_df = (self.select_columns(columns) if columns else self).df

        # 导出数据
        export_df.to_parquet(
            to_path,
            engine='pyarrow',
            compression='gzip' if compression else None
        )
        
    def to_duckdb(self, to_path: str | Path, if_exists: str = 'fail'):
        con = duckdb.connect(str(to_path))

        # Register the DataFrame with DuckDB
        con.register('df', self.df.sort_index(axis=1))

        # 检查表是否存在
        query = f"""
        SELECT count(*) 
        FROM information_schema.tables 
        WHERE table_name = '{self.name}'
        """
        table_exists = con.execute(query).fetchone()[0] > 0

        # 根据 if_exists 选项执行相应的操作
        if table_exists:
            if if_exists == 'fail':
                raise ValueError(f"Table '{self.name}' already exists.")
            elif if_exists == 'replace':
                con.execute(f"DROP TABLE {self.name}")
            elif if_exists == 'append':
                pass
            else:
                raise ValueError(f"Invalid value for 'if_exists': {if_exists}")
        
        # 将 DataFrame 导入到 DuckDB 数据库
        con.execute(f"CREATE TABLE {self.name} AS SELECT * FROM df")

        # 关闭数据库连接
        con.close()



@typechecked
class TidySource:
    """TidySource类"""
    
    def __init__(self, config: Config) -> None:
        self.sources  = config.sources
        self.fast_load_db = config.database.fast_load
        self.source_db = config.database.source
        
        if not self.sources:
            logging.error('There is no entity in sources')
        
        self.load()
        
        logging.info(f"完成数据预处理.")
    def load(self):
        for ds in self.sources:
            match ds.reader_type:
                case 'stata':
                    self.load_and_process_data(Table.from_stata, ds)
                case 'csv':
                    self.load_and_process_data(Table.from_csv, ds)
                case 'tsv':
                    self.load_and_process_data(Table.from_tsv, ds)
                case 'excel':
                    self.load_and_process_data(Table.from_excel, ds)
                case 'parquet':
                    self.load_and_process_data(Table.from_parquet, ds)

    def load_and_process_data(self, reader, ds):
        
        logging.info(f"正在导入并预处理数据集{ds.id}...")
        table = reader(ds.id, ds.location, usecols= ds.pre_column_names, fast_load_path=self.fast_load_db)

        if ds.pre_column_new_values:
            logging.info(f"正在值替换...")
            table = table.replace_values(value_mapper= ds.pre_column_new_values)
        
        if ds.pre_column_valid_values:
            logging.info(f"正在设置有效值...")
            table = table.specify_valid_values(valid_values= ds.pre_column_valid_values)
        
        if ds.pre_column_dtypes:
            logging.info(f"正在转换用户指定的列数据类型...")
            table = table.convert_dtypes(dtype_mapper=ds.pre_column_dtypes)
        
        if ds.id_names and ds.group_names and ds.widename_mapper:
            logging.info(f"正在宽格式转长格式...")
            table = table.melt_columns(i=ds.id_names, j=ds.group_names, prename_mapper=ds.widename_mapper)
        
        if ds.post_column_aliases:
            logging.info(f"正在重命名长格式列名...")
            table = table.rename_columns(column_mapper=ds.post_column_aliases)


        if ds.new_column_exprs:
            logging.info(f"正在创建新列...")
            table = table.add_columns(column_exprs=ds.new_column_exprs)
            if ds.new_column_dtypes:
                table = table.convert_dtypes(dtype_mapper=ds.new_column_dtypes)
                
        if ds.rows:
            logging.info(f"正在选取符合要求的行...")
            table = table.select_rows(exprs=ds.rows)
                
        logging.info(f"正在导出到'{self.source_db}'...")
        table.to_duckdb(to_path=self.source_db, if_exists='replace')
        
        logging.info(f"已完成预处理数据集{ds.id}.")
        return table
    

@typechecked
class TidyExport:
    """TidyExport类"""

    def __init__(self, config: Config, export_dir: Optional[str] = None) -> None:
        self.exports = config.exports
        self.db = str(config.database.source)
        self.export_dir = export_dir if export_dir is not None else str(config.database.export)

        if not self.exports:
            logging.error('There is no entity in exports')
                
        logging.info(f"运行导出模块...")
        self.export()

        if Path(self.db).exists():
            Path(self.db).unlink()
        logging.info(f"删除临时数据库...") 
        logging.info(f"完成数据导出.")
        
    def export(self):
        for ds in self.exports:
            for fa in ds.from_actions:

                from_edit = fa['edit_action']
            
                logging.info(f"正在创建Table对象'from_table'...")
                from_table = Table.from_duckdb(name = fa['fid'], connect=self.db, sql_statement=fa['query_action'])
                if from_edit:
                    logging.info(f"正在为Table对象'from_table'应用编辑函数")
                    from_table = from_table.apply_functions(functions=from_edit)
                    
                logging.info(f"完成编辑并以表名{fa['fid']}导入到数据库{self.db}(如果存在则替换!)")
                from_table.to_duckdb(to_path=self.db,if_exists='replace')
                logging.info(f"已完成表{fa['fid']}创建到数据库{self.db}")

            to_file = ds.to_actions['to_file']
            to_edit = ds.to_actions['edit_action']
            
            logging.info(f"正在创建Table对象'to_table'...")
            to_table = Table.from_duckdb(name=ds.to_actions['tid'],connect=self.db, sql_statement=ds.to_actions['query_action'])
            if to_edit:
                logging.info(f"正在为Table对象'to_table'应用编辑函数")
                to_table = to_table.apply_functions(functions=to_edit)
            
            logging.info(f"完成编辑并以表名{ds.to_actions['tid']}导入到数据库{self.db}(如果存在则替换!)")    
            to_table.to_duckdb(to_path=self.db,if_exists='replace')
            logging.info(f"已完成表{ds.to_actions['tid']}创建到数据库{self.db}")
            if to_file:
                logging.info(f"正在导出表{ds.to_actions['tid']}为文件{self.export_dir+'/'+to_file['filename']}")
                match to_file['filetype']:
                    case 'stata':
                        to_table.to_stata(to_path=self.export_dir+'/'+to_file['filename'])
                        logging.info(f"完成导出表{ds.to_actions['tid']}为文件{self.export_dir+'/'+to_file['filename']}")
                    case 'parquet':
                        to_table.to_parquet(to_path=self.export_dir+'/'+to_file['filename'])
                        logging.info(f"完成导出表{ds.to_actions['tid']}为文件{self.export_dir+'/'+to_file['filename']}")



           

        
        
        
        
        
        
        


            
