from dataclasses import dataclass
from typing import List
import sqlite3
from .defaults import DBQueries


@dataclass
class Customer:
    name: str
    mobile: str
    segment: str


class AllCustomers:
    def __init__(self, customers: List[Customer]):
        self.customers = customers

    def __str__(self):
        return f"{self.customers}"

    @classmethod
    def fetch_from_db(self, sqlite_path: str):
        customers = []
        with sqlite3.connect(sqlite_path) as connection:
            cursor = connection.cursor()
            cursor.execute(DBQueries.fetch_customer)
            rows = cursor.fetchall()
            for row in rows:
                customers.append(Customer(name=row[1], mobile=row[3], segment=row[2]))
        return AllCustomers(customers)
