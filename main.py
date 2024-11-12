import threading
from random import randint
from time import sleep


class Bank:
    def __init__(self, balance):
        self.balance = balance
        self.lock = threading.Lock()

    def deposit(self):
        for transaction in range(1, 101):
            replenishment = randint(50, 500)
            if self.balance >= 500 and self.lock.locked():
                self.lock.release()
                self.balance += replenishment
                sleep(0.001)
                print(f'Пополнение{replenishment}. Баланс: {self.balance}')

            else:
                self.balance += replenishment
                sleep(0.001)
                print(f'Пополнение {replenishment}. Баланс: {self.balance}')

    def take(self):
        for t in range(1, 101):
            take = randint(50, 500)
            print(f'Запрос на {take}')
            if take > self.balance:
                sleep(0.001)
                print(f'Запрос отклонён, недостаточно средств')
                self.lock.acquire()
            else:
                self.balance -= take
                sleep(0.001)
                print(f'Снятие: {take}. Баланс: {self.balance}')


bk = Bank(0)

# Т.к. методы принимают self, в потоки нужно передать сам объект класса Bank
th1 = threading.Thread(target=Bank.deposit, args=(bk,))
th2 = threading.Thread(target=Bank.take, args=(bk,))

th1.start()
th2.start()
th1.join()
th2.join()

print(f'Итоговый баланс: {bk.balance}')
