from faker import Faker


class GenerateData:
    def __init__(self):
        self.faker = Faker(locale="zh_CN")

    def get_now_time(self):
        #
        return self.faker.date_time()


if __name__ == "__main__":
    gd = GenerateData()
    print(gd.get_now_time())
