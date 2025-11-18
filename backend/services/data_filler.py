# app/services/data_filler.py
from faker import Faker

fake = Faker("zh_CN")


def generate_user_data():
    return {
        "username": fake.user_name(),
        "password": fake.password(),
        "email": fake.email(),
    }


def generate_order_data():
    return {
        "order_id": fake.uuid4(),
        "price": fake.pyfloat(2, 10, 1000),
    }
