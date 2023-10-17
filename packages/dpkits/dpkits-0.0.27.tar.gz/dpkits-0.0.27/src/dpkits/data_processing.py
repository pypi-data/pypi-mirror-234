import pandas as pd
import numpy as np



class DataProcessing:

    @staticmethod
    def add_qres(df_data: pd.DataFrame, df_info: pd.DataFrame, dict_add_new_qres: dict) -> (pd.DataFrame, pd.DataFrame):
        info_col_name = ['var_name', 'var_lbl', 'var_type', 'val_lbl']

        for key, val in dict_add_new_qres.items():

            if val[1] in ['MA']:
                qre_ma_name, max_col = str(key).rsplit('|', 1)

                for i in range(1, int(max_col) + 1):
                    df_info = pd.concat([df_info, pd.DataFrame(columns=info_col_name, data=[[f'{qre_ma_name}_{i}', val[0], val[1], val[2]]])], axis=0, ignore_index=True)
                    df_data = pd.concat([df_data, pd.DataFrame(columns=[f'{qre_ma_name}_{i}'], data=[val[-1]] * df_data.shape[0])], axis=1)

            else:
                df_info = pd.concat([df_info, pd.DataFrame(columns=info_col_name, data=[[key, val[0], val[1], val[2]]])], axis=0, ignore_index=True)
                df_data = pd.concat([df_data, pd.DataFrame(columns=[key], data=[val[-1]] * df_data.shape[0])], axis=1)

        df_data.reset_index(drop=True, inplace=True)
        df_info.reset_index(drop=True, inplace=True)

        return df_data, df_info

