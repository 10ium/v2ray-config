import requests
import os
import base64

# Function to generate base64 encoded header text for each protocol
def generate_header_text(protocol_name):
    titles = {
        'vmess': "8J+GkyBCYXJyeS1mYXIgfCB2bWVzc/Cfpbc=",
        'vless': "8J+GkyBCYXJyeS1mYXIgfCB2bGVzc/Cfpbc=",
        'trojan': "8J+GkyBCYXJyeS1mYXIgfCBUcm9qYW7wn6W3",
        'ss': "8J+GkyBCYXJyeS1mYXIgfCBTaGFkb3dTb2Nrc/Cfpbc=",
        'ssr': "8J+GkyBCYXJyeS1mYXIgfCBTaGFkb3dTb2Nrc1Ig8J+ltw==",
        'tuic': "8J+GkyBCYXJyeS1mYXIgfCBUdWljIPCfpbc=",
        'hy2': "8J+GkyBCYXJyeS1mYXIgfCBIeXN0ZXJpYTLwn6W3"
    }
    base_text = """#profile-title: base64:{base64_title}
#profile-update-interval: 1
#subscription-userinfo: upload=0; download=0; total=10737418240000000; expire=2546249531
#support-url: https://github.com/10ium/V2ray-Config
#profile-web-page-url: https://github.com/10ium/V2ray-Config

"""
    return base_text.format(base64_title=titles.get(protocol_name, ""))

protocols = {
    'vmess': 'vmess.txt',
    'vless': 'vless.txt',
    'trojan': 'trojan.txt',
    'ss': 'ss.txt',
    'ssr': 'ssr.txt',
    'tuic': 'tuic.txt',
    'hy2': 'hysteria2.txt'
}

# ptt مسیر ریشه ریپازیتوری را مشخص می‌کند (چون اسکریپت از داخل پوشه Files اجرا می‌شود)
ptt = os.path.abspath(os.path.join(os.getcwd(), '..'))

# --- شروع تغییر ---
# نام پوشه اصلی جدید که فایل‌های تقسیم شده در آن قرار گیرند، "SortedConfigs" انتخاب شده است.
new_parent_folder_name = "SortedConfigs"

# مسیر پایه برای خروجی‌ها، با احتساب پوشه والد جدید
base_output_path = os.path.join(ptt, new_parent_folder_name)

# مسیر کامل برای پوشه Splitted-By-Protocol، که حالا داخل new_parent_folder_name ("SortedConfigs") قرار می‌گیرد
splitted_path = os.path.join(base_output_path, 'Splitted-By-Protocol')
# --- پایان تغییر ---

# اطمینان از وجود دایرکتوری (os.makedirs در صورت عدم وجود، دایرکتوری‌های والد را نیز ایجاد می‌کند)
os.makedirs(splitted_path, exist_ok=True)

protocol_data = {protocol: generate_header_text(protocol) for protocol in protocols}

# Fetching the configuration data
# توجه: این قسمت همچنان از فایل موجود در آخرین کامیت بر روی شاخه main در GitHub می‌خواند.
# این یعنی فایل‌های دسته‌بندی شده بر اساس خروجی موفقیت‌آمیز قبلی app.py هستند.
response = requests.get("https://raw.githubusercontent.com/10ium/V2ray-Config/main/All_Configs_Sub.txt").text

# Processing and grouping configurations
for config in response.splitlines():
    for protocol_key in protocols.keys(): # تغییر نام متغیر تکراری protocol به protocol_key
        if config.startswith(protocol_key):
            protocol_data[protocol_key] += config + "\n"
            break # پس از پیدا کردن پروتکل، از حلقه داخلی خارج شو

# Encoding and writing the data to files
for protocol_key, data in protocol_data.items(): # تغییر نام متغیر تکراری protocol به protocol_key
    file_path = os.path.join(splitted_path, protocols[protocol_key])
    encoded_data = base64.b64encode(data.encode("utf-8")).decode("utf-8")
    with open(file_path, "w") as file:
        file.write(encoded_data)
