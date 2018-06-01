from gbdxtools import Interface
from gbdxtools import CatalogImage
from gbdxtools import IdahoImage

# establish connection
gbdx = Interface()

# To order the image with DG factory catalog id 10400100143FC900:
order_id = gbdx.ordering.order('10400100143FC900')
print order_id

# The order_id is unique to your image order and can be used to track the progress of your order. The ordered image sits in a directory on S3. The output of the following describes where:
status = gbdx.ordering.status(order_id)
# result:
# [{u'acquisition_id': u'10400100143FC900', 
#   u'state': u'delivered', 
#   u'location': u's3://receiving-dgcs-tdgplatform-com/055546367010_01_003'}]

# test a quick workflow on the item
data = str(status[0]['location'])

aoptask = gbdx.Task("AOP_Strip_Processor", data=data, enable_acomp=True, enable_pansharpen=True)
workflow = gbdx.Workflow( [aoptask] )

data = "s3://receiving-dgcs-tdgplatform-com/054813633050_01_003" # WV02 Image over San Francisco
aoptask = gbdx.Task("AOP_Strip_Processor", data=data)

s3task = gbdx.Task("StageDataToS3")
s3task.inputs.data = aoptask.outputs.data.value
s3task.inputs.destination = "s3://gbd-customer-data"

workflow = gbdx.Workflow([ aoptask, s3task ])
workflow.execute()

# workflow.execute()

# At this point the workflow is launched, and you can get status as follows:
workflow.status

# You can also get workflow events:
for event in workflow.events:
    print event['task'], event['event']
    
''' 
There are a few ways to check the status of a running workflow.

Checking the status directly:
>>> workflow.status
{u'state': u'pending', u'event': u'submitted'}

Checking whether a workflow is running:
>>> workflow.running
True

Checking whether a workflow has failed:
>>> workflow.failed
False

Checking whether a workflow has been canceled:
>>> workflow.canceled
False

Checking whether a workflow has succeeded:
>>> workflow.succeeded
True

Checking whether a workflow is complete (whether canceled, failed, or succeeded):
>>> workflow.complete
True
'''

while not workflow.succeeded:
    pass

# save the data to S3
folder = 'test_folder'
workflow.savedata(aoptask.outputs.data, location=folder)
workflow.savedata(aoptask.outputs.data)

# convert the result into an image
img = CatalogImage(aoptask.outputs.data.value)
id_img = IdahoImage(aoptask.outputs.data.value)

# >>> img = CatalogImage(aoptask.outputs.data)
# Traceback (most recent call last):
  # File "<stdin>", line 1, in <module>
  # File "C:\Anaconda2\envs\joemcg_rootclone\lib\site-packages\gbdxtools\images\catalog_image.py", line 57, in __init__
    # self._ipe_graphs = self._init_graphs()
  # File "C:\Anaconda2\envs\joemcg_rootclone\lib\site-packages\gbdxtools\images\catalog_image.py", line 119, in _init_graphs
    # for part in self.metadata['parts']:
  # File "C:\Anaconda2\envs\joemcg_rootclone\lib\site-packages\gbdxtools\images\catalog_image.py", line 82, in metadata
    # results = self._query_vectors(query)
  # File "C:\Anaconda2\envs\joemcg_rootclone\lib\site-packages\gbdxtools\images\catalog_image.py", line 68, in _query_vectors
    # raise Exception('Unable to query for image properties, the service may be currently down.', err)
# Exception: ('Unable to query for image properties, the service may be currently down.', HTTPError(u'504 Server Error: GATEWAY_TIMEOUT for url: https://vector.geobigdata.io/insight-vector/api/index/query/vector-gbdx-alpha-catalog-v2-*/paging?count=100&upper=90.0&lower=-90.0&right=180.0&q=item_type%3AIDAHOImage+AND+attributes.catalogID%3APort+data%3A%0A%09type%3A+directory%0A%09description%3A+The+output+data+directory%0A%09multiplex%3A+False&ttl=5m&left=-180.0',))





