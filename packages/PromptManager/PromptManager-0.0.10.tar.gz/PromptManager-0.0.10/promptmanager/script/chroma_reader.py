import logging

from promptmanager.runtime.flow import PMNodeOutput

logger = logging.getLogger('pm_log')


class ChromaReader:
    def __init__(self, host, port, connection):
        self.host = host
        self.port = port
        self.connection = connection

    def exec(self, query_text, n_results) -> list:
        import chromadb
        from chromadb.config import Settings
        # Example setup of the client to connect to your chroma server
        client = chromadb.HttpClient(host=self.host, port=self.port)

        from chromadb.utils import embedding_functions
        emb_fn = embedding_functions.ONNXMiniLM_L6_V2()
        # embedding_functions.DefaultEmbeddingFunction()
        # collection = client.create_collection(name="my_collection", embedding_function=emb_fn)
        collection = client.get_collection(name=self.connection, embedding_function=emb_fn)
        # collection.add(
        #     documents=["This is a document", "This is another document"],
        #     metadatas=[{"source": "my_source"}, {"source": "my_source"}],
        #     ids=["id1", "id2"]
        # )
        results = collection.query(
            query_texts=[query_text],
            n_results=int(n_results)
        )

        result_str_list = []
        if results:
            documents = results["documents"]
            if documents:
                result_str_list = documents[0]

        logger.info(result_str_list)

        return result_str_list


def run(params: dict, inputs: dict, outputs: dict) -> PMNodeOutput:
    logger.info("This is params info:")
    logger.info(params)
    logger.info("This is inputs info:")
    logger.info(inputs)
    logger.info("This is outputs info:")
    logger.info(outputs)

    host = params['script']['Host']['value']
    port = params['script']['Port']['value']
    connection = params['script']['Connection']['value']
    n_results = params['script']['n_results']['value']

    query_text = inputs['input']['value']

    logger.info("To query from chroma db:")
    chroma_reader = ChromaReader(host=host, port=port, connection=connection)
    results = chroma_reader.exec(query_text, n_results)

    output = PMNodeOutput()
    for output_name in outputs.keys():
        output.add_output(output_name, results)

    return output

# if __name__ == '__main__':
#     params = {
#         "script":{
#             "Host":{
#                 "value":'172.20.52.122'
#             },
#             "Port":{
#                 "value":8000
#             },
#             "Connection":{
#                 "value":"my_collection"
#             },
#             "n_results":{
#                 "value":10
#             }
#         }
#     }
#
#     inputs = {
#         "input":{ "value": "This is a query text"}
#
#     }
#
#     run(params, inputs, None)
