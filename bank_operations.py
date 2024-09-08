from sqlalchemy.orm import sessionmaker
from config import engine, User
from functools import wraps
from contextlib import contextmanager
from datetime import datetime
from sqlalchemy import update


Session = sessionmaker(bind=engine)


class BankAccount:
    """Класс для выполнения банковских операций с личным кабинетом"""


    @contextmanager
    def open_session(self):
        """Автоматическая работа с сессей базы данных"""
        session = Session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            return f'Ошибка соединения с базой данных!'
        finally:
            session.close()


    def authenticated(func):
        """Декоратор авторизации"""
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if not self.valid:
                return f'Необходимо пройти аунтификацию!'
            return func
        return wrapper


    def registate_user(self, phone_number: str, full_name: str, card_number: int, card_password: int):
        """Регистрация нового пользователя"""
        self.__balance = 0.0
        self.owner_full_name = full_name
        self.__owner_phone_number = phone_number
        self.__owner_card_number = card_number
        self.__owner_card_password = card_password
        self.auth = False
        self.add_user()


    def login(self, input_card_number: int, input_card_password: int) -> str:
        """Вход в аккаунт"""
        with self.open_session() as session:
            user = session.query(User).filter_by(
                card_password=input_card_password,
                card_number=input_card_number
            ).first()
            if user:
                user.auth = True
                return f'Вы успешно вошли в аккаунт'
            return f'Введены неверные данные'


    def logout(self, input_card_number: int):
        """Выход из аккаунта"""
        with self.open_session() as session:
            user = update(User).where(User.card_number == input_card_number).values(auth=False)
            result = session.execute(user)
            if result.rowcount > 0:
                return 'Вы успешно вышли из аккаунта'
            return 'Пользователь с таким номером карты не найден'


    @authenticated
    def deposit(self, value: float) -> str:
        """Пополнение баланса"""
        self.__balance += value
        self.update_balance()
        return f'{self.owner_full_name}, на ваш счет поступило {value}, баланс составляет {round(self.__balance, 2)}'

    @authenticated
    def withdraw(self, value: float) -> str:
        """Вывод с баланса"""
        if value <= self.__balance:
            self.__balance -= value
            self.update_balance()
            return f'{self.owner_full_name}, с вашего счета списано {value}, баланс составляет {round(self.__balance, 2)}'
        elif value > self.__balance:  # Варн нехватки средств
            return f'У вас на счете недостаточно средств для вывода!'

    @authenticated
    def get_balance(self) -> str:
        """Отображение баланса"""
        return f"{self.owner_full_name}, ваш баланс составляет {self.__balance}"


    def update_balance(self) -> None:
        """Пополнение баланса в БД"""
        with self.open_session() as session:
            user = session.query(User).filter_by(name=self.owner_full_name, card_number=self.__owner_card_number).first()
            if user:
                user.balance = self.__balance


    def add_user(self) -> None:
        """Добавление пользователя в БД"""
        with self.open_session() as session:
            user = session.query(User).filter_by(name=self.owner_full_name, card_number=self.__owner_card_number).first()
            if not user:
                new_user = User(
                    name=self.owner_full_name,
                    card_number=self.__owner_card_number,
                    card_password=self.__owner_card_password,
                    balance=self.__balance,
                    phone_number=self.__owner_phone_number
                )
                session.add(new_user)
            else:
                return f'Такой пользователь уже существует!'

    def logger(self):
        current_time = datetime.now()
        with open('logs.txt', 'a') as file:
            file.write(f'\n--------------------------------------'
                       f'\n{current_time} / {self.login(522, 2552)}'
                       f'\n{current_time} / {self.deposit(100)}'
                       f'\n{current_time} / {self.get_balance()}'
                       f'\n{current_time} / {self.withdraw(700)}'
                       f'\n{current_time} / {self.get_balance()}'
                       f'\n{current_time} / {self.withdraw(130)}'
                       f'\n{current_time} / {self.logout(522)}'
                       f'\n---------------------------------------'
                       )


if __name__ == '__main__':
    account = BankAccount()
    account.logger()

    #print(account.get_balance())
    #print(account.withdraw(700))
    #print(account.get_balance())
    #print(account.withdraw(130))


