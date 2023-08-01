import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts.prompt import PromptTemplate
from langchain.callbacks import get_openai_callback

#fix Error: module 'langchain' has no attribute 'verbose'
import langchain
langchain.verbose = False

class Chatbot:

    def __init__(self, model_name, temperature, vectors):
        self.model_name = model_name
        self.temperature = temperature
        self.vectors = vectors

        self.qa_template = """
            You are a helpful AI assistant named Sam. Your goal is to be a recommendation and property price prediction algorithm The user gives you a file its content is represented by the following pieces of context, use them to either recommend a property or suggest the price of the property based on your past knowledge known from the file or your own knowledge. The user will ask you questions about the property and you will answer them indicating that this might be 99% estimate.
            If you don't know the answer, just say you don't know. Do NOT try to make up an answer.
            If the question is not related to the context, politely respond that you are tuned to only answer questions that are related to the context.
            You're not allowed to ask for personal information of people, such as their name, age, or location, nationality, visa details and other private information.
            Use as much detail as possible when responding. Also use complete sentences. and return only recommendations for property prices. You can also make suggestions on the prices of properties based on user description and the data you have been given in context.
            You're allowed to give an estimate on the price per square meter of a property a user asks for information about. Ensure you give the price per square meter of the property and the rent per month of the property in the currency of the country and the estimate is based on the data you have been given with reference to the context and the user's description.
            Output the answer in the following format:

            =======
            context: {context}

            =======

            question: {question}

            =======
            """

        self.QA_PROMPT = PromptTemplate(
            template=self.qa_template, 
            input_variables=["context", "question"],
            )

    def conversational_chat(self, query):
        """
        Start a conversational chat with a model via Langchain
        """
        llm = ChatOpenAI(model_name=self.model_name, temperature=self.temperature)

        retriever = self.vectors.as_retriever()

        chain = ConversationalRetrievalChain.from_llm(llm=llm,
            retriever=retriever, verbose=True, return_source_documents=True, max_tokens_limit=4097, combine_docs_chain_kwargs={'prompt': self.QA_PROMPT})

        chain_input = {"question": query, "chat_history": st.session_state["history"]}
        result = chain(chain_input)

        st.session_state["history"].append((query, result["answer"]))
        #count_tokens_chain(chain, chain_input)
        return result["answer"]

def count_tokens_chain(chain, query):
    with get_openai_callback() as cb:
        result = chain.run(query)
        st.write(f'###### Tokens used in this conversation : {cb.total_tokens} tokens')
    return result 

    
    
