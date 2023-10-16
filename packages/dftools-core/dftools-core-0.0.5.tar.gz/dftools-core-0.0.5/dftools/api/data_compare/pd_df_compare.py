import os
import logging
from typing import List, Dict, Any

import pandas as pd
import numpy as np
from ordered_set import OrderedSet

from dftools.events import DfLoggable, StandardInfoEvent as StdInfoEvent, StandardDebugEvent as StdDebugEvent

class PandasDataFrameCompare(DfLoggable):
    """Comparison class to be used to compare whether two dataframes as equal.

    Both df1 and df2 should be dataframes containing all of the join_columns,
    with unique column names. Differences between values are compared to
    abs_tol + rel_tol * abs(df2['value']).

    Parameters
    ----------
    df1 : pandas ``DataFrame``
        First dataframe to check
    df2 : pandas ``DataFrame``
        Second dataframe to check
    join_columns : list or str, optional
        Column(s) to join dataframes on.  If a string is passed in, that one
        column will be used.
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

    Attributes
    ----------
    df1_unq_rows : pandas ``DataFrame``
        All records that are only in df1 (based on a join on join_columns)
    df2_unq_rows : pandas ``DataFrame``
        All records that are only in df2 (based on a join on join_columns)
    """
    def __init__(
        self,
        df1,
        df2,
        join_columns=None,
        on_index=False,
        abs_tol=0,
        rel_tol=0,
        df1_name="df1",
        df2_name="df2",
        comparison_name="default",
        ignore_spaces=False,
        ignore_case=False,
        cast_column_names_lower=True,
    ):
        self.cast_column_names_lower = cast_column_names_lower
        if on_index and join_columns is not None:
            raise Exception("Only provide on_index or join_columns")
        elif on_index:
            self.on_index = True
            self.join_columns = []
        elif isinstance(join_columns, (str, int, float)):
            self.join_columns = [
                str(join_columns).lower()
                if self.cast_column_names_lower
                else str(join_columns)
            ]
            self.on_index = False
        else:
            self.join_columns = [
                str(col).lower() if self.cast_column_names_lower else str(col)
                for col in join_columns
            ]
            self.on_index = False

        self.logger = logging.getLogger(__name__)
        self._any_dupes = False
        self.df1 = df1
        self.df2 = df2
        self.df1_name = df1_name
        self.df2_name = df2_name
        self.comparison_name = comparison_name
        self.abs_tol = abs_tol
        self.rel_tol = rel_tol
        self.ignore_spaces = ignore_spaces
        self.ignore_case = ignore_case
        self.df1_unq_rows = self.df2_unq_rows = self.intersect_rows = None
        self.column_stats = []
        self._compare(ignore_spaces, ignore_case)

    @property
    def df1(self):
        return self._df1

    @df1.setter
    def df1(self, df1):
        """Check that it is a dataframe and has the join columns"""
        self._df1 = df1
        self._validate_dataframe(
            "df1", cast_column_names_lower=self.cast_column_names_lower
        )

    @property
    def df2(self):
        return self._df2

    @df2.setter
    def df2(self, df2):
        """Check that it is a dataframe and has the join columns"""
        self._df2 = df2
        self._validate_dataframe(
            "df2", cast_column_names_lower=self.cast_column_names_lower
        )

    def _validate_dataframe(self, index, cast_column_names_lower=True):
        """Check that it is a dataframe and has the join columns

        Parameters
        ----------
        index : str
            The "index" of the dataframe - df1 or df2.
        cast_column_names_lower: bool, optional
            Boolean indicator that controls of column names will be cast into lower case
        """
        dataframe = getattr(self, index)
        if not isinstance(dataframe, pd.DataFrame):
            raise TypeError(f"{index} must be a pandas DataFrame")

        if cast_column_names_lower:
            dataframe.columns = [str(col).lower() for col in dataframe.columns]
        else:
            dataframe.columns = [str(col) for col in dataframe.columns]
        # Check if join_columns are present in the dataframe
        if not set(self.join_columns).issubset(set(dataframe.columns)):
            raise ValueError(f"{index} must have all columns from join_columns")

        if len(set(dataframe.columns)) < len(dataframe.columns):
            raise ValueError(f"{index} must have unique column names")

        if self.on_index:
            if dataframe.index.duplicated().sum() > 0:
                self._any_dupes = True
        else:
            if len(dataframe.drop_duplicates(subset=self.join_columns)) < len(
                dataframe
            ):
                self._any_dupes = True

    def _compare(self, ignore_spaces, ignore_case):
        """Actually run the comparison.  This tries to run df1.equals(df2)
        first so that if they're truly equal we can tell.

        This method will log out information about what is different between
        the two dataframes, and will also return a boolean.
        """
        self.log_event(StdDebugEvent("Checking equality"))
        if self.df1.equals(self.df2):
            self.log_event(StdInfoEvent("df1 Pandas.DataFrame.equals df2"))
        else:
            self.log_event(StdInfoEvent("df1 does not Pandas.DataFrame.equals df2"))
        self.log_event(StdInfoEvent(f"Number of columns in common: {len(self.intersect_columns())}"))
        
        self.log_event(StdDebugEvent("Checking column overlap"))
        for col in self.df1_unq_columns():
            self.log_event(StdInfoEvent(f"Column in df1 and not in df2: {col}"))
        self.log_event(StdInfoEvent(f"Number of columns in df1 and not in df2: {len(self.df1_unq_columns())}"))
        for col in self.df2_unq_columns():
            self.log_event(StdInfoEvent(f"Column in df2 and not in df1: {col}"))
        self.log_event(StdInfoEvent(f"Number of columns in df1 and not in df2: {len(self.df1_unq_columns())}"))
        
        self.log_event(StdDebugEvent("Merging dataframes"))
        self._dataframe_merge(ignore_spaces)
        self._intersect_compare(ignore_spaces, ignore_case)
        if self.matches():
            self.log_event(StdInfoEvent("df1 matches df2"))
        else:
            self.log_event(StdInfoEvent("df1 does not match df2"))

    def df1_unq_columns(self):
        """Get columns that are unique to df1"""
        return OrderedSet(self.df1.columns) - OrderedSet(self.df2.columns)

    def df2_unq_columns(self):
        """Get columns that are unique to df2"""
        return OrderedSet(self.df2.columns) - OrderedSet(self.df1.columns)

    def intersect_columns(self):
        """Get columns that are shared between the two dataframes"""
        return OrderedSet(self.df1.columns) & OrderedSet(self.df2.columns)

    def _dataframe_merge(self, ignore_spaces):
        """Merge df1 to df2 on the join columns, to get df1 - df2, df2 - df1
        and df1 & df2

        If ``on_index`` is True, this will join on index values, otherwise it
        will join on the ``join_columns``.
        """

        self.log_event(StdDebugEvent("Outer joining"))
        if self._any_dupes:
            self.log_event(StdDebugEvent("Duplicate rows found, deduping by order of remaining fields"))
            # Bring index into a column
            if self.on_index:
                index_column = temp_column_name(self.df1, self.df2)
                self.df1[index_column] = self.df1.index
                self.df2[index_column] = self.df2.index
                temp_join_columns = [index_column]
            else:
                temp_join_columns = list(self.join_columns)

            # Create order column for uniqueness of match
            order_column = temp_column_name(self.df1, self.df2)
            self.df1[order_column] = generate_id_within_group(
                self.df1, temp_join_columns
            )
            self.df2[order_column] = generate_id_within_group(
                self.df2, temp_join_columns
            )
            temp_join_columns.append(order_column)

            params = {"on": temp_join_columns}
        elif self.on_index:
            params = {"left_index": True, "right_index": True}
        else:
            params = {"on": self.join_columns}

        if ignore_spaces:
            for column in self.join_columns:
                if self.df1[column].dtype.kind == "O":
                    self.df1[column] = self.df1[column].str.strip()
                if self.df2[column].dtype.kind == "O":
                    self.df2[column] = self.df2[column].str.strip()

        outer_join = self.df1.merge(
            self.df2, how="outer", suffixes=("_df1", "_df2"), indicator=True, **params
        )
        # Clean up temp columns for duplicate row matching
        if self._any_dupes:
            if self.on_index:
                outer_join.index = outer_join[index_column]
                outer_join.drop(index_column, axis=1, inplace=True)
                self.df1.drop(index_column, axis=1, inplace=True)
                self.df2.drop(index_column, axis=1, inplace=True)
            outer_join.drop(order_column, axis=1, inplace=True)
            self.df1.drop(order_column, axis=1, inplace=True)
            self.df2.drop(order_column, axis=1, inplace=True)

        df1_cols = get_merged_columns(self.df1, outer_join, "_df1")
        df2_cols = get_merged_columns(self.df2, outer_join, "_df2")

        self.log_event(StdDebugEvent("Selecting df1 unique rows"))
        self.df1_unq_rows = outer_join[outer_join["_merge"] == "left_only"][
            df1_cols
        ].copy()
        self.df1_unq_rows.columns = self.df1.columns

        self.log_event(StdDebugEvent("Selecting df2 unique rows"))
        self.df2_unq_rows = outer_join[outer_join["_merge"] == "right_only"][
            df2_cols
        ].copy()
        self.df2_unq_rows.columns = self.df2.columns
        self.log_event(StdInfoEvent(f"Number of rows in df1 and not in df2: {len(self.df1_unq_rows)}"))
        self.log_event(StdInfoEvent(f"Number of rows in df2 and not in df1: {len(self.df2_unq_rows)}"))
        
        self.log_event(StdDebugEvent("Selecting intersecting rows"))
        self.intersect_rows = outer_join[outer_join["_merge"] == "both"].copy()
        self.log_event(StdInfoEvent("Number of rows in df1 and df2 (not necessarily equal): {len(self.intersect_rows)}"))
        
    def _intersect_compare(self, ignore_spaces, ignore_case):
        """Run the comparison on the intersect dataframe

        This loops through all columns that are shared between df1 and df2, and
        creates a column column_match which is True for matches, False
        otherwise.
        """
        self.log_event(StdDebugEvent("Comparing intersection"))
        row_cnt = len(self.intersect_rows)
        for column in self.intersect_columns():
            if column in self.join_columns:
                match_cnt = row_cnt
                col_match = ""
                max_diff = 0
                null_diff = 0
            else:
                col_1 = column + "_df1"
                col_2 = column + "_df2"
                col_match = column + "_match"
                self.intersect_rows[col_match] = columns_equal(
                    self.intersect_rows[col_1],
                    self.intersect_rows[col_2],
                    self.rel_tol,
                    self.abs_tol,
                    ignore_spaces,
                    ignore_case,
                )
                match_cnt = self.intersect_rows[col_match].sum()
                max_diff = calculate_max_diff(
                    self.intersect_rows[col_1], self.intersect_rows[col_2]
                )
                null_diff = (
                    (self.intersect_rows[col_1].isnull())
                    ^ (self.intersect_rows[col_2].isnull())
                ).sum()

            if row_cnt > 0:
                match_rate = float(match_cnt) / row_cnt
            else:
                match_rate = 0
            self.log_event(StdInfoEvent(f"{column}: {match_cnt} / {row_cnt} ({match_rate:.2%}) match"))

            self.column_stats.append(
                {
                    "column": column,
                    "match_column": col_match,
                    "match_cnt": match_cnt,
                    "unequal_cnt": row_cnt - match_cnt,
                    "dtype1": str(self.df1[column].dtype),
                    "dtype2": str(self.df2[column].dtype),
                    "all_match": all(
                        (
                            self.df1[column].dtype == self.df2[column].dtype,
                            row_cnt == match_cnt,
                        )
                    ),
                    "max_diff": max_diff,
                    "null_diff": null_diff,
                }
            )

    def all_columns_match(self):
        """Whether the columns all match in the dataframes"""
        return self.df1_unq_columns() == self.df2_unq_columns() == set()

    def all_rows_overlap(self):
        """Whether the rows are all present in both dataframes

        Returns
        -------
        bool
            True if all rows in df1 are in df2 and vice versa (based on
            existence for join option)
        """
        return len(self.df1_unq_rows) == len(self.df2_unq_rows) == 0

    def count_matching_rows(self):
        """Count the number of rows match (on overlapping fields)

        Returns
        -------
        int
            Number of matching rows
        """
        match_columns = []
        for column in self.intersect_columns():
            if column not in self.join_columns:
                match_columns.append(column + "_match")
        return self.intersect_rows[match_columns].all(axis=1).sum()

    def intersect_rows_match(self):
        """Check whether the intersect rows all match"""
        actual_length = self.intersect_rows.shape[0]
        return self.count_matching_rows() == actual_length

    def matches(self, ignore_extra_columns=False):
        """Return True or False if the dataframes match.

        Parameters
        ----------
        ignore_extra_columns : bool
            Ignores any columns in one dataframe and not in the other.
        """
        if not ignore_extra_columns and not self.all_columns_match():
            return False
        elif not self.all_rows_overlap():
            return False
        elif not self.intersect_rows_match():
            return False
        else:
            return True

    def subset(self):
        """Return True if dataframe 2 is a subset of dataframe 1.

        Dataframe 2 is considered a subset if all of its columns are in
        dataframe 1, and all of its rows match rows in dataframe 1 for the
        shared columns.
        """
        if not self.df2_unq_columns() == set():
            return False
        elif not len(self.df2_unq_rows) == 0:
            return False
        elif not self.intersect_rows_match():
            return False
        else:
            return True

    def sample_mismatch(self, column, sample_count=10, for_display=False):
        """Returns a sample sub-dataframe which contains the identifying
        columns, and df1 and df2 versions of the column.

        Parameters
        ----------
        column : str
            The raw column name (i.e. without ``_df1`` appended)
        sample_count : int, optional
            The number of sample records to return.  Defaults to 10.
        for_display : bool, optional
            Whether this is just going to be used for display (overwrite the
            column names)

        Returns
        -------
        Pandas.DataFrame
            A sample of the intersection dataframe, containing only the
            "pertinent" columns, for rows that don't match on the provided
            column.
        """
        row_cnt = self.intersect_rows.shape[0]
        col_match = self.intersect_rows[column + "_match"]
        match_cnt = col_match.sum()
        sample_count = min(sample_count, row_cnt - match_cnt)
        sample = self.intersect_rows[~col_match].sample(sample_count)
        return_cols = self.join_columns + [column + "_df1", column + "_df2"]
        to_return = sample[return_cols]
        if for_display:
            to_return.columns = self.join_columns + [
                column + " (" + self.df1_name + ")",
                column + " (" + self.df2_name + ")",
            ]
        return to_return

    def all_mismatch(self, ignore_matching_cols=False):
        """All rows with any columns that have a mismatch. Returns all df1 and df2 versions of the columns and join
        columns.

        Parameters
        ----------
        ignore_matching_cols : bool, optional
            Whether showing the matching columns in the output or not. The default is False.

        Returns
        -------
        Pandas.DataFrame
            All rows of the intersection dataframe, containing any columns, that don't match.
        """
        match_list = []
        return_list = []
        for col in self.intersect_rows.columns:
            if col.endswith("_match"):
                orig_col_name = col[:-6]

                col_comparison = columns_equal(
                    self.intersect_rows[orig_col_name + "_df1"],
                    self.intersect_rows[orig_col_name + "_df2"],
                    self.rel_tol,
                    self.abs_tol,
                    self.ignore_spaces,
                    self.ignore_case,
                )

                if not ignore_matching_cols or (
                    ignore_matching_cols and not col_comparison.all()
                ):
                    self.log_event(StdDebugEvent(f"Adding column {orig_col_name} to the result."))
                    match_list.append(col)
                    return_list.extend([orig_col_name + "_df1", orig_col_name + "_df2"])
                elif ignore_matching_cols:
                    self.log_event(StdDebugEvent(f"Column {orig_col_name} is equal in df1 and df2. It will not be added to the result."))

        mm_bool = self.intersect_rows[match_list].all(axis="columns")
        return self.intersect_rows[~mm_bool][self.join_columns + return_list]

    def get_match_stats(self, sample_count : int) -> None:
        """All rows with any columns that have a mismatch. Returns all df1 and df2 versions of the columns and join
        columns.

        Parameters
        ----------
        sample_count : int, optional
            The number of sample records to return.  Defaults to 10.

        Returns
        -------
        match_stats
            The match stats for all the columns with at least one mismatch in the comparison
        mismatch_sample
            The mismatch samples of data containing a maximum number of rows equal to the parameter sample_count
        any_mismatch
            Flag indicating if any mismatch on columns has been recorded on this comparison
        """
        match_stats = []
        mismatch_sample = []
        any_mismatch = False
        for column in self.column_stats:
            if not column["all_match"]:
                any_mismatch = True
                match_stats.append(
                    {
                        "Column": column["column"],
                        f"{self.df1_name} dtype": column["dtype1"],
                        f"{self.df2_name} dtype": column["dtype2"],
                        "# Unequal": column["unequal_cnt"],
                        "Max Diff": column["max_diff"],
                        "# Null Diff": column["null_diff"],
                    }
                )
                if column["unequal_cnt"] > 0:
                    mismatch_sample.append(
                        self.sample_mismatch(
                            column["column"], sample_count, for_display=True
                        )
                    )
        return match_stats, mismatch_sample, any_mismatch

    def df_to_str(self, pdf):
        if not self.on_index:
            pdf = pdf.reset_index(drop=True)
        return pdf.to_string(index=False)
    
    def report_header(self) -> str:
        return """DfDataComp Comparison
--------------------

"""

    def report_comparison_parameters(self) -> str:
        return f"""Parameters Summary
--------------------

Comparison Name : {self.comparison_name} ({self.df1_name} / {self.df2_name})
Absolute Tolerance: {self.abs_tol}
Relative Tolerance: {self.rel_tol}
Matching columns : {self.matched_on()}
Compared columns : {", ".join(self.compared_columns())}\n\n"""

    def report_comparison_summary(self) -> str:
        return f"""Comparison Summary
--------------------

Any duplicates on match values : {"Yes" if self._any_dupes else "No"}

Columns in common : {len(self.intersect_columns()) / self.get_number_of_unq_cols():.2%} ({len(self.intersect_columns())} / {self.get_number_of_unq_cols()})
    Columns only in {self.df1_name} : {len(self.df1_unq_columns())} ({', '.join(self.df1_unq_columns())})
    Columns only in {self.df2_name} : {len(self.df2_unq_columns())} ({', '.join(self.df2_unq_columns())})

Rows matching keys : {self.intersect_rows.shape[0] / self.get_number_of_unq_rows():.2%} ({self.intersect_rows.shape[0]} / {self.get_number_of_unq_rows()})
\tRows only in {self.df1_name} : {self.df1_unq_rows.shape[0] / self.get_number_of_unq_rows():.2%} ({self.df1_unq_rows.shape[0]} / {self.get_number_of_unq_rows()})
\tRows only in {self.df2_name} : {self.df2_unq_rows.shape[0] / self.get_number_of_unq_rows():.2%} ({self.df2_unq_rows.shape[0]} / {self.get_number_of_unq_rows()})

Column Comparison (on matching key rows): 
\tRows with all compared columns equal : {self.count_matching_rows() / self.intersect_rows.shape[0]:.2%} ({self.count_matching_rows()} / {self.intersect_rows.shape[0]})
\n"""
    
    def report_dataframe_summary(self) -> str:
        return """DataFrame Summary
--------------------

""" + pd.DataFrame(
            {
                "DataFrame": [self.df1_name, self.df2_name],
                "Columns": [self.df1.shape[1], self.df2.shape[1]],
                "Rows": [self.df1.shape[0], self.df2.shape[0]],
            }
        ).to_string(index=False) + "\n\n"
    
    def report_column_diff_summary(self, sample_count : int) -> str:
        match_stats, mismatch_sample, any_mismatch = self.get_match_stats(sample_count=sample_count)
        report_string = ""
        if any_mismatch:
            df_match_stats = pd.DataFrame(match_stats)
            df_match_stats.sort_values("Column", inplace=True)
            report_string += f"""Columns with Unequal Values or Types
--------------------

"""
            report_string += df_match_stats[
                [
                    "Column",
                    f"{self.df1_name} dtype",
                    f"{self.df2_name} dtype",
                    "# Unequal",
                    "Max Diff",
                    "# Null Diff",
                ]
            ].to_string(index=False) + "\n\n"

            if sample_count > 0:
                report_string += "Sample Rows with Unequal Values\n"
                report_string += "-------------------------------\n\n"
                for sample in mismatch_sample:
                    report_string += self.df_to_str(sample)
                    report_string += "\n\n"
                report_string += "\n\n"

        return report_string
    
    def report_df1_unq_rows_sample(self, sample_count : int, column_count : int) -> str:
        report_string = ""
        if min(sample_count, self.df1_unq_rows.shape[0]) > 0:
            report_string = f"""Sample Rows Only in {self.df1_name} (First {column_count} Columns)\n
---------------------------------------{'-' * len(self.df1_name)}\n"""
            columns = self.df1_unq_rows.columns[:column_count]
            unq_count = min(sample_count, self.df1_unq_rows.shape[0])
            report_string += self.df_to_str(self.df1_unq_rows.sample(unq_count)[columns])
            report_string += "\n\n"
        return report_string

    def report_df2_unq_rows_sample(self, sample_count : int, column_count : int) -> str:
        report_string = ""
        if min(sample_count, self.df2_unq_rows.shape[0]) > 0:
            report_string = f"""Sample Rows Only in {self.df2_name} (First {column_count} Columns)\n
---------------------------------------{'-' * len(self.df2_name)}\n"""
            columns = self.df1_unq_rows.columns[:column_count]
            unq_count = min(sample_count, self.df2_unq_rows.shape[0])
            report_string += self.df_to_str(self.df2_unq_rows.sample(unq_count)[columns])
            report_string += "\n\n"
        return report_string
    
    def report(self, sample_count=10, column_count=30, html_file=None):
        """Returns a string representation of a report.  The representation can
        then be printed or saved to a file.

        Parameters
        ----------
        sample_count : int, optional
            The number of sample records to return.  Defaults to 10.

        column_count : int, optional
            The number of columns to display in the sample records output.  Defaults to 10.

        html_file : str, optional
            HTML file name to save report output to. If ``None`` the file creation will be skipped.

        Returns
        -------
        str
            The report, formatted kinda nicely.
        """
        report = self.report_header()
        report += self.report_comparison_parameters()
        report += self.report_comparison_summary()
        report += self.report_dataframe_summary()
        report += self.report_column_diff_summary(sample_count=sample_count)
        report += self.report_df1_unq_rows_sample(sample_count=sample_count, column_count=column_count)
        report += self.report_df2_unq_rows_sample(sample_count=sample_count, column_count=column_count)
        
        if html_file:
            html_report = report.replace("\n", "<br>").replace(" ", "&nbsp;")
            html_report = f"<pre>{html_report}</pre>"
            with open(html_file, "w") as f:
                f.write(html_report)

        return report

    def matched_on(self) -> str:
        """Get the matched on fields as a string

        Returns
        ----------
        matched_on : str
            A string containing the list of join columns used in the comparison separated by the string ", "
        """
        if self.on_index:
            return "index"
        else:
            return ", ".join(self.join_columns)

    def compared_columns(self) -> List[str]:
        """Get the compared columns as a string

        Returns
        ----------
        compared_columns : str
            A string containing the list of join columns used in the comparison separated by the string ", "
        """
        compared_columns = list(self.intersect_columns())
        for column in self.join_columns:
            compared_columns.remove(column)
        return compared_columns

    def get_number_of_unq_rows(self) -> int:
        """Get the number of unique rows in both df1 and df2 dataframes

        Returns
        ----------
        unq_row_num : int
            The number of unique rows
        """
        return self.df1_unq_rows.shape[0] + self.df2_unq_rows.shape[0] + self.intersect_rows.shape[0]
    
    def get_number_of_unq_cols(self) -> int :
        """Get the number of unique columns in both df1 and df2 dataframes

        Returns
        ----------
        unq_col_num : int
            The number of unique columns
        """
        return len(self.intersect_columns()) + len(self.df1_unq_columns()) + len(self.df2_unq_columns())

    def get_intersect_rows_output(self, only_diff : bool = True) -> pd.DataFrame:
        """Get the intersect rows dataframe with all original, new and matching result in the same dataframe.

        The output dataset columns are : 
        - Join Columns
        - A column "att_match", which is the row matching status for all the compared columns. If any comparison on column equals False, this column is False.
        - For all the compared columns
            - A column from the df1 (original) dataframe, which is suffixed with "_orig"
            - A column from the df2 (new) dataframe, which is suffixed with "_new"
            - A match column, which is named by a combinaison of the columns' name and the suffix "_match"

        Parameters
        ----------
        only_diff : bool
            Includes only the rows with differences (at least one difference) in the returned dataframe, when True.
            Defaulted to True

        Returns
        ----------
        intersect_rows : pd.DataFrame
            A dataframe containing all the original, new and matching result
        """
        ordered_column_list = [column for column in self.join_columns]
        for column_name in self.compared_columns():
            ordered_column_list.extend([column_name + '_orig', column_name + '_new', column_name + '_match'])
        intersect_renaming_map = {}
        for column_name in self.compared_columns():
            intersect_renaming_map[column_name + '_df1'] = column_name + '_orig'
            intersect_renaming_map[column_name + '_df2'] = column_name + '_new'

        intersect_rows : pd.DataFrame = self.intersect_rows.copy()
        intersect_rows.rename(columns=intersect_renaming_map, inplace=True)
        intersect_rows = intersect_rows[ordered_column_list]

        i = 0
        att_match_formula = ''
        for att_column_name in self.compared_columns():
            if i > 0:
                att_match_formula += ' & '
            att_match_formula += att_column_name + '_match == True'
            i+=1
        if len(self.compared_columns()) > 0:
            intersect_rows.insert(len(self.join_columns), 'att_match', intersect_rows.eval(att_match_formula))
            
        if (only_diff & (len(self.compared_columns()) > 0)):
            return intersect_rows[intersect_rows.att_match.isin([False])]
        return intersect_rows

    def report_complete(self, output_folder_path : str) -> None:
        """Outputs to a folder the complete report information.

        The complete report contains :
        - The summary HTML
        - If any difference recorded on intersect rows
            - An intersect csv file
        - If any row is available only in the original dataframe (df1)
            - An orig_only csv file
        - If any row is available only in the new dataframe (df2)
            - An new_only csv file

        Parameters
        ----------
        output_folder_path : str
            The output folder path, which can be provided as relative or absolute, although using absolute path is recommended
        """
        os.makedirs(output_folder_path, exist_ok=True)
        intersect_rows = self.get_intersect_rows_output()
        if intersect_rows.shape[0] > 0 :
            intersect_rows.to_csv(os.path.join(output_folder_path, 'intersect.csv'))
        if self.df1_unq_rows.shape[0] > 0 :
            self.df1_unq_rows.to_csv(os.path.join(output_folder_path, 'orig_only.csv'))
        if self.df2_unq_rows.shape[0] > 0 :
            self.df2_unq_rows.to_csv(os.path.join(output_folder_path, 'new_only.csv'))
        self.report(sample_count=100, html_file=os.path.join(output_folder_path, 'summary.html'))

    def get_non_reg_complete_table(self) -> pd.DataFrame:
        comparison_dataframe = pd.merge(self.df1, self.df2, on=self.matched_on(), suffixes=['_orig', '_new'])
        ordered_column_list = [column for column in self.join_columns]
        for column_name in self.compared_columns():
            ordered_column_list.extend([column_name + '_orig', column_name + '_new'])
        comparison_dataframe = comparison_dataframe[ordered_column_list]
        for column_name in self.compared_columns():
            orig_column_name = column_name + '_orig'
            new_column_name = column_name + '_new'
            column_idx = comparison_dataframe.columns.get_loc(new_column_name)
            print(column_idx)
            comparison_dataframe.insert(
                column_idx + 1
                , column_name + '_comp'
                , columns_equal(comparison_dataframe[orig_column_name], comparison_dataframe[new_column_name])
            )
        return comparison_dataframe

def columns_equal(
    col_1, col_2, rel_tol=0, abs_tol=0, ignore_spaces=False, ignore_case=False
):
    """Compares two columns from a dataframe, returning a True/False series,
    with the same index as column 1.

    - Two nulls (np.nan) will evaluate to True.
    - A null and a non-null value will evaluate to False.
    - Numeric values will use the relative and absolute tolerances.
    - Decimal values (decimal.Decimal) will attempt to be converted to floats
      before comparing
    - Non-numeric values (i.e. where np.isclose can't be used) will just
      trigger True on two nulls or exact matches.

    Parameters
    ----------
    col_1 : Pandas.Series
        The first column to look at
    col_2 : Pandas.Series
        The second column
    rel_tol : float, optional
        Relative tolerance
    abs_tol : float, optional
        Absolute tolerance
    ignore_spaces : bool, optional
        Flag to strip whitespace (including newlines) from string columns
    ignore_case : bool, optional
        Flag to ignore the case of string columns

    Returns
    -------
    pandas.Series
        A series of Boolean values.  True == the values match, False == the
        values don't match.
    """
    try:
        compare = pd.Series(
            np.isclose(col_1, col_2, rtol=rel_tol, atol=abs_tol, equal_nan=True)
        )
    except TypeError:
        try:
            compare = pd.Series(
                np.isclose(
                    col_1.astype(float),
                    col_2.astype(float),
                    rtol=rel_tol,
                    atol=abs_tol,
                    equal_nan=True,
                )
            )
        except (ValueError, TypeError):
            try:
                if ignore_spaces:
                    if col_1.dtype.kind == "O":
                        col_1 = col_1.str.strip()
                    if col_2.dtype.kind == "O":
                        col_2 = col_2.str.strip()

                if ignore_case:
                    if col_1.dtype.kind == "O":
                        col_1 = col_1.str.upper()
                    if col_2.dtype.kind == "O":
                        col_2 = col_2.str.upper()

                if {col_1.dtype.kind, col_2.dtype.kind} == {"M", "O"}:
                    compare = compare_string_and_date_columns(col_1, col_2)
                else:
                    compare = pd.Series(
                        (col_1 == col_2) | (col_1.isnull() & col_2.isnull())
                    )
            except:
                # Blanket exception should just return all False
                compare = pd.Series(False, index=col_1.index)
    compare.index = col_1.index
    return compare


def compare_string_and_date_columns(col_1, col_2):
    """Compare a string column and date column, value-wise.  This tries to
    convert a string column to a date column and compare that way.

    Parameters
    ----------
    col_1 : Pandas.Series
        The first column to look at
    col_2 : Pandas.Series
        The second column

    Returns
    -------
    pandas.Series
        A series of Boolean values.  True == the values match, False == the
        values don't match.
    """
    if col_1.dtype.kind == "O":
        obj_column = col_1
        date_column = col_2
    else:
        obj_column = col_2
        date_column = col_1

    try:
        return pd.Series(
            (pd.to_datetime(obj_column) == date_column)
            | (obj_column.isnull() & date_column.isnull())
        )
    except:
        return pd.Series(False, index=col_1.index)


def get_merged_columns(original_df, merged_df, suffix):
    """Gets the columns from an original dataframe, in the new merged dataframe

    Parameters
    ----------
    original_df : Pandas.DataFrame
        The original, pre-merge dataframe
    merged_df : Pandas.DataFrame
        Post-merge with another dataframe, with suffixes added in.
    suffix : str
        What suffix was used to distinguish when the original dataframe was
        overlapping with the other merged dataframe.
    """
    columns = []
    for col in original_df.columns:
        if col in merged_df.columns:
            columns.append(col)
        elif col + suffix in merged_df.columns:
            columns.append(col + suffix)
        else:
            raise ValueError("Column not found: %s", col)
    return columns


def temp_column_name(*dataframes):
    """Gets a temp column name that isn't included in columns of any dataframes

    Parameters
    ----------
    dataframes : list of Pandas.DataFrame
        The DataFrames to create a temporary column name for

    Returns
    -------
    str
        String column name that looks like '_temp_x' for some integer x
    """
    i = 0
    while True:
        temp_column = f"_temp_{i}"
        unique = True
        for dataframe in dataframes:
            if temp_column in dataframe.columns:
                i += 1
                unique = False
        if unique:
            return temp_column


def calculate_max_diff(col_1, col_2):
    """Get a maximum difference between two columns

    Parameters
    ----------
    col_1 : Pandas.Series
        The first column
    col_2 : Pandas.Series
        The second column

    Returns
    -------
    Numeric
        Numeric field, or zero.
    """
    try:
        return (col_1.astype(float) - col_2.astype(float)).abs().max()
    except:
        return 0


def generate_id_within_group(dataframe, join_columns):
    """Generate an ID column that can be used to deduplicate identical rows.  The series generated
    is the order within a unique group, and it handles nulls.

    Parameters
    ----------
    dataframe : Pandas.DataFrame
        The dataframe to operate on
    join_columns : list
        List of strings which are the join columns

    Returns
    -------
    Pandas.Series
        The ID column that's unique in each group.
    """
    default_value = "DATACOMPY_NULL"
    if dataframe[join_columns].isnull().any().any():
        if (dataframe[join_columns] == default_value).any().any():
            raise ValueError(f"{default_value} was found in your join columns")
        return (
            dataframe[join_columns]
            .astype(str)
            .fillna(default_value)
            .groupby(join_columns)
            .cumcount()
        )
    else:
        return dataframe[join_columns].groupby(join_columns).cumcount()
