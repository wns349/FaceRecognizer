import logging
import py4j.java_gateway

class WidgetCommunicator:
  def __init__(self):
    self.widget = None
    self.gateway = None

  def initialize(self, configs):
    if(configs['widget.use'] != 'true'):
      return

    # Load client
    address = configs['widget.jvmaddress']
    port = int(configs['widget.jvmport'])
    client = py4j.java_gateway.GatewayClient(address, port)

    # Get class
    self.gateway = py4j.java_gateway.JavaGateway(gateway_client = client)
    contextWidgetFactory = self.gateway.entry_point.getContextWidgetFactory()

    # Create widget
    widgetName = configs['widget.widgetname']
    contextName = configs['widget.contextname']
    contextType = configs['widget.contexttype']

    logging.info('Initializing widget with ' + widgetName + '___' + contextName + '___' + contextType)
    self.widget = contextWidgetFactory.createFaceRecognitionContextWidget(widgetName, contextName, contextType)

  def report(self, predictResult):
    if (not self.widget is None):
      self.widget.callback(predictResult[0])

  def terminate(self):
    logging.info('Terminating WidgetCommunicator...')
    if (not self.gateway is None):
      self.gateway.shutdown()


