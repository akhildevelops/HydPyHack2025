from fintechagent import Agent, Sarvam, Customer, Products


def test_converse():
    sarvam = Sarvam.from_env()
    agent = Agent(sarvam)
    customer = Customer("Akhil", "+91 9876543210", "travel")
    prodcuts = Products.fetch_from_folder("./products")
    agent.converse(customer, prodcuts.default_product)
