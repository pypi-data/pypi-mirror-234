import datetime
import os
import time
from tqdm import tqdm
import urwid
import jsonlines
# from langchain.memory import ConversationSummaryMemory

FILE_PATH = os.path.abspath(__file__)
ROOT_PATH, FILE_NAME = os.path.split(FILE_PATH)

class Profiles:
    speak_rate = 25/6
    message_gap = 2
    dialog_gap = 60
    act_gap = 6 * 60 *60

    def __init__(self, path, names: list[str] = [], alias = {}, start_time: int = 0) -> None:
        self.source = path
        self.names = names
        self.alias = alias
        self.start_time = start_time
        self.load_jsonl()

    def load_jsonl(self, path=None):
        if not path: path = self.source
        with open(path, "r", encoding = 'utf-8') as f:
            profiles = []
            for item in jsonlines.Reader(f):
                profiles += [item]
        if self.start_time: time_log = self.start_time
        else: time_log = int(round(time.time()))
        self.profiles = []

        def check_key(obj, key, default = ''):
            return obj[key] if key in obj else default
        
        profile = None
        for prof in tqdm(profiles):
            role = check_key(prof, 'role', '')
            if role == '旁白': role = '' 
            content = check_key(prof, 'content', '').strip()
            dialog_id = check_key(prof, 'diag_id', None)
            act_id = check_key(prof, 'act_id', None)
            if 'create_time' in prof: time_log = prof['create_time']
            elif profile:
                time_log += int(len(profile['content'])*self.speak_rate)
                if act_id != profile['act_id']: time_log += self.act_gap
                elif dialog_id != profile['dialog_id']: time_log += self.dialog_gap
                else: time_log += self.message_gap
            host = False
            for name in self.names: 
                if name in role: host = True
            profile = {'role': role, 'host': host, 'content': content, 'create_time':time_log, 'dialog_id': dialog_id, 'act_id': act_id, 'seg_id': f"{act_id}-{dialog_id}"}
            self.profiles += [profile]
        
    # def load_json(self, path, alias):
    #     with open(path, "r", encoding = 'utf-8') as f:
    #         dialog_json = json.load(f)
    #     self.date = dialog_json['date']
    #     dialog = dialog_json['dialog']
    #     self.dialog = []
    #     self.user = {}
    #     user_log = ''
    #     time_log = 0
    #     step_timestamp = 1 * 60 *60 # 1h
    #     for msg in dialog:
    #         time_step = msg['create_time'] - time_log
    #         time_log = msg['create_time']
    #         username = msg['host'] if 'host' in msg else msg['user']
    #         if username in alias: username = alias[username]
    #         if user_log != username:
    #             user_log = username
    #             message = {'host':username, 'create_time':msg['create_time'], 'content':msg['content']}
    #             self.dialog += [message]
    #             if username in self.user: self.user[username] += 16 
    #             else: self.user[username] = 1
    #         elif time_step > step_timestamp:
    #             message = {'host':username, 'create_time':msg['create_time'], 'content':msg['content']}
    #             self.dialog += [message]
    #             if username in self.user: self.user[username] += 1
    #             else: self.user[username] = 1
    #         else:
    #             message['content'] += " \n " + msg['content']
            

    def format_profiles(self, prefix, content):
        padding_len = sum([urwid.str_util.get_width(ord(ch)) for ch in prefix])
        seg_list = []
        for seg in content.split("\n"):
            seg_list += seg.split("\r")
        result = ""
        for step, seg in enumerate(seg_list):
            if step == 0: 
                result += prefix
            else:
                result += " "*padding_len
            result += seg+"\n"
        return result[:-1]
    
    def get_txt_list(self, date = True, format = True, alias = {}):
        profiles = self.profiles
        result = []
        for message in profiles:
            create_time = message['create_time']
            create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(create_time))
            username = alias[message['role']] if message['role'] in alias else message['role']
            timestr = f"[{create_time}] " if date else ""
            userstr = f"{username}: " if username else ""
            if format:
                msg = self.format_profiles(f"{timestr}{userstr}", message['content'].strip())
            else:
                msg = f"{timestr}{userstr}" + message['content'].strip()
            result += [msg]
        return result
    
    def get_txt_by_index(self, insex, date = True, format = True, alias = {}):
        profiles = self.profiles
        message = profiles[insex]
        create_time = message['create_time']
        create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(create_time))
        username = alias[message['role']] if message['role'] in alias else message['role']
        timestr = f"[{create_time}] " if date else ""
        userstr = f"{username}: " if username else ""
        if format:
            msg = self.format_dialog(f"{timestr}{userstr}", message['content'].strip())
        else:
            msg = f"{timestr}{userstr}" + message['content'].strip()
        return msg

if __name__ == "__main__":
    # mark = 0
    # with open("/data1/zehao_ni/datasets/Character_Profiles/profiles-zh-包龙星.jsonl", "r", encoding = 'utf-8') as f:
    #     profiles = []
    #     for item in jsonlines.Reader(f):
    #         if item['act_id'] == 0: item['act_id'] = mark
    #         else: mark = item['act_id']
    #         profiles += [item]
    # with jsonlines.open("/data1/zehao_ni/datasets/Character_Profiles/profiles-zh-包龙星.jsonl", "w") as f:
    #     for item in profiles:
    #         f.write(item)
    start_time = int(time.mktime(time.strptime("1874-1-12", "%Y-%m-%d")))
    profiles = Profiles("/data1/zehao_ni/datasets/Character_Profiles/profiles-zh-包龙星.jsonl", ['少年','包龙星'],start_time=start_time)
    script = '\n'.join(profiles.get_txt_list())
    with open(os.path.join(ROOT_PATH, "sample.txt"), mode='w') as f:
        f.write(script)
    print()