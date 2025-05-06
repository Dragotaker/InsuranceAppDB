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
        
        <form action="/edit/{{table_key}}/{{row[0]}}" method="post">
            % for i, field in enumerate(fields[1:], 1):
                <div class="form-group">
                    <label for="{{field}}">{{TABLES[table_key]['field_names'][field]}}</label>
                    <input type="text" name="{{field}}" id="{{field}}" value="{{row[i]}}" required>
                </div>
            % end
            <button type="submit" class="button">Сохранить</button>
        </form>
    </div>
</body>
</html> 