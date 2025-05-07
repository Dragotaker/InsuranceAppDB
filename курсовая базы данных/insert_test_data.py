import psycopg2
from datetime import datetime
import hashlib
from dotenv import load_dotenv
import os

# Загрузка переменных окружения
load_dotenv()

# Настройки подключения к базе данных
DB_CONFIG = {
    'database': os.getenv('DB_NAME', 'insurance_db'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'drago'),
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', '5432'))
}

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def insert_test_data():
    try:
        # Подключение к базе данных
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        print("Начинаем вставку тестовых данных...")
        
        # 1. Категории страхования (не зависит от других таблиц)
        print("Вставляем категории страхования...")
        categories = [
            ('Автострахование', 'Страхование автомобилей от ущерба и угона', 5000.00),
            ('Медицинское страхование', 'Страхование здоровья и медицинских расходов', 3000.00),
            ('Страхование имущества', 'Страхование жилья и имущества от повреждений', 2000.00),
            ('Страхование жизни', 'Страхование жизни и здоровья', 4000.00),
            ('Страхование путешествий', 'Страхование во время поездок', 1500.00)
        ]
        category_ids = []
        for category in categories:
            cur.execute(
                "INSERT INTO insurance.category_insurances (category_name, description, base_rate) VALUES (%s, %s, %s) RETURNING category_id",
                category
            )
            category_ids.append(cur.fetchone()[0])
        
        # 2. Клиенты (не зависит от других таблиц)
        print("Вставляем клиентов...")
        clients = [
            ('Иванов Иван Иванович', 'ул. Ленина, 1', '+7(999)111-22-33', 'ivanov@mail.ru', '1990-01-15', '1234 567890'),
            ('Петров Петр Петрович', 'ул. Пушкина, 2', '+7(999)222-33-44', 'petrov@mail.ru', '1985-05-20', '2345 678901'),
            ('Сидорова Анна Сергеевна', 'ул. Гагарина, 3', '+7(999)333-44-55', 'sidorova@mail.ru', '1995-08-10', '3456 789012'),
            ('Козлов Алексей Николаевич', 'ул. Королева, 4', '+7(999)444-55-66', 'kozlov@mail.ru', '1988-12-25', '4567 890123'),
            ('Морозова Елена Владимировна', 'ул. Циолковского, 5', '+7(999)555-66-77', 'morozova@mail.ru', '1992-03-30', '5678 901234')
        ]
        client_ids = []
        for client in clients:
            cur.execute(
                "INSERT INTO insurance.clients (full_name, address, phone_number, email, birth_date, passport_data) VALUES (%s, %s, %s, %s, %s, %s) RETURNING client_id",
                client
            )
            client_ids.append(cur.fetchone()[0])
        
        # 3. Сотрудники (не зависит от других таблиц)
        print("Вставляем сотрудников...")
        employees = [
            ('Смирнов Александр Петрович', 'Менеджер', '+7(999)666-77-88', 'smirnov@mail.ru', '2020-01-01'),
            ('Кузнецова Мария Ивановна', 'Страховой агент', '+7(999)777-88-99', 'kuznetsova@mail.ru', '2021-02-15'),
            ('Новиков Дмитрий Сергеевич', 'Специалист по урегулированию', '+7(999)888-99-00', 'novikov@mail.ru', '2022-03-20'),
            ('Волкова Ольга Александровна', 'Страховой агент', '+7(999)999-00-11', 'volkova@mail.ru', '2023-04-25'),
            ('Лебедев Игорь Николаевич', 'Менеджер', '+7(999)000-11-22', 'lebedev@mail.ru', '2024-01-10')
        ]
        employee_ids = []
        for employee in employees:
            cur.execute(
                "INSERT INTO insurance.employees (full_name, position, phone_number, email, hire_date) VALUES (%s, %s, %s, %s, %s) RETURNING employee_id",
                employee
            )
            employee_ids.append(cur.fetchone()[0])
        
        # 4. Пользователи для клиентов (зависит от clients)
        print("Вставляем пользователей для клиентов...")
        client_users = [
            ('ivanov', hash_password('password'), 1, client_ids[0]),
            ('petrov', hash_password('password'), 1, client_ids[1]),
            ('sidorova', hash_password('password'), 1, client_ids[2]),
            ('kozlov', hash_password('password'), 1, client_ids[3]),
            ('morozova', hash_password('password'), 1, client_ids[4])
        ]
        for user in client_users:
            cur.execute(
                "INSERT INTO insurance.users (username, password_hash, role_id, client_id) VALUES (%s, %s, %s, %s)",
                user
            )
        
        # 5. Пользователи для сотрудников (зависит от employees)
        print("Вставляем пользователей для сотрудников...")
        employee_users = [
            ('smirnov', hash_password('password'), None, employee_ids[0]),
            ('kuznetsova', hash_password('password'), None, employee_ids[1]),
            ('novikov', hash_password('password'), None, employee_ids[2]),
            ('volkova', hash_password('password'), None, employee_ids[3]),
            ('lebedev', hash_password('password'), None, employee_ids[4])
        ]
        for user in employee_users:
            cur.execute(
                "INSERT INTO insurance.users (username, password_hash, role_id, employee_id) VALUES (%s, %s, %s, %s)",
                user
            )
        
        # 6. Страховые полисы (зависит от clients и category_insurances)
        print("Вставляем страховые полисы...")
        policies = [
            ('POL-001', client_ids[0], category_ids[0], '2024-01-01', '2025-01-01', 1000000.00, 5000.00, 'active'),
            ('POL-002', client_ids[1], category_ids[1], '2024-02-01', '2025-02-01', 500000.00, 3000.00, 'active'),
            ('POL-003', client_ids[2], category_ids[2], '2024-03-01', '2025-03-01', 750000.00, 2000.00, 'active'),
            ('POL-004', client_ids[3], category_ids[3], '2024-04-01', '2025-04-01', 2000000.00, 4000.00, 'active'),
            ('POL-005', client_ids[4], category_ids[4], '2024-05-01', '2025-05-01', 300000.00, 1500.00, 'active')
        ]
        policy_ids = []
        for policy in policies:
            cur.execute(
                "INSERT INTO insurance.insurance_policies (policy_number, client_id, category_id, start_date, end_date, insurance_amount, monthly_payment, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING policy_id",
                policy
            )
            policy_ids.append(cur.fetchone()[0])
        
        # 7. Страховые случаи (зависит от category_insurances)
        print("Вставляем страховые случаи...")
        events = [
            ('ДТП', 'Дорожно-транспортное происшествие', 'active', category_ids[0], 80.00, 5.00),
            ('Госпитализация', 'Экстренная госпитализация', 'active', category_ids[1], 90.00, 3.00),
            ('Пожар', 'Пожар в жилом помещении', 'active', category_ids[2], 85.00, 2.00),
            ('Травма', 'Травма на производстве', 'active', category_ids[3], 95.00, 4.00),
            ('Отмена поездки', 'Вынужденная отмена поездки', 'active', category_ids[4], 70.00, 6.00)
        ]
        event_ids = []
        for event in events:
            cur.execute(
                "INSERT INTO insurance.insured_events (event_name, description, status, category_id, coverage_percentage, probability) VALUES (%s, %s, %s, %s, %s, %s) RETURNING event_id",
                event
            )
            event_ids.append(cur.fetchone()[0])
        
        # 8. События по полисам (зависит от insurance_policies и insured_events)
        print("Вставляем события по полисам...")
        policy_events = [
            (policy_ids[0], event_ids[0], '2024-01-15', 'pending', 'Небольшое ДТП'),
            (policy_ids[1], event_ids[1], '2024-02-20', 'pending', 'Плановая госпитализация'),
            (policy_ids[2], event_ids[2], '2024-03-25', 'pending', 'Пожар в квартире'),
            (policy_ids[3], event_ids[3], '2024-04-30', 'pending', 'Травма на работе'),
            (policy_ids[4], event_ids[4], '2024-05-05', 'pending', 'Отмена командировки')
        ]
        policy_event_ids = []
        for event in policy_events:
            cur.execute(
                "INSERT INTO insurance.policy_events (policy_id, event_id, event_date, status, description) VALUES (%s, %s, %s, %s, %s) RETURNING policy_event_id",
                event
            )
            policy_event_ids.append(cur.fetchone()[0])
        
        # 9. Страховые претензии (зависит от policy_events и employees)
        print("Вставляем страховые претензии...")
        claims = [
            ('CLM-001', policy_event_ids[0], '2024-01-16', 'Ремонт автомобиля после ДТП', 50000.00, 40000.00, 'approved', employee_ids[0]),
            ('CLM-002', policy_event_ids[1], '2024-02-21', 'Оплата лечения', 30000.00, 27000.00, 'approved', employee_ids[1]),
            ('CLM-003', policy_event_ids[2], '2024-03-26', 'Восстановление имущества', 200000.00, 170000.00, 'pending', None),
            ('CLM-004', policy_event_ids[3], '2024-05-01', 'Оплата больничного', 15000.00, None, 'pending', None),
            ('CLM-005', policy_event_ids[4], '2024-05-06', 'Возврат стоимости билетов', 25000.00, None, 'pending', None)
        ]
        claim_ids = []
        for claim in claims:
            cur.execute(
                "INSERT INTO insurance.insurance_claims (claim_number, policy_event_id, claim_date, description, requested_amount, approved_amount, status, processed_by) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING claim_id",
                claim
            )
            claim_ids.append(cur.fetchone()[0])
        
        # 10. Платежи (зависит от clients, insurance_policies и insurance_claims)
        print("Вставляем платежи...")
        payments = [
            ('PAY-001', client_ids[0], policy_ids[0], None, 5000.00, '2024-01-01', 'premium', 'completed'),
            ('PAY-002', client_ids[1], policy_ids[1], None, 3000.00, '2024-02-01', 'premium', 'completed'),
            ('PAY-003', client_ids[2], policy_ids[2], None, 2000.00, '2024-03-01', 'premium', 'completed'),
            ('PAY-004', client_ids[0], None, claim_ids[0], 40000.00, '2024-01-17', 'claim', 'completed'),
            ('PAY-005', client_ids[1], None, claim_ids[1], 27000.00, '2024-02-22', 'claim', 'completed')
        ]
        for payment in payments:
            cur.execute(
                "INSERT INTO insurance.payments (payment_number, client_id, policy_id, claim_id, amount, payment_date, payment_type, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                payment
            )
        
        # Подтверждаем изменения
        conn.commit()
        print("Все данные успешно добавлены!")
        
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    insert_test_data() 