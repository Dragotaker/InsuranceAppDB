<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Редактировать запись - {{table_name}}</title>
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <div class="container">
        <h1>Редактировать запись в таблице "{{table_name}}"</h1>
        
        <form method="POST" class="form">
            % for i, field in enumerate(fields):
                % if not field.endswith('_id'):
                    <div class="form-group">
                        <label for="{{field}}">{{field}}</label>
                        <input type="text" id="{{field}}" name="{{field}}" value="{{row[i]}}" required>
                    </div>
                % end
            % end
            <button type="submit" class="btn">Сохранить</button>
        </form>
    </div>
</body>
</html> 