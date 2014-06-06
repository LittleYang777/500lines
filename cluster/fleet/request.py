import itertools
from . import INVOKE_RETRANSMIT, Invoke
from network import Component


class Request(Component):

    client_ids = itertools.count(start=100000)

    def __init__(self, node, n, callback):
        super(Request, self).__init__(node)
        self.client_id = self.client_ids.next()
        self.n = n
        self.output = None
        self.callback = callback

    def start(self):
        self.send([self.address], Invoke(caller=self.address,
                  client_id=self.client_id, input_value=self.n))
        self.invoke_timer = self.set_timer(INVOKE_RETRANSMIT, self.start)

    def do_INVOKED(self, sender, client_id, output):
        if client_id != self.client_id:
            return
        self.logger.debug("received output %r" % (output,))
        self.invoke_timer.cancel()
        self.callback(output)
        self.stop()
