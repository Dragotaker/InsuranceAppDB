from bottle import route, run, template, request, redirect, static_file
import psycopg2
import os
from dotenv import load_dotenv
from datetime import datetime

# Загрузка переменных окружения
load_dotenv()

# Настройки подключения к базе данных
DB_CONFIG = {
    'database': os.getenv('DB_NAME', 'insurance_db'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'drago'),
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', '5432')),
    'client_encoding': 'UTF8',
    'options': '-c client_encoding=UTF8'
}

def get_db_connection():
    conn = psycopg2.connect(**DB_CONFIG)
    # Устанавливаем кодировку UTF-8 для соединения
    conn.set_client_encoding('UTF8')
    # Устанавливаем кодировку для текущей сессии
    cur = conn.cursor()
    cur.execute("SET client_encoding TO 'UTF8'")
    cur.close()
    return conn

def ensure_utf8(text):
    if isinstance(text, str):
        try:
            # Пробуем декодировать как UTF-8
            text.encode('utf-8')
            return text
        except UnicodeEncodeError:
            # Если не получилось, пробуем разные варианты декодирования
            try:
                # Пробуем как CP1251
                return text.encode('cp1251').decode('utf-8')
            except:
                try:
                    # Пробуем как LATIN1
                    return text.encode('latin1').decode('utf-8')
                except:
                    # Если ничего не помогло, возвращаем как есть
                    return text
    return text

# Статические файлы
@route('/static/<filename:path>')
def serve_static(filename):
    return static_file(filename, root='static')

# Главная страница
@route('/')
def index():
    return template('templates/layout.tpl', 
                   title='Главная',
                   current_page='home',
                   base=template('templates/index.tpl'))

# Таблицы
TABLES = {
    'clients': {
        'name': 'Клиенты',
        'add_form_title': 'Добавить клиента',
        'fields': ['client_id', 'full_name', 'address', 'phone_number', 'email', 'birth_date', 'passport_data', 'username', 'password'],
        'field_names': {
            'client_id': 'ID клиента',
            'full_name': 'ФИО',
            'address': 'Адрес',
            'phone_number': 'Телефон',
            'email': 'Email',
            'birth_date': 'Дата рождения',
            'passport_data': 'Паспортные данные',
            'username': 'Логин',
            'password': 'Пароль'
        },
        'display_fields': {
            'client_id': 'Номер',
            'full_name': 'ФИО',
            'address': 'Адрес',
            'phone_number': 'Телефон',
            'email': 'Email',
            'birth_date': 'Дата рождения',
            'passport_data': 'Паспортные данные',
            'username': 'Логин'
        }
    },
    'employees': {
        'name': 'Сотрудники',
        'add_form_title': 'Добавить сотрудника',
        'fields': ['employee_id', 'full_name', 'position', 'phone_number', 'email', 'hire_date', 'username', 'password'],
        'field_names': {
            'employee_id': 'ID сотрудника',
            'full_name': 'ФИО',
            'position': 'Должность',
            'phone_number': 'Телефон',
            'email': 'Email',
            'hire_date': 'Дата приема',
            'username': 'Логин',
            'password': 'Пароль'
        },
        'display_fields': {
            'employee_id': 'Номер',
            'full_name': 'ФИО',
            'position': 'Должность',
            'phone_number': 'Телефон',
            'email': 'Email',
            'hire_date': 'Дата приема',
            'username': 'Логин'
        }
    },
    'category_insurances': {
        'name': 'Категории страхования',
        'add_form_title': 'Добавить категорию страхования',
        'fields': ['category_id', 'category_name', 'description', 'base_rate'],
        'field_names': {
            'category_id': 'ID категории',
            'category_name': 'Название категории',
            'description': 'Описание',
            'base_rate': 'Базовая ставка'
        },
        'display_fields': {
            'category_id': 'Номер',
            'category_name': 'Название категории',
            'description': 'Описание',
            'base_rate': 'Базовая ставка'
        }
    },
    'insurance_policies': {
        'name': 'Страховые полисы',
        'add_form_title': 'Добавить страховой полис',
        'fields': ['policy_id', 'policy_number', 'client_id', 'category_id', 'start_date', 'end_date', 'insurance_amount', 'monthly_payment', 'status'],
        'field_names': {
            'policy_id': 'ID полиса',
            'policy_number': 'Номер полиса',
            'client_id': 'ID клиента',
            'category_id': 'ID категории',
            'start_date': 'Дата начала',
            'end_date': 'Дата окончания',
            'insurance_amount': 'Страховая сумма',
            'monthly_payment': 'Ежемесячный платеж',
            'status': 'Статус'
        },
        'display_fields': {
            'policy_id': 'Номер',
            'policy_number': 'Номер полиса',
            'client_id': 'Номер клиента',
            'category_id': 'Номер категории',
            'start_date': 'Дата начала',
            'end_date': 'Дата окончания',
            'insurance_amount': 'Страховая сумма',
            'monthly_payment': 'Ежемесячный платеж',
            'status': 'Статус'
        },
        'display_values': {
            'status': {
                'active': 'Активен',
                'expired': 'Истек',
                'cancelled': 'Аннулирован'
            }
        }
    },
    'insured_events': {
        'name': 'Страховые случаи',
        'add_form_title': 'Добавить страховой случай',
        'fields': ['event_id', 'event_name', 'description', 'status', 'category_id', 'coverage_percentage', 'probability'],
        'field_names': {
            'event_id': 'ID случая',
            'event_name': 'Название случая',
            'description': 'Описание',
            'status': 'Статус',
            'category_id': 'ID категории',
            'coverage_percentage': 'Процент покрытия',
            'probability': 'Вероятность'
        },
        'display_fields': {
            'event_id': 'Номер',
            'event_name': 'Название случая',
            'description': 'Описание',
            'status': 'Статус',
            'category_id': 'Номер категории',
            'coverage_percentage': 'Процент покрытия',
            'probability': 'Вероятность'
        }
    },
    'policy_events': {
        'name': 'События по полисам',
        'add_form_title': 'Добавить событие по полису',
        'fields': ['policy_event_id', 'policy_id', 'event_id', 'event_date', 'status', 'description'],
        'field_names': {
            'policy_event_id': 'ID события',
            'policy_id': 'ID полиса',
            'event_id': 'ID случая',
            'event_date': 'Дата события',
            'status': 'Статус',
            'description': 'Описание'
        },
        'display_fields': {
            'policy_event_id': 'Номер',
            'policy_id': 'Номер полиса',
            'event_id': 'Номер случая',
            'event_date': 'Дата события',
            'status': 'Статус',
            'description': 'Описание'
        }
    },
    'insurance_claims': {
        'name': 'Страховые претензии',
        'add_form_title': 'Добавить страховую претензию',
        'fields': ['claim_id', 'claim_number', 'policy_event_id', 'claim_date', 'description', 'requested_amount', 'approved_amount', 'status', 'processed_by', 'processed_at'],
        'field_names': {
            'claim_id': 'ID претензии',
            'claim_number': 'Номер претензии',
            'policy_event_id': 'ID события',
            'claim_date': 'Дата претензии',
            'description': 'Описание',
            'requested_amount': 'Запрошенная сумма',
            'approved_amount': 'Утвержденная сумма',
            'status': 'Статус',
            'processed_by': 'Обработано',
            'processed_at': 'Дата обработки'
        },
        'display_fields': {
            'claim_id': 'Номер',
            'claim_number': 'Номер претензии',
            'policy_event_id': 'Номер события',
            'claim_date': 'Дата претензии',
            'description': 'Описание',
            'requested_amount': 'Запрошенная сумма',
            'approved_amount': 'Утвержденная сумма',
            'status': 'Статус',
            'processed_by': 'Обработано',
            'processed_at': 'Дата обработки'
        }
    },
    'payments': {
        'name': 'Платежи',
        'add_form_title': 'Добавить платеж',
        'fields': ['payment_id', 'payment_number', 'client_id', 'policy_id', 'claim_id', 'amount', 'payment_date', 'payment_type', 'status'],
        'field_names': {
            'payment_id': 'ID платежа',
            'payment_number': 'Номер платежа',
            'client_id': 'ID клиента',
            'policy_id': 'ID полиса',
            'claim_id': 'ID претензии',
            'amount': 'Сумма',
            'payment_date': 'Дата платежа',
            'payment_type': 'Тип платежа',
            'status': 'Статус'
        },
        'display_fields': {
            'payment_id': 'Номер',
            'payment_number': 'Номер платежа',
            'client_id': 'Номер клиента',
            'policy_id': 'Номер полиса',
            'claim_id': 'Номер претензии',
            'amount': 'Сумма',
            'payment_date': 'Дата платежа',
            'payment_type': 'Тип платежа',
            'status': 'Статус'
        }
    },
    'roles': {
        'name': 'Роли',
        'add_form_title': 'Добавить роль',
        'fields': ['role_id', 'role_name', 'access_rights'],
        'field_names': {
            'role_id': 'ID роли',
            'role_name': 'Название роли',
            'access_rights': 'Права доступа'
        },
        'display_fields': {
            'role_id': 'Номер',
            'role_name': 'Название роли',
            'access_rights': 'Права доступа'
        }
    },
    'users': {
        'name': 'Пользователи',
        'add_form_title': 'Добавить пользователя',
        'fields': ['user_id', 'username', 'password_hash', 'role_id', 'client_id', 'employee_id'],
        'field_names': {
            'user_id': 'ID пользователя',
            'username': 'Логин',
            'password_hash': 'Пароль',
            'role_id': 'Роль',
            'client_id': 'Клиент',
            'employee_id': 'Сотрудник'
        },
        'display_fields': {
            'user_id': 'Номер',
            'username': 'Логин',
            'password_hash': 'Пароль',
            'role_id': 'Роль',
            'client_id': 'Клиент',
            'employee_id': 'Сотрудник'
        },
        'foreign_keys': {
            'client_id': {
                'table': 'clients',
                'display_field': 'full_name'
            },
            'employee_id': {
                'table': 'employees',
                'display_field': 'full_name'
            },
            'role_id': {
                'table': 'roles',
                'display_field': 'role_name'
            }
        }
    }
}

# Просмотр таблицы
@route('/table/<table_name>')
def show_table(table_name):
    if table_name not in TABLES:
        return "Таблица не найдена"
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Get search parameters and ensure proper encoding
    search_query = request.query.get('search', '').strip()
    search_field = request.query.get('search_field', '')
    
    # Ensure proper UTF-8 encoding for search query
    if search_query:
        try:
            # Try to decode as UTF-8 first
            search_query = search_query.encode('latin1').decode('utf-8')
        except:
            try:
                # If that fails, try CP1251
                search_query = search_query.encode('latin1').decode('cp1251')
            except:
                # If all fails, leave as is
                pass
    
    # Base query
    if table_name in ['clients', 'employees']:
        id_field = 'client_id' if table_name == 'clients' else 'employee_id'
        query = f"""
            SELECT t.*, u.username 
            FROM insurance.{table_name} t 
            LEFT JOIN insurance.users u ON t.{id_field} = u.{id_field}
        """
    else:
        query = f"SELECT * FROM insurance.{table_name}"
    
    params = []
    
    # Add search conditions if search query is provided
    if search_query:
        if search_field:
            # Search in specific field
            if table_name in ['clients', 'employees'] and search_field == 'username':
                query += f" WHERE u.username ILIKE %s"
            else:
                query += f" WHERE {search_field}::text ILIKE %s"
            params.append(f'%{search_query}%')
        else:
            # Search in all fields
            conditions = []
            for field in TABLES[table_name]['fields']:
                if field != 'password':  # Exclude password field from search
                    if table_name in ['clients', 'employees'] and field == 'username':
                        conditions.append(f"u.username ILIKE %s")
                    else:
                        conditions.append(f"{field}::text ILIKE %s")
                params.append(f'%{search_query}%')
            query += " WHERE " + " OR ".join(conditions)
    
    # Add ORDER BY clause
    if table_name in ['clients', 'employees']:
        query += f" ORDER BY t.{TABLES[table_name]['fields'][0]}"
    else:
        query += f" ORDER BY {TABLES[table_name]['fields'][0]}"
    
    # Set client encoding for this session
    cur.execute("SET client_encoding TO 'UTF8'")
    
    cur.execute(query, params)
    rows = cur.fetchall()
    
    # Convert rows to dictionaries for easier access
    field_names = TABLES[table_name]['fields']
    rows = [dict(zip(field_names, row)) for row in rows]
    
    # Remove password field from display
    display_fields = [f for f in field_names if f != 'password']
    
    # Determine if we should show add/delete buttons
    show_add_delete = table_name != 'users'
    
    cur.close()
    conn.close()
    
    return template('templates/layout.tpl',
                   title=TABLES[table_name]['name'],
                   current_page=table_name,
                   base=template('templates/table.tpl',
                                table_name=TABLES[table_name]['name'],
                                fields=display_fields,
                                rows=rows,
                                table_key=table_name,
                                table_info=TABLES[table_name],
                                search_query=search_query,
                                search_field=search_field,
                                show_add_delete=show_add_delete))

# Добавление записи
@route('/add/<table_name>', method=['GET', 'POST'])
def add_record(table_name):
    if table_name not in TABLES:
        return "Таблица не найдена"
    
    if request.method == 'POST':
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Устанавливаем кодировку для текущей сессии
        cur.execute("SET client_encoding TO 'UTF8'")
        
        fields = TABLES[table_name]['fields']
        values = []
        field_names = []
        
        # Пропускаем первое поле (ID), так как оно будет автоинкрементироваться
        for field in fields[1:]:
            # Пропускаем username и password, они будут использованы для создания пользователя
            if field in ['username', 'password']:
                continue
                
                value = request.forms.getunicode(field)  # Получаем строку в unicode (UTF-8)
                if value:  # Добавляем только если значение не пустое
                    values.append(value)
                    field_names.append(field)
        
        placeholders = ', '.join(['%s'] * len(values))
        field_names_str = ', '.join(field_names)
        
        query = f"INSERT INTO insurance.{table_name} ({field_names_str}) VALUES ({placeholders}) RETURNING {fields[0]}"
        cur.execute(query, values)
        new_id = cur.fetchone()[0]
        
        # Создаем пользователя для клиента или сотрудника
        if table_name in ['clients', 'employees']:
            username = request.forms.getunicode('username')
            password = request.forms.getunicode('password')
            
            if username and password:
                # Определяем role_id и соответствующий id (client_id или employee_id)
                role_id = 1 if table_name == 'clients' else None
                id_field = 'client_id' if table_name == 'clients' else 'employee_id'
                
                # Создаем пользователя
                cur.execute(f"""
                    INSERT INTO insurance.users (username, password_hash, role_id, {id_field})
                    VALUES (%s, %s, %s, %s)
                """, (username, hash_password(password), role_id, new_id))
        
        conn.commit()
        cur.close()
        conn.close()
        
        redirect(f'/table/{table_name}')
    
    # Получаем данные для выпадающих списков
    foreign_data = {}
    if 'foreign_keys' in TABLES[table_name]:
        conn = get_db_connection()
        cur = conn.cursor()
        for field, fk_info in TABLES[table_name]['foreign_keys'].items():
            cur.execute(f"SELECT {field}, {fk_info['display_field']} FROM insurance.{fk_info['table']}")
            foreign_data[field] = cur.fetchall()
        cur.close()
        conn.close()
    
    return template('templates/layout.tpl',
                   title=TABLES[table_name]['add_form_title'],
                   current_page=table_name,
                   base=template('templates/add.tpl',
                                table_name=TABLES[table_name]['name'],
                                fields=TABLES[table_name]['fields'],
                                table_key=table_name,
                                TABLES=TABLES,
                                foreign_data=foreign_data,
                                error=None))

def hash_password(password):
    # Простая функция хеширования пароля
    import hashlib
    return hashlib.sha256(password.encode()).hexdigest()

# Редактирование записи
@route('/edit/<table_name>/<id>', method=['GET', 'POST'])
def edit_record(table_name, id):
    if table_name not in TABLES:
        return "Таблица не найдена"
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    if request.method == 'POST':
        fields = TABLES[table_name]['fields']
        updates = []
        values = []
        
        # Обновляем основные поля
        for field in fields:
            if field.endswith('_id'):  # Пропускаем ID
                continue
            if field == 'password':  # Хешируем пароль если он был изменен
                password = request.forms.getunicode(field)
                if password:  # Обновляем пароль только если он был введен
                    updates.append(f"{field} = %s")
                    values.append(hash_password(password))
            else:
                value = request.forms.getunicode(field)
            updates.append(f"{field} = %s")
            values.append(value)
        
        values.append(id)  # Добавляем ID для WHERE условия
        query = f"UPDATE insurance.{table_name} SET {', '.join(updates)} WHERE {fields[0]} = %s"
        cur.execute(query, values)
        
        # Если редактируем клиента или сотрудника, обновляем данные пользователя
        if table_name in ['clients', 'employees']:
            username = request.forms.getunicode('username')
            password = request.forms.getunicode('password')
            id_field = 'client_id' if table_name == 'clients' else 'employee_id'
            
            # Проверяем существование пользователя
            cur.execute(f"SELECT user_id FROM insurance.users WHERE {id_field} = %s", (id,))
            user = cur.fetchone()
            
            if user:  # Если пользователь существует, обновляем его
                user_updates = []
                user_values = []
                
                if username:
                    user_updates.append("username = %s")
                    user_values.append(username)
                
                if password:
                    user_updates.append("password_hash = %s")
                    user_values.append(hash_password(password))
                
                if user_updates:
                    user_values.append(user[0])
                    cur.execute(f"""
                        UPDATE insurance.users 
                        SET {', '.join(user_updates)}
                        WHERE user_id = %s
                    """, user_values)
            else:  # Если пользователя нет, создаем нового
                if username and password:
                    role_id = 1 if table_name == 'clients' else None
                    cur.execute(f"""
                        INSERT INTO insurance.users (username, password_hash, role_id, {id_field})
                        VALUES (%s, %s, %s, %s)
                    """, (username, hash_password(password), role_id, id))
        
        conn.commit()
        cur.close()
        conn.close()
        
        redirect(f'/table/{table_name}')
    
    cur.execute(f"SELECT * FROM insurance.{table_name} WHERE {TABLES[table_name]['fields'][0]} = %s", (id,))
    row = cur.fetchone()
    
    # Если это клиент или сотрудник, получаем данные пользователя
    if table_name in ['clients', 'employees']:
        id_field = 'client_id' if table_name == 'clients' else 'employee_id'
        cur.execute(f"SELECT username FROM insurance.users WHERE {id_field} = %s", (id,))
        user_data = cur.fetchone()
        if user_data:
            # Преобразуем row в список для изменения
            row = list(row)
            # Добавляем username в конец
            row.append(user_data[0])
            # Преобразуем обратно в кортеж
            row = tuple(row)
    
    cur.close()
    conn.close()
    
    return template('templates/layout.tpl',
                   title=f"Редактировать {TABLES[table_name]['name'].lower()}",
                   current_page=table_name,
                   base=template('templates/edit.tpl',
                                table_name=TABLES[table_name]['name'],
                                fields=TABLES[table_name]['fields'],
                                row=row,
                                table_key=table_name,
                                TABLES=TABLES))

# Удаление записи
@route('/delete/<table_name>/<id>')
def delete_record(table_name, id):
    if table_name not in TABLES:
        return "Таблица не найдена"
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Если удаляем клиента или сотрудника, сначала удаляем связанного пользователя
    if table_name in ['clients', 'employees']:
        id_field = 'client_id' if table_name == 'clients' else 'employee_id'
        cur.execute(f"DELETE FROM insurance.users WHERE {id_field} = %s", (id,))
    
    # Удаляем запись
    cur.execute(f"DELETE FROM insurance.{table_name} WHERE {TABLES[table_name]['fields'][0]} = %s", (id,))
    
    # Сбрасываем последовательность
    sequence_name = f"insurance.{table_name}_{TABLES[table_name]['fields'][0]}_seq"
    cur.execute(f"SELECT setval(%s, COALESCE((SELECT MAX({TABLES[table_name]['fields'][0]}) FROM insurance.{table_name}), 0) + 1, false)", (sequence_name,))
    
    conn.commit()
    cur.close()
    conn.close()
    
    redirect(f'/table/{table_name}')

@route('/reports')
def reports_index():
    return template('templates/layout.tpl',
        title='Отчёты',
        current_page='reports',
        base=template('templates/reports.tpl'))

@route('/report/policies_by_category')
def report_policies_by_category():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        SELECT ci.category_name, COUNT(ip.policy_id) AS total_policies, SUM(ip.insurance_amount) AS total_insurance_amount
        FROM insurance.category_insurances ci
        LEFT JOIN insurance.insurance_policies ip ON ci.category_id = ip.category_id
        GROUP BY ci.category_name
        ORDER BY total_policies DESC
    ''')
    rows = cur.fetchall()
    cur.close()
    conn.close()
    headers = ['Категория', 'Количество полисов', 'Общая страховая сумма']
    return template('templates/report.tpl', title='Полисы по категориям', headers=headers, rows=rows)

@route('/report/active_clients')
def report_active_clients():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        SELECT c.full_name, c.phone_number, c.email, COUNT(ip.policy_id) AS active_policies_count
        FROM insurance.clients c
        JOIN insurance.insurance_policies ip ON c.client_id = ip.client_id
        WHERE ip.status = 'active'
        GROUP BY c.client_id, c.full_name, c.phone_number, c.email
        ORDER BY active_policies_count DESC
    ''')
    rows = cur.fetchall()
    cur.close()
    conn.close()
    headers = ['ФИО', 'Телефон', 'Email', 'Активных полисов']
    return template('templates/report.tpl', title='Клиенты с активными полисами', headers=headers, rows=rows)

@route('/report/claims_by_period', method=['GET', 'POST'])
def report_claims_by_period():
    rows = []
    start_date = end_date = ''
    if request.method == 'POST':
        start_date = request.forms.get('start_date')
        end_date = request.forms.get('end_date')
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            SELECT ic.claim_number, c.full_name, ip.policy_number, ic.claim_date, ic.description, ic.requested_amount, ic.approved_amount, ic.status, e.full_name
            FROM insurance.insurance_claims ic
            JOIN insurance.policy_events pe ON ic.policy_event_id = pe.policy_event_id
            JOIN insurance.insurance_policies ip ON pe.policy_id = ip.policy_id
            JOIN insurance.clients c ON ip.client_id = c.client_id
            LEFT JOIN insurance.employees e ON ic.processed_by = e.employee_id
            WHERE ic.claim_date BETWEEN %s AND %s
        ''', (start_date, end_date))
        rows = cur.fetchall()
        cur.close()
        conn.close()
    headers = ['Номер претензии', 'Клиент', 'Номер полиса', 'Дата', 'Описание', 'Запрошено', 'Утверждено', 'Статус', 'Обработал']
    return template('templates/report_form.tpl', title='Страховые случаи за период', headers=headers, rows=rows, start_date=start_date, end_date=end_date, form_action='/report/claims_by_period')

@route('/report/payments_by_period', method=['GET', 'POST'])
def report_payments_by_period():
    rows = []
    start_date = end_date = ''
    if request.method == 'POST':
        start_date = request.forms.get('start_date')
        end_date = request.forms.get('end_date')
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            SELECT payment_type, status, COUNT(payment_id) AS total_payments, SUM(amount) AS total_amount
            FROM insurance.payments
            WHERE payment_date BETWEEN %s AND %s
            GROUP BY payment_type, status
            ORDER BY payment_type, status
        ''', (start_date, end_date))
        rows = cur.fetchall()
        cur.close()
        conn.close()
    headers = ['Тип платежа', 'Статус', 'Количество', 'Сумма']
    return template('templates/report_form.tpl', title='Платежи за период', headers=headers, rows=rows, start_date=start_date, end_date=end_date, form_action='/report/payments_by_period')

@route('/report/events_by_category')
def report_events_by_category():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        SELECT ci.category_name, ie.event_name, ie.description, ie.probability
        FROM insurance.insured_events ie
        JOIN insurance.category_insurances ci ON ie.category_id = ci.category_id
        ORDER BY ci.category_name, ie.probability DESC
    ''')
    rows = cur.fetchall()
    cur.close()
    conn.close()
    headers = ['Категория', 'Событие', 'Описание', 'Вероятность']
    return template('templates/report.tpl', title='События по категориям', headers=headers, rows=rows)

if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True) 