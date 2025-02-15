from fintechagent.cutomer import AllCustomers


def test_customers():
    AllCustomers.fetch_from_db("./bank.sqlite")
