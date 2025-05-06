from faker import Faker
import json
from datetime import datetime, timedelta
import random
from dateutil.relativedelta import relativedelta

fake = Faker('ru_RU')

def generate_clients(count=100):
    clients = []
    for _ in range(count):
        client = {
            'full_name': fake.name(),
            'address': fake.address(),
            'phone_number': fake.phone_number(),
            'email': fake.email(),
            'birth_date': fake.date_of_birth(minimum_age=18, maximum_age=80).isoformat(),
            'passport_data': fake.passport_number()
        }
        clients.append(client)
    return clients

def generate_employees(count=20):
    employees = []
    for _ in range(count):
        employee = {
            'full_name': fake.name(),
            'position': fake.job(),
            'phone_number': fake.phone_number(),
            'email': fake.email(),
            'hire_date': fake.date_between(start_date='-5y', end_date='today').isoformat()
        }
        employees.append(employee)
    return employees

def generate_category_insurances():
    categories = [
        {
            'category_name': 'Автомобильное страхование',
            'description': 'Страхование автомобилей от ущерба и угона',
            'base_rate': 5.0
        },
        {
            'category_name': 'Страхование имущества',
            'description': 'Страхование жилья и имущества от повреждений',
            'base_rate': 3.5
        },
        {
            'category_name': 'Страхование жизни',
            'description': 'Страхование жизни и здоровья',
            'base_rate': 4.0
        },
        {
            'category_name': 'Страхование путешествий',
            'description': 'Страхование при поездках за границу',
            'base_rate': 2.5
        }
    ]
    return categories

def generate_insurance_policies(count=200, client_ids=None, category_ids=None):
    policies = []
    statuses = ['active', 'expired', 'cancelled']
    
    for _ in range(count):
        start_date = fake.date_between(start_date='-1y', end_date='+1y')
        end_date = start_date + relativedelta(years=1)
        
        policy = {
            'policy_number': fake.unique.random_number(digits=8),
            'client_id': random.choice(client_ids),
            'category_id': random.choice(category_ids),
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat(),
            'insurance_amount': round(random.uniform(100000, 1000000), 2),
            'monthly_payment': round(random.uniform(1000, 10000), 2),
            'status': random.choice(statuses)
        }
        policies.append(policy)
    return policies

def generate_insured_events(category_ids=None):
    events = []
    statuses = ['active', 'inactive']
    
    for category_id in category_ids:
        for _ in range(5):  # 5 events per category
            event = {
                'event_name': fake.sentence(nb_words=3),
                'description': fake.text(max_nb_chars=200),
                'status': random.choice(statuses),
                'category_id': category_id,
                'coverage_percentage': round(random.uniform(50, 100), 2),
                'probability': round(random.uniform(0.1, 5.0), 2)
            }
            events.append(event)
    return events

def generate_policy_events(count=100, policy_ids=None, event_ids=None):
    events = []
    statuses = ['pending', 'approved', 'rejected']
    
    for _ in range(count):
        event = {
            'policy_id': random.choice(policy_ids),
            'event_id': random.choice(event_ids),
            'event_date': fake.date_between(start_date='-1y', end_date='today').isoformat(),
            'status': random.choice(statuses),
            'description': fake.text(max_nb_chars=200)
        }
        events.append(event)
    return events

def generate_insurance_claims(count=50, policy_event_ids=None, employee_ids=None):
    claims = []
    statuses = ['pending', 'approved', 'rejected', 'paid']
    
    for _ in range(count):
        claim_date = fake.date_between(start_date='-1y', end_date='today')
        processed_at = None
        processed_by = None
        approved_amount = None
        
        if random.random() > 0.3:  # 70% chance of being processed
            processed_at = (claim_date + timedelta(days=random.randint(1, 30))).isoformat()
            processed_by = random.choice(employee_ids)
            approved_amount = round(random.uniform(10000, 100000), 2)
        
        claim = {
            'claim_number': fake.unique.random_number(digits=8),
            'policy_event_id': random.choice(policy_event_ids),
            'claim_date': claim_date.isoformat(),
            'description': fake.text(max_nb_chars=200),
            'requested_amount': round(random.uniform(10000, 100000), 2),
            'approved_amount': approved_amount,
            'status': random.choice(statuses),
            'processed_by': processed_by,
            'processed_at': processed_at
        }
        claims.append(claim)
    return claims

def generate_payments(count=100, client_ids=None, policy_ids=None, claim_ids=None):
    payments = []
    payment_types = ['premium', 'claim', 'refund']
    statuses = ['pending', 'completed', 'failed']
    
    for _ in range(count):
        payment = {
            'payment_number': fake.unique.random_number(digits=8),
            'client_id': random.choice(client_ids),
            'policy_id': random.choice(policy_ids) if random.random() > 0.3 else None,
            'claim_id': random.choice(claim_ids) if random.random() > 0.7 else None,
            'amount': round(random.uniform(1000, 50000), 2),
            'payment_date': fake.date_between(start_date='-1y', end_date='today').isoformat(),
            'payment_type': random.choice(payment_types),
            'status': random.choice(statuses)
        }
        payments.append(payment)
    return payments

def generate_roles():
    roles = [
        {
            'role_name': 'admin',
            'access_rights': 'full access'
        },
        {
            'role_name': 'manager',
            'access_rights': 'manage policies and claims'
        },
        {
            'role_name': 'agent',
            'access_rights': 'create policies'
        },
        {
            'role_name': 'client',
            'access_rights': 'view own policies'
        }
    ]
    return roles

def generate_users(count=50, role_ids=None, client_ids=None, employee_ids=None):
    users = []
    for _ in range(count):
        user_type = random.choice(['client', 'employee'])
        user = {
            'username': fake.user_name(),
            'password_hash': fake.sha256(),  # В реальном приложении здесь должен быть хеш пароля
            'role_id': random.choice(role_ids),
            'client_id': random.choice(client_ids) if user_type == 'client' else None,
            'employee_id': random.choice(employee_ids) if user_type == 'employee' else None
        }
        users.append(user)
    return users

def main():
    # Generate base data
    roles = generate_roles()
    clients = generate_clients(100)
    employees = generate_employees(20)
    categories = generate_category_insurances()
    
    # Get IDs for relationships
    role_ids = list(range(1, len(roles) + 1))
    client_ids = list(range(1, len(clients) + 1))
    employee_ids = list(range(1, len(employees) + 1))
    category_ids = list(range(1, len(categories) + 1))
    
    # Generate dependent data
    policies = generate_insurance_policies(200, client_ids, category_ids)
    policy_ids = list(range(1, len(policies) + 1))
    
    events = generate_insured_events(category_ids)
    event_ids = list(range(1, len(events) + 1))
    
    policy_events = generate_policy_events(100, policy_ids, event_ids)
    policy_event_ids = list(range(1, len(policy_events) + 1))
    
    claims = generate_insurance_claims(50, policy_event_ids, employee_ids)
    claim_ids = list(range(1, len(claims) + 1))
    
    payments = generate_payments(100, client_ids, policy_ids, claim_ids)
    users = generate_users(50, role_ids, client_ids, employee_ids)
    
    # Combine all data
    data = {
        'roles': roles,
        'clients': clients,
        'employees': employees,
        'category_insurances': categories,
        'insurance_policies': policies,
        'insured_events': events,
        'policy_events': policy_events,
        'insurance_claims': claims,
        'payments': payments,
        'users': users
    }
    
    # Save to JSON file
    with open('generated_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("Data generation completed successfully!")

if __name__ == "__main__":
    main() 