from typing import Optional
from sqlalchemy.orm import sessionmaker
from config import engine, User



Session = sessionmaker(bind=engine)


class BankAccount:
    """Класс для выполнения банковских операций с аунтификацией по ФИО"""
    def __init__(self, __balance: float, owner_full_name: str, card_number: int, card_password: int):
        self.__balance = __balance
        self.owner_full_name = owner_full_name
        self.card_number = card_number
        self.card_password = card_password
        self.valid = False
        self.add_user()


    def validate(self, input_card_password: int) -> Optional[str]:
        """Аунтификация по паролю"""
        if input_card_password == self.card_password:
            self.valid = True
            return f'Вы успешно вошли в аккаунт'
        elif input_card_password != self.owner_full_name: # Предупреждение если пароль неправильное
            return f'Пароль неправильный!'


    def deposit(self, value: float) -> Optional[str]:
        """Пополнение баланса"""
        if self.valid == True:
            self.__balance += value
            self.update_balance_in_db()
            return f'{self.owner_full_name}, на ваш счет поступило {value}, баланс составляет {round(self.__balance, 2)}'
        return 'Необходимо пройти аунтификацию'


    def withdraw(self, value: float) -> Optional[str]:
        """Вывод с баланса"""
        if self.valid == True:
            if value <= self.__balance:
                self.__balance -= value
                self.update_balance()
                return f'{self.owner_full_name}, с вашего счета списано {value}, баланс составляет {round(self.__balance, 2)}'
            elif value > self.__balance: # Предупреждение нехватки средств
                return f'У вас на счете недостаточно средств для вывода!'
        return 'Необходимо пройти аунтификацию'


    def get_balance(self) -> Optional[str]:
        """Отображение баланса"""
        if self.valid == True:
            return f"{self.owner_full_name}, ваш баланс составляет {self.__balance}"


    def update_balance(self) -> Optional[str]:
        session = Session()
        try:
            user = session.query(User).filter_by(full_name=self.owner_full_name).first()
            if user:
                user.balance = self.__balance
                session.commit()
        except Exception:
            session.rollback()
            print('Ошибка соединения с базой данных!')
        finally:
            session.close()


    def add_user(self) -> Optional[str]:
        session = Session()
        try:
            user = session.query(User).filter_by(name=self.owner_full_name, card_number=self.card_number).first()
            if not user:
                new_user = User(
                    name=self.owner_full_name,
                    card_number=self.card_number,
                    card_password=self.card_password,
                    balance=self.__balance
                )
                session.add(new_user)
                session.commit()
            else:
                return 'Такой пользователь уже существует!'

        except Exception as e:
            session.rollback()
            print('Ошибка соединения с базоый данных:', e)
        finally:
            session.close()


account = BankAccount(520.0,'Денисов Денис Денисович', 52,2552)
account.validate('Денисов Денис Денисович')
account.get_balance()
account.deposit(50)
account.withdraw(700)
account.get_balance()
account.withdraw(73)