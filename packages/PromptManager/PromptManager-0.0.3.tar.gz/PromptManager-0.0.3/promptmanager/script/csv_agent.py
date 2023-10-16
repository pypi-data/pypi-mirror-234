from promptmanager.runtime.flow import PMNodeOutput
import logging

logger = logging.getLogger('pm_log')


class CsvAgent:
    def __init__(self):
        pass

    def exec(self, open_api_key, model, csv_path, query_text) -> str:
        import os
        # from langchain.llms import OpenAI
        from langchain.chat_models import ChatOpenAI
        from langchain.agents.agent_types import AgentType
        from langchain.agents import create_csv_agent

        os.environ['OPENAI_API_KEY'] = open_api_key

        agent = create_csv_agent(
            ChatOpenAI(temperature=0, model=model),
            csv_path,
            verbose=True,
            agent_type=AgentType.OPENAI_FUNCTIONS,
        )

        results = agent.run(query_text)

        logger.info(results)

        return results


def run(params: dict = None, inputs: dict = None, outputs=None) -> PMNodeOutput:
    logger.info("Welcome to Use Csv Agent!")
    logger.info("This is params info:")
    logger.info(params)
    logger.info("This is inputs info:")
    logger.info(inputs)
    logger.info("This is outputs info:")
    logger.info(outputs)

    open_api_key = params['script']['open_api_key']['value']
    model = params['script']['model']['value']
    csv_path = params['script']['csv_path']['value']

    query_text = inputs['input']['value']

    csv_agent = CsvAgent()
    result = csv_agent.exec(open_api_key, model, csv_path, query_text)

    output = PMNodeOutput()
    for output_name in outputs.keys():
        output.add_output(output_name, result)

    return output
