```python
from promptmanager.runtime.app import PMApp
from promptmanager.runtime.flow import PMFlow

# example1:
pmFlow = PMFlow.load('/opt/data/text_pm.pmflow');
pmApp = PMApp.publish_from_flow(pmFlow, 'http://127.0.0.1:8888')
# text variable type
variables = {'title': 'Black hole traversal', 'number': 500}
pmApp.run_by_pm_flow(variables=variables)

pmApp.show_result()

# example2:
pmFlow = PMFlow.load('/opt/data/text_pm.pmflow');
pmApp = PMApp.publish_from_flow(pmFlow, 'http://127.0.0.1:8888')
# file variable type
variables = [{'variable': 'filename', 'type': 'file', 'value': '/opt/data/flow/text_txt.txt'}]
pmApp.run_by_pm_flow(variables=variables)

pmApp.show_result()


# example3:
variables = {'title': 'Black hole traversal', 'number': 500}
url = 'http://127.0.0.1:8888/api/app/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/run'
PMApp.run_by_app_url(url, variables)
```