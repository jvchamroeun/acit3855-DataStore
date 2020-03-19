from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime


class FreightAssignment(Base):
    """ Freight Assignment """

    __tablename__ = "freight_assignment"

    id = Column(Integer, primary_key=True)
    freight_company = Column(String(250), nullable=False)
    freight_id = Column(String(250), nullable=False)
    freight_type_in_feet = Column(Integer, nullable=False)
    max_weight_in_pounds = Column(Integer, nullable=False)
    freight_load = Column(String(250), nullable=False)
    timestamp = Column(String(100), nullable=False)
    date_created = Column(DateTime, nullable=False)

    def __init__(self, freight_company, freight_id, freight_type_in_feet, max_weight_in_pounds, freight_load,timestamp):
        """ Initializes freight assignment details """
        self.freight_company = freight_company
        self.freight_id = freight_id
        self.freight_type_in_feet = freight_type_in_feet
        self.max_weight_in_pounds = max_weight_in_pounds
        self.freight_load = freight_load
        self.timestamp = timestamp
        self.date_created = datetime.datetime.now()

    def to_dict(self):
        """ Dictionary Representation of freight assignment details """
        dict = {}
        dict['id'] = self.id
        dict['freight_company'] = self.freight_company
        dict['freight_id'] = self.freight_id
        dict['freight_type_in_feet'] = self.freight_type_in_feet
        dict['max_weight_in_pounds'] = self.max_weight_in_pounds
        dict['freight_load'] = self.freight_load
        dict['timestamp'] = self.timestamp

        return dict
