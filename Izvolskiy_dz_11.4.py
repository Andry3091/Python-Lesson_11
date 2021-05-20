"""
4.	Начать работу над проектом «Склад оргтехники». Создать класс, описывающий склад.
А также класс «Оргтехника», который будет базовым для классов-наследников. Эти классы — конкретные типы оргтехники
(принтер, сканер, ксерокс). В базовом классе определить параметры, общие для приведённых типов. В классах-наследниках
реализовать параметры, уникальные для каждого типа оргтехники.
"""

# class OfficeEquipmentWarehouse:
#     """Класс, описывающий склад оргтехники"""
#     print("\nСклад оргтехники")
#
#
# class OfficeEquipment:
#     """Базовый класс оргтехники"""
#     def __init__(self, producer, color):
#         self.producer = producer
#         self.color = color
#
#
# class Printer(OfficeEquipment):
#     """Класс принтер"""
#     amount_pr = 0
#
#     def __init__(self, producer, color, pr_type):
#         super().__init__(producer, color)
#         self.pr_type = pr_type
#         Printer.amount_pr += 1
#
#     @staticmethod
#     def name():
#         return "<<Принтер>>"
#
#     def type_printer(self):
#         return self.pr_type
#
#     def __str__(self):
#         return "\tпроизводитель: {} \tцвет: {}  \tтип принтера: {}".format(self.producer, self.color, self.pr_type)
#
#
# class Scanner(OfficeEquipment):
#     """Класс сканер"""
#     amount_sc = 0
#
#     def __init__(self, producer, color, sc_sensor):
#         super().__init__(producer, color)
#         self.sc_sensor = sc_sensor
#         Scanner.amount_sc += 1
#
#     @staticmethod
#     def name():
#         return"<<Сканер>>"
#
#     def type_sensor(self):
#         return self.sc_sensor
#
#     def __str__(self):
#         return "\tпроизводитель: {} \tцвет: {} \tтип сенсора: {}".format(self.producer, self.color, self.sc_sensor)
#
#
# class Xerox(OfficeEquipment):
#     """Класс ксерокс"""
#     amount_x = 0
#
#     def __init__(self, producer, color, xer_wi_fi):
#         super().__init__(producer, color)
#         self.xer_wi_fi = xer_wi_fi
#         Xerox.amount_x += 1
#
#     @staticmethod
#     def name():
#         return "<<Ксерокс>>"
#
#     def wi_fi_module(self):
#         return self.xer_wi_fi
#
#     def __str__(self):
#         return "\tпроизводитель: {} \tцвет: {}   \tWi-Fi модуль: {}".format(self.producer, self.color, self.xer_wi_fi)
#
#
# p = Printer('Ricon', 'black', 'струйный')
# p2 = Printer('HP', 'pink', 'лазерный')
# print(p.name(), p.amount_pr, "шт")
# print(p.__str__())
# print(p2.__str__())
#
#
# s = Scanner('Brother', 'black', 'CIS')
# s2 = Scanner('Benq', 'white', 'CCD')
# s3 = Scanner('Samsung', 'green', 'CMOS')
# print(s.name(), s.amount_sc, "шт")
# print(s.__str__())
# print(s2.__str__())
# print(s3.__str__())
#
#
# x = Xerox('LG', 'white', 'есть')
# x2 = Xerox('Fujifilm', 'black', 'отсутствует')
# x3 = Xerox('Xerox', 'yellow', 'есть')
# x4 = Xerox('Epson', 'red', 'отсутствует')
# print(x.name(), x.amount_x, "шт")
# print(x.__str__())
# print(x2.__str__())
# print(x3.__str__())
# print(x4.__str__())

class NotFoundEquipmentType(Exception):
    def __init__(self, message):
        self.message = message


class InvalidSkuNumber(Exception):
    def __init__(self, message):
        self.message = message


class Warehouse:
    # здесь будет хранится вся техника
    __office_equipment_collection = {
        'printer': [],
        'xerox': [],
        'scan': []
    }

    # здесь будет поструктурно хранится учтенная техника
    """
    EXAMPLE MAP
        {
            'бухгалтерия':{
                xerox:['xe-12-23', 'xe-22-11'],
                scan:[],
                printer:['pr-123']
            },

            'ресепшн':{
                printer:['pr-123']
            }
        }
    """
    __structure_assigned_equipment = {

    }

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Warehouse, cls).__new__(cls)
        return cls.instance

    # добавляем единицу в общий список
    def add_equipment(self, equipment_type: str, equipment: dict):
        try:
            if not self.__office_equipment_collection.get(equipment_type):
                raise NotFoundEquipmentType(f'Оборудование {equipment_type} не учитывается')

            self.__office_equipment_collection[equipment_type].append(equipment)
        except NotFoundEquipmentType as error:
            print(error.message)

    # закрепляем по артикулу единицу за соответствующей структурой
    def assign_equipment_to_structure(self, structure: str, equipment_type: str, equipment_sku_number: str):
        try:
            if not self.__office_equipment_collection.get(equipment_type):
                raise NotFoundEquipmentType(f'Оборудование {equipment_type} не учитывается')

            if not self.__validate_sku(equipment_sku_number, equipment_type):
                raise InvalidSkuNumber(f'Артикул {equipment_sku_number} не найден в раздее {equipment_type}')

            self.__structure_assigned_equipment[structure][equipment_type].append(equipment_sku_number)

        except NotFoundEquipmentType as error:
            print(error.message)
        except InvalidSkuNumber as sku_error:
            print(sku_error.message)

    def __validate_sku(self, equipment_sku_number: str, equipment_type: str):
        for item in self.__office_equipment_collection[equipment_type]:
            if item['sku'] == equipment_sku_number:
                return True
            else:
                return False

    # полное количество техники
    def get_full_qty(self):
        result = {}
        for eq_type, eq_list in self.__office_equipment_collection:
            result[eq_type] = len(eq_list)
        return result

    # оставшаяся на складе техника. Из полного перечня удалим зарезервированное кол-во
    def get_in_stock_qty(self):
        full_qty = self.get_full_qty()
        assigned_qty = self.get_assigned_qty()
        result = {}
        for key, value in full_qty:
            result[key] = value - assigned_qty[key]

        return result

    # техника в подразделениях
    def get_assigned_qty(self):
        result = {}
        for structure, equipment in self.__structure_assigned_equipment:
            for eq_type, eq_sku_list in equipment:
                result[eq_type] += len(eq_sku_list) if result.get(eq_type) is not None else len(eq_sku_list)
        return result


class OfficeEquipment:
    name: str
    sku: str
    eq_type: str

    def add_item(self, **kwargs):
        self.__dict__.update(kwargs)


class Xerox(OfficeEquipment):
    eq_type = 'xerox'
    is_color: bool


class OnlyNumericPrinterSku(Exception):
    def __init__(self, message):
        self.message = message


class Printer(OfficeEquipment):
    is_color: bool
    sku: int
    eq_type = 'printer'

    def add_item(self, **kwargs):
        try:
            if not kwargs['sku'].isnumetic():
                raise OnlyNumericPrinterSku('Sku для принтера только числовые!')
            kwargs['sku'] = int(kwargs['sku'])
        except OnlyNumericPrinterSku as error:
            print(error)


class Scan(OfficeEquipment):
    dpi: int
    eq_type = 'scan'


Printer().add_item(
    name='epson',
    is_color=False,
    sku='123'
)

Warehouse().add_equipment(Printer.eq_type, Printer.__dict__)

Scan().add_item(
    name="hp",
    dpi=123,
    sku='h-11-22-32'
)

Warehouse().add_equipment(Scan.eq_type, Scan.__dict__)

Xerox().add_item(
    name='xerox',
    is_color=True,
    sku='xe-11-22'
)

Warehouse().add_equipment(Xerox.eq_type, Scan.__dict__)

Warehouse().get_full_qty()
Warehouse().get_assigned_qty()
Warehouse().get_in_stock_qty()