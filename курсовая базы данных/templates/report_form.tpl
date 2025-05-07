<style>
.table-condensed {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    background: #fff;
    border-radius: 10px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    margin-bottom: 30px;
    overflow: hidden;
}
.table-condensed th {
    background: #f2f4f8;
    font-weight: 600;
    padding: 8px 10px;
    border-bottom: 1px solid #e0e0e0;
    text-align: left;
}
.table-condensed td {
    padding: 7px 10px;
    border-bottom: 1px solid #f0f0f0;
    vertical-align: top;
}
.table-condensed tr:last-child td {
    border-bottom: none;
}
.report-form {
    background: #f9f9fb;
    border: 1px solid #e0e0e0;
    border-radius: 10px;
    padding: 16px 20px;
    margin-bottom: 24px;
    display: inline-block;
}
.report-form label {
    font-weight: 500;
    margin-right: 8px;
}
</style>
<h2>{{title}}</h2>
<form action="{{form_action}}" method="post" class="report-form">
    <label>Период: </label>
    <input type="date" name="start_date" value="{{start_date}}" required> —
    <input type="date" name="end_date" value="{{end_date}}" required>
    <button type="submit" class="button">Показать</button>
</form>
<table class="table-condensed">
    <thead>
        <tr>
            % for h in headers:
                <th>{{h}}</th>
            % end
        </tr>
    </thead>
    <tbody>
        % if rows:
            % for row in rows:
                <tr>
                    % for cell in row:
                        <td>{{cell}}</td>
                    % end
                </tr>
            % end
        % else:
            <tr><td colspan="{{len(headers)}}">Нет данных для отображения</td></tr>
        % end
    </tbody>
</table> 