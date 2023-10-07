import sys
import warnings

import msgpack
from requests.exceptions import HTTPError

from bec_lib.core import MessageEndpoints, RedisConnector, bec_logger

logger = bec_logger.logger

try:
    import scilog
except ImportError:
    logger.info("Unable to import `scilog` optional dependency")


class LogbookConnector:
    def __init__(self, connector: RedisConnector) -> None:
        self.connector = connector
        self.producer = connector.producer()
        self.connected = False
        self._scilog_module = None
        self._connect()
        self.logbook = None

    def _connect(self):
        if "scilog" not in sys.modules:
            return

        msg = self.producer.get(MessageEndpoints.logbook())
        if not msg:
            return
        msg = msgpack.loads(msg)

        account = self.producer.get(MessageEndpoints.account())
        if not account:
            return
        account = account.decode()
        account = account.replace("e", "p")

        self._scilog_module = scilog

        self.log = self._scilog_module.SciLog(msg["url"], options={"token": msg["token"]})
        # FIXME the python sdk should not use the ownergroup
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            try:
                logbooks = self.log.get_logbooks(readACL={"inq": [account]})
            except HTTPError:
                self.producer.set(MessageEndpoints.logbook(), b"")
                return
        if len(logbooks) > 1:
            logger.warning("Found two logbooks. Taking the first one.")
        self.log.select_logbook(logbooks[0])

        # set aliases
        # pylint: disable=no-member, invalid-name
        self.LogbookMessage = self._scilog_module.LogbookMessage
        self.send_logbook_message = self.log.send_logbook_message
        self.send_message = self.log.send_message

        self.connected = True


# if __name__ == "__main__":
#     import datetime

#     logbook = LogbookConnector()
#     msg = LogbookMessage(logbook)
#     # msg.add_text("Test").add_file("/Users/wakonig_k/Desktop/lamni_logo.png")
#     msg.add_text(
#         f"<p><mark class='pen-red'><strong>Beamline checks failed at {str(datetime.datetime.now())}.</strong></mark></p>"
#     ).add_tag("BEC")
#     logbook.send_logbook_message(msg)
