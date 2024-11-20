from dotenv import load_dotenv
import os
import streamlit as st

from .agent_base import AgentBase
from langchain_pinecone import PineconeVectorStore
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from src.helper import load_embeddings
from src.prompt import *
from langchain_ollama import OllamaLLM


class QandATool(AgentBase):
    def __init__(self, max_retries=3, verbose=True):
        super().__init__(name="QandA Tool", max_retries=max_retries, verbose=verbose)
        load_dotenv()
        PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
        os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY

        # Initialize embedding and Pinecone
        embedding = load_embeddings()
        self.llm = OllamaLLM(model="llama3.2", max_tokens=2048, temperature=0.01) 
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

        self.vector_store = PineconeVectorStore.from_existing_index(index_name="dp", embedding=embedding)
        self.retriever = self.vector_store.as_retriever(search_kwargs={"k": 3})

        self.chain =  ConversationalRetrievalChain.from_llm(llm=self.llm, chain_type='stuff',
                                                            retriever=self.retriever,
                                                            memory=self.memory)

        
        # self.ques_ans_chain = create_stuff_documents_chain(self.llm, self.prompt)
        # self.rag_chain = create_retrieval_chain(self.retriever, self.ques_ans_chain)

    def execute(self, question):
        # result = self.chain({"question": question, "chat_history": st.session_state['history']})
        formatted_history = "".join(
            f"<|start_header_id|>user<|end_header_id|>\n{q}<|eot_id|>\n<|start_header_id|>assistant<|end_header_id|>\n{a}<|eot_id|>\n"
            for q, a in st.session_state['history']
        )
        prompt = (
            f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n"
            f"Provide helpful, context-aware responses about software design patterns.\n<|eot_id|>\n"
            f"{formatted_history}"
            f"<|start_header_id|>user<|end_header_id|>\n{question}<|eot_id|>\n<|start_header_id|>assistant<|end_header_id|>\n"
        )
        
        result = self.chain({"question": prompt})
        st.session_state['history'].append((question, result["answer"]))

        return result["answer"]
    
