class BankAccount:
    """Класс для выполнения банковских операций с аунтификацией по ФИО"""
    def __init__(self, __balance = 0.0, owner_fio = 'Иванов Иван Иванович'):
        self.__balance = __balance
        self.owner_fio = owner_fio

    def deposit(self, value: float, fio: str):
        """Если пользователь ввел корректное ФИО, то введеная им сумма зачислится на счет"""
        if fio == self.owner_fio:
            self.__balance += value
            return f'{self.owner_fio}, на ваш счет поступило {value}, баланс составляет {round(self.__balance, 2)}'
        elif fio != self.owner_fio: # Если ФИО не верное то отобразится предупреждение
            return f'Такой пользователь не найден!'

    def withdraw(self, value: float, fio: str):
        """Если пользователь ввел корректное ФИО, то введеная им сумма выведется со счета"""
        if fio == self.owner_fio and value <= self.__balance:
            self.__balance -= value
            return f'{self.owner_fio}, с вашего счета списано {value}, баланс составляет {round(self.__balance, 2)}'
        elif fio == self.owner_fio and value > self.__balance: # Если на счете недостаточно средств, то отобразится предупреждение
            return f'У вас на счете недостаточно средств для вывода!'
        elif fio != self.owner_fio: # Если ФИО не верное то отобразится предупреждение
            return f'Такой пользователь не найден!'

    def get_balance(self, fio: str):
        """Если пользователь ввел корректное ФИО, то баланс его счета отобразится"""
        if fio == self.owner_fio:
            return f'{self.owner_fio}, ваш баланс составляет {self.__balance}'
        else: # Если ФИО не верное то отобразится предупреждение
            return f'Такой пользователь не найден!'


account = BankAccount(520.5, 'Денисов Денис Денисович')
print(account.get_balance('Денисов Денис Денисович'))
print(account.deposit(40.2, 'Денисов Денис Денисович'))
print(account.withdraw(5230,'Денисов Денис Денисович'))
print(account.withdraw(52,'Денисов Денис Денисович'))
