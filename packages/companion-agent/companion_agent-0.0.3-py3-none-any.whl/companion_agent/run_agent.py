import datetime
import logging
import math
import os
import time
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models.openai import ChatOpenAI
from langchain.chat_models import AzureChatOpenAI
from langchain import InMemoryDocstore
import faiss

FILE_PATH = os.path.abspath(__file__)
ROOT_PATH, FILE_NAME = os.path.split(FILE_PATH)

from companion_agent.myfaiss import MyFAISS
from companion_agent.profiles import Profiles
from companion_agent.frequency_weighted_retriever import ImportanceWeightedVectorStoreRetriever
from companion_agent.utils.chUtil import increment_path, check_path
from companion_agent.memory import AgentMemory
from companion_agent.companion_agent import CompanionAgent

def run_agent(checkpoint, save_path='', human_prefix = 'human', ai_prefix = '', age = None, traits="", status=""):
    llm_core = ChatOpenAI(model="gpt-3.5-turbo-16k")

    # llm_seg = AzureChatOpenAI(
    #     openai_api_base="https://cair-1.openai.azure.com/",
    #     openai_api_version="2023-03-15-preview",
    #     deployment_name="gpt_35_turbo",
    #     openai_api_key=os.getenv("AZURE_API_KEY"),
    #     openai_api_type = "azure",
    #     temperature=0
    # )
    llm_seg = ChatOpenAI(model="gpt-3.5-turbo-16k")

    # llm_summary = AzureChatOpenAI(
    #     openai_api_base="https://cair-1.openai.azure.com/",
    #     openai_api_version="2023-03-15-preview",
    #     deployment_name="gpt_35_turbo",
    #     openai_api_key=os.getenv("AZURE_API_KEY"),
    #     openai_api_type = "azure",
    #     temperature=0
    # )
    llm_summary = ChatOpenAI(model="gpt-3.5-turbo-16k")

    # embeddings = OpenAIEmbeddings(
    #     deployment = "text_embedding_ada_002",
    #     openai_api_base = "https://cair-1.openai.azure.com/",
    #     openai_api_type = "azure",
    #     openai_api_key=os.getenv("AZURE_API_KEY"),
    # )
    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
    
    consciousness_capacity = 500
    reflection_threshold = 5
    agent_memory = AgentMemory(
        SAVE_PATH=save_path,
        llm=llm_core,
        llm_seg=llm_seg,
        llm_summary=llm_summary,
        embeddings=embeddings
    )
    agent_memory.init_from_checkpoint(checkpoint)
    print()

    #### read memory
    # db, ld = memory.init_from_Memory(SAVE_PATH, 'index')

    ### start chat
    # docs = db.similarity_search_with_score('篮球')
    def interview_agent(agent: CompanionAgent, message: str) -> str:
        """Help the notebook user interact with the agent."""
        # new_message = f"{human_prefix}说{message}"
        do, action =  agent.generate_reaction(message, human_prefix, datetime.datetime(1876, 2, 12))
        if do: return action
        else: return ''
    
    ChatMe = CompanionAgent(
        name=ai_prefix,
        age=age,
        traits=traits,  # You can add more persistent traits here
        status=status,  # When connected to a virtual world, we can have the characters update their status
        llm=llm_core,
        memory=agent_memory,
    )
    # print(interview_agent(ChatMe, "你是谁？"))
    while True:
        now_time=datetime.datetime.now().strftime('%H:%M:%S')
        message = input(f"[{now_time}] {human_prefix}：")
        if message == 'exit': break
        answer = interview_agent(ChatMe, message)
        now_time=datetime.datetime.now().strftime('%H:%M:%S')
        answer = answer.split('said')[-1].strip('"')
        print(f"[{now_time}] {ai_prefix}：{answer}")
    print()

if __name__ == '__main__':
    dataset_name = '包龙星'
    SAVE_PATH = increment_path(os.path.join(ROOT_PATH, "runs", dataset_name, "agent_exp"))
    check_path(SAVE_PATH)
    checkpoint_path = '/data1/zehao_ni/projects/companion_agent/runs/包龙星/base-event4-well/step541'
    human_prefix = '上帝'
    ai_prefix = '包龙星'
    run_agent(checkpoint_path, SAVE_PATH, human_prefix = human_prefix, ai_prefix = ai_prefix)