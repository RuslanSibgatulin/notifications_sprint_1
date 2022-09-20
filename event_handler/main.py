import logging

from config import events_config
from db.rabbit_exchange import RabbitExchange
from events_handler import EventsHandler
from settings import kafka_settings, rabbit_settings

if __name__ == "__main__":
    logger = logging.getLogger("Event Handler")
    logger.info("Started")
    rabbit = RabbitExchange(rabbit_settings.uri, exchange="Notice")
    events = EventsHandler(kafka_settings.uri, rabbit, events_config)
    try:
        events.run()
    except KeyboardInterrupt:
        logger.info("Stop reading")

    logger.info("Finished")
