import pandas as pd
import pyreadstat
import io
import numpy as np
import zipfile
import re
import os
from fastapi import UploadFile
from colorama import Fore, Back, Style



class APDataConverter:

    def __init__(self, files: list[UploadFile] = None, file_name: str = '', is_qme: bool = True):

        self.lstDrop = [
            'Approve',
            'Reject',
            'Re - do request', 'Re-do request',
            'Reason to reject',
            'Memo',
            'No.',
            'Date',
            'Country',
            'Channel',
            'Chain / Type',
            'Distributor',
            'Method',
            'Panel FB',
            'Panel Email',
            'Panel Phone',
            'Panel Age',
            'Panel Gender',
            'Panel Area',
            'Panel Income',
            'Login ID',
            'User name',
            'Store ID',
            'Store Code',
            'Store name',
            'Store level',
            'District',
            'Ward',
            'Store address',
            'Area group',
            'Store ranking',
            'Region 2',
            'Nhóm cửa hàng',
            'Nhà phân phối',
            'Manager',
            'Telephone number',
            'Contact person',
            'Email',
            'Others 1',
            'Others 2',
            'Others 3',
            'Others 4',
            'Check in',
            'Store Latitude',
            'Store Longitude',
            'User Latitude',
            'User Longitude',
            'Check out',
            'Distance',
            'Task duration',
            'Panel ID',
            'InterviewerID',
            'InterviewerName',
            'RespondentName',
            'Edited',
            'Edited by',
            'Edited ratio',
            'Verify Status',
            'Images',
            'PVV',
            'Name',
            'Phone_number',
            'Q_Name',
            'Q_SDT',
            'Q_GT',
            'Tenpvv',
            'Infor',
            'Infor_1',
            'Infor_2',
            'infor',
            'infor_1',
            'infor_2',
            'InvitorName',
            'Phone',
            'RespondentAddress',
            'Respondent_name',
            'Respondent_info_1',
            'Respondent_info_2',
            'Respondent_NextSurvey',
            'Respondent_Channel',
            'RespondentPhonenumber',
            'ResName',
            'ResPhone',
            'ResAdd',
            'ResAdd_1',
            'ResAdd_2',
            'ResAdd_3',
            'ResDistrictHCM',
            'ResDistrictHN',
            'B2B_reward',
            'Company_Name',
            'Company_tax_number',
            'Company_tax_number_o3',
            'Phone_DV',
            'RespondentPhone',
            'PVV_Name',
            'Invite',
            'Interviewer_Name',
            'Address',
        ]

        # Input vars
        self.is_qme = is_qme

        if file_name:
            data_file = open(file_name, 'rb')
            file = UploadFile(file=data_file, filename=file_name)
            self.upload_files = [file]
        else:
            self.upload_files = files


        # Output vars
        self.str_file_name = str()
        self.zip_name = str()
        self.df_data_converted, self.df_info_converted = pd.DataFrame(), pd.DataFrame()


    def check_duplicate_variables(self) -> list:

        dup_vars = self.df_info_converted.duplicated(subset=['Name of items'])

        lst_dup_vars = list()
        if dup_vars.any():
            lst_dup_vars = self.df_info_converted.loc[dup_vars, 'Name of items'].values.tolist()
            print(Fore.RED, 'Please check duplicated variables:', ', '.join(lst_dup_vars))

        return lst_dup_vars


    def read_file_xlsx(self, file, is_qme: bool) -> (pd.DataFrame, pd.DataFrame):

        print(f'Read file "{file.filename}"')

        xlsx = io.BytesIO(file.file.read())

        if is_qme:

            df_data = pd.read_excel(xlsx, sheet_name='Data')

            df_data_header = df_data.iloc[[3, 4, 5], :].copy().T
            df_data_header.loc[((pd.isnull(df_data_header[3])) & (df_data_header[5] == 'Images')), 3] = ['Images']
            # df_data_header[3].fillna(method='ffill', inplace=True)

            df_data_header[3].ffill(inplace=True)

            df_temp = df_data_header.loc[
                      (df_data_header[3].duplicated(keep=False)) & ~(pd.isnull(df_data_header[3])) & ~(
                          pd.isnull(df_data_header[4])), :].copy()

            for idx in df_temp.index:
                df_data_header.at[idx, 3] = f"{df_data_header.at[idx, 3]}_{df_data_header.at[idx, 4].rsplit('_', 1)[1]}"

            df_data_header.loc[pd.isnull(df_data_header[3]), 3] = df_data_header.loc[pd.isnull(df_data_header[3]), 5]
            dict_header = df_data_header[3].to_dict()
            df_data.rename(columns=dict_header, inplace=True)
            df_data.drop(list(range(6)), inplace=True)
            set_drop = set(dict_header.values()).intersection(set(self.lstDrop))
            df_data.drop(columns=list(set_drop), inplace=True, axis=1)

            df_qres = pd.read_excel(xlsx, sheet_name='Question')
            df_qres.replace({np.nan: None}, inplace=True)

        else:
            df_data = pd.read_excel(xlsx, sheet_name='Rawdata')
            df_qres = pd.read_excel(xlsx, sheet_name='Datamap')

        df_data.reset_index(drop=True, inplace=True)
        df_qres.reset_index(drop=True, inplace=True)

        return df_data, df_qres


    @staticmethod
    def read_file_sav(file) -> (pd.DataFrame, pd.DataFrame):

        print('Read file sav')

        # PENDING - NOT YET COMPLETED

        file_location = f"{file.filename}"
        with open(file_location, "wb+") as file_object:
            file_object.write(file.file.read())

        df_data_output, meta = pyreadstat.read_sav(file.filename)
        os.remove(file.filename)

        # ['var_name', 'var_lbl', 'var_type', 'val_lbl']
        # arr = np.array(df_data_output.columns)
        # arr = arr.T

        df_info_output = pd.DataFrame(columns=['var_name'], data=np.array(df_data_output.columns))
        df_info_output.index = df_data_output.columns

        # column_names_to_labels
        # readstat_variable_types
        # variable_value_labels
        df_info_output = pd.concat([df_info_output, pd.DataFrame.from_dict(meta.column_names_to_labels, orient='index', columns=['var_lbl'])], axis=1)

        return df_data_output, df_info_output


    def convert_upload_files_to_df_converted(self):

        files = self.upload_files
        is_qme = self.is_qme

        if len(files) == 1:
            file = files[0]
            self.str_file_name = file.filename

            if '.sav' in file.filename:
                # this function is pending
                self.df_data_converted, self.df_info_converted = self.read_file_sav(file)
                self.zip_name = file.filename.replace('.sav', '_Data.zip')
            else:
                self.df_data_converted, self.df_info_converted = self.read_file_xlsx(file, is_qme)
                self.zip_name = file.filename.replace('.xlsx', '_Data.zip')

        else:
            self.str_file_name = f"{files[0].filename.rsplit('_', 1)[0]}.xlsx"
            self.zip_name = self.str_file_name.replace('.xlsx', '_Data.zip')

            df_data_converted_merge = pd.DataFrame()
            df_info_converted_merge = pd.DataFrame()

            for i, file in enumerate(files):
                df_data_converted, df_info_converted = self.read_file_xlsx(file, is_qme)

                if not df_data_converted.empty:
                    df_data_converted_merge = pd.concat([df_data_converted_merge, df_data_converted], axis=0)

                if df_info_converted_merge.empty:
                    df_info_converted_merge = df_info_converted

            df_data_converted_merge.reset_index(drop=True, inplace=True)

            self.df_data_converted, self.df_info_converted = df_data_converted_merge, df_info_converted_merge

        print(f'Convert uploaded files "{self.str_file_name}" to dataframe')

        if self.check_duplicate_variables():
            exit()



    @staticmethod
    def cleanhtml(raw_html) -> str:

        if isinstance(raw_html, str):
            CLEANR = re.compile('{.*?}|<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});|\n|\xa0')
            cleantext = re.sub(CLEANR, '', raw_html)
            return cleantext

        return raw_html


    def convert_df_md(self) -> (pd.DataFrame, pd.DataFrame):

        self.convert_upload_files_to_df_converted()

        print('Convert to MD dataframe')

        df_data, df_info = self.df_data_converted, self.df_info_converted

        dictQres = dict()
        for idx in df_info.index:

            strMatrix = '' if df_info.loc[idx, 'Question(Matrix)'] is None else f"{df_info.loc[idx, 'Question(Matrix)']}_"
            strNormal = df_info.loc[idx, 'Question(Normal)'] if strMatrix == '' else f"{strMatrix}{df_info.loc[idx, 'Question(Normal)']}"
            strQreName = str(df_info.loc[idx, 'Name of items'])
            strQreName = strQreName.replace('Rank_', 'Rank') if 'Rank_' in strQreName else strQreName

            dictQres[strQreName] = {
                'type': df_info.loc[idx, 'Question type'],
                'label': f'{strNormal}',
                'isMatrix': True if strMatrix != '' else False,
                'cats': {}
            }

            lstHeaderCol = list(df_info.columns)
            lstHeaderCol.remove('Name of items')
            lstHeaderCol.remove('Question type')
            lstHeaderCol.remove('Question(Matrix)')
            lstHeaderCol.remove('Question(Normal)')

            for col in lstHeaderCol:
                if df_info.loc[idx, col] is not None and len(str(df_info.loc[idx, col])) > 0:
                    dictQres[strQreName]['cats'].update({str(col): self.cleanhtml(str(df_info.loc[idx, col]))})

        lstMatrixHeader = list()
        for k in dictQres.keys():
            if dictQres[k]['isMatrix'] and dictQres[k]['type'] == 'MA' and len(dictQres[k]['cats'].keys()):
                lstMatrixHeader.append(k)

        if len(lstMatrixHeader):
            for i in lstMatrixHeader:
                for code in dictQres[i]['cats'].keys():
                    lstLblMatrixMA = dictQres[f'{i}_{code}']['label'].split('_')
                    dictQres[f'{i}_{code}']['cats'].update({'1': self.cleanhtml(lstLblMatrixMA[1])})
                    dictQres[f'{i}_{code}']['label'] = f"{dictQres[i]['label']}_{lstLblMatrixMA[1]}"

        df_data_output, df_info_output = df_data, pd.DataFrame(data=[['ID', 'ID', 'FT', {}]], columns=['var_name', 'var_lbl', 'var_type', 'val_lbl'])

        for qre, qre_info in dictQres.items():

            if qre in df_data_output.columns:
                arr_row = [qre, self.cleanhtml(qre_info['label']), f"{qre_info['type']}_mtr" if qre_info['isMatrix'] else qre_info['type'], qre_info['cats']]
                df_info_output = pd.concat([df_info_output, pd.DataFrame(data=[arr_row], columns=['var_name', 'var_lbl', 'var_type', 'val_lbl'])])


        df_data_output.replace({None: np.nan}, inplace=True)
        df_info_output.reset_index(drop=True, inplace=True)

        df_data_output, df_info_output = self.auto_convert_ft_to_float(df_data_output, df_info_output)

        return df_data_output, df_info_output


    def convert_df_mc(self, lst_new_row: list = None) -> (pd.DataFrame, pd.DataFrame):
        """
        Convert data with MA questions format by columns instead of code
        """

        self.convert_upload_files_to_df_converted()

        print('Convert to MC dataframe')

        df_data, df_info = self.df_data_converted, self.df_info_converted

        if lst_new_row:
            df_info = pd.concat([df_info, pd.DataFrame(
                columns=df_info.columns,
                data=lst_new_row,
            )], axis=0)
            df_info.reset_index(drop=True, inplace=True)

        df_data.replace({None: np.nan}, inplace=True)

        lstFullCodelist = list(df_info.columns)
        lstFullCodelist.remove('Name of items')
        lstFullCodelist.remove('Question type')
        lstFullCodelist.remove('Question(Matrix)')
        lstFullCodelist.remove('Question(Normal)')

        dictQres = dict()
        for idx in df_info.index:

            strQreName = str(df_info.loc[idx, 'Name of items'])
            strQreName = strQreName.replace('Rank_', 'Rank') if 'Rank_' in strQreName else strQreName
            strQreType = df_info.loc[idx, 'Question type']
            isMatrix = False if df_info.loc[idx, 'Question(Matrix)'] is None else True
            strMatrix = '' if df_info.loc[idx, 'Question(Matrix)'] is None else self.cleanhtml(f"{df_info.loc[idx, 'Question(Matrix)']}")
            strNormal = '' if df_info.loc[idx, 'Question(Normal)'] is None else self.cleanhtml(f"{df_info.loc[idx, 'Question(Normal)']}")

            if strQreName not in dictQres.keys():

                if strQreType == 'MA':

                    if isMatrix:

                        ser_codelist = df_info.loc[idx, lstFullCodelist]
                        ser_codelist.dropna(inplace=True)
                        dict_codelist = ser_codelist.to_dict()

                        if not ser_codelist.empty:
                            dictQres[strQreName] = {
                                'type': strQreType,
                                'label': f'{strMatrix}_{strNormal}' if isMatrix else strNormal,
                                'isMatrix': isMatrix,
                                'MA_Matrix_Header': strQreName,
                                'MA_cols': [f'{strQreName}_{k}' for k in dict_codelist.keys()],
                                'cats': {str(k): self.cleanhtml(v) for k, v in dict_codelist.items()},
                            }
                    else:

                        maName, maCode = strQreName.rsplit('_', 1)
                        maLbl = self.cleanhtml(df_info.at[idx, 1])

                        if maName not in dictQres.keys():

                            dictQres[maName] = {
                                'type': strQreType,
                                'label': strNormal,
                                'isMatrix': isMatrix,
                                'MA_cols': [strQreName],
                                'cats': {str(maCode): maLbl}
                            }

                        else:

                            dict_qre = dictQres[maName]
                            dict_qre['MA_cols'].append(strQreName)
                            dict_qre['cats'].update({str(maCode): maLbl})


                else:  # ['SA', 'RANKING', 'FT']

                    dictQres[strQreName] = {
                        'type': strQreType,
                        'label': str(),
                        'isMatrix': isMatrix,
                        'cats': dict(),
                    }

                    dict_qre = dictQres[strQreName]
                    dict_qre['label'] = f'{strMatrix}_{strNormal}' if isMatrix else strNormal

                    if strQreType in ['SA', 'RANKING']:
                        ser_codelist = df_info.loc[idx, lstFullCodelist]
                        ser_codelist.dropna(inplace=True)
                        dict_qre['cats'] = {str(k): self.cleanhtml(v) for k, v in ser_codelist.to_dict().items()}

        df_data_output = df_data.loc[:, ['ID']].copy()

        df_info_output = pd.DataFrame(data=[['ID', 'ID', 'FT', {}]], columns=['var_name', 'var_lbl', 'var_type', 'val_lbl'])

        for qre, qre_info in dictQres.items():

            if qre_info['type'] == 'MA':

                dfMA = df_data.loc[:, qre_info['MA_cols']]

                for col_name in qre_info['MA_cols']:
                    maName, maCode = col_name.rsplit('_', 1)
                    dfMA[col_name].replace({1: int(maCode)}, inplace=True)

                dfMA['combined'] = [[e for e in row if e == e] for row in dfMA[qre_info['MA_cols']].values.tolist()]
                dfMA = pd.DataFrame(dfMA['combined'].tolist(), index=dfMA.index)

                for i, col_name in enumerate(qre_info['MA_cols']):

                    if i in list(dfMA.columns):
                        dfColMA = dfMA[i].to_frame()
                        dfColMA.rename(columns={i: col_name}, inplace=True)
                    else:
                        dfColMA = pd.DataFrame([np.nan] * dfMA.shape[0], columns=[col_name])

                    df_data_output = pd.concat([df_data_output, dfColMA], axis=1)
                    dfInfoRow = pd.DataFrame([[col_name, qre_info['label'], 'MA_mtr' if qre_info['isMatrix'] else 'MA', qre_info['cats']]], columns=['var_name', 'var_lbl', 'var_type', 'val_lbl'])
                    df_info_output = pd.concat([df_info_output, dfInfoRow], axis=0)

            else:
                if qre in df_data.columns:
                    df_data_output = pd.concat([df_data_output, df_data[qre]], axis=1)
                    dfInfoRow = pd.DataFrame([[qre, qre_info['label'], f"{qre_info['type']}_mtr" if qre_info['isMatrix'] else qre_info['type'], qre_info['cats']]], columns=['var_name', 'var_lbl', 'var_type', 'val_lbl'])
                    df_info_output = pd.concat([df_info_output, dfInfoRow], axis=0)

        # dfQreInfo.set_index('var_name', inplace=True)
        df_info_output.reset_index(drop=True, inplace=True)

        df_data_output, df_info_output = self.auto_convert_ft_to_float(df_data_output, df_info_output)

        return df_data_output, df_info_output


    @staticmethod
    def generate_sps(df_info: pd.DataFrame, is_md: bool, sps_name: str):

        if is_md:
            temp = """
                *{0}.
                MRSETS
                /MDGROUP NAME=${1}
                    LABEL='{2}'
                    CATEGORYLABELS=COUNTEDVALUES 
                    VARIABLES={3}
                    VALUE=1
                /DISPLAY NAME=[${4}].
                """
        else:
            temp = """
                *{0}.
                MRSETS
                /MCGROUP NAME=${1}
                    LABEL='{2}' 
                    VARIABLES={3}
                /DISPLAY NAME=[${4}].
                """

        df_qres_ma = df_info.loc[(df_info['var_type'].str.contains('MA')), :].copy()

        lst_ignore_col = list()

        dict_ma_cols = dict()
        for idx in df_qres_ma.index:

            ma_name = df_qres_ma.at[idx, 'var_name'].rsplit('_', 1)[0]

            if ma_name in lst_ignore_col:
                dict_ma_cols[ma_name]['vars'].append(df_qres_ma.at[idx, 'var_name'])
            else:
                lst_ignore_col.append(ma_name)

                dict_ma_cols[ma_name] = {
                    'name': ma_name,
                    'lbl': df_qres_ma.at[idx, 'var_lbl'],
                    'vars': [df_qres_ma.at[idx, 'var_name']],
                }

        str_MRSet = '.'
        for key, val in dict_ma_cols.items():
            str_MRSet += temp.format(key, val['name'], val['lbl'], ' '.join(val['vars']), val['name'])

        with open(f'{sps_name}', 'w', encoding='utf-8-sig') as text_file:
            text_file.write(str_MRSet)


    @staticmethod
    def unnetted_qre_val(dict_netted) -> dict:
        dict_unnetted = dict()

        if 'net_code' not in dict_netted.keys():
            return dict_netted

        for key, val in dict_netted.items():

            if 'net_code' in key:
                val_lbl_lv1 = dict_netted['net_code']

                for net_key, net_val in val_lbl_lv1.items():

                    if isinstance(net_val, str):
                        dict_unnetted.update({str(net_key): net_val})
                    else:
                        dict_unnetted.update(net_val)

            else:
                dict_unnetted.update({str(key): val})

        return dict_unnetted


    def remove_net_code(self, df_info: pd.DataFrame) -> pd.DataFrame():
        df_info_without_net = df_info.copy()

        for idx in df_info_without_net.index:
            val_lbl = df_info_without_net.at[idx, 'val_lbl']

            if 'net_code' in val_lbl.keys():
                df_info_without_net.at[idx, 'val_lbl'] = self.unnetted_qre_val(val_lbl)

        return df_info_without_net


    @staticmethod
    def zipfiles(zip_name: str, lst_file_name: list):
        with zipfile.ZipFile(zip_name, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
            for f_name in lst_file_name:
                zf.write(f_name)
                os.remove(f_name)


    def generate_multiple_data_files(self, dict_dfs: dict, is_md: bool = False, is_export_sav: bool = True, is_export_xlsx: bool = True, is_zip: bool = True):

        lst_zip_file_name = list()

        str_name = self.str_file_name.replace('.xlsx', '')

        xlsx_name = f"{str_name}_Rawdata.xlsx"
        # topline_name = f"{str_name}_Topline.xlsx"

        for key, val in dict_dfs.items():

            str_full_file_name = f"{str_name}_{val['tail_name']}" if val['tail_name'] else str_name
            str_sav_name = f"{str_full_file_name}.sav"
            # str_sps_name = f"{str_full_file_name}.sps"

            df_data = val['data']
            df_info = val['info']

            print('Remove netted codes in df_info')
            df_info = self.remove_net_code(df_info)

            is_recode_to_lbl = val['is_recode_to_lbl']

            if is_export_sav:
                print(f'Create {str_sav_name}')
                dict_val_lbl = {a: {int(k): str(v) for k, v in b.items()} for a, b in zip(df_info['var_name'], df_info['val_lbl'])}
                dict_measure = {a: 'nominal' for a in df_info['var_name']}
                pyreadstat.write_sav(df_data, str_sav_name, column_labels=df_info['var_lbl'].values.tolist(), variable_value_labels=dict_val_lbl, variable_measure=dict_measure)

                # print(f'Create {str_sps_name}')
                # self.generate_sps(df_info, is_md, str_sps_name)
                # lst_zip_file_name.extend([str_sav_name, str_sps_name])

                lst_zip_file_name.extend([str_sav_name])

            if is_export_xlsx:

                df_data_xlsx = df_data.copy()

                if is_recode_to_lbl:
                    df_info_recode = df_info.loc[df_info['val_lbl'] != {}, ['var_name', 'val_lbl']].copy()
                    df_info_recode.set_index('var_name', inplace=True)
                    df_info_recode['val_lbl'] = [{int(cat): lbl for cat, lbl in dict_val.items()} for dict_val in df_info_recode['val_lbl']]

                    dict_recode = df_info_recode.loc[:, 'val_lbl'].to_dict()
                    df_data_xlsx.replace(dict_recode, inplace=True)

                print(f"Create {xlsx_name} - sheet {val['sheet_name']}")

                with pd.ExcelWriter(xlsx_name, engine="openpyxl", mode="a" if os.path.isfile(xlsx_name) else "w") as writer:

                    wb = writer.book
                    ws_data_name = f"{val['sheet_name']}_Rawdata" if val['sheet_name'] else "Rawdata"
                    ws_info_name = f"{val['sheet_name']}_Datamap" if val['sheet_name'] else "Datamap"

                    try:
                        print(f'Check sheets existing and remove - {ws_data_name} & {ws_info_name}')
                        wb.remove(wb[ws_data_name])
                        wb.remove(wb[ws_info_name])

                    except Exception:
                        print('There is no sheet existing')

                    finally:
                        print(f'Create sheets - {ws_data_name} & {ws_info_name}')
                        df_data_xlsx.to_excel(writer, sheet_name=ws_data_name, index=False)
                        df_info.to_excel(writer, sheet_name=ws_info_name, index=False)

                if xlsx_name not in lst_zip_file_name:
                    lst_zip_file_name.extend([xlsx_name])

        if is_zip:
            print(f'Create {self.zip_name} with files: {", ".join(lst_zip_file_name)}')
            self.zipfiles(self.zip_name, lst_zip_file_name)



    @staticmethod
    def auto_convert_ft_to_float(df_data: pd.DataFrame, df_info: pd.DataFrame) -> (pd.DataFrame, pd.DataFrame):

        df_info_fil = df_info.query("var_type == 'FT' & var_name != 'ID' & not var_name.str.contains('_o')")

        for col_name in df_info_fil['var_name'].values.tolist():
            try:
                df_data[col_name] = pd.to_numeric(df_data[col_name], downcast='float')
                print(f'Convert {col_name} from FT to NUM type')
            except Exception:
                print(f'Cannot convert {col_name} from FT to NUM type')
                continue

        return df_data, df_info





