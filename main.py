from fintechagent import AllCustomers, Products, Customer
from fintechagent.agent import Sarvam, Agent
from fintechagent.audio import PlayAudio
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_suitable_product(customer: Customer, products: Products):
    for product in products.products:
        if customer.segment == product.segment:
            return product
    return products.default_product


def main():
    logger.info("Initializing Audio, Sarvam and Agent instances")
    pa = PlayAudio()
    sarvam = Sarvam.from_env()
    agent = Agent(sarvam)

    logger.info("Greeting to Audience")
    response = sarvam.tts("Welcome to Hyderabad Python Hackathon by HyPy")
    pa.play(response.audio)

    response = sarvam.tts(
        "I'm bulbul your fintech agent. Let's see how Akhil solved Challenge 2. Now the Demo starts"
    )
    pa.play(response.audio)

    logger.info("Initialize db for fetching the customer details and products")
    db_url = os.environ["DB_URL"]
    all_customers = AllCustomers.fetch_from_db(db_url)
    products = Products.fetch_from_folder("./products")
    for customer in all_customers.customers:
        product = get_suitable_product(customer, products)
        logger.info(
            "Conversation started between customer: %s and the agent for pitching the product: %s",
            customer.name,
            product.title,
        )
        agent.converse(customer, product)
        # Comment below line to run sales pitch for all customers
        break
    logger.info("Conversations ended")


if __name__ == "__main__":
    main()
