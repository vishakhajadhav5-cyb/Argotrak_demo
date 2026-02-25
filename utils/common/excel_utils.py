import pandas as pd
import os

def table_to_excel(table_data, file_name='Main_Device_List.xlsx', download_path='result/'):
    os.makedirs(download_path, exist_ok=True)
    df = pd.DataFrame(table_data)
    file_path = os.path.join(download_path, file_name)
    df.to_excel(file_path, index=False)
    return file_path
