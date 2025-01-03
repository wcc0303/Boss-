import pandas as pd
import os

# 设置文件夹路径
folder_path_bj2 = 'd:/boss_detail_renli'  # 替换为 bj2 文件夹的路径 
# 获取 bj2 和 bj3 文件夹中的所有 Excel 文件
excel_files_bj2 = [f for f in os.listdir(folder_path_bj2) if f.endswith(('.xlsx', '.xls'))] 

# 初始化一个空的 DataFrame
merged_df = pd.DataFrame()

# 逐个读取 bj2 文件夹中的 Excel 文件并合并
for file in excel_files_bj2:
    file_path = os.path.join(folder_path_bj2, file)  # 获取文件完整路径
    df = pd.read_excel(file_path)  # 读取 Excel 文件
    merged_df = pd.concat([merged_df, df], ignore_index=True)  # 合并 DataFrame

 

# 保存合并后的 DataFrame 到一个新的 Excel 文件
merged_df.to_csv('d:/boss_renli.csv', index=False)
print("合并完成")
