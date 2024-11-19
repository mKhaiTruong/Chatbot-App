from .agent_base import AgentBase
from langchain_pinecone import PineconeVectorStore
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from src.helper import load_embeddings
from src.prompt import *
from langchain_ollama import OllamaLLM
from dotenv import load_dotenv
import os

class QandATool(AgentBase):
    def __init__(self, max_retries=3, verbose=True):
        super().__init__(name="QandA Tool", max_retries=max_retries, verbose=verbose)
        load_dotenv()
        PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
        os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY

        # Initialize embedding and Pinecone
        embedding = load_embeddings()
        self.doc_search = PineconeVectorStore.from_existing_index(index_name="dp", embedding=embedding)

        # Define the prompt for Q&A
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}"),
        ])

        self.llm = OllamaLLM(model="llama3.2", max_tokens=2048, temperature=0.5) 

        self.retriever = self.doc_search.as_retriever(search_type='similarity', search_kwargs={"k": 3})
        self.ques_ans_chain = create_stuff_documents_chain(self.llm, self.prompt)
        self.rag_chain = create_retrieval_chain(self.retriever, self.ques_ans_chain)

    def execute(self, question):
        res = self.rag_chain.invoke({"input": question})
        print(f"Response: {res['answer']}")
        return str(res['answer'])
