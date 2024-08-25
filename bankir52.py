from typing import Optional

class BankAccount:
    """Класс для выполнения банковских операций с аунтификацией по ФИО"""
    def __init__(self, __balance: float, owner_full_name: str):
        self.__balance = __balance
        self.owner_full_name = owner_full_name
        self.valid = False


    def validate(self, full_name: str) -> Optional[str]:
        """Аунтификация по ФИО"""
        if full_name == self.owner_full_name:
            self.valid = True
            return f'Вы успешно вошли в аккаунт'
        elif full_name != self.owner_full_name: # Предупреждение если ФИО неправильное
            return f'Такой пользователь не найден!'


    def deposit(self, value: float) -> Optional[str]:
        """Пополнение баланса"""
        if self.valid == True:
            self.__balance += value
            return f'{self.owner_full_name}, на ваш счет поступило {value}, баланс составляет {round(self.__balance, 2)}'


    def withdraw(self, value: float) -> Optional[str]:
        """Вывод с баланса"""
        if self.valid == True:
            if value <= self.__balance:
                self.__balance -= value
                return f'{self.owner_full_name}, с вашего счета списано {value}, баланс составляет {round(self.__balance, 2)}'
            elif value > self.__balance: # Предупреждение нехватки средств
                return f'У вас на счете недостаточно средств для вывода!'


    def get_balance(self) -> Optional[str]:
        """Отображение баланса"""
        if self.valid == True:
            return f"{self.owner_full_name}, ваш баланс составляет {self.__balance}"


account = BankAccount(520.0,'Денисов Денис Денисович')
account.validate('Денисов Денис Денисович')
account.get_balance()
account.deposit(50)
account.withdraw(700)
account.get_balance()
account.withdraw(73)
