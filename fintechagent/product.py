from dataclasses import dataclass
from typing import List
from pathlib import Path
import os


@dataclass
class Product:
    title: str
    content: str
    segment: str


class Products:
    def __init__(self, products: List[Product]):
        self.products = products
        self.default_product: Product = None
        for product in self.products:
            if product.segment == "generic":
                self.default_product = product
        if self.default_product is None:
            raise ValueError("Cannot found generic product")

    def __str__(self):
        return f"{self.products}"

    @classmethod
    def fetch_from_folder(cls, folder_path: str):
        products = []
        folder_path = Path(folder_path)
        files = os.listdir(folder_path)
        for file in files:
            segment, title = file.split("-")
            with open(folder_path / file, "r") as fileobj:
                data = fileobj.read()
            p = Product(title=title.strip(), content=data, segment=segment.strip())
            products.append(p)
        return Products(products)
