"""Contains functionality related to Lines"""
import json
import logging

from models import Line


logger = logging.getLogger(__name__)


class Lines:
    """Contains all train lines"""

    def __init__(self):
        """Creates the Lines object"""
        self.red_line = Line("red")
        self.green_line = Line("green")
        self.blue_line = Line("blue")

    def process_message(self, message):
        
#         print("message", message.value())
        """Processes a station message"""
        if "org.chicago.cta.station" in message.topic():
            value = message.value()
            if message.topic() == "org.chicago.cta.stations.table.v1":
                value = json.loads( message.value() )
#                 print("topic", message.topic())
                print("value", value)
            if value["line"] == "green" or value["line"] == 1:
                self.green_line.process_message(message)
            elif value["line"] == "red" or value["line"] == 2:
                self.red_line.process_message(message)
            elif value["line"] == "blue" or value["line"] == 0:
                self.blue_line.process_message(message)
            else:
                print("discarding unknown line msg %s", value["line"])
                logger.debug("discarding unknown line msg %s", value["line"])
        elif "TURNSTILE_SUMMARY" == message.topic():
            self.green_line.process_message(message)
            self.red_line.process_message(message)
            self.blue_line.process_message(message)
        else:
            logger.info("ignoring non-lines message %s", message.topic())
