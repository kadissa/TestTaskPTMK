import random
import time
from datetime import datetime

import psycopg2
from faker import Faker
from psycopg2.extras import execute_values

from core import connect_db

fake = Faker()


class Employee:
    def __init__(self, full_name: str, birth_date: str, gender: str):
        self.full_name = full_name
        self.birth_date = datetime.strptime(birth_date, "%Y-%m-%d").date()
        self.gender = gender

    def save(self):
        """Сохраняет сотрудника в базу данных."""
        with connect_db() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "INSERT INTO employees (full_name, birth_date, gender) "
                    "VALUES (%s, %s, %s) ON CONFLICT DO NOTHING;",
                    (self.full_name, self.birth_date, self.gender),
                )
                conn.commit()
            except psycopg2.Error as e:
                print("Ошибка при сохранении сотрудника:", e)

    def calculate_age(self):
        """Рассчитывает возраст (полных лет)."""
        today = datetime.today().date()
        age = today.year - self.birth_date.year - (
                (today.month, today.day) < (
                 self.birth_date.month, self.birth_date.day)
        )
        return age

    @staticmethod
    def get_all():
        """Выводит всех сотрудников, отсортированных по ФИО."""
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT DISTINCT full_name, birth_date, gender FROM employees "
                "ORDER BY full_name;")
            employees = cursor.fetchall()
            if not employees:
                print("Список сотрудников пуст.")

            print("\nСписок сотрудников:")
            for staff_member in employees:
                birth_date = staff_member[1].strftime("%Y-%m-%d")
                # print(f'{staff_member=}', birth_date)
                age = Employee(staff_member[0], str(birth_date),
                               staff_member[2]).calculate_age()
                print(
                    f"{staff_member[0]} | {birth_date} | {staff_member[2]} | "
                    f"Возраст(полных лет): {age}")

    @staticmethod
    def delete_f():
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM employees WHERE full_name LIKE 'F%'"
            )
            conn.commit()


class EmployeeGenerator:
    @staticmethod
    def generate_employees(n=1_000_000):
        """Генерирует список сотрудников с равномерным распределением пола."""
        employees = []
        for _ in range(n):
            gender = random.choice(["Male", "Female"])
            full_name = fake.name_male() if gender == "Male" else fake.name_female()
            birth_date = fake.date_of_birth(minimum_age=18,
                                            maximum_age=65).strftime(
                "%Y-%m-%d")
            employees.append(Employee(full_name, birth_date, gender))
        return employees

    @staticmethod
    def generate_special_employees(n=100):
        """Генерирует 100 сотрудников, где пол - мужской, а фамилия начинается на 'F'."""
        employees = []
        for _ in range(n):
            full_name = f"F{fake.last_name()} {fake.first_name_male()} {fake.last_name()}"
            birth_date = fake.date_of_birth(minimum_age=18,
                                            maximum_age=65).strftime(
                "%Y-%m-%d")
            employees.append(Employee(full_name, birth_date, "Male"))
        return employees

    @staticmethod
    def bulk_insert(employees):
        """Пакетная вставка данных в БД."""
        with connect_db() as conn:
            cursor = conn.cursor()
            data = [(emp.full_name, emp.birth_date, emp.gender) for emp in
                    employees]
            query = """
            INSERT INTO employees (full_name, birth_date, gender) 
            VALUES %s
            ON CONFLICT DO NOTHING;
            """
            execute_values(cursor, query, data)
            conn.commit()

    @staticmethod
    def find_male_with_f():
        """
        Находит сотрудников с полом 'Male' и фамилией, начинающейся с 'F'.
        Замеряет время выполнения.
        """
        with connect_db() as conn:
            cursor = conn.cursor()
            query = """
                SELECT full_name, birth_date, gender FROM employees
                WHERE gender = 'Male' AND full_name LIKE 'F%';
                """
            start_time = time.time()
            cursor.execute(query)
            elapsed_time = time.time() - start_time
            return elapsed_time

