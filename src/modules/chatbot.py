import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts.prompt import PromptTemplate
from langchain.callbacks import get_openai_callback
from langchain.chains import FlareChain
from langchain.prompts import MessagesPlaceholder


#fix Error: module 'langchain' has no attribute 'verbose'
import langchain
langchain.verbose = False

class Chatbot:

    def __init__(self, model_name, temperature, vectors, qa_template):
        self.model_name = model_name
        self.temperature = temperature
        self.vectors = vectors
        self.retriever = self.vectors.as_retriever()
        self.qa_template = qa_template

        self.QA_PROMPT = PromptTemplate(
            template=self.qa_template, 
            input_variables=["context", "question"],
            )

    def conversational_chat(self, query):
        """
        Start a conversational chat with a model via Langchain
        """
        llm = ChatOpenAI(model_name=self.model_name, temperature=self.temperature)

        chain = ConversationalRetrievalChain.from_llm(llm=llm,
            retriever=self.retriever, verbose=True, return_source_documents=True, max_tokens_limit=4097, combine_docs_chain_kwargs={'prompt': self.QA_PROMPT})

        chain_input = {"question": query, "chat_history": st.session_state["history"]}
        result = chain(chain_input)

        st.session_state["history"].append((query, result["answer"]))
        return result["answer"]
    
    def conversational_chatagent(self, query):
        """
        Start a conversational chat with a model via Langchain
        """
        llm = ChatOpenAI(model_name=self.model_name, temperature=self.temperature)

        chain = FlareChain.from_llm(llm=llm,
            retriever=self.retriever, max_generation_len=164, min_prob=0.3)

        chain_input = {"question": query, "chat_history": st.session_state["history"]}
        result = chain.run(query)

        st.session_state["history"].append((query, result["answer"]))
        return result["answer"]

def count_tokens_chain(chain, query):
    with get_openai_callback() as cb:
        result = chain.run(query)
        st.write(f'###### Tokens used in this conversation : {cb.total_tokens} tokens')
    return result 

    
    
