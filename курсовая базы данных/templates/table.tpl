<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{{table_name}}</title>
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <div class="container">
        <h1>{{table_name}}</h1>
        <a href="/add/{{table_key}}" class="button">Добавить запись</a>
        
        <table>
            <thead>
                <tr>
                    % for field in fields:
                        <th>{{table_info['display_fields'][field]}}</th>
                    % end
                    <th>Действия</th>
                </tr>
            </thead>
            <tbody>
                % for row in rows:
                    <tr>
                        % for field in fields:
                            <td>
                                % if 'display_values' in table_info and field in table_info['display_values']:
                                    {{table_info['display_values'][field].get(row[field], row[field])}}
                                % else:
                                    {{row[field]}}
                                % end
                            </td>
                        % end
                        <td>
                            <a href="/edit/{{table_key}}/{{row[fields[0]]}}" class="button">Редактировать</a>
                            <a href="/delete/{{table_key}}/{{row[fields[0]]}}" class="button delete">Удалить</a>
                        </td>
                    </tr>
                % end
            </tbody>
        </table>
    </div>
</body>
</html> 