from DrissionPage import ChromiumOptions, SessionPage, ChromiumPage
import re
import pandas as pd
import json
import time
import random
#薪资转换代码
import pandas as pd
import re
start = 0
end = 20
m=0
def convert_salary_list_to_annual(salary_list):
    """
    Convert a list of salary formats to annual salaries.

    Parameters:
    - salary_list: list of str, the salary strings to convert.

    Returns:
    - annual_salary_list: list of float, the converted annual salaries.
    """

    def convert_to_annual_salary(salary_str):
        """Convert various salary formats to annual salary."""
        if 'K' in salary_str:
            # 解析K薪字符串，提取数字部分
            salary_parts = salary_str.replace('K', '').split('·')
            salary_range = salary_parts[0].split('-')
            # 检查是否有足够的薪资范围
            if len(salary_range) < 2:
                print(f"警告：薪资格式不正确 '{salary_str}'，使用默认值0处理。")
                return 0.0
            min_monthly_salary = float(salary_range[0]) * 1000
            max_monthly_salary = float(salary_range[1]) * 1000
            months_per_year = 12
            if len(salary_parts) > 1:
                salary_years = int(salary_parts[1].replace('薪', ''))
                months_per_year = salary_years
            annual_salary = (min_monthly_salary + max_monthly_salary) / 2 * months_per_year
        elif '元/时' in salary_str:
            hourly_salary_range = salary_str.replace('元/时', '').split('-')
            if len(hourly_salary_range) < 2:
                print(f"警告：薪资格式不正确 '{salary_str}'，使用默认值0处理。")
                return 0.0
            min_hourly_salary = float(hourly_salary_range[0])
            max_hourly_salary = float(hourly_salary_range[1])
            annual_salary = ((min_hourly_salary + max_hourly_salary) / 2) * 8 * 250
        elif '元/天' in salary_str:
            daily_salary_range = salary_str.replace('元/天', '').split('-')
            if len(daily_salary_range) < 2:
                print(f"警告：薪资格式不正确 '{salary_str}'，使用默认值0处理。")
                return 0.0
            min_daily_salary = float(daily_salary_range[0])
            max_daily_salary = float(daily_salary_range[1])
            annual_salary = (min_daily_salary + max_daily_salary) / 2 * 250
        elif '元/月' in salary_str:
            monthly_salary_range = salary_str.replace('元/月', '').split('-')
            if len(monthly_salary_range) < 2:
                print(f"警告：薪资格式不正确 '{salary_str}'，使用默认值0处理。")
                return 0.0
            min_monthly_salary = float(monthly_salary_range[0])
            max_monthly_salary = float(monthly_salary_range[1])
            annual_salary = (min_monthly_salary + max_monthly_salary) / 2 * 12
        elif '元/周' in salary_str:
            weekly_salary_range = salary_str.replace('元/周', '').split('-')
            if len(weekly_salary_range) < 2:
                print(f"警告：薪资格式不正确 '{salary_str}'，使用默认值0处理。")
                return 0.0
            min_weekly_salary = float(weekly_salary_range[0])
            max_weekly_salary = float(weekly_salary_range[1])
            annual_salary = (min_weekly_salary + max_weekly_salary) / 2 * 52
        else:
            try:
                annual_salary = float(salary_str)
            except ValueError:
                print(f"警告：无法解析薪资 '{salary_str}'，使用默认值0处理。")
                return 0.0

        return annual_salary

    # 使用列表推导式转换薪资列表
    annual_salary_list = [convert_to_annual_salary(salary) for salary in salary_list]
    return annual_salary_list





#具体城市代码
def json_read_city():
    # 打开 JSON 文件并读取数据
    c_id = []
    with open('D:\\city_id.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    # 提取省级单位及其编号
    province_list = [[province, list(details.keys())[0]] for province, details in data.items()]
    for i in province_list:
        c_id.append(i[1])
    return c_id
#具体岗位代码

def json_read_p():
    # 打开 JSON 文件并读取数据
    position_names = []
    position_codes = []
    with open(r'D:\job_name.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        job_list = []

        for _, subdomains in data.items():
            for _, subdomain_info in subdomains.items():
                for _, jobs in subdomain_info.items():
                    for _, job_info in jobs.items():
                        for job_title, job_code in job_info.items():
                            job_list.append([job_title, job_code])
                            position_names.append(job_title)  # 存储职位名称
                            position_codes.append(job_code)    # 存储职位代码

    return position_names, position_codes  # 返回职位名称和代码列表

#岗位和城市代码
c_id=json_read_city()
position_names, p_id = json_read_p()

driver = ChromiumPage()
cityName=[]
jobDegree=[]
jobName=[]
salaryDesc=[]
encryptJobId=[]
jobLabels=[]
job_detail=[]
jobtype=[]
salaryDesc1=[]
#1.网页爬取请求
def get_list(city: int, position: str):
    # 监听网站数据包，必须在请求之前先执行
    driver.listen.start('/wapi/zpgeek/search/joblist.json')
    driver.get(f"https://www.zhipin.com/web/geek/job?city={city}&position={position}")
    # 等待数据包内容加载
    resp = driver.listen.wait()
    # 获取数据包内容
    jsondata = resp.response.body
    time.sleep(random.uniform(0.5, 1))
    return jsondata
#2.替换所有的标签
def replace_html_tags(text):
    try:
        # 替换 <div> 标签
        text = re.sub(r'<div[^>]*>', '', text)
        # 替换 <br> 标签
        text = re.sub(r'<br[^>]*>', '', text)
        # 替换 </div> 标签
        text = re.sub(r'</div[^>]*>', '', text)
        # 使用正则表达式替换不可见的控制字符
        text = re.sub(r'[\u200b-\u200f\u202a-\u202e\u2060-\u206f\ufff0-\uffff]', '', text)
    except Exception as e:
        print(f"Error processing text: {e}")
    return text
#3.将爬取到的所有数据存入temp_post_list
temp_post_list=[]
print(len(c_id))
print(len(p_id))
#爬取的城市个数
for i in c_id[m:m+1]:
        print(i)
        #爬取的职位个数
        for j in p_id[start:end]:
            print(j)
            filename = f'd:\\boss_detail_zhibo\\{i}_{start}_{end}.xlsx'
            temp_post_list.append(get_list(i,j))
print(len(temp_post_list))

#4.定义job_id列表，以便后续访问
for i in range(0,len(temp_post_list)):
    try:
        joblist_1 = temp_post_list[i]
        joblist=joblist_1['zpData']['jobList']
        for job in joblist:
            cityName.append(str(job['cityName']))
            jobtype.append(position_names[(i % len(p_id))])  #前面的数字根据开始的数来变化
            jobDegree.append(str(job['jobDegree']))
            jobName.append(str(job['jobName']))
            encryptJobId.append(str(job['encryptJobId']))
            salaryDesc.append(str(job['salaryDesc']))
            salaryDesc1=convert_salary_list_to_annual(salaryDesc)
            jobLabels.append(str(job['jobLabels']))
    except KeyError as e:
            print(f"KeyError: {e} 在 temp_post_list[{i}] 中，跳过该条目。")
    except Exception as e:
        print(f"发生错误：{e} 在 temp_post_list[{i}] 中。")


data = {
    '城市': cityName,
    '职位类型':jobtype,
    '学历要求 ': jobDegree,
    '岗位名称': jobName,
    '地址': encryptJobId,
'薪资': salaryDesc,
    '年薪': salaryDesc1,
    '学历': jobLabels
    #'职位描述': job_detail
}

# 创建 DataFrame
df = pd.DataFrame(data)
print(df)
df.to_excel(filename)
print(filename)




