from faker import Faker
faker = Faker()

def generate_email():
    return faker.email()

def generate_password():
    return faker.password()