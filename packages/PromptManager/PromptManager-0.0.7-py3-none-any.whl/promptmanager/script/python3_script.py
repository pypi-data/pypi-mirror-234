from promptmanager.runtime.flow import PMNodeOutput
import logging

logger = logging.getLogger('pm_log')


class PMCustomScript:
    def __init__(self):
        pass

    def exec(self, inputs: dict = None) -> dict:
        logger.info("To get the input of inputs value")
        logger.info(inputs['input'])

        logger.info("write your script here")

        logger.info("To set the output of outputs value")

        return "this a result text"


def run(params: dict = None, inputs: dict = None, outputs=None) -> PMNodeOutput:
    logger.info("Welcome to Large Model Prompt Manager World!")
    # runtime =PMRuntime.get_current_runtime()
    logger.info("This is params info:")
    logger.info(params)
    logger.info("This is inputs info:")
    logger.info(inputs)
    logger.info("This is outputs info:")
    logger.info(outputs)

    custom_script = PMCustomScript()
    text = custom_script.exec(inputs)

    output = PMNodeOutput()
    for output_name in outputs.keys():
        output.add_output(output_name, text)

    return output
