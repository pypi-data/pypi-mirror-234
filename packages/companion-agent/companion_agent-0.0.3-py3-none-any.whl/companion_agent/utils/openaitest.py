import datetime
import json
import os
import time
import openai
# openai.api_type = "azure"
# openai.api_base = "https://cair-1.openai.azure.com/"
# openai.api_version = "2023-03-15-preview"
# openai.api_key = os.getenv("OPENAI_API_KEY")
model_list = openai.Model.list().data
model_ids = [model.openai_id for model in model_list]
# model = "gpt-4"
model = "gpt-3.5-turbo"
def chat(input):
    start_time = time.time()
    response = openai.ChatCompletion.create(**input)
    # create variables to collect the stream of chunks
    collected_chunks = []
    collected_messages = []
    # iterate through the stream of events
    now_time=datetime.datetime.now().strftime('%H:%M:%S')
    print(f'[{now_time}] 小助手：', end='')
    for chunk in response:
        chunk_time = time.time() - start_time  # calculate the time delay of the chunk
        collected_chunks.append(chunk)  # save the event response
        chunk_message = chunk['choices'][0]['delta'].get('content', '')  # extract the message
        collected_messages.append(chunk_message)  # save the message
        # print(f"Message received {chunk_time:.2f} seconds after request: {chunk_message}")  # print the delay and text
        print(chunk_message, end='')
    print(f"  [{chunk_time:.2f}s]")
    # print the time delay and text received
    # print(f"Full response received {chunk_time:.2f} seconds after request")
    # full_reply_content = ''.join([m.get('content', '') for m in collected_messages])
    # print(f"Full conversation received: {full_reply_content}")
    return ''.join(collected_messages)

def get_chat_args(prompt, input = None):
    if input:
        input['messages'] += [{"role": "user", "content": prompt}]
        return input
    else:
        return {
            # "model": model,
            "engine":"gpt_35_turbo",
            "stream": True,
            "messages": [{"role": "system", "content": "你是ChatGPT，一个由OpenAI训练的聊天模型。始终使用中文。回答具有对话性且尽量长。"}, 
                        {"role": "user", "content": prompt}]
        }

args = None
while True:
    now_time=datetime.datetime.now().strftime('%H:%M:%S')
    str = input(f"[{now_time}] 用户：")
    if str == 'exit': break
    args = get_chat_args(str, args)
    respond = chat(args)
    args['messages'] += [{"role": "assistant", "content": respond}]