import json
import logging
# import math
import os
import re
import csv
from datetime import datetime
# import time
from typing import Any, Dict, List, Optional
import jieba
import numpy as np
from tqdm import tqdm
import faiss
from companion_agent.myfaiss import MyFAISS
from companion_agent.profiles import Profiles
from companion_agent.frequency_weighted_retriever import ImportanceWeightedVectorStoreRetriever
from companion_agent.utils.bm25 import BM25
from companion_agent.utils.chUtil import check_path, increment_path, mock_now

# from langchain import InMemoryDocstore
from langchain.chains import LLMChain
# from langchain.retrievers import TimeWeightedVectorStoreRetriever
from langchain.schema import BaseMemory, Document
from langchain.schema.language_model import BaseLanguageModel
from langchain.embeddings.base import Embeddings
from langchain_experimental.generative_agents.memory import GenerativeAgentMemory
from langchain.prompts import (
    ChatPromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chat_models.openai import ChatOpenAI
from langchain.chat_models import AzureChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings



logger = logging.getLogger(__name__)

FILE_PATH = os.path.abspath(__file__)
ROOT_PATH, FILE_NAME = os.path.split(FILE_PATH)

class AgentMemory(GenerativeAgentMemory):
    """Memory for the generative agent."""

    SAVE_PATH: str
    llm: BaseLanguageModel
    """The core language model."""
    llm_seg: BaseLanguageModel
    """The segment language model."""
    llm_summary: BaseLanguageModel
    """The summary language model."""
    embeddings: Embeddings
    """The embedding language model."""
    consciousness_retriever: ImportanceWeightedVectorStoreRetriever = None
    """The retriever to fetch related conciseness."""
    consciousness_capacity: int = 100
    
    """The maximum number of documents to store."""
    memory_retriever: ImportanceWeightedVectorStoreRetriever = None
    """The retriever to fetch related memories. no retrive & reflect, only visit by index(int or key)"""
    memory_capacity: int = -1
    """The maximum number of documents to store."""
    names: List[str] = ['']
    latest_summary: str = None
    language: str = 'zh'
    reflect = True
    not_been_ref = 0
    
    
    verbose: bool = False
    reflection_threshold: Optional[float] = None
    """When aggregate_importance exceeds reflection_threshold, stop to reflect."""
    current_plan: List[str] = []
    """The current plan of the agent."""
    # A weight of 0.15 makes this less important than it
    # would be otherwise, relative to salience and time
    importance_weight: float = 0.5
    """How much weight to assign the memory importance."""
    aggregate_importance: float = 0.0  # : :meta private:
    """Track the sum of the 'importance' of recent memories.

    Triggers reflection when it reaches reflection_threshold."""

    max_tokens_limit: int = 1200  # : :meta private:
    # input keys
    queries_key: str = "queries"
    most_recent_memories_token_key: str = "recent_memories_token"
    add_memory_key: str = "add_memory"
    # output keys
    relevant_memories_key: str = "relevant_memories"
    relevant_memories_simple_key: str = "relevant_memories_simple"
    most_recent_memories_key: str = "most_recent_memories"
    now_key: str = "now"
    reflecting: bool = False


    def chain(self, prompt: PromptTemplate) -> LLMChain:
        return LLMChain(llm=self.llm, prompt=prompt, verbose=self.verbose)


    @staticmethod
    def _parse_list(text: str) -> List[str]:
        """Parse a newline-separated string into a list of strings."""
        lines = re.split(r"\n", text.strip())
        lines = [line for line in lines if line.strip()]  # remove empty lines
        return [re.sub(r"^\s*\d+\.\s*", "", line).strip() for line in lines]
    

    def segmentation(self, history, input):
        with open(os.path.join(ROOT_PATH, "template/seg_template.txt"), "r", encoding = 'utf-8') as f:
            seg_template = f.read()
        system_message_prompt = SystemMessagePromptTemplate.from_template(seg_template)
        human_template = "history: {history} \n input: {input} \n 请判断input中的最近输入与history中的历史对话是否相关"
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
        chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
        inputs = {"history": history, "input": input}
        prompt = chat_prompt.format_prompt(**inputs).to_messages()
        return self.llm_seg(prompt)


    def summarize(self, dialog, pre_summary):
        with open(os.path.join(ROOT_PATH, "template/summary_template.txt"), "r", encoding = 'utf-8') as f:
            summary_template = f.read()
        system_message_prompt = SystemMessagePromptTemplate.from_template(summary_template)
        human_template = "先前总结: {summary} \n 行为: {dialog} \n 新的总结:"
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
        chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
        # if pre_summary and : dialog = dialog[-1]
        inputs = {"summary": pre_summary, "dialog": dialog}
        prompt = chat_prompt.format_prompt(**inputs).to_messages()
        return self.llm_summary(prompt)


    def judge(self, text1, text2, threshold):
        v1 = np.array(self.embeddings.embed_query(text1))
        v2 = np.array(self.embeddings.embed_query(text2))
        dist = np.sqrt(np.power(v1-v2, 2).sum())
        return dist<threshold, dist


    def _get_topics_of_reflection(self, last_k: int = 30, topic_num = 5) -> List[str]:
        """Return the 3 most salient high-level questions about recent observations."""
        con_r = self.consciousness_retriever
        prompt_en = PromptTemplate.from_template(
            "{observations}\n\n"
            f"Given only the information above, what are the {topic_num} most salient "
            "high-level questions we can answer about the subjects in the statements?\n"
            "Provide each question on a new line."
        )
        prompt_zh = PromptTemplate.from_template(
            "{observations}\n\n"
            f"凭上述信息，基于理解和推测，我们可以回答的 {topic_num} 个最重要的高层次问题是什么？\n"
            "每个问题单独一行。"
        )
        if self.language == 'en': prompt = prompt_en
        else: prompt = prompt_zh
        observations = con_r._get_documents_by_keys(con_r.consciousness[-last_k:])
        observation_str = "\n".join(
            [self._format_memory_detail(o) for o in observations]
        )
        result = self.chain(prompt).run(observations=observation_str)
        return self._parse_list(result)


    def _get_insights_on_topic(
        self, topic: str, now: Optional[datetime] = None
    ) -> Dict[str, List[str]]:
        """Generate 'insights' on a topic of reflection, based on pertinent memories."""
        prompt_en = PromptTemplate.from_template(
            "Statements relevant to: '{topic}'\n"
            "---\n"
            "{related_statements}\n"
            "---\n"
            "What 3 high-level novel insights can you infer from the above statements "
            "that are relevant for answering the following question?\n"
            "Do not include any insights that are not relevant to the question.\n"
            "Do not repeat any insights that have already been made.\n"
            "Add the resource statements behind the insight with parentheses\n\n"
            "Question: {topic}\n\n"
            "(example format: insight (because of 1, 5, 3))\n"
        )
        prompt_zh = PromptTemplate.from_template(
            "与 '{topic}' 相关的陈述有：\n"
            "---\n"
            "{related_statements}\n"
            "---\n"
            "你能从上述陈述中推断出哪些针对问题的高层次见解？请说出最关键的 2 条\n"
            "不要包括任何与问题无关的见解。\n"
            "不要重复已经提出的见解。\n"
            "直接说出见解，不要重复问题。\n"
            "在见解后面用括号加上其源自的陈述的序号\n\n"
            "问题：{topic}\n\n"
            "（示例: 。。。 (因为 1, 5, 3)）\n"
        )
        if self.language == 'en': prompt = prompt_en
        else: prompt = prompt_zh

        related_memories = self.fetch_memories(topic, now=now, importance_weight=0.4, threshold=0.75)
        related_statements = "\n".join(
            [
                self._format_memory_detail(memory, prefix=f"{i+1}. ")
                for i, memory in enumerate(related_memories)
            ]
        )
        result = self.chain(prompt).run(
            topic=topic, related_statements=related_statements
        )
        insights = self._parse_list(result)
        # TODO: Parse the connections between memories and insights
        results = {}
        for insight in insights:
            find_sources = re.compile(r'\((.*?)\)')
            sources = re.findall(find_sources, insight)
            find_sources = re.compile(r'\（(.*?)\）')
            sources += re.findall(find_sources, insight)
            buffer = []
            if sources:
                sources = re.findall(r'\d+', ';'.join(sources))
                for i in sources:
                    if int(i) < len(related_memories): buffer += [related_memories[int(i)-1].metadata['buffer_idx']]
            results[insight] = buffer
        return results
    
    def _get_insights_on_summary(
        self, summary: str
    ) -> Dict[str, List[str]]:
        """Generate 'insights' on a topic of reflection, based on pertinent memories."""
        prompt_en = PromptTemplate.from_template(
            "Statements relevant to: '{topic}'\n"
            "---\n"
            "{related_statements}\n"
            "---\n"
            "What 3 high-level novel insights can you infer from the above statements "
            "that are relevant for answering the following question?\n"
            "Do not include any insights that are not relevant to the question.\n"
            "Do not repeat any insights that have already been made.\n"
            "Add the resource statements behind the insight with parentheses\n\n"
            "Question: {topic}\n\n"
            "(example format: insight (because of 1, 5, 3))\n"
        )
        prompt_zh = PromptTemplate.from_template(
            "---\n"
            "{summary}\n"
            "---\n"
            "你能从上述陈述中知道哪些关键信息，请说出最关键的 3 条\n"
            "不要包括任何无关的见解。\n"
            "不要重复已经提出的见解。\n"
        )
        if self.language == 'en': prompt = prompt_en
        else: prompt = prompt_zh

        result = self.chain(prompt).run(summary=summary)
        insights = self._parse_list(result)
        return insights
    

    def whether_pause_to_reflect(self, now: Optional[datetime] = None):
        # After an agent has processed a certain amount of memories (as measured by
        # aggregate importance), it is time to reflect on recent events to add
        # more synthesized memories to the agent's memory stream.
        if (
            self.reflection_threshold is not None
            and self.aggregate_importance > self.reflection_threshold
            and not self.reflecting
        ):
            self.reflecting = True
            self.mid_coverage_reflect(now=now)
            # Hack to clear the importance from reflection
            self.aggregate_importance = 0.0
            self.not_been_ref = 0
            self.reflecting = False


    def mid_coverage_reflect(self, now: Optional[datetime] = None) -> List[str]:
        """Reflect on recent observations and generate 'insights'."""
        if self.verbose:
            logger.info("Character is reflecting")
        new_insights = {}
        topics = self._get_topics_of_reflection(last_k=int(self.not_been_ref*1.2), topic_num=int(self.reflection_threshold*2))
        for topic in topics:
            insights = self._get_insights_on_topic(topic, now=now)
            new_insights.update(insights)
        for insight in new_insights:
            self.add_thought(insight, sources=new_insights[insight], now=now)
        return new_insights
    
    def event_reflect(self, key: str, now: Optional[datetime] = None) -> List[str]:
        """Reflect on recent observations and generate 'insights'."""
        self.reflecting = True
        if self.verbose:
            logger.info("Character is reflecting (event)")
        con_r = self.consciousness_retriever
        event: Document = con_r.memory_stream[key]
        new_insights = self._get_insights_on_summary(event.page_content)
        for insight in new_insights:
            self.add_thought(insight, sources=[key], now=now, reflect=False)
        self.reflecting = False
        return new_insights


    def _score_memory_importance(self, memory_content: str) -> float:
        """Score the absolute importance of the given memory."""
        prompt = PromptTemplate.from_template(
            "On the scale of 1 to 10, where 1 is purely mundane"
            + " (e.g., brushing teeth, making bed) and 10 is"
            + " extremely poignant (e.g., a break up, college"
            + " acceptance), rate the likely poignancy of the"
            + " following piece of memory. Respond with a single integer."
            + "\nMemory: {memory_content}"
            + "\nRating: "
        )
        score = self.chain(prompt).run(memory_content=memory_content).strip()
        if self.verbose:
            logger.info(f"Importance score: {score}")
        match = re.search(r"^\D*(\d+)", score)
        if match:
            return (float(match.group(1)) / 10)
        else:
            return 0.0


    def _score_memories_importance(self, memory_content: str) -> List[float]:
        """Score the absolute importance of the given memory."""
        prompt = PromptTemplate.from_template(
            "On the scale of 1 to 10, where 1 is purely mundane"
            + " (e.g., brushing teeth, making bed) and 10 is"
            + " extremely poignant (e.g., a break up, college"
            + " acceptance), rate the likely poignancy of the"
            + " following piece of memory. Always answer with only a list of numbers."
            + " If just given one memory still respond in a list."
            + " Memories are separated by semi colans (;)"
            + "\Memories: {memory_content}"
            + "\nRating: "
        )
        scores = self.chain(prompt).run(memory_content=memory_content).strip()

        if self.verbose:
            logger.info(f"Importance scores: {scores}")

        # Split into list of strings and convert to floats
        scores_list = [float(x) for x in scores.split(";")]

        return scores_list

    
    def _refresh(self, new_obs_keys: List[str]):
        # 不走memory的add_thought, 直接在retriever层面操作
        mem_r = self.memory_retriever
        con_r = self.consciousness_retriever
        cur_summary = con_r.remove_documents_by_keys([self.latest_summary])[0]
        # 先加新的observation再重新summarize,再修正权重
        cur_summary.metadata['sources'] += new_obs_keys
        hist_obrs = mem_r._get_documents_by_keys(cur_summary.metadata['sources'])
        hist_obrs = str([obr.page_content for obr in hist_obrs])
        new_summary = self.summarize(hist_obrs, '').content
        cur_summary.page_content = new_summary
        cur_summary.metadata['obj_imp'] = self._score_memory_importance(new_summary)
        con_r.add_thoughts([cur_summary], ids=[self.latest_summary])


    def _resort(self, result, now: Optional[datetime] = None):
        # 需要确保刚加入的 thought (result) 和 latest_summary 在conscious内
        con_r = self.consciousness_retriever
        mem_r = self.memory_retriever
        top_k = self.consciousness_capacity
        active_importance = con_r._get_consciousness_importance(now)
        frozen_importance = mem_r._get_consciousness_importance(now)
        # result 和 latest_summary 不参与重排
        except_list = [result, self.latest_summary]
        all_importance = {**active_importance,**frozen_importance}
        for exp in except_list:
            if exp in all_importance: all_importance.pop(exp)
        sorted_importance = sorted(all_importance.items(), key=lambda x:x[1], reverse=True)
        active2frozen = []
        frozen2active = []
        for step, (key, _) in enumerate(sorted_importance):
            in_active = step<top_k-len(except_list)
            used_active = key in active_importance
            if in_active ^ used_active:
                if used_active: active2frozen += [key]
                else: frozen2active += [key]

        def migration(move_list, orig, dest):
            if move_list:
                poped_docs = orig.remove_documents_by_keys(move_list)
                new_keys = dest.add_thoughts(poped_docs, ids=move_list)
                assert new_keys == move_list

        if active2frozen: migration(active2frozen, con_r, mem_r)
        if frozen2active: migration(frozen2active, mem_r, con_r)
        return result


    # def add_memories(
    #     self, memory_content: str, now: Optional[datetime] = None
    # ) -> List[str]:
    #     """Add an observations or memories to the agent's memory."""
    #     importance_scores = self._score_memories_importance(memory_content)

    #     self.aggregate_importance += max(importance_scores)
    #     memory_list = memory_content.split(";")
    #     documents = []

    #     for i in range(len(memory_list)):
    #         documents.append(
    #             Document(
    #                 page_content=memory_list[i],
    #                 metadata={"obj_imp": importance_scores[i]},
    #             )
    #         )

    #     result = self.consciousness_retriever.add_documents(documents, current_time=now)
    #     self.whether_pause_to_reflect(now)
        
        # return result


    def add_memory(
        self, memory_content: str, role: str = '', host = False, now: Optional[datetime] = None, refresh=False, reflect=None
    ) -> List[str]:
        """
        Add an observation to the agent's memory.
        It's better to use the save_context which combined the autoseg
        """
        # refresh 是否刷新summary
        # reflect 是否开启reflect机制
        if reflect == None: reflect = self.reflect
        mem_r = self.memory_retriever
        con_r = self.consciousness_retriever
        if self.language == 'en':
            # hoststr = '' if host else f'{self.names[0]} observed '
            hoststr = ''
            userstr = f'{role} says ' if role else ''
            if host: userstr = f'{self.names[0]} says '
            observation = f"{hoststr}{userstr}{memory_content}" 
        else:
            # hoststr = '' if host else f'{self.names[0]}发现'
            # hoststr = ''
            # userstr = f'{role}说：' if role else ''
            # if host: userstr = f'{self.names[0]}说：'
            # observation = f"{hoststr}{userstr}“{memory_content}”" 
            observation = f"{self.names[0] if host else role}{memory_content}" 
        importance_score = self._score_memory_importance(observation)
        new_obs = Document(
            page_content=observation, metadata={"obj_imp": importance_score, 'role': role, 'content': memory_content}
        )
        new_obs_keys = mem_r.add_observations([new_obs], current_time=now)
        if refresh and self.latest_summary:
            self._refresh(new_obs_keys)
        else:
            if self.latest_summary: 
                self.aggregate_importance += con_r.memory_stream[self.latest_summary].metadata['obj_imp']
                self.event_reflect(self.latest_summary, now)
            self.latest_summary = None #清空latest_summary，使得旧的latest_summary参与resort
            if reflect:self.whether_pause_to_reflect(now)
            new_summary = self.summarize(str([observation]), '').content
            self.latest_summary = self.add_thought(new_summary, sources=new_obs_keys, reflect=False, now=now)

        return new_obs
    

    def add_thought(
        self, thought_content: str, importance_score=None, sources: List[str] = [], now: Optional[datetime] = None, resort=True, reflect=None
    ) -> List[str]:
        """Add a thought to the agent's consciousness."""
        # reflect 用于控制是否开启reflect 机制
        if reflect == None: reflect = self.reflect
        con_r = self.consciousness_retriever
        
        if not importance_score: importance_score = self._score_memory_importance(thought_content)
        if reflect: self.aggregate_importance += importance_score
        self.not_been_ref += 1
        thought = Document(
            page_content=thought_content, metadata={"obj_imp": importance_score, "sources": sources, "insight": self.reflecting}
        )

        result = con_r.add_thoughts([thought], current_time=now)[0]
        if reflect: self.whether_pause_to_reflect(now)
        top_k = self.consciousness_capacity
        if (resort 
            and not self.reflecting 
            and len(con_r.consciousness) > top_k): 
            # result 和 latest_summary 不参与重排
            result = self._resort(result, now)
        
        return result
    

    def _get_memories_by_keys(self, keys: List[str]) -> List[Document]:
        memories = []
        con_r = self.consciousness_retriever
        mem_r = self.memory_retriever
        for key in keys:
            doc = con_r._get_document_by_key(key)
            doc = doc if doc else mem_r._get_document_by_key(key)
            if doc: memories += [doc]
        assert len(keys) == len(memories)
        return memories
    

    def get_latest_summary(self):
        mem_r = self.memory_retriever
        con_r = self.consciousness_retriever
        cur_summary = con_r._get_document_by_key(self.latest_summary)
        # TODO change to deep retrive
        summary = self._format_memory_detail(cur_summary)
        return summary


    def reranking(self, query: str, documents: List[Document], threshold: float=0.7):
        if not documents: return documents
        if threshold == None: threshold = 0.7
        query_seg = list(jieba.cut(query, cut_all=True))
        # if not isinstance(documents[0], Document): documents = [Document(page_content=doc) for doc in documents]    
        documents_seg = [list(jieba.cut(doc.page_content, cut_all=True)) for doc in documents]
        bm25Model = BM25(documents_seg)
        scores = np.array(bm25Model.get_scores(query_seg))
        assert len(scores) == len(documents), "the length of scores list dose not matches the length of documents"
        scores -= scores.min()
        scores /= scores.max() if scores.max() else 0.001
        doc_list = np.array(documents)
        return doc_list[scores>=threshold].tolist()


    

    # simple retrive
    def fetch_memories(
        self, observation: str, now: Optional[datetime] = None, importance_weight: float = None, threshold: float = None, top_k: int = 0,  time_sorted: bool = None
    ) -> List[Document]:
        """Fetch related memories."""
        kwargs = {'importance_weight': importance_weight, 'threshold': threshold, 'top_k': top_k, 'time_sorted': time_sorted}
        if importance_weight == None: importance_weight=self.importance_weight
        if now is not None:
            with mock_now(now):
                return self.consciousness_retriever.get_relevant_documents(observation, **kwargs)
        else:
            return self.consciousness_retriever.get_relevant_documents(observation, **kwargs)
    

    #deep retrive
    def fetch_deep_memories(
        self, observation: str, now: Optional[datetime] = None, retrive_depth: int = 1, importance_weight: float = None, threshold: float = None, top_k: int = 0, time_sorted: bool = None
    ) -> List[Document]:
        """
        Fetch related memories.
        retrive_depth: the depth of 
        """
        if importance_weight == None: importance_weight=self.importance_weight
        kwargs = {'importance_weight': importance_weight, 'threshold': threshold, 'top_k': top_k, 'time_sorted': time_sorted}
        if now is not None:
            with mock_now(now):
                base_memories = self.consciousness_retriever.get_relevant_documents(observation, **kwargs)
        else:
            base_memories = self.consciousness_retriever.get_relevant_documents(observation, **kwargs)
        expand_list = []
        base_keys = []
        for memory in base_memories:
            base_keys += [memory.metadata['buffer_idx']]
            expand_list.extend(memory.metadata['sources'])

        def _getridof(expand_list):
            temp_list = []
            for i in range(len(expand_list)-1, -1, -1):
                key = expand_list.pop(i) 
                if not key in temp_list: temp_list.append(key)
            return temp_list

        # 去重
        expand_list = _getridof(expand_list)
        for i in range(len(expand_list)-1, -1, -1):
            if expand_list[i] in base_keys:
                expand_list.pop(i)

        expand_memories: List[Document] = self._get_memories_by_keys(expand_list)
        # 排序 expand_memories 筛选
        if expand_memories: expand_memories = self.reranking(observation, expand_memories, threshold)
        # 更新扩展列表的访问次数
        for mem in expand_memories:
            mem.metadata['hits'] += 1
        results = base_memories + expand_memories
        return results


    def format_memories_detail(self, relevant_memories: List[Document]) -> str:
        content = []
        for mem in relevant_memories:
            content.append(self._format_memory_detail(mem, prefix="- "))
        return "\n".join([f"{mem}" for mem in content])


    def _format_memory_detail(self, memory: Document, prefix: str = "") -> str:
        created_time = memory.metadata["created_at"].strftime("%Y-%m-%d %H:%M:%S")
        return f"{prefix}[{created_time}] {memory.page_content.strip()}"


    def format_memories_simple(self, relevant_memories: List[Document]) -> str:
        return "; ".join([f"{mem.page_content}" for mem in relevant_memories])


    def _get_memories_until_limit(self, consumed_tokens: int) -> str:
        """Reduce the number of tokens in the documents."""
        result = []
        for doc in self.consciousness_retriever.memory_stream[::-1]:
            if consumed_tokens >= self.max_tokens_limit:
                break
            consumed_tokens += self.llm.get_num_tokens(doc.page_content)
            if consumed_tokens < self.max_tokens_limit:
                result.append(doc)
        return self.format_memories_simple(result)


    @property
    def memory_variables(self) -> List[str]:
        """Input keys this memory class will load dynamically."""
        return []


    def load_memory_variables(self, inputs: Dict[str, Any]) -> Dict[str, str]:
        """Return key-value pairs given the text input to the chain."""
        queries = inputs.get(self.queries_key)
        now = inputs.get(self.now_key)
        depth = inputs.get('depth') if 'depth' in inputs else 0
        threshold = inputs.get('threshold') if 'threshold' in inputs else 0
        importance_weight = inputs.get('importance_weight') if 'importance_weight' in inputs else 0.5
        time_sorted = inputs.get('time_sorted') if 'time_sorted' in inputs else None
        top_k = inputs.get('top_k') if 'top_k' in inputs else None
        most_recent_memories_token = inputs.get(self.most_recent_memories_token_key) if self.most_recent_memories_token_key in inputs else None
        if queries is not None:
            if depth <= 0: retrieve_methods = self.fetch_memories
            else: retrieve_methods = self.fetch_deep_memories
            relevant_memories = [
                mem for query in queries for mem in retrieve_methods(query, now=now, importance_weight=importance_weight, threshold=threshold, top_k=top_k, time_sorted=time_sorted)
            ]
            result = {
                self.relevant_memories_key: self.format_memories_detail(
                    relevant_memories
                ),
                self.relevant_memories_simple_key: self.format_memories_simple(
                    relevant_memories
                ),
            }
            if most_recent_memories_token is not None:
                result[self.most_recent_memories_key] = self.get_latest_summary()
            return result

        if most_recent_memories_token is not None:
            return {
                self.most_recent_memories_key: self.get_latest_summary()
            }
        return {}
    

    def autoseg(self, role, content):
        def get_sources():
            latest_summary = self._get_memories_by_keys([self.latest_summary])[0]
            obs = self._get_memories_by_keys(latest_summary.metadata['sources'])
            return obs
        
        def format_obs(role = '', content = ''):
            if self.language == 'en': 
                userstr = f"{role}: " if role else ''
            else: 
                userstr = f"{role}：" if role else ''
            return f"{userstr}{content}"
        refresh = True
        if not self.latest_summary: refresh = False
        else:
            sources = get_sources()
            history = [format_obs(s) for s in sources]
            obs = format_obs(role, content)
            dir_related = self.segmentation(str([history[-1]]), str([obs])).content
            if dir_related == "irrelevant":
                related = self.segmentation(str(history), str([obs])).content
                if related == "irrelevant":
                    refresh = False
        return refresh


    def save_context(self, inputs: Dict[str, Any], outputs: Dict[str, Any]) -> None:
        """Save the context of this model run to memory. used by agent interactive """
        # TODO: fix the save memory key
        mem = outputs.get(self.add_memory_key)
        role = outputs.get('role') if 'role' in outputs else ''
        host = outputs.get('host') if 'host' in outputs else False
        seg = outputs.get('seg') if 'seg' in outputs else None
        if seg == None:
            refresh = self.autoseg(role, mem)
        else: refresh = not seg
        now = outputs.get(self.now_key)
        if mem:
            self.add_memory(mem, role, host, now=now, refresh=refresh)


    def init_from_profile(self, profiles: Profiles, autoseg = True, segkey = ''):
        list(jieba.cut("开始初始化记忆内容", cut_all=True))
        self.names = profiles.names
        
        def format_reasoning(obs):
            if self.language == 'en':
                userstr = f"{obs['role']} to say" if obs['role'] else ''
                if obs['host']: userstr = f'{self.names[0]}说：'
                return f"What caused {userstr} '{obs['content']}'"
            else:
                userstr = f"{obs['role']}说：" if obs['role'] else ''
                if obs['host']: userstr = f'{self.names[0]}说：'
                return f"什么导致了{userstr}“{obs['content']}”"

        id_log = None
        for step, profile in enumerate(tqdm(profiles.profiles)):
            refresh = True
            # 判别是否分段
            if autoseg:
                refresh = self.autoseg(profile['role'], profile['content'])
            else:
                assert segkey in profile
                if (id_log == None or 
                    profile[segkey] != id_log):
                    refresh = False
                    id_log = profile[segkey]
            # aligned initial
            
            now = datetime.fromtimestamp(profile['create_time'])
            if profile['host']: self.fetch_deep_memories(format_reasoning(profile), now, importance_weight=0.2, threshold=0.75)
            self.add_memory(profile['content'], profile['role'], profile['host'], now, refresh=refresh)
            if (step+1) % 50 == 0: 
                self.store(True, True)


    def init_from_checkpoint(self, path):
        args_file = os.path.join(path,"arguments.json")
        if os.path.exists(args_file):
            with open(args_file, "r", encoding = 'utf-8') as f:
                args = json.load(f)
        consciousness_path = os.path.join(path, args['consciousness_retriever'])
        memory_path = os.path.join(path, args['memory_retriever'])
        args['consciousness_retriever'] = ImportanceWeightedVectorStoreRetriever().init_from_checkpoint(consciousness_path, self.embeddings)
        args['memory_retriever'] = ImportanceWeightedVectorStoreRetriever().init_from_checkpoint(memory_path, self.embeddings)
        self.__dict__.update(args)


    def store(self, log_step = False, log_csv = False):
        steps = len(self.memory_retriever.observations)
        save_path = os.path.join(self.SAVE_PATH, f'step{steps}') if log_step else self.SAVE_PATH
        args = {}
        args.update(self.__dict__)
        exp_list = ['SAVE_PATH', 'llm', 'llm_seg', 'llm_summary', 'embeddings']
        for key in exp_list: args.pop(key)
        consciousness_name = 'consciousness'
        consciousness_path = os.path.join(save_path, consciousness_name)
        memory_name = 'memory'
        memory_path = os.path.join(save_path, memory_name)
        check_path(consciousness_path)
        check_path(memory_path)
        args['consciousness_retriever'].store(consciousness_path)
        args['memory_retriever'].store(memory_path)
        args['consciousness_retriever'] = consciousness_name
        args['memory_retriever'] = memory_name
        jsonstr = json.dumps(args, ensure_ascii=False)
        with open(os.path.join(save_path, "arguments.json"),"w") as f:
            f.write(jsonstr+'\n')

        if log_csv: self.output2csv(save_path)
    

    def clear(self) -> None:
        """Clear memory contents."""
        pass
    
    
    def output2csv(self, path = ''):
        if not path: path = self.SAVE_PATH
        con_r, mem_r = self.consciousness_retriever, self.memory_retriever
        con_r._update_subject_impotance()
        mem_r._update_subject_impotance()
        thougths, observations = {}, {}
        thougths.update(con_r.memory_stream)
        thougths.update(mem_r.memory_stream)
        for key in mem_r.observations:
            doc = thougths.pop(key)
            observations.update({key:doc})

        def format_doc(doc):
            content = doc.page_content
            metadata = doc.metadata
            key_list = ['buffer_idx', 'created_at', 'started_at', 'insight', 'last_accessed_at', 'hits', 'obj_imp', 'sub_imp', 'sources']
            result = []
            for key in key_list:
                if key in metadata:
                    if isinstance(metadata[key], datetime):
                        data = metadata[key].strftime("%Y-%m-%d %H:%M:%S")
                    # elif isinstance(metadata[key])
                    else: data = f"{metadata[key]}"
                    result += [data]

            result += [content]
            return result
        
        thougths_results = []
        observations_results = []
        for doc in thougths.values():
            thougths_results += [format_doc(doc)]

        for doc in observations.values():
            observations_results += [format_doc(doc)]

        # dataframe = pd.DataFrame({'a_name':a,'b_name':b})
        
        save_path = os.path.join(path, 'log')
        check_path(save_path)
        with open(os.path.join(save_path, 'thoughts_log.csv'), mode='w') as f:
            writer = csv.writer(f)
            writer.writerow(['buffer_idx', 'created_at', 'started_at', 'insight', 'last_accessed_at', 'hits', 'obj_imp', 'sub_imp', 'sources', 'content'])
            for result in thougths_results:
                writer.writerow(result)

        with open(os.path.join(save_path, 'observations_log.csv'), mode='w') as f:
            writer = csv.writer(f)
            writer.writerow(['buffer_idx', 'created_at', 'started_at', 'last_accessed_at', 'hits', 'obj_imp', 'sub_imp', 'content'])
            for result in observations_results:
                writer.writerow(result)

        return thougths_results, observations_results
        



if __name__ == "__main__":
    llm_core = ChatOpenAI(model="gpt-3.5-turbo-16k")

    llm_seg = AzureChatOpenAI(
        openai_api_base="https://cair-1.openai.azure.com/",
        openai_api_version="2023-03-15-preview",
        deployment_name="gpt_35_turbo",
        openai_api_key=os.getenv("AZURE_API_KEY"),
        openai_api_type = "azure",
        temperature=0
    )

    llm_summary = ChatOpenAI(model="gpt-3.5-turbo-16k")

    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

    dataset_name = '包龙星'
    human_prefix = '方唐镜'
    ai_prefix = '包龙星'
    SAVE_PATH = increment_path(os.path.join(ROOT_PATH, "runs", dataset_name, "base"))
    check_path(SAVE_PATH)
    consciousness_capacity = 500
    reflection_threshold = 3

    
    
    # initial from profiles

    # def create_new_memory_retriever(embeddings_model):
    #     """Create a new vector store retriever unique to the agent."""
    #     # Define your embedding model
    #     # Initialize the vectorstore as empty
    #     embedding_size = 1536
    #     index = faiss.IndexFlatL2(embedding_size)
    #     vectorstore = MyFAISS(
    #         embeddings_model.embed_query,
    #         index,
    #         InMemoryDocstore({}),
    #         {},
    #         relevance_score_fn=lambda score: 1.0 - score / math.sqrt(2),
    #     )
    #     return ImportanceWeightedVectorStoreRetriever(
    #         vectorstore=vectorstore, other_score_keys=["sub_imp", "obj_imp"], k=15, search_kwargs={'k':consciousness_capacity, 'fetch_k':consciousness_capacity}
    #     )

    # agent_memory = AgentMemory(
    #     SAVE_PATH=SAVE_PATH,
    #     llm=llm_core,
    #     llm_seg=llm_seg,
    #     llm_summary=llm_summary,
    #     embeddings=embeddings,
    #     consciousness_retriever=create_new_memory_retriever(embeddings),
    #     consciousness_capacity=consciousness_capacity,
    #     memory_retriever=create_new_memory_retriever(embeddings),
    #     verbose=False,
    #     reflection_threshold=reflection_threshold,  # we will give this a relatively low number to show how reflection works
    # )

    # profiles = Profiles("/data1/zehao_ni/datasets/Character_Profiles/profiles-zh-包龙星-18.jsonl", ['包龙星','少年'],start_time=int(time.mktime(time.strptime("1874-1-12", "%Y-%m-%d"))))
    # agent_memory.init_from_profile(profiles, autoseg=False, segkey='seg_id')
    # agent_memory.store(True, True)


    # reload
    agent_memory = AgentMemory(
        SAVE_PATH=SAVE_PATH,
        llm=llm_core,
        llm_seg=llm_seg,
        llm_summary=llm_summary,
        embeddings=embeddings
    )
    agent_memory.init_from_checkpoint('/data1/zehao_ni/projects/companion_agent/runs/包龙星/base-event4-well/step541')
    print()
    
    dialogs = [
        "包龙星说：“将军！”",
        "爷爷说：“恩恩……”",
        "包龙星说：“我飞帅再将。”",
        "爷爷说：“你飞帅，我就吃你的帅。”",
        "包龙星说：“啊……哎呀……”",
        "爷爷说：“你不要以为当了官就很威风。”",
        "包龙星说：“我那比得上你？”",
        "爷爷说：“你还记不记的我告诉过你，当官呢要清如水，廉如镜。”",
        "包龙星说：“爹，听说你以前都是……”",
        "爷爷说：“没错，我以前是个贪官。我诨名叫“弯了能弄直，死了能救活”，就是因为我做了太多缺德事，所以你十二个哥哥没有一个养得活，害得我每年白发人送黑发人。最后没有办法，我唯有告老还乡，把家产全捐出去做善事，就这样，才保住你这一条小命呀儿子。（转身回屋）你看，我给你写了个字挂在中堂上，就是这个廉洁的“廉”字。”",
        "包龙星说：“我怎么看，它分明都像个……贪字。”"
    ]
    preview = ''
    for i in range(len(dialogs)):
        preview = agent_memory.summarize([dialogs[i]], preview).content
        print(preview)
    print(agent_memory.summarize(dialogs, '').content)

    # for doc in agent_memory.fetch_deep_memories("戚秦氏说：“常威是凶手”", importance_weight=0, time_sorted=False):
    #     print(doc.page_content)