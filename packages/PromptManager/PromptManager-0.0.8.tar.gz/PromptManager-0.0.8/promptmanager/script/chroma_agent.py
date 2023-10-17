from promptmanager.runtime.flow import PMNodeOutput
import logging

logger = logging.getLogger('pm_log')


class ChromaAgent:
    def __init__(self):
        pass

    def exec(self, open_api_key, model, csv_path, query_text) -> str:
        from langchain.embeddings.openai import OpenAIEmbeddings
        from langchain.vectorstores import Chroma
        from langchain.text_splitter import CharacterTextSplitter
        from langchain.llms import OpenAI
        from langchain.chains import VectorDBQA
        import os

        llm = OpenAI(temperature=0)

        os.environ['OPENAI_API_KEY'] = open_api_key

        Chroma.get()



        results = agent.run(query_text)

        logger.info(results)

        return results


# def run(params: dict = None, inputs: dict = None, outputs=None) -> PMNodeOutput:
#     logger.info("Welcome to Use Csv Agent!")
#     logger.info("This is params info:")
#     logger.info(params)
#     logger.info("This is inputs info:")
#     logger.info(inputs)
#     logger.info("This is outputs info:")
#     logger.info(outputs)
#
#     open_api_key = params['script']['open_api_key']['value']
#     model = params['script']['model']['value']
#     csv_path = params['script']['csv_path']['value']
#
#     query_text = inputs['input']['value']
#
#     csv_agent = CsvAgent()
#     result = csv_agent.exec(open_api_key, model, csv_path, query_text)
#
#     output = PMNodeOutput()
#     for output_name in outputs.keys():
#         output.add_output(output_name, result)
#
#     return output
