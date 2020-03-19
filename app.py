import connexion
from connexion import NoContent
import yaml
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
from delivery_details import DeliveryDetails
from freight_assignment import FreightAssignment
import datetime
from pykafka import KafkaClient
from threading import Thread
import json
import logging.config

with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

DB_ENGINE = create_engine('mysql+pymysql://' +
                          app_config['datastore']['user'] + ':' +
                          app_config['datastore']['password'] + '@' +
                          app_config['datastore']['hostname'] + ':' +
                          app_config['datastore']['port'] + '/' +
                          app_config['datastore']['db'])

Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)


def add_booking_details(deliveryDetails):
    """Receives the details for customer delivery"""
    session = DB_SESSION()

    dd = DeliveryDetails(deliveryDetails['customer_id'],
                         deliveryDetails['delivery_id'],
                         deliveryDetails['pickup'],
                         deliveryDetails['destination'],
                         deliveryDetails['delivery_weight_in_pounds'],
                         deliveryDetails['delivery_dimensions_in_feet'],
                         deliveryDetails['timestamp'])

    session.add(dd)

    session.commit()
    session.close()

    return NoContent, 201


def get_booking_details(startDate, endDate):
    """Get customer delivery details from the data store"""
    try:
        start = datetime.datetime.strptime(startDate, "%Y-%m-%dT%H:%M:%S")
        end = datetime.datetime.strptime(endDate, "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        bad_request = {
            "detail": "startData or endDate must be in this format '2020-01-22T20:00:00'",
            "status": 400,
            "title": "Bad Request",
            "type": "about:blank"
        }
        return bad_request, 400

    results_list = []

    session = DB_SESSION()

    results = (session.query(DeliveryDetails).filter(DeliveryDetails.date_created.between(start, end)))

    for result in results:
        results_list.append(result.to_dict())
        print(result.to_dict())

    session.close()

    return results_list, 200


def add_freight_assignment(freightAssignment):
    """Receives the details for freight assignment"""

    session = DB_SESSION()

    fa = FreightAssignment(freightAssignment['freight_company'],
                           freightAssignment['freight_id'],
                           freightAssignment['freight_type_in_feet'],
                           freightAssignment['max_weight_in_pounds'],
                           freightAssignment['freight_load'],
                           freightAssignment['timestamp'])

    session.add(fa)

    session.commit()
    session.close()
    return NoContent, 201


def get_freight_assignment(startDate, endDate):
    """Get freight assignment details from the data store"""
    try:
        start = datetime.datetime.strptime(startDate, "%Y-%m-%dT%H:%M:%S")
        end = datetime.datetime.strptime(endDate, "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        bad_request = {
            "detail": "startData or endDate must be in this format '2020-01-22T20:00:00'",
            "status": 400,
            "title": "Bad Request",
            "type": "about:blank"
        }
        return bad_request, 400

    results_list = []

    session = DB_SESSION()

    results = (session.query(FreightAssignment).filter(FreightAssignment.date_created.between(start, end)))

    for result in results:
        results_list.append(result.to_dict())

    session.close()

    return results_list, 200


def process_messages():
    client = KafkaClient(hosts=app_config['kafka']['server'] + ":" + app_config['kafka']['port'])
    topic = client.topics[app_config['kafka']['topic']]

    consumer = topic.get_simple_consumer(auto_commit_enable=True,
                                         auto_commit_interval_ms=1000)

    try:
        with open('offset_data.json', 'r') as d:
            json_data = json.load(d)
    except FileNotFoundError:
        json_data = {}

    if not json_data.get('offset_saved'):
        json_data['offset_saved'] = 0

    offset_count = json_data['offset_saved']

    for msg in consumer:
        if msg.offset > json_data['offset_saved']:
            msg_str = msg.value.decode('utf  -8')
            msg = json.loads(msg_str)
            if msg['type'] == "booking_details":
                add_booking_details(msg['payload'])
                offset_count += 1
                logger.debug("Added Content: " + str(msg['payload']))
            elif msg['type'] == "freight_assignment":
                add_freight_assignment(msg['payload'])
                offset_count += 1
                logger.debug("Added Content: " + str(msg['payload']))

    json_data['offset_saved'] = offset_count

    with open('offset_data.json', 'w') as wr:
        wr.write(json.dumps(json_data, indent=2))


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yaml")

if __name__ == "__main__":
    t1 = Thread(target=process_messages)
    t1.setDaemon(True)
    t1.start()
    app.run(port=8090)
