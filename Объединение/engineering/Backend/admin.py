from database import execute_query, fetch_query, authenticate_user, sqlite3  # Добавлен импорт sqlite3
from database import authenticate_user

def admin_login():
    email = input("Почта: ")
    password = input("Пароль: ")

    user = authenticate_user(email, password)
    if user and user[0][4] == "admin":
        print("Авторизация успешна!")
        admin_menu()
    else:
        print("Неверная почта, пароль или недостаточно прав.")

def admin_menu():
    while True:
        print("\n1. Добавить инвентарь")
        print("2. Редактировать инвентарь")
        print("3. Планирование закупок")
        print("4. Создать отчет")
        print("5. Выйти")
        choice = input("Выберите действие: ")

        if choice == '1':
            add_inventory()
        elif choice == '2':
            edit_inventory()
        elif choice == '3':
            plan_purchase()
        elif choice == '4':
            generate_report()
        elif choice == '5':
            break
        else:
            print("Неверный выбор.")

def add_inventory():
    name = input("Введите название инвентаря: ")
    quantity = int(input("Введите количество: "))
    status = input("Введите состояние (new, used, broken): ")

    execute_query('INSERT INTO inventory (name, quantity, status) VALUES (?, ?, ?)', (name, quantity, status))
    print("Инвентарь добавлен!")

def edit_inventory():
    item_id = int(input("Введите ID инвентаря для редактирования: "))
    
    # Проверяем, существует ли инвентарь с таким ID
    inventory_item = fetch_query('SELECT * FROM inventory WHERE id = ?', (item_id,))
    if not inventory_item:
        print("Ошибка: Инвентарь с таким ID не найден.")
        return  # Выходим из функции

    name = input("Введите новое название (оставьте пустым, чтобы не изменять): ").strip()
    quantity = input("Введите новое количество (оставьте пустым, чтобы не изменять): ").strip()
    status = input("Введите новое состояние (new, used, broken) (оставьте пустым, чтобы не изменять): ").strip()

    conn = sqlite3.connect('sport_inventory.db')
    cursor = conn.cursor()

    if name:
        cursor.execute('UPDATE inventory SET name = ? WHERE id = ?', (name, item_id))
    if quantity:  # Проверяем, не пустое ли поле количества
        try:
            quantity_int = int(quantity)  # Преобразуем в целое число
            cursor.execute('UPDATE inventory SET quantity = ? WHERE id = ?', (quantity_int, item_id))
        except ValueError:
            print("Ошибка: Введите корректное числовое значение для количества.")
    if status:
        cursor.execute('UPDATE inventory SET status = ? WHERE id = ?', (status, item_id))

    conn.commit()
    conn.close()
    print("Инвентарь обновлен!")

def plan_purchase():
    while True:
        try:
            item_id = int(input("Введите ID инвентаря для закупки: "))
            
            # Проверяем, существует ли инвентарь с таким ID
            inventory_item = fetch_query('SELECT * FROM inventory WHERE id = ?', (item_id,))
            if not inventory_item:
                print("Ошибка: Инвентарь с таким ID не найден.")
                continue  # Запрашиваем ввод заново

            supplier = input("Введите название поставщика: ")

            # Убираем все нечисловые символы (например, "р", "руб", пробелы)
            price_input = input("Введите цену: ").replace("р", "").replace("руб", "").strip()
            price = float(price_input)  # Преобразуем в число

            # Проверяем, что цена положительная
            if price <= 0:
                print("Ошибка: Цена должна быть положительной.")
                continue  # Запрашиваем ввод заново

            break  # Если все данные корректны, выходим из цикла
        except ValueError:
            print("Ошибка: Введите корректное числовое значение для цены.")

    execute_query('INSERT INTO purchases (item_id, supplier, price) VALUES (?, ?, ?)', (item_id, supplier, price))
    print("Закупка запланирована!")

def generate_report():
    inventory = fetch_query('SELECT * FROM inventory')
    purchases = fetch_query('SELECT * FROM purchases')

    print("\nОтчет по инвентарю:")
    for item in inventory:
        print(f"ID: {item[0]}, Название: {item[1]}, Количество: {item[2]}, Состояние: {item[3]}")

    print("\nОтчет по закупкам:")
    for purchase in purchases:
        print(f"ID: {purchase[0]}, ID инвентаря: {purchase[1]}, Поставщик: {purchase[2]}, Цена: {purchase[3]}")