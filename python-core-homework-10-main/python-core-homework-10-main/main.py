from collections import UserDict
from datetime import datetime

class Field:
    def __init__(self, value):
        self._value = value


    def __str__(self):
        return str(self.value)
    
    @property
    def value(self):
        return self._value 

    @value.setter
    def value(self, new_value):
        self._value = new_value   

class Name(Field):
    pass  

class Birthday(Field):
    def validate_birthday(self):
        try:
            datetime.strptime(self._value, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Неправильний формат дня народження. Використовуйте рік-місяць-день (приклд, '2000-01-01').")

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value
        self.validate_birthday()


    def __init__(self, value):
        super().__init__(value)
        if value:
            self.validate_birthday()

class Phone(Field):
    def validate_phone(self):
        if not self._value.isdigit() or len(self._value) != 10:
            raise ValueError("Неправильний номер телефону. Він повинен містити 10 цифр.")
        
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value
        self.validate_phone()

    def __init__(self, value):
        super().__init__(value)
        self.validate_phone()

class Record:
    def __init__(self, name, birthday = None ):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday) if birthday else None

    def add_phone(self, phone):
        new_phone = Phone(phone)
        new_phone.validate_phone()
        self.phones.append(new_phone)

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        # Перевіряємо чи існує номер телефону для редагування
        if old_phone not in [phone.value for phone in self.phones]:
            raise ValueError("Номер телефону не існує у записі.")

        #  валідність нового номера телефону
        new_phone_obj = Phone(new_phone)

        # Замінюємо старий номер новим
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone_obj.value
                break

    def find_phone(self, value):
        for phone in self.phones:
            if value == phone.value:
                return phone
            
    def days_to_birthday(self):
        if self.birthday:
            today = datetime.now()
            next_birthday = datetime(today.year, self.birthday.value.month, self.birthday.value.day)
            if today > next_birthday:
                next_birthday = datetime(today.year + 1, self.birthday.value.month, self.birthday.value.day)
            days_left = (next_birthday - today).days
            return days_left
        return None

    def __str__(self):
        phones_str = '; '.join(str(p) for p in self.phones)
        return f"Contact name: {self.name.value}, phones: {phones_str}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def iterator(self, page_size=5):
        all_records = list(self.data.values())
        for i in range(0, len(all_records), page_size):
            yield all_records[i:i + page_size]
        
book = AddressBook()

john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")

book.add_record(john_record)

jane_record = Record("Jane")
jane_record.add_phone("9876543210")

book.add_record(jane_record)

for name, record in book.data.items():
    print(record)

john = book.find("John")
john.edit_phone("1234567890", "1112223333")

print(john)

found_phone = john.find_phone("5555555555")
print(f"{john.name.value}: {found_phone}")

book.delete("Jane")

