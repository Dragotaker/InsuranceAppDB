<style>
.report-card {
    background: #f9f9fb;
    border: 1px solid #e0e0e0;
    border-radius: 10px;
    padding: 18px 20px;
    margin-bottom: 22px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    max-width: 600px;
}
.report-card form, .report-card a.button {
    margin-top: 10px;
    display: inline-block;
}
.report-card label {
    font-weight: 500;
    margin-right: 8px;
}
</style>
<h1>Отчёты</h1>
<div style="display: flex; flex-direction: column; align-items: flex-start;">
    <div class="report-card">
        <div><b>Полисы по категориям</b></div>
        <a href="/report/policies_by_category" class="button">Показать</a>
    </div>
    <div class="report-card">
        <div><b>Клиенты с активными полисами</b></div>
        <a href="/report/active_clients" class="button">Показать</a>
    </div>
    <div class="report-card">
        <div><b>Страховые случаи за период</b></div>
        <form action="/report/claims_by_period" method="post">
            <label>Период:</label>
            <input type="date" name="start_date" required> —
            <input type="date" name="end_date" required>
            <button type="submit" class="button">Показать</button>
        </form>
    </div>
    <div class="report-card">
        <div><b>Платежи за период</b></div>
        <form action="/report/payments_by_period" method="post">
            <label>Период:</label>
            <input type="date" name="start_date" required> —
            <input type="date" name="end_date" required>
            <button type="submit" class="button">Показать</button>
        </form>
    </div>
    <div class="report-card">
        <div><b>События по категориям</b></div>
        <a href="/report/events_by_category" class="button">Показать</a>
    </div>
</div> 