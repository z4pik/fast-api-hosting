import databases  # Позволяет выполнять асинхронные запросы в БД
import sqlalchemy


# Сonnect db
metadata = sqlalchemy.MetaData()  # Работаем с ядром для генерации sql запросов
database = databases.Database("sqlite:///sqlite.db")  # Указываем бд
engine = sqlalchemy.create_engine("sqlite:///sqlite.db")

