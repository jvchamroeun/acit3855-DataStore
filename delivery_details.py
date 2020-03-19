from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime


class DeliveryDetails(Base):
    """ Delivery Details """

    __tablename__ = "delivery_details"

    id = Column(Integer, primary_key=True)
    customer_id = Column(String(250), nullable=False)
    delivery_id = Column(String(250), nullable=False)
    pickup = Column(String(250), nullable=False)
    destination = Column(String(250), nullable=False)
    delivery_weight_in_pounds = Column(Integer, nullable=False)
    delivery_dimensions_in_feet = Column(Integer, nullable=False)
    timestamp = Column(String(100), nullable=False)
    date_created = Column(DateTime, nullable=False)

    def __init__(self, customer_id, delivery_id, pickup, destination, delivery_weight_in_pounds,delivery_dimensions_in_feet, timestamp):
        """ Initializes customer delivery details """
        self.customer_id = customer_id
        self.delivery_id = delivery_id
        self.pickup = pickup
        self.destination = destination
        self.delivery_weight_in_pounds = delivery_weight_in_pounds
        self.delivery_dimensions_in_feet = delivery_dimensions_in_feet
        self.timestamp = timestamp
        self.date_created = datetime.datetime.now()

    def to_dict(self):
        """ Dictionary Representation of customer delivery details """
        dict = {}
        dict['id'] = self.id
        dict['customer_id'] = self.customer_id
        dict['delivery_id'] = self.delivery_id
        dict['pickup'] = self.pickup
        dict['destination'] = self.destination
        dict['delivery_weight_in_pounds'] = self.delivery_weight_in_pounds
        dict['delivery_dimensions_in_feet'] = self.delivery_dimensions_in_feet
        dict['timestamp'] = self.timestamp

        return dict
