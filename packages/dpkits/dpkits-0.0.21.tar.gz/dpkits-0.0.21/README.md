# Data processing Package

- Requirements
    - pandas
    - pyreadstat
    - numpy
    - zipfile
    - fastapi[UploadFile]

- Step 1: import classes
    ```
    # Convert data to pandas dataframe
    from dpkits.ap_data_converter import APDataConverter

    # Calculate LSM score
    from dpkits.calculate_lsm import LSMCalculation

    # Transpose data to stack and untack
    from dpkits.data_transpose import DataTranspose

    # Create the tables from converted dataframe 
    from dpkits.table_generator import DataTableGenerator

    # Format data tables 
    from dpkits.table_formater import TableFormatter
    ```

- Step 2: Convert data files to dataframe
    - class APDataConverter(files=None, file_name='', is_qme=True)
        - input 1 of files or file_name
        - files: list[UploadFile] default = None
        - file_name: str default = ''
        - is_qme: bool default = True
        - Returns: 
            - df_data: pandas.Dataframe
            - df_info: pandas.Dataframe
        ```
        converter = APDataConverter(file_name='APDataTesting.xlsx')
        
        df_data, df_info = converter.convert_df_mc() 
        
        # Use 'converter.convert_df_md()' if you need md data
        ```

- Step 3: Calculate LSM classificate (only for LSM projects)
    - class LSMCalculation.cal_lsm_6(df_data, df_info)
        - df_data: pandas.Dataframe
        - df_info: pandas.Dataframe
        - Returns:
            - df_data: pandas.Dataframe
            - df_info: pandas.Dataframe
        ```
        df_data, df_info = LSMCalculation.cal_lsm_6(df_data, df_info)

        # df_data, df_info will contains the columns CC1_Score to CC6_Score & LSM_Score
        ```

- Step 4: Data cleaning (if needed)
```

```

- Step 5: Transpose data (if needed)
```

```

- Step 6: Export *.sav & *.xlsx
```

```

- Step 7: Export data tables
```

```





This is a simple example package. You can use
[Github-flavored Markdown](https://guides.github.com/features/mastering-markdown/)
to write your content.