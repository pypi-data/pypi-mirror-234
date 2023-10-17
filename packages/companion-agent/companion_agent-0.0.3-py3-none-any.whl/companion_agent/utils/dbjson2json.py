import datetime
import json
import os
import hashlib
import time
from tqdm import tqdm

domain = "cheney"
ROOT_PATH = "/data1/zehao_ni/datasets/NoChatNoLife"
source = 'raw_chat'
target = 'r_chat'
file_dir = os.path.join(ROOT_PATH, domain, source)
save_dir = os.path.join(ROOT_PATH, domain, target)
db_list = os.listdir(file_dir)
db_list.remove('Contact')
file_list = {}
for db in db_list:
    file_path = os.path.join(file_dir, db)
    file_names = os.listdir(file_path)
    for name in file_names:
        file_id = name.split('.')[0]
        file_id = file_id.split('_')[-1]
        file_list[file_id] = (file_path, name)
    

contact_dir = "raw_chat\Contact\WCContact.json"
contact_path = os.path.join(ROOT_PATH, domain, contact_dir)
contact_names = [('m_nsRemark','remark'), ('nickname','nickname'), ('m_nsUsrName','username'), ('m_nsAliasName','aliasname')]
with open(contact_path, "r", encoding = 'utf-8') as f:
    raw_contacts = json.load(f)

contact_list = []
for contact in raw_contacts:
    contact_ft = {}
    for name1,name2 in contact_names:
        contact_ft[name2] = contact[name1]
    if not 'gh' in contact_ft['username']:
        contact_ft['id'] = hashlib.md5(contact_ft['username'].encode("utf-8")).hexdigest()
        contact_list += [contact_ft]

def get_name(contact):
    if contact['remark']: return contact['remark']
    else: return contact['nickname']

for contact in tqdm(contact_list):
    if contact['id'] in file_list:
        dialog_json = {"date":datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "dialog":[]}
        contact_name = get_name(contact).replace("|", "-").replace("/", "-")
        file = file_list[contact['id']]
        with open(os.path.join(*file), "r", encoding = 'utf-8') as f:
            dialog = json.load(f)
        for dic in dialog:
            if dic["messageType"] == 1:
                create_time = dic['msgCreateTime']
                # create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(create_time))
                content = dic["msgContent"]
                if dic["mesDes"] == 1: host = contact_name
                else: host = domain
                dialog_json['dialog'] += [{'host': host, 'create_time': create_time, 'content': content}]
        json_str = json.dumps(dialog_json, ensure_ascii=False)
        
        if not os.path.exists(save_dir): os.mkdir(save_dir)
        save_path = os.path.join(save_dir,contact_name+".json")
        with open(save_path, 'w', encoding = 'utf-8') as write_f:
            write_f.write(json_str)

# count = 0
# for contact in tqdm(contact_list):
#     if contact['id'] in file_list:
#         contact_name = get_name(contact).replace("|", "-").replace("/", "-")
#         # print(contact_name, end='  ')
#         # count += 1
#         file = file_list[contact['id']]
#         with open(os.path.join(*file), "r", encoding = 'utf-8') as f:
#             dialog = json.load(f)
#         with open(os.path.join(save_dir,contact_name+".txt"), "w", encoding = 'utf-8') as f:
#             for dic in dialog:
#                 if dic["messageType"] == 1:
#                     create_time = dic['msgCreateTime']
#                     create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(create_time))
#                     content = dic["msgContent"]
#                     if dic["mesDes"] == 1:
#                         # msg = content.strip().replace("\n", " ").replace("\r", " ")
#                         # msg = f"[{create_time}] {contact_name}" + "：" + content.strip()
#                         msg = format_dialog(f"[{create_time}] {contact_name}：", content.strip())
#                     else:
#                         # msg = content.strip().replace("\n", " ").replace("\r", " ")
#                         # msg = f"[{create_time}] cheney：" + content.strip()
#                         msg = format_dialog(f"[{create_time}] {domain}：", content.strip())
#                     f.write("{}\n".format(msg))
print()
