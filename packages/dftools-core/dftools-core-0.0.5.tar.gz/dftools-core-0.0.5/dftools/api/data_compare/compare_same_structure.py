import pandas as pd
import os
from datetime import datetime

from typing import List, Dict

from dftools.core.structure import Structure, StructureCatalog, StructureCatalogCsv
from dftools.api.data_compare.pd_df_compare import PandasDataFrameCompare

class PandasDfSameStructureCompare(PandasDataFrameCompare):
    """Comparison class to be used to compare whether two dataframes as equal with standard rules to extract only data required in the comparison

    Both df1 and df2 should be dataframes containing all of the join_columns,
    with unique column names. Differences between values are compared to
    abs_tol + rel_tol * abs(df2['value']).

    Parameters
    ----------
    df1 : pandas ``DataFrame``
        First dataframe to check
    df2 : pandas ``DataFrame``
        Second dataframe to check
    on_index : bool, optional
        If True, the index will be used to join the two dataframes.  If both
        ``join_columns`` and ``on_index`` are provided, an exception will be
        raised.
    abs_tol : float, optional
        Absolute tolerance between two values.
    rel_tol : float, optional
        Relative tolerance between two values.
    df1_name : str, optional
        A string name for the first dataframe.  This allows the reporting to
        print out an actual name instead of "df1", and allows human users to
        more easily track the dataframes.
    df2_name : str, optional
        A string name for the second dataframe
    comparison_name : str, optional
        A string name for this comparison
    ignore_spaces : bool, optional
        Flag to strip whitespace (including newlines) from string columns (including any join
        columns)
    ignore_case : bool, optional
        Flag to ignore the case of string columns
    cast_column_names_lower: bool, optional
        Boolean indicator that controls of column names will be cast into lower case
    df_structure: dftools ``Structure``
        The structure metadata applicable for both dataframes
    join_characterisation: str
        The field characterisation to consider the join columns
    field_characterisations_to_exclude: str
        The list of field characterisations to exclude from the comparison
    field_names_to_exclude: str
        The list of field names to exclude from the comparison

    Attributes
    ----------
    df1_unq_rows : pandas ``DataFrame``
        All records that are only in df1 (based on a join on join_columns)
    df2_unq_rows : pandas ``DataFrame``
        All records that are only in df2 (based on a join on join_columns)
    """
    def __init__(
        self,
        df1 : pd.DataFrame,
        df2 : pd.DataFrame,
        on_index=False,
        abs_tol=0,
        rel_tol=0,
        df1_name="df1",
        df2_name="df2",
        comparison_name="default",
        ignore_spaces=False,
        ignore_case=False,
        cast_column_names_lower=True,
        df_structure : Structure = None,
        join_characterisation : str = 'TEC_ID',
        field_characterisations_to_exclude : List[str] = None,
        field_names_to_exclude : List[str] = None
        ) -> None:
        field_characterisations_to_exclude = field_characterisations_to_exclude if field_characterisations_to_exclude is not None else []
        self.df_structure = df_structure
        join_columns = self.df_structure.get_field_names_with_characterisation(join_characterisation)
        field_names_to_exclude : List[str] = self.df_structure.get_field_names_with_characterisations(field_characterisations_to_exclude)
        if field_names_to_exclude is not None : 
            field_names_to_exclude.extend(field_names_to_exclude)

        df1_for_check=df1[df1.columns.difference(field_names_to_exclude)]
        df2_for_check=df2[df2.columns.difference(field_names_to_exclude)]

        super().__init__(df1=df1_for_check, df2=df2_for_check, join_columns=join_columns, on_index=on_index, abs_tol=abs_tol, rel_tol=rel_tol, df1_name=df1_name, df2_name=df2_name
            , comparison_name=comparison_name, ignore_spaces=ignore_spaces, ignore_case=ignore_case, cast_column_names_lower=cast_column_names_lower)

def get_pandas_dtype_from_structure(structure : Structure) -> Dict[str, str]:
    pd_dtype_dict : Dict[str, str]= {}
    for field in structure.fields:
        field_pd_dtype = 'str'
        if field.data_type.upper() in ['INT']:
            field_pd_dtype = 'Int64'
        pd_dtype_dict.update({field.name : field_pd_dtype})
    return pd_dtype_dict

def compare_identical_structure_data_from_files(
        folder_path : str
        , structure_name : str
        , files_prefix : str = ""
        , files_suffix : str = ""
        , data_files_encoding : str = 'ISO-8859-1'
        , df1_name : str = "Original"
        , df2_name : str = "New"
        , abs_tol : float = 0
        , rel_tol : float = 0
        , field_characterisations_to_exclude : List[str] = None
        , output_folder_path : str = None
    ) -> PandasDfSameStructureCompare:
    """Compares data between 2 datasets with the same structure and outputs the result if required.

    This compare method requires 3 files :
    - The structure metadata file, which should be named using the pattern "structure_name + files_prefix + '.metadata.csv'"
    - The original csv data file, which should be named using the pattern "structure_name + files_prefix + '.orig.' + files_suffix + '.csv'"
    - The new csv data file, which should be named using the pattern "structure_name + files_prefix + '.new.' + files_suffix + '.csv'"

    Encoding of the data files should be ISO-8859-1.

    Parameters
    ----------
    folder_path : str
        The folder path containing all the input files
    structure_name : str
        The structure name
    files_prefix : str, optional
        The prefix on all the files
    files_suffix : str, optional
        The suffix on all the data files
    data_files_encoding : str, optional
        The encoding of the data files
    abs_tol : float, optional
        Absolute tolerance between two values.
    rel_tol : float, optional
        Relative tolerance between two values.
    field_characterisations_to_exclude : List[str], optional
        The list of field characterisations to exclude from the comparison
    output_folder_path : str, optional
        The compare report output folder path. If not provided, no output is generated.

    Returns
    ----------
    compare : PandasDfSameStructureCompare
        The comparison object
    """
    folder_abs_path = os.path.abspath(folder_path)
    field_characterisations_to_exclude = \
        ['REC_DELETION_TST','REC_DELETION_USER_NAME','REC_INSERT_TST','REC_INSERT_USER_NAME','REC_LAST_UPDATE_TST','REC_LAST_UPDATE_USER_NAME'] \
            if field_characterisations_to_exclude is None else field_characterisations_to_exclude
    
    str_catalog : StructureCatalog = StructureCatalogCsv.read_csv(os.path.join(folder_abs_path, structure_name + files_prefix + '.metadata.csv'))
    structure = str_catalog.get_structure_by_name(structure_name)

    df_orig = pd.read_csv(os.path.join(folder_abs_path, structure_name + files_prefix + '.orig.' + files_suffix + '.csv'), sep=";" ,encoding=data_files_encoding
        , dtype = get_pandas_dtype_from_structure(structure))
    df_new = pd.read_csv(os.path.join(folder_abs_path, structure_name + files_prefix + '.new.' + files_suffix + '.csv'), sep=";", encoding=data_files_encoding
        , dtype = get_pandas_dtype_from_structure(structure))
    
    compare = PandasDfSameStructureCompare(df1=df_orig, df2=df_new, df1_name=df1_name, df2_name=df2_name, comparison_name='Comparison of ' + structure_name 
        , df_structure = structure, field_characterisations_to_exclude=field_characterisations_to_exclude, abs_tol = abs_tol, rel_tol = rel_tol)
    if output_folder_path is not None :
        now = datetime.now()
        now_str=now.strftime("%Y%m%d_%H%M%S")
        compare.report_complete(output_folder_path=os.path.join(output_folder_path, now_str + '_' + structure_name))

    return compare
