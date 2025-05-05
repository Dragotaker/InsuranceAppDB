<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{{TABLES[table_key]['add_form_title']}}</title>
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <div class="container">
        <h1>{{TABLES[table_key]['add_form_title']}}</h1>
        
        % if error:
        <div class="error-message">
            {{error}}
        </div>
        % end
        
        <form method="post">
            % for field in fields:
            % if field == fields[0]:  # Пропускаем первое поле (ID)
                <input type="hidden" name="{{field}}" value="1">  <!-- Значение не важно, так как будет автоинкремент -->
            % elif not field.endswith('_id'):
            <div class="form-group">
                <label for="{{field}}">{{TABLES[table_key]['display_fields'][field]}}:</label>
                % if field in ['birth_date', 'hire_date', 'start_date', 'end_date', 'claim_date', 'payment_date', 'event_date']:
                <input type="date" id="{{field}}" name="{{field}}" required>
                % elif field == 'password_hash':
                <input type="password" id="{{field}}" name="{{field}}" required>
                % else:
                <input type="text" id="{{field}}" name="{{field}}" required>
                % end
            </div>
            % elif field in foreign_data and table_key != 'users':
            <div class="form-group">
                <label for="{{field}}">{{TABLES[table_key]['display_fields'][field]}}:</label>
                <select id="{{field}}" name="{{field}}">
                    <option value="">-- Выберите --</option>
                    % for id, name in foreign_data[field]:
                    <option value="{{id}}">{{name}}</option>
                    % end
                </select>
            </div>
            % elif field.endswith('_id'):
            <div class="form-group">
                <label for="{{field}}">{{TABLES[table_key]['display_fields'][field]}}:</label>
                % if table_key == 'users' and field in ['client_id', 'employee_id']:
                <input type="number" id="{{field}}" name="{{field}}" min="1">
                % else:
                <input type="number" id="{{field}}" name="{{field}}" min="1" required>
                % end
            </div>
            % end
            % end
            <button type="submit" class="button">Добавить</button>
        </form>
    </div>
</body>
</html> 