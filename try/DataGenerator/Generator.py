import random              # import, from 순.. 기능별/알파벳 순으로 정렬
import uuid
from Csv_operator import  CsvOperator

# 클래스 밖은 import할 때 다 실행되어버림 >> 함수로 통째로 따로 분리 or 클래스 생성자 초기화!!!! (init) csv_input csv_temp csv_output
THIS_YEAR = 2024
MIN_YEAR = 1950
MAX_YEAR = 2010

class Generator:

    def __init__(self):
        self.csv_operator = CsvOperator()
        self.firstname = self.csv_operator.read_csv('./csvs/firstname.csv')
        self.lastnameF = self.csv_operator.read_csv('./csvs/lastnameF.csv')
        self.lastnameM = self.csv_operator.read_csv('./csvs/lastnameM.csv')
        self.city = self.csv_operator.read_csv('./csvs/city.csv')
        self.street = self.csv_operator.read_csv('./csvs/street.csv')
        self.storetype = self.csv_operator.read_csv('./csvs/storetype.csv')
        self.coffee = self.csv_operator.read_dict('./csvs/coffee.csv')
        self.beverage = self.csv_operator.read_dict('./csvs/beverage.csv')
        self.food = self.csv_operator.read_dict('./csvs/food.csv')

    def generator(self):
        mode = input('원하는 생성모드(user/store/item/order/orderItem): ')
        if mode.lower() == 'user':
            return self.generate_users()
        elif mode.lower() == 'store':
            return self.generate_stores()
        elif mode.lower() == 'item':
            return self.generate_items()
        elif mode.lower() == 'order':
            return self.generate_orders()
        elif mode.lower() == 'orderitem':
            return self.generate_orderItems()
        else:
            print('생성모드에서 유효하지 않은 값이 입력되었습니다.')
            exit()


    def generate_users(self):
        num = int(input('생성하고 싶은 사용자 갯수: '))
        lst = [('Id', 'Name', 'Gender', 'Age', 'Birthdate', 'Address')]

        for _ in range(num):
            id = str(uuid.uuid4())
            gender = random.choice(['Male', 'Female'])
            if gender == 'Male':
                name = random.choice(self.firstname) + random.choice(self.lastnameM)
            else:
                name = random.choice(self.firstname) + random.choice(self.lastnameF)
            year = random.randint(MIN_YEAR, MAX_YEAR)
            month = random.randint(1,12)
            day = random.randint(1,28)
            birthdate = f'{year}-{month:02d}-{day:02d}'
            age = THIS_YEAR - year
            address = random.choice(self.city) + '시 ' + random.choice(self.street) + ' ' + str(random.randint(1,99)) + '길 ' + str(random.randint(1,99))

            lst.append((id, name, gender, age, birthdate, address))

        return lst


    def generate_stores(self):
        num = int(input('생성하고 싶은 점포 갯수: '))
        lst = [('Id', 'Name', 'Type', 'Address')]

        for _ in range(num):
            id = str(uuid.uuid4())
            street1 = random.choice(self.street)
            type = random.choice(self.storetype)
            name = type + ' '+ street1 + str(random.randint(1,10)) + '호점'
            address = random.choice(self.city) + '시 ' + street1 + ' ' + str(random.randint(1,99)) + '길 ' + str(random.randint(1,99))

            lst.append((id, name, type, address))

        return lst
    

    def generate_items(self):
        num = int(input('생성하고 싶은 아이템 갯수: '))
        lst = [('Id', 'Item', 'Type', 'Price')]

        for _ in range(num):
            id = str(uuid.uuid4())
            type = random.randint(1,3)

            if type == 1:
                type = 'coffee'
                item = random.choice(self.coffee)
            elif type == 2:
                type = 'beverage'
                item = random.choice(self.beverage)
            else:
                type = 'food'
                item = random.choice(self.food)
            
            lst.append((id, item['menu'], type, item['price']+'원'))

        return lst


    def generate_orders(self):
        num = int(input('생성하고 싶은 주문 갯수: '))
        lst = [('Id', 'OrderAt', 'StoreId', 'UserId')]
        
        try:
            users = input('가져올 user 파일명: ')
            users = self.csv_operator.read_dict(users)
            stores = input('가져올 store 파일명: ')
            stores = self.csv_operator.read_dict(stores)
        except IndexError:
            print("파일 내용이 잘못되어있습니다.")        # 오류 처리 안됨........ㅠㅠ
            exit()
        except FileNotFoundError:
            print("파일이 존재하지 않습니다.")
            exit()

        for _ in range(num):
            id = str(uuid.uuid4())
            date = f'{random.randint(2022, 2023)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}'
            time = f'{random.randint(0,23):02d}:{random.randint(0,59):02d}:{random.randint(1,59):02d}'
            storeId = random.choice(stores)['Id']
            userId = random.choice(users)['Id']

            lst.append((id, date + ' '+ time, storeId, userId))

        return lst
    

    def generate_orderItems(self):
        lst = [('Id', 'OrderId', 'ItemId')]
        
        try:
            orders = input('가져올 order 파일명: ')
            orders = self.csv_operator.read_dict(orders)
            items = input('가져올 item 파일명: ')
            items = self.csv_operator.read_dict(items)
        except IndexError:
            print("파일 내용이 잘못되어있습니다.")
            exit()
        except FileNotFoundError:
            print("파일이 존재하지 않습니다.")
            exit()

        for order in orders:
            time = random.randint(1,4)
            for i in range(time):
                id = str(uuid.uuid4())
                orderId = order['Id']
                itemId = random.choice(items)['Id']

                lst.append((id, orderId, itemId))

        return lst


    # def generate_orderItems(self):
    #     num = int(input('생성하고 싶은 주문아이템 갯수: '))
    #     lst = [('Id', 'OrderId', 'ItemId')]
        
    #     try:
    #         orders = input('가져올 order 파일명: ')
    #         orders = self.csv_operator.read_dict(orders)
    #         items = input('가져올 item 파일명: ')
    #         items = self.csv_operator.read_dict(items)
    #     except IndexError:
    #         print("파일 내용이 잘못되어있습니다.")
    #         exit()
    #     except FileNotFoundError:
    #         print("파일이 존재하지 않습니다.")
    #         exit()

    #     for _ in range(num):
    #         id = str(uuid.uuid4())
    #         orderId = random.choice(orders)['Id']
    #         itemId = random.choice(items)['Id']

    #         lst.append((id, orderId, itemId))

    #     return lst