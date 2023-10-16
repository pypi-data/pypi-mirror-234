from pydantic import BaseModel, FilePath, HttpUrl, validator, Field
from dataclasses import dataclass
from typing import List, Dict, Optional, Literal, Union, Any
from collections import Counter
import yaml
import sqlparse
from collections import defaultdict, Counter
from typeguard import typechecked
from itertools import chain
from pathlib import Path
import pandas as pd
import numpy as np
from tidydata.variable import (
    nasum,
    namin,
    namax,
    naprod,
    namean,
    nalog, 
    where, 
    replace, 
    fill,
    ciloc, 
    clast_notna, 
    cfirst_notna,
    cbfillna,
    cffillna,
    reval,
    rassign,
    to_date,
    back1year,
    datecount,
    leftsum)

FUNCTION_MAP = {
    "clast_notna": clast_notna,
    "reval": reval,
    "rassign": rassign,
    "cbfillna": cbfillna
}

global_counter = 0

@typechecked
def _uid(prefix:str = '_uid'):
    global global_counter
    global_counter += 1
    return prefix + str(global_counter)



PandasType = Literal['int', 'float', 'bool', 'str', 'cat', 'date']
ValidValue = Union[int, float, bool, str]



Ext2IOtype = {
            '.csv': 'csv',
            '.tsv': 'tsv',
            '.dta': 'stata',
            '.xls': 'excel',
            '.xlsx': 'excel',
            '.parquet': 'parquet'
}
        

      
PANDAS_DTYPES = {
  'int': 'Int64',
  'uint': 'UInt64',
  'str': 'string',
  'bool': 'boolean',
  'float': 'Float64',
  'cat': 'category',
  'date': 'datetime64[ns]'
}


    

class ColumnBase(BaseModel):
    name: str                           # 选取需要处理的列名
    label: str              # 导出stata时导出为变量标签
    dtype: PandasType       # 转换列的数据类型

class Column(ColumnBase):
    alias: Optional[str]               # 重命名列
    valid_values: Optional[List[List[ValidValue]] | List[ValidValue]]   # 有效值范围
    new_values: Optional[Dict[Any, Any]] # 有效值修改
    value_labels: Optional[Dict[int, str]] # 当列数据类型为整数时， 导出为stata时为值标签
    obs: Optional[int | str]
    expr: Optional[str]

    @validator('dtype')
    def check_and_transform_dtype(cls, v):
        if v is not None:
            if v not in PANDAS_DTYPES:
                raise ValueError(f"dtype '{v}' is not valid. It must be one of {list(PANDAS_DTYPES.keys())}.")
            return PANDAS_DTYPES[v]
        return v

    @validator('valid_values')
    def check_and_transform_valid_values(cls, v):
        if isinstance(v, list):
            if all(isinstance(sub_v, list) for sub_v in v):
                return [tuple(sub_v) if len(sub_v) == 2 and all(isinstance(i, (int, float)) for i in sub_v) else sub_v for sub_v in v]
        return v



    @validator('new_values')
    def check_and_transform_new_values(cls, v):
        if v is not None:
            return {
                (key if key != 'NA' else (None, pd.NA, np.nan)): (value if value != 'NA' else pd.NA)
                for key, value in v.items()
            }
        return v

    
    @validator('value_labels')
    def check_value_labels(cls, v, values):
        if values['dtype'] != PANDAS_DTYPES['int'] and v is not None:
            raise ValueError(f"value_labels in column '{values['name']}' must be None when dtype is not 'int'")
        return v
    

    @validator('expr')
    def transform_expr_to_lambda(cls, v):
        if v is not None:
            return  eval('lambda x: ' + v)
        return v

class ColumnGroup(BaseModel):
    gname: str
    members: List[Column]
    glabel: Optional[str]
    galias: Optional[str]
    gdtype: Optional[PandasType]
    gvlabel: Optional[Dict[int, str]]
    obsname: Optional[str]




    @validator('gdtype')
    def check_and_transform_gdtype(cls, v):
        if v is not None:
            if v not in PANDAS_DTYPES:
                raise ValueError(f"gdtype '{v}' is not valid. It must be one of {list(PANDAS_DTYPES.keys())}.")
            return PANDAS_DTYPES[v]
        return v

    @validator('gvlabel')
    def check_group_value_labels(cls, v, values):
        if values['gdtype'] != PANDAS_DTYPES['int'] and v is not None:
            raise ValueError(f"value_labels in column group '{values['gname']}' must be None when its dtype is not 'int'")
        return v
    
    @validator('members')
    def check_obs_unique(cls, v, values):
        obs_values = {member.obs for member in v}
        if len(obs_values) != len(v):
            raise ValueError(f"obs values in members of group {values['gname']} must be unique.")
        return v
    
class Dataset(BaseModel):
    id: str
    description: Optional[str]
    location: FilePath | HttpUrl
    rows: Optional[List[str]]
    newcols: Optional[List[Column]]
    idcols: List[Column]
    longcols: Optional[List[Column]]
    widecols: Optional[List[ColumnGroup]]

    @validator('location')
    def stringify_location(cls, v):
        return str(v)
    
    @property
    def reader_type(self) -> str:
        """创建文件读取类型的只读属性"""
        ext = Path(self.location).suffix
        return Ext2IOtype[ext]
        
    @property
    def id_names(self):
        """数据集的ID列名，用于检查数据集ID是否唯一, 宽转长和横向合并"""
        return [col.name for col in self.idcols]

    @property
    def group_names(self):
        if self.widecols:
            group_names = defaultdict(list)

            for colgroup in self.widecols:
                group_names[colgroup.obsname].append(colgroup.gname)
                
            return dict(group_names)

    @property
    def widename_mapper(self):
        if self.widecols:
            return {
                member.name: f"{colgroup.gname}-{member.obs}"
                for colgroup in self.widecols 
                for member in colgroup.members 
                if member.name != f"{colgroup.gname}-{member.obs}"
            }

    @property
    def _pre_columns(self):
        return chain(
            self.idcols, 
            self.longcols or [], 
            *(g.members for g in self.widecols or [])
        )

    @property
    def pre_column_names(self):
        return [col.name for col in self._pre_columns]

    @property
    def pre_column_dtypes(self):
        # 使用 all_columns 属性
        column_dtypes = {col.name: col.dtype for col in self._pre_columns if col.dtype}

        return column_dtypes if column_dtypes else None
    
    @property
    def _post_columns(self):
        return chain(
            self.idcols, 
            self.longcols or [], 
            self.widecols or []
        )
        
    @property
    def post_column_aliases(self):
        column_aliases = defaultdict(str)

        for col in self._post_columns:
            if isinstance(col, Column) and col.alias and col.alias != col.name:
                column_aliases[col.name] = col.alias
            elif isinstance(col, ColumnGroup) and col.galias and col.galias != col.gname:
                column_aliases[col.gname] = col.galias

        return dict(column_aliases) if column_aliases else None

    @property
    def post_column_value_labels(self):
        column_value_labels = defaultdict(str)

        for col in self._post_columns:
            if isinstance(col, Column) and col.valid_values:
                column_value_labels[col.name] = col.valid_values
            elif isinstance(col, ColumnGroup) and col.gvlabel:
                column_value_labels[col.name] = col.gvlabel

        return dict(column_value_labels) if column_value_labels else None

    @property
    def pre_column_valid_values(self):
        
        valid_values = {col.name: col.valid_values for col in self._pre_columns if col.valid_values}

        return valid_values if valid_values else None

    @property
    def pre_column_new_values(self):

        new_values = {col.name: col.new_values for col in self._pre_columns if col.new_values}

        return new_values if new_values else None

    @property
    def new_column_dtypes(self):
        if self.newcols:
            new_column_dtypes = {col.name: col.dtype for col in self.newcols if col.dtype}
            return new_column_dtypes if new_column_dtypes else None

    @property
    def new_column_exprs(self):
        if self.newcols:
            new_column_exprs = [{col.name: col.expr} for col in self.newcols if col.expr is not None]
            return new_column_exprs if new_column_exprs else None



class Query(BaseModel):
    """构造单个原始表的查询语句"""
    from_: str = Field(..., alias='from')
    select: Optional[List[str]]
    where: Optional[str]
    groupby: Optional[str]
    having: Optional[str]
    orderby: Optional[str]

    @property
    def sql(self):
        clauses = [
            f"SELECT {', '.join(self.select) if self.select else '*'}",
            f"FROM {self.from_}",
        ]
        if self.where:
            clauses.append(f"WHERE {self.where}")
        if self.groupby:
            clauses.append(f"GROUP BY {self.groupby}")
        if self.having:
            if self.groupby is None:
                raise ValueError("SQL Error: HAVING can only be used when GROUP BY is specified.")
            clauses.append(f"HAVING {self.having}")
        if self.orderby:
            clauses.append(f"ORDER BY {self.orderby}")

        return sqlparse.format(" ".join(clauses), reindent=True, keyword_case='upper')



class Edit(BaseModel):
    """构造合并表的单个编辑函数"""
    func: str = Field(..., description="Function to be applied",
                      choices=list(FUNCTION_MAP.keys()))  # 使用函数名列表作为选择
    kwargs: Optional[Dict[str, Any]]

    @validator('func')
    def map_func(cls, v):
        return FUNCTION_MAP[v]
    
    @validator('kwargs')
    def map_kwargs(cls,v):
        return v if v else {}
    
    @property
    def editor(self):
        return {'func':self.func, 'kwargs': self.kwargs}


    
@typechecked
def union(sql_statements: List[str], method: str, use: Optional[List[str]] = None, where: Optional[str]=None) -> str:
    """纵向合并表的SQL语句解析"""
    columns = '*' if not use else ', '.join(use)
    queries = [stmt.replace('SELECT *', f'SELECT {columns}') for stmt in sql_statements]
    unioned_result = f"\n{method}\n  ".join(f"{query}" for query in queries)
    return unioned_result if not where else f"SELECT * FROM ({unioned_result}) WHERE {where}"


@typechecked
def join(sql_statements: List[str], method: str, use: List[str], where: Optional[str]=None) -> str:
    # For join operations, using clause is necessary
    if not use:
        raise ValueError('The "use" argument is required for JOIN operations')
    using_clause = ', '.join(use)
    # Add a UUID alias to the first query
    
    join_query = f"({sql_statements[0]}) AS {_uid()}"
    # And then add a UUID alias for each additional query, and join them
    for stmt in sql_statements[1:]:
        join_query += f"\n{method}\n({stmt}) AS {_uid()} USING ({using_clause})"
    
    joined_result = f"SELECT * FROM ({join_query})" if not where else f"SELECT * FROM ({join_query}) WHERE {where}"
    return  joined_result



@typechecked
def combine(sql_statements: List[str], method: str, use: Optional[List[str]] = None, where: Optional[str]=None) -> str:
    if len(sql_statements) < 2:
        raise ValueError("At least two SQL statements are required for combining.")
    
    
    COMBINE_METHOD = {
        'union': 'UNION',
        'union_all': 'UNION ALL',
        'left_join': 'LEFT JOIN',
        'right_join': 'RIGHT JOIN',
        'join': 'JOIN',
        'full_join': 'FULL JOIN'
    }
    
    
    if method in {'union', 'union_all'}:
        return union(sql_statements, COMBINE_METHOD[method], use, where)

    elif method in {'left_join', 'right_join', 'join', 'full_join'}:
        return join(sql_statements, COMBINE_METHOD[method], use, where)
    

    else:
        raise ValueError(f"Unknown method: {method}")


class Combine(BaseModel):
    method: Literal['union','union_all','left_join','right_join', 'join','full_join']
    use: List[str]
    where: Optional[str]

class FromAction(BaseModel):
    fid: Optional[str]
    description: Optional[str]
    query: List[Query] 
    combine: Optional[Combine]
    edit: Optional[List[Edit]]


    @validator('combine')
    def check_combine(cls, combine, values):
        query = values.get('query')
        if query is not None:
            if combine is None and len(query) != 1:
                raise ValueError('When "combine" is None, "query" must have exactly 1 element.')
            elif combine is not None and len(query) <= 1:
                raise ValueError('When "combine" is not None, "query" must have more than 1 element.')
        return combine



    @property
    def query_action(self):
        if len(self.query) == 1:
            sql = sqlparse.format(self.query[0].sql, reindent=True, keyword_case='upper')
        else:
            sql_statements = [q.sql for q in self.query]
            method = self.combine.method
            use = self.combine.use
            where = self.combine.where
            sql = combine(sql_statements, method=method, use=use, where=where)

        return sql
    
    @property
    def edit_action(self):
        if self.edit:
            return [edit.editor for edit in self.edit]    
    

class ToAction(BaseModel):
    combine: Optional[Combine]
    edit: Optional[List[Edit]]
    export: Optional[Literal['parquet','stata']] = None

    @property
    def edit_action(self):
        if self.edit:
            return [edit.editor for edit in self.edit] 
        
        
class Export(BaseModel):
    name: str 
    description: str
    from_tables: List[FromAction]
    to_table: Optional[ToAction]

    @validator('to_table')
    def validate_tables(cls, v, values):
        from_tables = values.get('from_tables')
        if (not v or not v.combine) and len(from_tables) >= 2:
            raise ValueError('When from_tables contain more than one element, the combine attribute of to_table must be not None')
        elif v and v.combine and len(from_tables) == 1:
            raise ValueError('When from_tables contain only one element, the combine attribute of to_table must be None')
        return v

    @property
    def from_actions(self) -> List[Dict[str, Any]]:
        from_actions = [{'fid': fa.fid if fa.fid else '_'+self.name+str(i+1),
                         'description': fa.description,
                         'query_action': fa.query_action, 
                         'edit_action': fa.edit_action} for i, fa in enumerate(self.from_tables)]
        return from_actions


    @property
    def to_actions(self):
        
        sql_statements = [f"SELECT * FROM {fa_dict['fid']}" for fa_dict in self.from_actions]
        query_action = (
                combine(sql_statements = sql_statements, 
                        method = self.to_table.combine.method, 
                        use = self.to_table.combine.use) 
                if self.to_table and self.to_table.combine 
                else sql_statements[0]
            )
        
        edit_action = self.to_table.edit_action if self.to_table else None
        
        ToFileExtension = {
            'stata':'.dta',
            'parquet':'.parquet'
        }
        
        to_file = {'filetype':self.to_table.export, 'filename': self.name+ToFileExtension[self.to_table.export]} if self.to_table and self.to_table.export else None
  
        return {'tid':self.name, 'description': self.description, 'to_file': to_file, 'query_action': query_action, 'edit_action': edit_action}


class DataBase(BaseModel):
    fast_load: Optional[str]=None
    source: str  = 'source.duckdb'
    export: str  = './'

    @validator('fast_load',always=True)
    def check_fast_load(cls, v):
        if v and not v.endswith('.duckdb'):
            raise ValueError(f"Database for fast load {v} should be a file path with a suffix '.duckdb'")
        return Path(v) if v else v
        
    @validator('source',always=True)
    def check_source(cls, v):
        if not v.endswith('.duckdb'):
            raise ValueError(f"Database for source {v} should be a file path with a suffix '.duckdb'")
        return Path(v)
    

    @validator('export',always=True)
    def check_export(cls, v):
        if not v.endswith('/'):
            raise ValueError(f"Database for export {v} should be a directory with a suffix '/'")
        
        path = Path(v)
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
        
        if not path.is_dir():
            raise ValueError(f"Database for export {v} should be a directory")
        
        return path

class Config(BaseModel):
    database: DataBase = DataBase()
    sources: List[Dataset]
    exports: Optional[List[Export]]


    
    @validator('sources')
    def validate_unique_ids(cls, sources):
        ids = [source.id for source in sources]
        id_counts = Counter(ids)
        duplicate_ids = [id for id, count in id_counts.items() if count > 1]
        if duplicate_ids:
            raise ValueError(f"The id(s) {duplicate_ids} of Dataset in sources are not unique.")
        return sources

    @classmethod
    def from_yaml(cls, path: str):
        with open(path, 'r') as f:
            data = yaml.safe_load(f)
        return cls(**data)