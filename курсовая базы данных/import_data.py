import json
import pg8000
from datetime import datetime
import os

def connect_to_db():
    return pg8000.connect(
        user="postgres",
        password="drago",
        host="localhost",
        port=5432,
        database="insurance_db"
    )

def get_existing_ids(cur, table_name, id_column):
    cur.execute(f"SELECT {id_column} FROM insurance.{table_name}")
    return [row[0] for row in cur.fetchall()]

def import_data():
    # Read the generated JSON file
    with open('generated_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    conn = connect_to_db()
    cur = conn.cursor()
    
    try:
        # Get existing IDs
        existing_role_ids = get_existing_ids(cur, 'roles', 'role_id')
        existing_client_ids = get_existing_ids(cur, 'clients', 'client_id')
        existing_employee_ids = get_existing_ids(cur, 'employees', 'employee_id')
        existing_category_ids = get_existing_ids(cur, 'category_insurances', 'category_id')
        
        # Import roles first (they are referenced by users)
        print("Importing roles...")
        roles_data = [(r['role_name'], r['access_rights']) for r in data['roles']]
        cur.executemany("""
            INSERT INTO insurance.roles (role_name, access_rights)
            VALUES (%s, %s)
            RETURNING role_id
        """, roles_data)
        role_ids = [r[0] for r in cur.fetchall()]
        print(f"Imported {len(role_ids)} roles")
        
        # Import clients
        print("Importing clients...")
        clients_data = [(
            c['full_name'],
            c['address'],
            c['phone_number'],
            c['email'],
            c['birth_date'],
            c['passport_data']
        ) for c in data['clients']]
        cur.executemany("""
            INSERT INTO insurance.clients (full_name, address, phone_number, email, birth_date, passport_data)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING client_id
        """, clients_data)
        client_ids = [c[0] for c in cur.fetchall()]
        print(f"Imported {len(client_ids)} clients")
        
        # Import employees
        print("Importing employees...")
        employees_data = [(
            e['full_name'],
            e['position'],
            e['phone_number'],
            e['email'],
            e['hire_date']
        ) for e in data['employees']]
        cur.executemany("""
            INSERT INTO insurance.employees (full_name, position, phone_number, email, hire_date)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING employee_id
        """, employees_data)
        employee_ids = [e[0] for e in cur.fetchall()]
        print(f"Imported {len(employee_ids)} employees")
        
        # Import insurance categories
        print("Importing insurance categories...")
        categories_data = [(
            c['category_name'],
            c['description'],
            c['base_rate']
        ) for c in data['category_insurances']]
        cur.executemany("""
            INSERT INTO insurance.category_insurances (category_name, description, base_rate)
            VALUES (%s, %s, %s)
            RETURNING category_id
        """, categories_data)
        category_ids = [c[0] for c in cur.fetchall()]
        print(f"Imported {len(category_ids)} categories")
        
        # Import insurance policies
        print("Importing insurance policies...")
        policies_data = [(
            p['policy_number'],
            p['client_id'],
            p['category_id'],
            p['start_date'],
            p['end_date'],
            p['insurance_amount'],
            p['monthly_payment'],
            p['status']
        ) for p in data['insurance_policies']]
        
        # Update client_id and category_id to match actual database IDs
        for i, policy in enumerate(policies_data):
            policies_data[i] = list(policy)
            
            # Update client_id
            client_idx = policy[1] - 1  # Convert from 1-based to 0-based index
            if 0 <= client_idx < len(client_ids):
                policies_data[i][1] = client_ids[client_idx]
            else:
                # If client_id is out of range, use the first available client
                policies_data[i][1] = client_ids[0] if client_ids else existing_client_ids[0]
            
            # Update category_id
            category_idx = policy[2] - 1  # Convert from 1-based to 0-based index
            if 0 <= category_idx < len(category_ids):
                policies_data[i][2] = category_ids[category_idx]
            else:
                # If category_id is out of range, use the first available category
                policies_data[i][2] = category_ids[0] if category_ids else existing_category_ids[0]
        
        cur.executemany("""
            INSERT INTO insurance.insurance_policies (
                policy_number, client_id, category_id, start_date, end_date,
                insurance_amount, monthly_payment, status
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING policy_id
        """, policies_data)
        policy_ids = [p[0] for p in cur.fetchall()]
        print(f"Imported {len(policy_ids)} policies")
        
        # Import insured events
        print("Importing insured events...")
        events_data = [(
            e['event_name'],
            e['description'],
            e['status'],
            e['category_id'],
            e['coverage_percentage'],
            e['probability']
        ) for e in data['insured_events']]
        
        # Update category_id to match actual database IDs
        for i, event in enumerate(events_data):
            category_idx = event[3] - 1  # Convert from 1-based to 0-based index
            if 0 <= category_idx < len(category_ids):
                events_data[i] = list(event)
                events_data[i][3] = category_ids[category_idx]
            else:
                # If category_id is out of range, use the first available category
                events_data[i] = list(event)
                events_data[i][3] = category_ids[0] if category_ids else existing_category_ids[0]
        
        cur.executemany("""
            INSERT INTO insurance.insured_events (
                event_name, description, status, category_id,
                coverage_percentage, probability
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING event_id
        """, events_data)
        event_ids = [e[0] for e in cur.fetchall()]
        print(f"Imported {len(event_ids)} events")
        
        # Import policy events
        print("Importing policy events...")
        policy_events_data = [(
            pe['policy_id'],
            pe['event_id'],
            pe['event_date'],
            pe['status'],
            pe['description']
        ) for pe in data['policy_events']]
        
        # Update policy_id and event_id to match actual database IDs
        for i, event in enumerate(policy_events_data):
            policy_idx = event[0] - 1  # Convert from 1-based to 0-based index
            event_idx = event[1] - 1
            policy_events_data[i] = list(event)
            if 0 <= policy_idx < len(policy_ids):
                policy_events_data[i][0] = policy_ids[policy_idx]
            else:
                policy_events_data[i][0] = policy_ids[0] if policy_ids else None
            if 0 <= event_idx < len(event_ids):
                policy_events_data[i][1] = event_ids[event_idx]
            else:
                policy_events_data[i][1] = event_ids[0] if event_ids else None
        
        cur.executemany("""
            INSERT INTO insurance.policy_events (
                policy_id, event_id, event_date, status, description
            )
            VALUES (%s, %s, %s, %s, %s)
            RETURNING policy_event_id
        """, policy_events_data)
        policy_event_ids = [pe[0] for pe in cur.fetchall()]
        print(f"Imported {len(policy_event_ids)} policy events")
        
        # Import insurance claims
        print("Importing insurance claims...")
        claims_data = [(
            c['claim_number'],
            c['policy_event_id'],
            c['claim_date'],
            c['description'],
            c['requested_amount'],
            c['approved_amount'],
            c['status'],
            c['processed_by'],
            c['processed_at']
        ) for c in data['insurance_claims']]
        
        # Update policy_event_id and processed_by to match actual database IDs
        for i, claim in enumerate(claims_data):
            event_idx = claim[1] - 1
            claims_data[i] = list(claim)
            if 0 <= event_idx < len(policy_event_ids):
                claims_data[i][1] = policy_event_ids[event_idx]
            else:
                claims_data[i][1] = policy_event_ids[0] if policy_event_ids else None
            if claim[7] is not None:  # processed_by
                employee_idx = claim[7] - 1
                if 0 <= employee_idx < len(employee_ids):
                    claims_data[i][7] = employee_ids[employee_idx]
                else:
                    claims_data[i][7] = employee_ids[0] if employee_ids else existing_employee_ids[0]
        
        cur.executemany("""
            INSERT INTO insurance.insurance_claims (
                claim_number, policy_event_id, claim_date, description,
                requested_amount, approved_amount, status, processed_by, processed_at
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING claim_id
        """, claims_data)
        claim_ids = [c[0] for c in cur.fetchall()]
        print(f"Imported {len(claim_ids)} claims")
        
        # Import payments
        print("Importing payments...")
        payments_data = [(
            p['payment_number'],
            p['client_id'],
            p['policy_id'],
            p['claim_id'],
            p['amount'],
            p['payment_date'],
            p['payment_type'],
            p['status']
        ) for p in data['payments']]
        
        # Update client_id, policy_id, and claim_id to match actual database IDs
        for i, payment in enumerate(payments_data):
            client_idx = payment[1] - 1
            payments_data[i] = list(payment)
            if 0 <= client_idx < len(client_ids):
                payments_data[i][1] = client_ids[client_idx]
            else:
                payments_data[i][1] = client_ids[0] if client_ids else existing_client_ids[0]
            if payment[2] is not None:  # policy_id
                policy_idx = payment[2] - 1
                if 0 <= policy_idx < len(policy_ids):
                    payments_data[i][2] = policy_ids[policy_idx]
                else:
                    payments_data[i][2] = policy_ids[0] if policy_ids else None
            if payment[3] is not None:  # claim_id
                claim_idx = payment[3] - 1
                if 0 <= claim_idx < len(claim_ids):
                    payments_data[i][3] = claim_ids[claim_idx]
                else:
                    payments_data[i][3] = claim_ids[0] if claim_ids else None
        
        cur.executemany("""
            INSERT INTO insurance.payments (
                payment_number, client_id, policy_id, claim_id,
                amount, payment_date, payment_type, status
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING payment_id
        """, payments_data)
        print(f"Imported {len(payments_data)} payments")
        
        # Import users
        print("Importing users...")
        users_data = [(
            u['username'],
            u['password_hash'],
            u['role_id'],
            u['client_id'],
            u['employee_id']
        ) for u in data['users']]
        
        # Update role_id, client_id, and employee_id to match actual database IDs
        for i, user in enumerate(users_data):
            role_idx = user[2] - 1
            users_data[i] = list(user)
            if 0 <= role_idx < len(role_ids):
                users_data[i][2] = role_ids[role_idx]
            else:
                users_data[i][2] = role_ids[0] if role_ids else existing_role_ids[0]
            if user[3] is not None:  # client_id
                client_idx = user[3] - 1
                if 0 <= client_idx < len(client_ids):
                    users_data[i][3] = client_ids[client_idx]
                else:
                    users_data[i][3] = client_ids[0] if client_ids else existing_client_ids[0]
            if user[4] is not None:  # employee_id
                employee_idx = user[4] - 1
                if 0 <= employee_idx < len(employee_ids):
                    users_data[i][4] = employee_ids[employee_idx]
                else:
                    users_data[i][4] = employee_ids[0] if employee_ids else existing_employee_ids[0]
        
        cur.executemany("""
            INSERT INTO insurance.users (
                username, password_hash, role_id, client_id, employee_id
            )
            VALUES (%s, %s, %s, %s, %s)
        """, users_data)
        print(f"Imported {len(users_data)} users")
        
        conn.commit()
        print("Data import completed successfully!")
        
    except Exception as e:
        conn.rollback()
        print(f"Error during import: {str(e)}")
        raise
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    import_data() 