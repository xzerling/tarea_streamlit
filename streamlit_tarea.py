import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(
    page_title="Grupo 40",
    layout="wide",
    initial_sidebar_state="expanded")

col = st.columns((2, 4, 2), gap='medium')

df = pd.read_csv("data.csv")

# Columna Date transformada a tipo date para hacer los filtros
df['Date'] = pd.to_datetime(df['Date'])

# Se crea una sidebar para contener los filtros
with st.sidebar:
    st.header("Filtros")

    # Filtros por fecha
    start_date = st.date_input("Fecha inicio", df['Date'].min(), min_value=df['Date'].min(), max_value=df['Date'].max())
    end_date = st.date_input("Fecha termino", df['Date'].max(), min_value=df['Date'].min(), max_value=df['Date'].max())

    # Filtros de sucursal
    branch_options = ['Todos'] + list(df['Branch'].unique())
    selected_branch = st.selectbox("Branch", branch_options, index=0)

    # Filtros de linea de producto
    product_line_options = ['Todos'] + list(df['Product line'].unique())
    selected_product_line = st.selectbox("Product Line", product_line_options, index=0)

    # Filtro por genero
    gender_options = ['Todos'] + list(df['Gender'].unique())
    selected_gender = st.selectbox("Genero", gender_options, index=0)

# Se aplican los filtro sobre una copia del df original
dfFiltrado = df[(df['Date'] >= pd.to_datetime(start_date)) & (df['Date'] <= pd.to_datetime(end_date))]

if selected_branch != 'Todos':
    dfFiltrado = dfFiltrado[dfFiltrado['Branch'] == selected_branch]

if selected_product_line != 'Todos':
    dfFiltrado = dfFiltrado[dfFiltrado['Product line'] == selected_product_line]

if selected_gender != 'Todos':
    dfFiltrado = dfFiltrado[dfFiltrado['Gender'] == selected_gender]


# Se separa el dashboard en 3 columnas para ordenar los graficos
with col[0]:
    # Columna 0

    # Grafico 1
    st.title('Frecuencia de Métodos de Pago')

    # Conteo de elementos repetidos en la columna payment
    payment_counts = dfFiltrado['Payment'].value_counts()
    payment_counts_df = pd.DataFrame({'Payment': payment_counts.index, 'Frequency': payment_counts.values})
    st.bar_chart(
        data=payment_counts_df,
        x='Payment',
        y='Frequency',
        x_label='Método de Pago',
        y_label='Frecuencia',
        use_container_width=True
    )

    # Grafico 2
    st.title('Distribución del Gasto Total por Tipo de Cliente')

    chart = alt.Chart(dfFiltrado).mark_boxplot().encode(
        x=alt.X('Customer type', axis=alt.Axis(title='Tipo de Cliente')),
        y=alt.Y('Total', axis=alt.Axis(title='Gasto Total')),
        tooltip=[
        alt.Tooltip('Customer type', title='Tipo de Cliente'),
        alt.Tooltip('Total', title='Gasto Total')
    ]).properties(title='Distribución del Gasto Total por Tipo de Cliente').interactive()

    st.altair_chart(chart, use_container_width=True)


with col[1]:
    # Columna 1

    # Grafico 3
    st.title('Variación de Ventas Totales a lo Largo del Tiempo')
    # dataframe filtrado agrupado por fecha y sumando los totales
    ventasPorFecha = dfFiltrado.groupby('Date')['Total'].sum().reset_index()

    # Grafico de barra con el df agrupado
    st.line_chart(
        data=ventasPorFecha,
        x='Date',
        y='Total',
        x_label="Fecha",
        y_label="Ventas Totales"
    )

    # Grafico 4
    st.title('Total de ventas por línea de producto')

    # Calculo del total de ventas por linea de producto
    ingresoPorProducto = dfFiltrado.groupby('Product line')['Total'].sum().reset_index()

    st.bar_chart(
        data=ingresoPorProducto,
        x='Product line',
        y='Total',
        x_label="Linea de producto",
        y_label="Total de ventas",
        use_container_width=True
    )


with col[2]:
# Columna 2

# Grafico 5
    st.title('Ingreso bruto por sucursal y linea de producto')

    # df agrupado por sucursal, linea de producto, y la suma de los ingresos brutos
    df_grouped = dfFiltrado.groupby(['Branch', 'Product line'])['gross income'].sum().reset_index()

    # Grafico de columnas apiladas
    chart = alt.Chart(df_grouped).mark_bar().encode(
        x=alt.X('Branch', axis=alt.Axis(title='Sucursal')),
        y=alt.Y('gross income', axis=alt.Axis(title='Ingreso bruto')),
        color='Product line',
        tooltip=[
        alt.Tooltip('Branch', title='Sucursal'),
        alt.Tooltip('Product line', title='Línea de Producto'),
        alt.Tooltip('gross income', title='Ingreso Bruto')
        ]
    ).properties(
        title='Ingreso bruto por sucursal y linea de producto'
    ).interactive()

    st.altair_chart(chart, use_container_width=True)

# Dataframe con capacidades de filtrado
st.title('Ventas realizadas')
st.dataframe(dfFiltrado)
