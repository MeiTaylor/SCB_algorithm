import os
import openai
import re  # 导入正则表达式模块
import sys
import time
import json



os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890" 


# os.environ["OPENAI_API_BASE"]="https://api.openai.com"
# openai.api_key = "sk-"

openai.api_base="https://textai.buzz/v1"
# os.environ["OPENAI_API_BASE"]="https://aigptx.top/"
openai.api_key = "sk-"



# 打开文件并读取内容
with open('E:\\softbei\\code\\txt\\45.txt', 'r', encoding='utf-8') as file: 
    resume_text = file.read()

# 读取txt文件
with open('E:\\softbei\\code\\requirements.txt', 'r', encoding='utf-8') as file:
    system_message = file.read().replace('\n', '')


# resume_text = sys.argv[1]  # Get the first argument passed from the C# code
# system_message = sys.argv[2]  # Get the second argument passed from the C# code





message = [
    {"role": "system", "content": system_message},
    {"role": "user", "content": f"我这里有一份简历，我需要获取其中的一些信息。简历如下：{resume_text}"},
]



response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",  # gpt-3.5-turbo-0301
    messages=message,
    temperature=0.2,
    max_tokens=1000,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
)

# response = response['choices'][0]['message']['content']
# response = response['choices'][0]['text']
#print(response)
#print(response['choices'][0]['message']['content'])


answer = response['choices'][0]['message']['content']


# 使用正则表达式找出需要的信息
info_keys = ["姓名", "年龄", "个人邮箱","手机号","性别", "求职意向岗位", "自我评价", "最高学历", "毕业院校", "技能证书", "获奖荣誉", "工作总时间", "各段工作经历", "工作稳定性的程度", "工作稳定性判断的原因","人岗匹配程度分数","人岗匹配的理由" ]
resume_info = {}
for key in info_keys:
    if key == "各段工作经历":
        match = re.search("工作经历：\n(.*?)\n工作总时间", answer, re.DOTALL)
        if match is not None:
            value = match.group(1).strip()  # 获取匹配的值并删除前后的空格
            # 将工作经历分割成多个部分，并删除每部分前后的空格
            value = [part.strip() for part in value.split('\n') if part.strip() != '']
            resume_info["各段工作经历"] = value  # 将信息存入字典

    else:
        match = re.search(f"{key}：(.*)", answer)
        if match is not None:
            value = match.group(1).strip()  # 获取匹配的值并删除前后的空格
            resume_info[key] = value  # 将信息存入字典



if "手机号" in resume_info:
    age_match = re.search(r"(\d+)", resume_info["手机号"])
    if age_match is not None:
        resume_info["手机号"] = int(age_match.group(1))   # Convert the age string to an integer
            
# Handle the age value
if "年龄" in resume_info:
    age_match = re.search(r"(\d+)", resume_info["年龄"])
    if age_match is not None:
        resume_info["年龄"] = int(age_match.group(1)) +1   # Convert the age string to an integer

# Handle the work years value
if "工作总时间" in resume_info:
    years_match = re.search(r"(\d+)", resume_info["工作总时间"])
    if years_match is not None:
        resume_info["工作总时间"] = int(years_match.group(1)) + 1  # Convert the work years string to an integer


# for key, value in resume_info.items():
#     print(f"{key}: {value}")


# Convert the resume_info dictionary to a JSON string
json_str = json.dumps(resume_info)
print(json_str)
