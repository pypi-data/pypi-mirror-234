import logging

from promptmanager.runtime.flow import PMNodeOutput

logger = logging.getLogger('pm_log')


class DingoReader:
    def __init__(self, host, port, user, password, index_name):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.index_name = index_name

    def exec(self, text_key, query_text):
        from dingodb import DingoDB
        from langchain.vectorstores import Dingo

        dingo_client = DingoDB(user=self.user, password=self.password, host=[self.host + ":" + self.port])

        # First, check if our index already exists. If it doesn't, we create it
        # if index_name not in dingo_client.get_index():
        #     # we create a new index, modify to your own
        #     dingo_client.create_index(
        #         index_name=index_name,
        #         dimension=1024,
        #         metric_type='cosine',
        #         auto_id=False
        #     )

        from langchain.embeddings.huggingface import HuggingFaceEmbeddings

        model_name = "GanymedeNil/text2vec-large-chinese"
        ###向量化工具
        # embeddings = HuggingFaceEmbeddings(model_name=model_name, model_kwargs={'device': "cuda"})
        embeddings = HuggingFaceEmbeddings(model_name=model_name, model_kwargs={'device': "cpu"})  # 换成cpu也行

        vectorstore = Dingo(embeddings, text_key, client=dingo_client, index_name=self.index_name)
        # vectorstore.add_texts(["more text!","text a","cool","text b"])

        # query = "What did the president say about Ketanji Brown Jackson"
        result = vectorstore.similarity_search(query_text)

        logger.info(result)
        result_str_list = []
        for i, d in enumerate(result):
            result_str_list.append(d.page_content)

        return result_str_list


def run(params: dict, inputs: dict, outputs: dict) -> PMNodeOutput:
    logger.info("This is params info:")
    logger.info(params)
    logger.info("This is inputs info:")
    logger.info(inputs)
    logger.info("This is outputs info:")
    logger.info(outputs)

    logger.info("To query from dingo db:")

    host = params['script']['Host']['value']
    port = params['script']['Port']['value']
    index_name = params['script']['Index']['value']
    user = params['script']['user']['value']
    password = params['script']['password']['value']
    text_key = params['script']['text_key']['value']

    query_text = inputs['input']['value']

    dingo_reader = DingoReader(host, port, user, password, index_name)
    results = dingo_reader.exec(text_key, query_text)

    output = PMNodeOutput()
    for output_name in outputs.keys():
        output.add_output(output_name, results)

    return output

    # [Document(page_content='more text!', metadata={'id': 1807286027280, 'text': 'more text!', 'score': 0.53109527}), Document(page_content='more text!', metadata={'id': 1279276667843, 'text': 'more text!', 'score': 0.5310954}), Document(page_content='more text!', metadata={'id': 2707983485852, 'text': 'more text!', 'score': 0.5310954}), Document(page_content='text b', metadata={'id': 1279277372974, 'text': 'text b', 'score': 0.58489686})]

    # retriever = vectorstore.as_retriever(search_type="mmr")
    # matched_docs = retriever.get_relevant_documents(query)
    # for i, d in enumerate(matched_docs):
    #     print(f"\n## Document {i}\n")
    #     print(d.page_content)

    #    ## Document 0

    #    more text!

    #    ## Document 1

    #    text b

    #    ## Document 2

    #    more text!

    #    ## Document 3

    #    more text!
