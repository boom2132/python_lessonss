from sqlalchemy.orm import sessionmaker
from config import engine, User
from functools import wraps
from contextlib import contextmanager

Session = sessionmaker(bind=engine)


class BankAccount:
    """Класс для выполнения банковских операций с аунтификацией по ФИО"""
    def __init__(self, __balance: float, owner_full_name: str, card_number: int, card_password: int):
        self.__balance = __balance
        self.owner_full_name = owner_full_name
        self.owner_card_number = card_number
        self.owner_card_password = card_password
        self.valid = False
        self.add_user()

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
            return func(self, *args, **kwargs)
        return wrapper


    def authenticate_user(self, full_name, input_card_number, input_card_password: int) -> str:
        """Аунтификация по паролю к карте"""
        with self.open_session() as session:
            user = session.query(User).filter_by(
                name=full_name,
                card_password=input_card_password,
                card_number=input_card_number
            ).first()
            if user:
                self.valid = True
                return f'Вы успешно вошли в аккаунт'
            return f'Введены неверные данные'


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
            user = session.query(User).filter_by(name=self.owner_full_name, card_number=self.owner_card_number).first()
            if user:
                user.balance = self.__balance


    def add_user(self) -> None:
        """Добавление пользователя в БД"""
        with self.open_session() as session:
            user = session.query(User).filter_by(name=self.owner_full_name, card_number=self.owner_card_number).first()
            if not user:
                new_user = User(
                    name=self.owner_full_name,
                    card_number=self.owner_card_number,
                    card_password=self.owner_card_password,
                    balance=self.__balance
                )
                session.add(new_user)
            else:
                return f'Такой пользователь уже существует!'



account = BankAccount(320.0,'Иванов Денис Денисович', 522,2552)
account.authenticate_user('Иванов Денис Денисович', 522,2552)
#print(account.get_balance())
print(account.deposit(523))
print(account.get_balance())
#print(account.withdraw(700))
#print(account.get_balance())
#print(account.withdraw(130))