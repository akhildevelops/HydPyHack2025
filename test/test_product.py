from fintechagent.product import Products


def test_product():
    products = Products.fetch_from_folder("./products")
