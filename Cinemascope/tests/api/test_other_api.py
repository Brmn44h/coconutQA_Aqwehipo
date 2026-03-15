from sqlalchemy.orm import Session
import pytest
from Cinemascope.utils.data_generator import Datagenerator
from db_requester.models import AccountTransactionTemplate
def test_accounts_transaction_template(db_session: Session):
    # ====================================================================== Подготовка к тесту
    # Создаем новые записи в базе данных (чтоб точно быть уверенными что в базе присутствуют данные для тестирования)

    stan = AccountTransactionTemplate(user=f"Stan_{Datagenerator.generate_random_int(10)}", balance=100)
    bob = AccountTransactionTemplate(user=f"Bob_{Datagenerator.generate_random_int(10)}", balance=500)

    # Добавляем записи в сессию
    db_session.add_all([stan, bob])
    # Фиксируем изменения в базе данных
    db_session.commit()
    stan_initial_balance = stan.balance
    bob_initial_balance = bob.balance

    def transfer_money(session, from_account, to_account, amount):
        # пример функции выполняющей транзакцию
        # представим что она написана на стороне тестируемого сервиса
        # и вызывая метод transfer_money, мы какбудтобы делем запрос в api_manager.movies_api.transfer_money
        """
        Переводит деньги с одного счета на другой.
        :param session: Сессия SQLAlchemy.
        :param from_account_id: ID счета, с которого списываются деньги.
        :param to_account_id: ID счета, на который зачисляются деньги.
        :param amount: Сумма перевода.
        """
        # Получаем счета
        from_account = session.query(AccountTransactionTemplate).filter_by(user=from_account).one()
        to_account = session.query(AccountTransactionTemplate).filter_by(user=to_account).one()

        # Проверяем, что на счете достаточно средств
        if from_account.balance < amount:
            raise ValueError("Недостаточно средств на счете")

        # Выполняем перевод
        from_account.balance -= amount
        to_account.balance += amount

        # Сохраняем изменения
        session.commit()

    # ====================================================================== Тест
    # Проверяем начальные балансы
    assert stan.balance == 100
    assert bob.balance == 500

    try:
        transfer_money(db_session, from_account=stan.user, to_account=bob.user, amount=200)
        pytest.fail("Должна была быть ошибка!")
    except ValueError as e:
        assert "Недостаточно средств" in str(e)
        print(f"\n✅ Получена ожидаемая ошибка: {e}")

    # ====================================================================== ВАЛИДАЦИЯ
    # Проверяем, что балансы в БД НЕ ИЗМЕНИЛИСЬ
    db_session.refresh(stan)
    db_session.refresh(bob)

    assert stan.balance == stan_initial_balance, "❌ Баланс Стена изменился!"
    assert bob.balance == bob_initial_balance, "❌ Баланс Боба изменился!"

    print(f"\n✅ ВАЛИДАЦИЯ ПРОЙДЕНА:")
    print(f"   Баланс Стена: {stan.balance} (не изменился)")
    print(f"   Баланс Боба: {bob.balance} (не изменился)")
    print(f"   Деньги остались на месте у каждого")

    # ====================================================================== Очистка
    db_session.delete(stan)
    db_session.delete(bob)
    db_session.commit()


