from database import fetch_query, execute_query, create_user, authenticate_user
from database import create_user, authenticate_user

def user_register():
    username = input("Имя пользователя: ")
    email = input("Почта: ")
    password = input("Пароль: ")
    password_confirm = input("Подтвердите пароль: ")

    if password != password_confirm:
        print("Ошибка: Пароли не совпадают.")
        return

    if create_user(username, email, password, "user"):
        print("Регистрация успешна!")
    else:
        print("Ошибка: Имя пользователя или почта уже заняты.")

def user_login():
    email = input("Почта: ")
    password = input("Пароль: ")

    user = authenticate_user(email, password)
    if user and user[0][4] == "user":
        print("Авторизация успешна!")
        user_menu(user[0][0])
    else:
        print("Неверная почта или пароль.")

def user_menu(user_id):
    while True:
        print("\n1. Просмотреть инвентарь")
        print("2. Создать заявку на получение инвентаря")
        print("3. Отслеживание статуса заявок")
        print("4. Создать заявку на ремонт")
        print("5. Выйти")
        choice = input("Выберите действие: ")

        if choice == '1':
            view_inventory()
        elif choice == '2':
            create_request(user_id)
        elif choice == '3':
            track_requests(user_id)
        elif choice == '4':
            create_repair_request(user_id)
        elif choice == '5':
            break
        else:
            print("Неверный выбор.")

def view_inventory():
    inventory = fetch_query('SELECT * FROM inventory')
    print("\nДоступный инвентарь:")
    for item in inventory:
        print(f"ID: {item[0]}, Название: {item[1]}, Количество: {item[2]}, Состояние: {item[3]}")

def create_request(user_id):
    while True:
        try:
            item_id = int(input("Введите ID инвентаря для заявки: "))
            
            # Проверяем, существует ли инвентарь с таким ID
            inventory_item = fetch_query('SELECT * FROM inventory WHERE id = ?', (item_id,))
            if not inventory_item:
                print("Ошибка: Инвентарь с таким ID не найден.")
                continue  # Запрашиваем ввод заново

            # Проверяем, доступен ли инвентарь
            quantity = inventory_item[0][2]  # Количество инвентаря
            if quantity <= 0:
                print("Ошибка: Инвентарь недоступен (количество: 0).")
                continue  # Запрашиваем ввод заново

            break  # Если инвентарь доступен, выходим из цикла
        except ValueError:
            print("Ошибка: Введите числовое значение для ID инвентаря.")

    execute_query('INSERT INTO requests (user_id, item_id, status) VALUES (?, ?, "pending")', (user_id, item_id))
    print("Заявка создана!")

def track_requests(user_id):
    requests = fetch_query('SELECT * FROM requests WHERE user_id = ?', (user_id,))
    print("\nВаши заявки:")
    for req in requests:
        print(f"ID: {req[0]}, ID инвентаря: {req[2]}, Статус: {req[3]}")

def create_repair_request(user_id):
    while True:
        try:
            item_id = int(input("Введите ID инвентаря для заявки на ремонт: "))
            
            # Проверяем, существует ли инвентарь с таким ID
            inventory_item = fetch_query('SELECT * FROM inventory WHERE id = ?', (item_id,))
            if not inventory_item:
                print("Ошибка: Инвентарь с таким ID не найден.")
                continue  # Запрашиваем ввод заново

            break  # Если инвентарь существует, выходим из цикла
        except ValueError:
            print("Ошибка: Введите числовое значение для ID инвентаря.")

    execute_query('INSERT INTO requests (user_id, item_id, status) VALUES (?, ?, "repair")', (user_id, item_id))
    print("Заявка на ремонт создана!")