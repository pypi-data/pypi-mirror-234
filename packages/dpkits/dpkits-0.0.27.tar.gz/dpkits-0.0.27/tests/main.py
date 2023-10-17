import pandas as pd
import numpy as np

# from dpkits.ap_data_converter import APDataConverter
# from dpkits.data_processing import DataProcessing
# from dpkits.data_transpose import DataTranspose
# from dpkits.table_generator import DataTableGenerator
# from dpkits.table_formater import TableFormatter
# from dpkits.calculate_lsm import LSMCalculation


# IGNORE THIS-----------------------------------------------------------------------------------------------------------
import sys
sys.path.insert(0, 'C:/Users/PC/OneDrive/Dev Area/PyPackages/packaging_dpkits/src/dpkits')

from ap_data_converter import APDataConverter
from data_processing import DataProcessing
from data_transpose import DataTranspose
from table_generator import DataTableGenerator
from table_formater import TableFormatter
from codeframe_reader import CodeframeReader
from calculate_lsm import LSMCalculation
# IGNORE THIS-----------------------------------------------------------------------------------------------------------



# Define input/output files name
str_file_name = 'VN8413_Data'
str_tbl_file_name = f'{str_file_name}_Topline.xlsx'


# Call Class APDataConverter with file_name
converter = APDataConverter(file_name=f'{str_file_name}.xlsx')

converter.lstDrop.extend(['DV'])

"""
README: Convert input file to dataframe

- df_data: contains data as pandas dataframe
- df_info: contains data info as pandas dataframe (ex: var_name, var_lbl, var_type, val_lbl)
    - var_name = data column name (variable)
    - var_lbl = variable label
    - var_type = variable type
    - val_lbl = value label
"""


df_data, df_info = converter.convert_df_mc()  # Use 'converter.convert_df_md()' if you need md data

# LSM 6 CALCULATION - Only use for Unilever projects which have LSM questions
# df_data, df_info = LSMCalculation.cal_lsm_6(df_data, df_info)

df_data = pd.DataFrame(df_data)
df_info = pd.DataFrame(df_info)

# AFTER CONVERTING YOU CAN DO ANYTHING WITH DATAFRAME-------------------------------------------------------------------
# df_info columns must be ['var_name', 'var_lbl', 'var_type', 'val_lbl']

dict_add_new_qres = {
    'Ma_SP_1': ['Mã SP', 'SA', {'1': 'Concept 1', '2': 'Concept 2', '3': 'Concept 3'}, 1],
    'Ma_SP_2': ['Mã SP', 'SA', {'1': 'Concept 1', '2': 'Concept 2', '3': 'Concept 3'}, 2],
    'Ma_SP_3': ['Mã SP', 'SA', {'1': 'Concept 1', '2': 'Concept 2', '3': 'Concept 3'}, 3],

    'New_FT': ['New FT', 'FT', {}, np.nan],
    'New_Num': ['New Num', 'NUM', {}, np.nan],
    'New_MA|6': ['New MA', 'MA', {'1': '1', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7'}, np.nan],
}

df_data, df_info = DataProcessing.add_qres(df_data, df_info, dict_add_new_qres)
df_data = pd.DataFrame(df_data)
df_info = pd.DataFrame(df_info)







# Just for checking
with pd.ExcelWriter(f'{str_file_name}_preview.xlsx', engine="openpyxl") as writer:
    df_data.to_excel(writer, sheet_name='df_data')
    df_info.to_excel(writer, sheet_name='df_info')


# TRANSPOSE TO STACK----------------------------------------------------------------------------------------------------
lst_scr = [
    'S1',
    'S2',
    'S3_a',
    'S3_b',
    'S4',
    'S5',
    'S6_1',
    'S6_2',
    'S6_3',
    'S6_4',
    'S6_5',
    'S6_6',
    'S7',
    'S8',
    'S10',
]

lst_fc = ['F1_ByProdCode']

dict_stack_structure = {
    'id_col': 'ID',
    'sp_col': 'Ma_SP',
    'lst_scr': lst_scr,
    'dict_sp': {
        1: {
            'Ma_SP_1': 'Ma_SP',
            'Q1_1': 'Q1',
            'Q2_1': 'Q2',
            'Q3_1': 'Q3',
            'Q4_1': 'Q4',
            'Q5_1': 'Q5',
            'Q9_1': 'Q9',
            'Q6_1': 'Q6',
            'Q7_1': 'Q7',
            'Q8_1': 'Q8',
            'Q10_1': 'Q10',
            'F1_YN_1': 'F1_YN_New',
            'F2_OE_1': 'F2_OE_New',
        },
        2: {
            'Ma_SP_2': 'Ma_SP',
            'Q1_2': 'Q1',
            'Q2_2': 'Q2',
            'Q3_2': 'Q3',
            'Q4_2': 'Q4',
            'Q5_2': 'Q5',
            'Q9_2': 'Q9',
            'Q6_2': 'Q6',
            'Q7_2': 'Q7',
            'Q8_2': 'Q8',
            'Q10_2': 'Q10',
            'F1_YN_2': 'F1_YN_New',
            'F2_OE_2': 'F2_OE_New',
        },
        3: {
            'Ma_SP_3': 'Ma_SP',
            'Q1_3': 'Q1',
            'Q2_3': 'Q2',
            'Q3_3': 'Q3',
            'Q4_3': 'Q4',
            'Q5_3': 'Q5',
            'Q9_3': 'Q9',
            'Q6_3': 'Q6',
            'Q7_3': 'Q7',
            'Q8_3': 'Q8',
            'Q10_3': 'Q10',
            'F1_YN_3': 'F1_YN_New',
            'F2_OE_3': 'F2_OE_New',
        },
    },
    'lst_fc': lst_fc
}

df_data_stack, df_info_stack = DataTranspose.to_stack(df_data, df_info, dict_stack_structure)




# TRANSPOSE TO UNSTACK--------------------------------------------------------------------------------------------------
dict_unstack_structure = {
    'id_col': 'ID',
    'sp_col': 'Ma_SP',
    'lst_col_part_head': lst_fc,
    'lst_col_part_body': [
        'Ma_SP',
        'Q1',
        'Q2',
        'Q3',
        'Q4',
        'Q5',
        'Q9',
        'Q6',
        'Q7',
        'Q8',
        'Q10',
        'F1_YN_New',
        'F2_OE_New',
    ],
    'lst_col_part_tail': lst_fc
}

df_data_unstack, df_info_unstack = DataTranspose.to_unstack(df_data_stack, df_info_stack, dict_unstack_structure)


# ----------------------------------------------------------------------------------------------------------------------
# OE RUNNING------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# NOT YET START

cfr = CodeframeReader(cf_file_name='VN8413_Codeframe.xlsm')

cfr.to_dataframe_file()

df_data_stack, df_info_stack = DataProcessing.add_qres(df_data_stack, df_info_stack, cfr.dict_add_new_qres_oe)
df_data_stack, df_info_stack = pd.DataFrame(df_data_stack), pd.DataFrame(df_info_stack)

df_coding = pd.DataFrame(cfr.df_full_oe_coding)

df_coding[['ID', 'Ma_SP']] = df_coding['RESPONDENTID'].str.rsplit('_', n=1, expand=True)
df_coding.drop(columns=['RESPONDENTID'], inplace=True)

df_data_stack['Ma_SP'] = df_data_stack['Ma_SP'].astype(int)
df_coding['Ma_SP'] = df_coding['Ma_SP'].astype(int)

lst_drop = df_coding.columns.tolist()
lst_drop.remove('ID')
lst_drop.remove('Ma_SP')

df_data_stack.drop(columns=lst_drop, inplace=True)

df_data_stack = df_data_stack.merge(df_coding, how='left', on=['ID', 'Ma_SP'])

for i in lst_drop:
    df_data_stack[i].replace({99999: np.nan}, inplace=True)



# ----------------------------------------------------------------------------------------------------------------------
# EXPORT SAV DATA FILES-------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
dict_dfs = {
    1: {
        'data': df_data,
        'info': df_info,
        'tail_name': 'ByCode',
        'sheet_name': 'ByCode',
        'is_recode_to_lbl': False,
    },
    2: {
        'data': df_data_stack,
        'info': df_info_stack,
        'tail_name': 'Stack',
        'sheet_name': 'Stack',
        'is_recode_to_lbl': False,
    },
    3: {
        'data': df_data_unstack,
        'info': df_info_unstack,
        'tail_name': 'Unstack',
        'sheet_name': 'Unstack',
        'is_recode_to_lbl': False,
    },
}

converter.generate_multiple_data_files(dict_dfs=dict_dfs, is_zip=False, is_export_sav=False)


# ----------------------------------------------------------------------------------------------------------------------
# EXPORT DATA TABLES----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
"""
README:
    - Side question properties:
    {
        "qre_name": "$Q15",  # column name, must set '$' if it is MA question
        "qre_lbl": "{lbl}: new label",  # default df_info label, input {lbl} top keep original label and addin new label
        "qre_filter": "Age.isin([2, 3])",  # use for filter question
        "sort": "des", # sort options: acs / des
        "mean": {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}  # calculate mean base on dict: key == code in data, value = weighted values
        "cats": {  # use for define net/combine code with specify format
            'net_code': {
                '900001|combine|Group 1 + 2': {
                    '1': 'Yellow/dull teeth',
                    '2': 'Sensitive teeth',
                    '3': 'Dental plaque',
                    '4': 'Caries',
                },
                '900002|net|Group 1': {
                    '1': 'Yellow/dull teeth',
                    '2': 'Sensitive teeth',
                },
                '900003|net|Group 2': {
                    '3': 'Dental plaque',
                    '4': 'Caries',
                },
            },
            '8': 'Other (specify)',
            '9': 'No problem',
        }
    },

    - Header question properties:
    {
        "qre_name": "S1",  # define 'S1' if SA, '$S1' if MA, '@S1_xxx' if create header base on specify condition
        "qre_lbl": "City",  # typing every label is fine
        "cats":
            # SA/MA: define category list base on df_info, use 'TOTAL' if need to display total column
            {
                "TOTAL": "TOTAL",
                '3': 'Hồ Chí Minh',
                '4': 'Cần Thơ'

            }
            # @: define header base on specify condition
            {
                "S3_b.isin([2])": "<=30 (22-30 tuổi)",
                "S3_b.isin([3, 4])": ">30 (31-39 tuổi)",
            }
    },

    - Table properties:
        + key: table key name
        + value: table specify properties

        "Main": {
            "tbl_name": "Main",  # display on excel sheet name
            "tbl_filter": "Ma_SP > 0",  # filter of this table
            "is_count": 0,  # 1 for count, 0 for percentage
            "is_pct_sign": 1,  # 1 for display '%' else 0
            "is_hide_oe_zero_cats": 1,  # 1 for hide answers which percentage = 0% at all header columns
            "is_hide_zero_cols": 1,  # 1 for hide header columns which percentage = 0% at all row
            "sig_test_info":  # define significant test
            {
                "sig_type": "rel",  # 'rel' for dependent sig test, 'ind' for independent sig test
                "sig_cols": [],  # define columns to sig, leave it blank if need to sig all columns
                "lst_sig_lvl": [90, 95]  # sig level: maximum 2 levels
            },
            "lst_side_qres": lst_side_main,  # list of side question
            "lst_header_qres": lst_header  # list of header defines
        },

"""


lst_header = [
    # header lvl 1
    [
        {
            "qre_name": "S1",
            "qre_lbl": "City",
            "cats": {
                "TOTAL": "TOTAL",
                '3': 'Hồ Chí Minh',
                '4': 'Cần Thơ'

            }
        },
    ],

    # header lvl 2
    [
        {
            "qre_name": "@S3_b_Group",
            "qre_lbl": "Age",
            "cats": {
                "S3_b > 0": "TOTAL",
                "S3_b.isin([2])": "<=30 (22-30 tuổi)",
                "S3_b.isin([3, 4])": ">30 (31-39 tuổi)",
            }
        },
        {
            "qre_name": "@S4_Class",
            "qre_lbl": "Class",
            "cats": {
                "S4.isin([1, 2])": "A&B (Từ 13,500,000 đến 22,499,000 VND & Trên 22,500,000)",
                "S4.isin([3])": "C (Từ 7,500,000 đến 13,499,000 VND)",
            }
        },
        {
            "qre_name": "@S8_BUMO",
            "qre_lbl": "BUMO",
            "cats": {
                "S8.isin([2])": "Tiger nâu",
                "S8.isin([6, 7, 8])": "Sài Gòn",
                "S8.isin([12, 13, 14])": "Larue",
            }
        },
    ],

    # header lvl 3
    [
        {
            "qre_name": "Ma_SP",
            "qre_lbl": "Mã Concept",
            "cats": {'1': 'Concept 1', '2': 'Concept 2', '3': 'Concept 3'}
        },
    ],
]

lst_side_scr_tagon = [
    {"qre_name": "S1"},
    {"qre_name": "S2"},
    {"qre_name": "S3_b"},
    {"qre_name": "S4"},
    {"qre_name": "S5"},
    {"qre_name": "$S6"},
    {"qre_name": "S7"},
    {"qre_name": "S8"},
    {"qre_name": "S10"},
]



lst_side_main = [
    {"qre_name": "Q1", 'cats': {
        '1': '1 - Hoàn toàn không thích', '2': '2 - Không thích', '3': '3 - Không thích cũng không ghét', '4': '4 - Thích', '5': '5 - Rất thích',
        'net_code': {
            '900001|combine|T2B': {'4': '4', '5': '5'},
            '900002|combine|Medium': {'3': '3'},
            '900003|combine|B2B': {'1': '1', '2': '2'},
        }
    }, "mean": {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}},

    {"qre_name": "Q4", 'cats': {
        '1': 'Hoàn toàn không phù hợp', '2': 'Không phù hợp', '3': 'Hơi không phù hợp', '4': 'Phù hợp', '5': 'Rất Phù hợp',
        'net_code': {
            '900001|combine|T2B': {'4': '4', '5': '5'},
            '900002|combine|Medium': {'3': '3'},
            '900003|combine|B2B': {'1': '1', '2': '2'},
        }
    }, "mean": {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}},

    {"qre_name": "Q5", 'cats': {
        '1': 'Hoàn toàn không mới lạ và khác biệt', '2': 'Không mới lạ và khác biệt', '3': 'Hơi không mới lạ và khác biệt', '4': 'Mới lạ và khác biệt', '5': 'Rất mới lạ và khác biệt',
        'net_code': {
            '900001|combine|T2B': {'4': '4', '5': '5'},
            '900002|combine|Medium': {'3': '3'},
            '900003|combine|B2B': {'1': '1', '2': '2'},
        }
    }, "mean": {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}},

    {"qre_name": "Q9", 'cats': {
        '1': 'Hoàn toàn không cao cấp', '2': 'Không cao cấp', '3': 'Hơi không cao cấp', '4': 'Cao cấp', '5': 'Rất cao cấp',
        'net_code': {
            '900001|combine|T2B': {'4': '4', '5': '5'},
            '900002|combine|Medium': {'3': '3'},
            '900003|combine|B2B': {'1': '1', '2': '2'},
        }
    }, "mean": {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}},

    {"qre_name": "Q6", 'cats': {
        '1': 'Chắc chắn sẽ không mua', '2': 'Không mua', '3': 'Có thể sẽ mua hoặc không', '4': 'Sẽ mua', '5': 'Chắc chắn sẽ mua',
        'net_code': {
            '900001|combine|T2B': {'4': '4', '5': '5'},
            '900002|combine|Medium': {'3': '3'},
            '900003|combine|B2B': {'1': '1', '2': '2'},
        }
    }, "mean": {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}},

    {"qre_name": "Q10", 'cats': {
        '1': 'Chắc chắn sẽ không mua', '2': 'Không mua', '3': 'Có thể sẽ mua hoặc không', '4': 'Sẽ mua', '5': 'Chắc chắn sẽ mua',
        'net_code': {
            '900001|combine|T2B': {'4': '4', '5': '5'},
            '900002|combine|Medium': {'3': '3'},
            '900003|combine|B2B': {'1': '1', '2': '2'},
        },
    }, "mean": {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}},

    {"qre_name": "F1_YN_New"},

]

lst_side_oe = [
    {"qre_name": "$Q2_OE"},
    {"qre_name": "$Q3_OE"},
    {"qre_name": "$Q7_OE"},
    {"qre_name": "$Q8_OE"},
    {"qre_name": "$F2_OE_OE"},
]


lst_func_to_run = [
    # SCREENER
    {
        'func_name': 'run_standard_table_sig',
        'tables_to_run': [
            'Scr_Tagon',
        ],
        'tables_format': {
            "Scr_Tagon": {
                "tbl_name": "Screener",
                "tbl_filter": "S1 > 0",
                "is_count": 0,
                "is_pct_sign": 1,
                "is_hide_oe_zero_cats": 1,
                "is_hide_zero_cols": 1,
                "sig_test_info": {
                    "sig_type": "",
                    "sig_cols": [],
                    "lst_sig_lvl": []
                },
                "lst_side_qres": lst_side_scr_tagon,
                "lst_header_qres": lst_header[:-1]
            },
        },
    },

    # MAIN
    {
        'func_name': 'run_standard_table_sig',
        'tables_to_run': [
            'Main',
            'Main_oe',
        ],
        'tables_format': {

            "Main": {
                "tbl_name": "Main",
                "tbl_filter": "Ma_SP > 0",
                "is_count": 0,
                "is_pct_sign": 1,
                "is_hide_oe_zero_cats": 1,
                "is_hide_zero_cols": 1,
                "sig_test_info": {
                    "sig_type": "rel",
                    "sig_cols": [],
                    "lst_sig_lvl": [90, 95]
                },
                "lst_side_qres": lst_side_main,
                "lst_header_qres": lst_header
            },

            "Main_oe": {
                "tbl_name": "Main_oe",
                "tbl_filter": "Ma_SP > 0",
                "is_count": 0,
                "is_pct_sign": 1,
                "is_hide_oe_zero_cats": 1,
                "is_hide_zero_cols": 1,
                "sig_test_info": {
                    "sig_type": "",
                    "sig_cols": [],
                    "lst_sig_lvl": []
                },
                "lst_side_qres": lst_side_oe,
                "lst_header_qres": lst_header
            },
        },

    },
]

# RUN TABLE FOR SCREENER
dtg = DataTableGenerator(df_data=df_data, df_info=df_info, xlsx_name=str_tbl_file_name)
dtg.run_tables_by_js_files(lst_func_to_run[:1])

# RUN TABLE FOR MAIN
dtg = DataTableGenerator(df_data=df_data_stack, df_info=df_info_stack, xlsx_name=str_tbl_file_name)
dtg.run_tables_by_js_files(lst_func_to_run[1:], is_append=True)




# FORMAT TABLES---------------------------------------------------------------------------------------------------------
dtf = TableFormatter(xlsx_name=str_tbl_file_name)
dtf.format_sig_table()



print('\n==>TESTING PROCESS DONE')

