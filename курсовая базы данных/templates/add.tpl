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
        
        <form action="/add/{{table_key}}" method="post">
            % for field in fields[1:]:
                <div class="form-group">
                    <label for="{{field}}">{{TABLES[table_key]['field_names'][field]}}</label>
                    % if field in foreign_data:
                        <select name="{{field}}" id="{{field}}">
                            <option value="">-- Выберите --</option>
                            % for value, display in foreign_data[field]:
                                <option value="{{value}}">{{display}}</option>
                            % end
                        </select>
                    % else:
                        <input type="text" name="{{field}}" id="{{field}}" required>
                    % end
                </div>
            % end
            <button type="submit" class="button">Сохранить</button>
        </form>
    </div>
</body>
</html> 