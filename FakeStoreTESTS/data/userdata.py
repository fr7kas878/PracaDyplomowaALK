from generator_emails import GeneratorEmails
from faker import Faker
faker = Faker()


class UserData:
    DATA_EMAIL = GeneratorEmails().generate_email()
    DATA_PASSWORD = "JakiesNowe87#"
    DATA_FAKE_PASSWORD = faker.password()
    DATA_FIRST_NAME = "Maryla"
    DATA_LAST_NAME = "Blank"
    DATA_STREET = "Truskawkowa 22"
    DATA_POSTAL_CODE = "55-080"
    DATA_CITY ="Koniecswiata"
    DATA_PHONE = 697974334

class DataToLogIn:
    DATA1_USEREXISTINGEMAIL = "rightadresstome@gmail.com"
    DATA1_PASSWORD = "JakiesNowe67&"
    DATA2_WRONGEMAIL ="fr7kas@@gmail.com"
    DATA2_TOSHORTPASSWORD = "jakies"


# class TestDataToRegistration

