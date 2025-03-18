import argparse
from db import create_table
from models import Employee, EmployeeGenerator


def main():
    parser = argparse.ArgumentParser(description="Employee Management CLI")
    parser.add_argument("mode", type=int, help="Режим работы приложения (1-5)")
    parser.add_argument("full_name", nargs="?", type=str,
                        help="ФИО сотрудника")
    parser.add_argument("birth_date", nargs="?", type=str,
                        help="Дата рождения (YYYY-MM-DD)")
    parser.add_argument("gender", nargs="?", type=str,
                        choices=["Male", "Female"], help="Пол сотрудника")

    args = parser.parse_args()

    if args.mode == 1:
        create_table()
        print("Таблица сотрудников <employees> создана.")

    elif args.mode == 2:
        if not all([args.full_name, args.birth_date, args.gender]):
            print("Ошибка: необходимо указать ФИО, дату рождения и пол.\n "
                  "Попробуйте снова.")
            return
        employee = Employee(args.full_name, args.birth_date, args.gender)
        employee.save()
        print(f"Сотрудник {args.full_name} добавлен.")
    elif args.mode == 3:
        Employee.get_all()
    elif args.mode == 4:
        employees = EmployeeGenerator.generate_employees()
        special_employees = EmployeeGenerator.generate_special_employees()
        EmployeeGenerator.bulk_insert(employees + special_employees)
        print("Добавлено 1_000_000 + 100 записей.")
    elif args.mode == 5:
        elapsed_time = EmployeeGenerator.find_male_with_f()
        print(f"Время выполнения запроса: {elapsed_time:.4f} сек.")
    else:
        print("Неизвестный режим.")


if __name__ == "__main__":
    main()
