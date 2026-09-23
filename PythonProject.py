from datetime import date

class Medicine:

    def __init__(self, name, formula, pharmaceutical, mrp, brand):
        self.name = name
        self.formula = formula
        self.pharma = pharmaceutical
        self.mrp = mrp
        self.brand = brand
        self.qty = 0
        self.expiry = list()


    def __buy__(self, quantity, reatailprice, expiry):
        self.qty += quantity
        self.expiry.append([expiry, quantity])

    def __sell__(self, quantity):
        if self.qty < quantity:
            print("Out of Stock")
            return
        else:
            print(f'Total cost : {quantity * self.mrp}')
            self.qty -= quantity
            while self.expiry[0][1] < quantity:
                quantity -= self.expiry[0][1]
                self.expiry.pop(0)
            if self.expiry[0][1] == quantity:
                self.expiry.pop(0)
            else:
                self.expiry[0][1] -= quantity

    def __detail__(self):
        print("mrp:",self.mrp)
        print("name:",self.name)
        print("formula:",self.formula)
        print("pharmaceutical:",self.pharma)
        print("brand:",self.brand)
        print("quantity:", self.qty)

    def __check_expiry__(self):
        current_date = date.today()
        expired = 0
        while self.qty > 0 and self.expiry[0][0] < current_date:
            self.qty -= self.expiry[0][1]
            expired += self.expiry[0][1]
            self.expiry.pop(0)
        if expired > 0:
            print(expired, 'items have expired.')
        else:
            print('No items were expired.')

class Medicine_manager:
    def __init__(self):
        self.medicines = dict()
        self.path = ''

    def __create_medicine__(self):
        name = input('Enter name of medicine:').lower()
        if name in self.medicines:
            print('Medicine already exists.')
            return
        formula = input('Enter formulla of medicine:')
        mrp = int(input('Enter MRP of medicine:'))
        pharma = input('Enter pharmaceutical of medicine:')
        brand = input('Enter brand of medicine:')
        self.medicines[name] = Medicine(name, formula, pharma, mrp, brand)

    def __get_medicine__(self):
        medicine_name = input('Enter name of medicine:').lower()
        if medicine_name in self.medicines:
            return self.medicines[medicine_name]

    def __buy_medicine__(self):
        medicine = self.__get_medicine__()
        if medicine is None:
            print('Medicine does not exist.')
            return
        quantity = int(input('Enter how much medicine to buy:'))
        retail = int(input('Enter retail price of medicine:'))
        expiry = string_to_date(input('Enter expiry date in format dd.mm.yyyy'))
        medicine.__buy__(quantity, retail, expiry)

    def __sell_medicine__(self):
        medicine = self.__get_medicine__()
        if medicine is None:
            print('Medicine does not exist.')
            return
        quantity = int(input('Enter how much medicine to sell:'))
        medicine.__sell__(quantity)

    def __get_details__(self):
        medicine = self.__get_medicine__()
        if medicine is None:
            print('Medicine does not exist')
            return
        medicine.__detail__()

    def __remove_expiry__(self):
        for i in self.medicines:
            print(i, ':', end = ' ')
            self.medicines[i].__check_expiry__()

    def __list_medicine__(self):
        for i in self.medicines:
            print(i)

    def __save__(self):
        with open(self.path + 'pharmacy_project.txt', 'w') as file:
            for i in self.medicines:
                file.write(medicine_to_string(self.medicines[i]))
                file.write('\n')

    def __load__(self):
        with open(self.path + 'pharmacy_project.txt', 'a') as file:
            pass
        with open(self.path + 'pharmacy_project.txt', 'r') as file:
            medicine_strings = file.read().splitlines()
        for i in medicine_strings:
            medicine, quantity, expiry = line_to_medicine(i)
            medicine.expiry = expiry
            medicine.qty = quantity
            self.medicines[medicine.name] = medicine

def string_to_date(date_string):
    day, month, year = tuple(map(int, date_string.split('.')))
    return date(year, month, day)

def medicine_to_string(medicine):
    sep = '|'
    medicine_list = [medicine.name, sep, medicine.formula, sep, str(medicine.mrp), sep, medicine.pharma, sep, medicine.brand]
    for i in medicine.expiry:
        medicine_list.extend((sep, i[0].strftime('%d'), sep, i[0].strftime('%m'), sep, i[0].strftime('%Y'), sep, str(i[1])))
    return ''.join(medicine_list)

def line_to_medicine(line):
    medicine_list = line.split('|')
    name = medicine_list[0]
    formula = medicine_list[1]
    mrp = int(medicine_list[2])
    pharma = medicine_list[3]
    brand = medicine_list[4]
    expiry = list()
    index = 5
    total_quantity = 0
    while index < len(medicine_list):
        day, month, year, quantity = int(medicine_list[index]), int(medicine_list[index + 1]), int(medicine_list[index + 2]), int(medicine_list[index + 3])
        expiry.append([date(year, month, day), quantity])
        index += 4
        total_quantity += quantity
    return Medicine(name, formula, pharma, mrp, brand), total_quantity, expiry

def pharmacy():
    manager = Medicine_manager()
    manager.__load__()
    manager.__remove_expiry__()
    while True:
        print('1. Enter new medicine')
        print('2. Buy medicine')
        print('3. Sell medicine')
        print('4. Get medicine details')
        print('5. Remove expired medicine')
        print('6. Get medicines')
        print('7. Save')
        print('8. Save and quit')
        print('9. Quit')
        choice = input('Enter choice:')
        if choice == '1':
            manager.__create_medicine__()
        elif choice == '2':
            manager.__buy_medicine__()
        elif choice == '3':
            manager.__sell_medicine__()
        elif choice == '4':
            manager.__get_details__()
        elif choice == '5':
            manager.__remove_expiry__()
        elif choice == '6':
            manager.__list_medicine__()
        elif choice == '7':
            manager.__save__()
        elif choice == '8':
            manager.__save__()
            return
        elif choice == '9':
            return
        else:
            print('Invalid choice')

pharmacy()
    

