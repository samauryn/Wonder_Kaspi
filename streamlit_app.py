import pandas as pd
import plotly.graph_objects as go
import plotly.subplots as sp
import streamlit as st

# Загружаем данные
df_original = pd.read_csv("Akbope_report_clean.csv")

cutoff_date = pd.to_datetime('1-07-2024', format='%d-%m-%Y')
df_original['Date'] = pd.to_datetime(df_original['Date'])  # Автоматическое определение формата

df_filtered_cancelled = df_original[(df_original['Date'] != '2024-11-01') & 
                                    (df_original['status'].isin(["CANCELLED", "CANCELLING"]))]

# Группируем данные по месяцу: общее количество продаж и количество отмен
monthly_sales_all = df_original['Date'].dt.to_period('M').value_counts().sort_index()
monthly_sales_cancelled = df_filtered_cancelled['Date'].dt.to_period('M').value_counts().sort_index()

# Разделяем данные на до и после cutoff_date
monthly_sales_all_before = monthly_sales_all[monthly_sales_all.index < cutoff_date.to_period('M')]
monthly_sales_all_after = monthly_sales_all[monthly_sales_all.index >= cutoff_date.to_period('M')]
monthly_sales_cancelled_before = monthly_sales_cancelled[monthly_sales_cancelled.index < cutoff_date.to_period('M')]
monthly_sales_cancelled_after = monthly_sales_cancelled[monthly_sales_cancelled.index >= cutoff_date.to_period('M')]

# Создаем график с Plotly
st.title("Анализ данных о заказах")
fig1 = go.Figure()

# Добавляем данные по общим продажам до cutoff_date
fig1.add_trace(go.Bar(
    x=monthly_sales_all_before.index.astype(str),
    y=monthly_sales_all_before.values,
    name='До 1.07.2024 (все продажи)',
    marker_color='#5CA4F8'
))

# Добавляем данные по общим продажам после cutoff_date
fig1.add_trace(go.Bar(
    x=monthly_sales_all_after.index.astype(str),
    y=monthly_sales_all_after.values,
    name='После 1.07.2024 (все продажи)',
    marker_color='#FDA25E'
))

# Добавляем данные по отменам до cutoff_date (заполнением)
fig1.add_trace(go.Bar(
    x=monthly_sales_cancelled_before.index.astype(str),
    y=monthly_sales_cancelled_before.values,
    name='До 1.07.2024 (отмененные)',
    marker_color='#0A7CFE',
    opacity=0.5
))

# Добавляем данные по отменам после cutoff_date (заполнением)
fig1.add_trace(go.Bar(
    x=monthly_sales_cancelled_after.index.astype(str),
    y=monthly_sales_cancelled_after.values,
    name='После 1.07.2024 (отмененные)',
    marker_color='#FF6D00',
    opacity=0.5
))

# Вычисляем проценты отмен для каждого месяца
percent_cancelled_before = (monthly_sales_cancelled_before / monthly_sales_all_before) * 100
percent_cancelled_after = (monthly_sales_cancelled_after / monthly_sales_all_after) * 100

# Добавляем аннотации с процентами отмен
for i, month in enumerate(monthly_sales_all_before.index.astype(str)):
    fig1.add_annotation(
        x=month,
        y=monthly_sales_all_before.values[i] + 1,  # Смещение по оси Y для удобства
        text=f"{percent_cancelled_before[i]:.1f}%",
        showarrow=False,
        font=dict(color="black"),
        align="center"
    )

for i, month in enumerate(monthly_sales_all_after.index.astype(str)):
    fig1.add_annotation(
        x=month,
        y=monthly_sales_all_after.values[i] + 1,  # Смещение по оси Y для удобства
        text=f"{percent_cancelled_after[i]:.1f}%",
        showarrow=False,
        font=dict(color="black"),
        align="center"
    )

# Настройка графика с измененной шириной и высотой
fig1.update_layout(
    title='Ежемесячное количество продаж и отмен',
    xaxis_title='Месяц',
    yaxis_title='Количество',
    barmode='overlay',  # Позволяет накладывать отмены на общие продажи
    xaxis_tickangle=-45,
    width=1000,   # Задайте нужную ширину
    height=600    # Задайте нужную высоту
)

# fig1.show()

st.plotly_chart(fig1)
st.title("")
cutoff_date = pd.to_datetime('1-07-2024', format='%d-%m-%Y')
df_original['Date'] = pd.to_datetime(df_original['Date'], format='%d-%m-%Y')


df_filtered_cancelled = df_original[(df_original['Date'] != '2024-11-01') & 
                                    (df_original['status'].isin(["CANCELLED", "CANCELLING"]))]

# Группируем данные по месяцу: сумма продаж и сумма отмен по колонке total_price
monthly_sales_all = df_original.groupby(df_original['Date'].dt.to_period('M'))['total_price'].sum()
monthly_sales_cancelled = df_filtered_cancelled.groupby(df_filtered_cancelled['Date'].dt.to_period('M'))['total_price'].sum()

# Разделяем данные на до и после cutoff_date
monthly_sales_all_before = monthly_sales_all[monthly_sales_all.index < cutoff_date.to_period('M')]
monthly_sales_all_after = monthly_sales_all[monthly_sales_all.index >= cutoff_date.to_period('M')]
monthly_sales_cancelled_before = monthly_sales_cancelled[monthly_sales_cancelled.index < cutoff_date.to_period('M')]
monthly_sales_cancelled_after = monthly_sales_cancelled[monthly_sales_cancelled.index >= cutoff_date.to_period('M')]

# Создаем график с Plotly
fig2 = go.Figure()

# Добавляем данные по сумме продаж до cutoff_date
fig2.add_trace(go.Bar(
    x=monthly_sales_all_before.index.astype(str),
    y=monthly_sales_all_before.values,
    name='До 1.07.2024 (все продажи)',
    marker_color='#5CA4F8'
))

# Добавляем данные по сумме продаж после cutoff_date
fig2.add_trace(go.Bar(
    x=monthly_sales_all_after.index.astype(str),
    y=monthly_sales_all_after.values,
    name='После 1.07.2024 (все продажи)',
    marker_color='#FDA25E'
))

# Добавляем данные по сумме отмен до cutoff_date (с полупрозрачностью)
fig2.add_trace(go.Bar(
    x=monthly_sales_cancelled_before.index.astype(str),
    y=monthly_sales_cancelled_before.values,
    name='До 1.07.2024 (отмененные)',
    marker_color='#0A7CFE',
    opacity=0.5
))

# Добавляем данные по сумме отмен после cutoff_date (с полупрозрачностью)
fig2.add_trace(go.Bar(
    x=monthly_sales_cancelled_after.index.astype(str),
    y=monthly_sales_cancelled_after.values,
    name='После 1.07.2024 (отмененные)',
    marker_color='#FF6D00',
    opacity=0.5
))

# Вычисляем процент отмен от общей суммы продаж для каждого месяца
percent_cancelled_before = (monthly_sales_cancelled_before / monthly_sales_all_before) * 100
percent_cancelled_after = (monthly_sales_cancelled_after / monthly_sales_all_after) * 100

# Добавляем аннотации с процентами отмен
for i, month in enumerate(monthly_sales_all_before.index.astype(str)):
    fig2.add_annotation(
        x=month,
        y=monthly_sales_all_before.values[i] + 10000,  # Смещение по оси Y для удобства
        text=f"{percent_cancelled_before[i]:.1f}%",
        showarrow=False,
        font=dict(color="black"),
        align="center"
    )

for i, month in enumerate(monthly_sales_all_after.index.astype(str)):
    fig2.add_annotation(
        x=month,
        y=monthly_sales_all_after.values[i] + 10000,  # Смещение по оси Y для удобства
        text=f"{percent_cancelled_after[i]:.1f}%",
        showarrow=False,
        font=dict(color="black"),
        align="center"
    )

# Настройка графика
fig2.update_layout(
    title='Ежемесячная сумма продаж и отмен по total_price',
    xaxis_title='Месяц',
    yaxis_title='Сумма (total_price)',
    barmode='overlay',  # Наложение отмен на общие продажи
    xaxis_tickangle=-45,
    width=1000,   # Ширина графика
    height=600    # Высота графика
)


st.plotly_chart(fig2)
st.title("")
df_original['Date'] = pd.to_datetime(df_original['Date'], format='%d-%m-%Y')

# Определяем группы статусов
status_groups = {
    "Cancelled": ["CANCELLED", "CANCELLING"],
    "Completed": ["ACCEPTED_BY_MERCHANT", "COMPLETED"],
    "Returned": ["RETURNED"]
}

# Создаем DataFrame для хранения данных по статусам
df_original['StatusGroup'] = df_original['status'].apply(lambda x: 
    "Cancelled" if x in status_groups["Cancelled"] else
    "Completed" if x in status_groups["Completed"] else
    "Returned" if x in status_groups["Returned"] else None
)

# Группируем данные по месяцу и по статусу, затем считаем количество каждого статуса
monthly_status_counts = df_original.groupby([df_original['Date'].dt.to_period('M'), 'StatusGroup']).size().unstack(fill_value=0)

# Преобразуем количество в проценты по каждой строке
monthly_status_percentages = monthly_status_counts.div(monthly_status_counts.sum(axis=1), axis=0) * 100
monthly_status_percentages.index = monthly_status_percentages.index.astype(str)  # Преобразуем индексы в строки для графика

# Получаем данные за последний месяц
last_month = monthly_status_percentages.iloc[-1]
last_month_index = monthly_status_percentages.index[-1]

# Создаем график
st.title("")
fig3 = go.Figure()

# Добавляем каждую группу как область на графике с пастельными цветами
fig3.add_trace(go.Scatter(
    x=monthly_status_percentages.index,
    y=monthly_status_percentages['Cancelled'],
    mode='lines',
    name='Cancelled',
    stackgroup='one',
    fillcolor='rgba(255, 182, 193, 0.6)',  # Пастельный розовый для Cancelled
    line=dict(color='rgba(255, 182, 193, 1)')  # Цвет линии соответствует заполнению
))

fig3.add_trace(go.Scatter(
    x=monthly_status_percentages.index,
    y=monthly_status_percentages['Completed'],
    mode='lines',
    name='Completed',
    stackgroup='one',
    fillcolor='rgba(152, 251, 152, 0.6)',  # Пастельный зеленый для Completed
    line=dict(color='rgba(152, 251, 152, 1)')  # Цвет линии соответствует заполнению
))

fig3.add_trace(go.Scatter(
    x=monthly_status_percentages.index,
    y=monthly_status_percentages['Returned'],
    mode='lines',
    name='Returned',
    stackgroup='one',
    fillcolor='rgba(173, 216, 230, 0.6)',  # Пастельный голубой для Returned
    line=dict(color='rgba(173, 216, 230, 1)')  # Цвет линии соответствует заполнению
))

# Добавляем аннотации для последнего месяца для каждой группы, размещая их по высоте в центре каждой области
fig3.add_annotation(
    x=last_month_index,
    y=last_month['Cancelled'] / 2,  # Центр области "Cancelled"
    text=f"{last_month['Cancelled']:.1f}%",
    showarrow=False,
    font=dict(size=14, color="rgba(255, 0, 0, 0.8)")  # Красный текст с прозрачностью
)

fig3.add_annotation(
    x=last_month_index,
    y=last_month['Completed'] / 2 + last_month['Cancelled'],  # Центр области "Completed"
    text=f"{last_month['Completed']:.1f}%",
    showarrow=False,
    font=dict(size=14, color="rgba(0, 128, 0, 0.8)")  # Зеленый текст с прозрачностью
)

fig3.add_annotation(
    x=last_month_index,
    y=last_month['Returned'] / 2 + last_month['Cancelled'] + last_month['Completed'],  # Центр области "Returned"
    text=f"{last_month['Returned']:.1f}%",
    showarrow=False,
    font=dict(size=14, color="rgba(0, 0, 255, 0.8)")  # Синий текст с прозрачностью
)

# Добавляем вертикальную линию для июля 2024 года с прозрачностью
fig3.update_layout(
    shapes=[
        dict(
            type="line",
            x0="2024-07",
            x1="2024-07",
            y0=0,
            y1=100,
            line=dict(color="rgba(0, 0, 0, 0.6)", width=2, dash="dash")  # Черный с 60% прозрачностью
        )
    ]
)

# Настройка графика
fig3.update_layout(
    title='Процентное соотношение статусов заказов по месяцам',
    xaxis_title='Месяц',
    yaxis_title='Процент',
    yaxis=dict(ticksuffix='%'),  # Добавляем % к значениям по оси Y
    width=1000,
    height=600
)

st.plotly_chart(fig3)
st.title("")
status_groups = {
    "Cancelled": ["CANCELLED", "CANCELLING"],
    "Completed": ["ACCEPTED_BY_MERCHANT", "COMPLETED"],
    "Returned": ["RETURNED"]
}

# Создаем новый столбец 'StatusGroup', чтобы классифицировать статусы
df_original['StatusGroup'] = df_original['status'].apply(
    lambda x: "Cancelled" if x in status_groups["Cancelled"] else
              "Completed" if x in status_groups["Completed"] else
              "Returned" if x in status_groups["Returned"] else None
)

# Получаем уникальные значения 'Delivery_type'
delivery_types = df_original['Delivery_type'].unique()

# Создаем пустой subplot для всех графиков
fig4 = go.Figure()
fig4 = sp.make_subplots(rows=1, cols=len(delivery_types), subplot_titles=delivery_types, specs=[[{'type': 'domain'}]*len(delivery_types)])

# Цвета для каждого статуса
colors = {"Cancelled": "#ff6b6b", "Completed": "#4caf50", "Returned": "#2196f3"}

# Генерируем отдельный график для каждого типа доставки
for i, delivery_type in enumerate(delivery_types):
    # Фильтруем данные для текущего типа доставки
    df_filtered = df_original[df_original['Delivery_type'] == delivery_type]
    
    # Подсчитываем количество каждого статуса
    status_counts = df_filtered['StatusGroup'].value_counts()
    
    # Добавляем круговую диаграмму в subplot
    fig4.add_trace(go.Pie(
        labels=status_counts.index,
        values=status_counts.values,
        name=delivery_type,
        marker=dict(colors=[colors[label] for label in status_counts.index]),
        textinfo='label+percent'
    ), row=1, col=i+1)

# Настройка графика
fig4.update_layout(
    title_text="Распределение статусов заказов по типу доставки",
    width=1200,
    height=400
)
st.plotly_chart(fig4)
