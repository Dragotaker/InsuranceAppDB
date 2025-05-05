from bottle import route, run, template, request, redirect, static_file
import pg8000
import os
from dotenv import load_dotenv

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

def get_db_connection():
    return pg8000.connect(**DB_CONFIG)

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
        'fields': ['client_id', 'full_name', 'address', 'phone_number', 'email', 'birth_date', 'passport_data'],
        'field_names': {
            'client_id': 'ID клиента',
            'full_name': 'ФИО',
            'address': 'Адрес',
            'phone_number': 'Телефон',
            'email': 'Email',
            'birth_date': 'Дата рождения',
            'passport_data': 'Паспортные данные'
        },
        'display_fields': {
            'client_id': 'Номер',
            'full_name': 'ФИО',
            'address': 'Адрес',
            'phone_number': 'Телефон',
            'email': 'Email',
            'birth_date': 'Дата рождения',
            'passport_data': 'Паспортные данные'
        }
    },
    'employees': {
        'name': 'Сотрудники',
        'add_form_title': 'Добавить сотрудника',
        'fields': ['employee_id', 'full_name', 'position', 'phone_number', 'email', 'hire_date'],
        'field_names': {
            'employee_id': 'ID сотрудника',
            'full_name': 'ФИО',
            'position': 'Должность',
            'phone_number': 'Телефон',
            'email': 'Email',
            'hire_date': 'Дата приема'
        },
        'display_fields': {
            'employee_id': 'Номер',
            'full_name': 'ФИО',
            'position': 'Должность',
            'phone_number': 'Телефон',
            'email': 'Email',
            'hire_date': 'Дата приема'
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
def view_table(table_name):
    if table_name not in TABLES:
        return "Таблица не найдена"
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM insurance.{table_name}")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    
    # Преобразуем строки в словари для удобства работы в шаблоне
    table_data = []
    for row in rows:
        row_dict = {}
        for i, field in enumerate(TABLES[table_name]['fields']):
            row_dict[field] = row[i]
        table_data.append(row_dict)
    
    return template('templates/layout.tpl',
                   title=TABLES[table_name]['name'],
                   current_page=table_name,
                   base=template('templates/table.tpl',
                                table_name=TABLES[table_name]['name'],
                                fields=TABLES[table_name]['fields'],
                                rows=table_data,
                                table_key=table_name,
                                table_info=TABLES[table_name]))

# Добавление записи
@route('/add/<table_name>', method=['GET', 'POST'])
def add_record(table_name):
    if table_name not in TABLES:
        return "Таблица не найдена"
    
    if request.method == 'POST':
        conn = get_db_connection()
        cur = conn.cursor()
        
        fields = TABLES[table_name]['fields']
        values = []
        field_names = []
        
        # Проверяем существование связанных записей
        if table_name == 'users':
            client_id = request.forms.get('client_id')
            employee_id = request.forms.get('employee_id')
            role_id = request.forms.get('role_id')
            
            # Проверяем существование роли
            if role_id:
                cur.execute("SELECT COUNT(*) FROM insurance.roles WHERE role_id = %s", (role_id,))
                if cur.fetchone()[0] == 0:
                    # Получаем данные для выпадающих списков
                    foreign_data = {}
                    if 'foreign_keys' in TABLES[table_name]:
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
                                               error="Указанная роль не существует"))
            
            # Проверяем существование клиента
            if client_id:
                cur.execute("SELECT COUNT(*) FROM insurance.clients WHERE client_id = %s", (client_id,))
                if cur.fetchone()[0] == 0:
                    # Получаем данные для выпадающих списков
                    foreign_data = {}
                    if 'foreign_keys' in TABLES[table_name]:
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
                                               error="Указанный клиент не существует"))
            
            # Проверяем существование сотрудника
            if employee_id:
                cur.execute("SELECT COUNT(*) FROM insurance.employees WHERE employee_id = %s", (employee_id,))
                if cur.fetchone()[0] == 0:
                    # Получаем данные для выпадающих списков
                    foreign_data = {}
                    if 'foreign_keys' in TABLES[table_name]:
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
                                               error="Указанный сотрудник не существует"))
        
        # Пропускаем первое поле (ID), так как оно будет автоинкрементироваться
        for field in fields[1:]:
            if field == 'password_hash':  # Хешируем пароль
                values.append(hash_password(request.forms.get(field)))
                field_names.append(field)
            else:
                value = request.forms.get(field)
                if value:  # Добавляем только если значение не пустое
                    values.append(value)
                    field_names.append(field)
        
        placeholders = ', '.join(['%s'] * len(values))
        field_names_str = ', '.join(field_names)
        
        query = f"INSERT INTO insurance.{table_name} ({field_names_str}) VALUES ({placeholders})"
        cur.execute(query, values)
        conn.commit()
        cur.close()
        conn.close()
        
        redirect(f'/table/{table_name}')
    
    # Получаем данные для выпадающих списков (кроме таблицы users)
    foreign_data = {}
    if 'foreign_keys' in TABLES[table_name] and table_name != 'users':
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
        for field in fields:
            if field.endswith('_id'):  # Пропускаем ID
                continue
            updates.append(f"{field} = %s")
            values.append(request.forms.get(field))
        
        values.append(id)  # Добавляем ID для WHERE условия
        query = f"UPDATE insurance.{table_name} SET {', '.join(updates)} WHERE {fields[0]} = %s"
        cur.execute(query, values)
        conn.commit()
        cur.close()
        conn.close()
        
        redirect(f'/table/{table_name}')
    
    cur.execute(f"SELECT * FROM insurance.{table_name} WHERE {TABLES[table_name]['fields'][0]} = %s", (id,))
    row = cur.fetchone()
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
    cur.execute(f"DELETE FROM insurance.{table_name} WHERE {TABLES[table_name]['fields'][0]} = %s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    
    redirect(f'/table/{table_name}')

if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True) 