
import time
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import datetime

from embed_provider import EmbeddingsProvider


class Chatbot:

    def __init__(self, api_key):
        self.initialize(api_key)


    def initialize(self, api_key):
   
        embed_provider = EmbeddingsProvider()
        while not embed_provider.initialized:
            time.sleep(100)

        self.embeddings, self.knowledge_base = embed_provider.get_embeddings()

        self.openai_model = self.load_openai_model(openai_api_key=api_key)
        self.prompt = self.load_prompt_template()
        self.qa_chain : LLMChain = LLMChain(llm=self.openai_model, prompt=self.prompt)
        self.is_inicialized = True


    def load_openai_model(self, openai_api_key):
        current_date = datetime.datetime.now().date()
        target_date = datetime.date(2024, 6, 12)

        if current_date > target_date:
            llm_model = "gpt-3.5-turbo"
        else:
            llm_model = "gpt-3.5-turbo-0301"

        return ChatOpenAI(openai_api_key=openai_api_key, model=llm_model, temperature = 0.7)
    
    def load_prompt_template(self):
        prompt_template = """Utiliza la siguiente información para responder a la pregunta. 

        {context}

        Pregunta: {question}
      
        Respuesta Útil: """

        PROMPT = PromptTemplate(
            template=prompt_template, input_variables=["context", "question"]
        )
        return PROMPT



    def ask_question(self, question):
        k=4

        documents = self.knowledge_base.similarity_search(question, k=k)
        docs = [document.page_content for document in documents]

        prediction_msg: dict = self.qa_chain.invoke({"question":question, 'context':docs})
        return prediction_msg['text']
