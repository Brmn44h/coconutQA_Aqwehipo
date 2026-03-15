import os
import sys
sys.path.insert(0, r"C:\Users\BrmnY\coconutQA_Aqwehipo")
import psycopg2
from Cinemascope.resources.db_creds import DBCreds



def connect_to_postgres():

    connection = None
    cursor = None

    try:
        connection = psycopg2.connect(**DBCreds.get_connection_params())

        cursor = connection.cursor()


    except psycopg2.OperationalError as e:
        print(f"\n❌ Ошибка подключения: {e}")

    except Exception as e:
        print(f"\n❌ Непредвиденная ошибка: {e}")

    finally:
        # Закрытие соединения
        if cursor:
            cursor.close()
            print("\n🔒 Курсор закрыт")
        if connection:
            connection.close()
            print("🔒 Соединение с PostgreSQL закрыто")


def print_env_help():
    """Помощь по настройке .env файла"""
    print("\n📝 ДЛЯ НАСТРОЙКИ ПОДКЛЮЧЕНИЯ:")
    print("=" * 40)
    print("Создайте файл .env в корне проекта:")
    print("""
    DB_NAME=your_database
    DB_USER=your_username
    DB_PASSWORD=your_password
    DB_HOST=your_host
    DB_PORT=your_port
    """)
    print("Или просто задайте переменные окружения в системе")


if __name__ == "__main__":
    print("🚀 ТЕСТ ПОДКЛЮЧЕНИЯ К POSTGRESQL")
    print("=" * 40)
    connect_to_postgres()

    # Проверяем, загружены ли переменные
    if not os.getenv("DB_NAME"):
        print_env_help()

