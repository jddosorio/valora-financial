import pandas as pd
import streamlit as st

from src.queries import get_sales, get_purchases


def show_dashboard():

    company_id = st.session_state.company_id

    sales = get_sales(company_id)
    purchases = get_purchases(company_id)

    df_sales = pd.DataFrame(sales)
    df_purchases = pd.DataFrame(purchases)

    if df_sales.empty and df_purchases.empty:
        st.warning("No existen datos financieros disponibles.")
        return

    # --------------------------------------------------------
    # Period
    # --------------------------------------------------------

    periods = sorted(
        set(df_sales["periodo"].tolist())
        | set(df_purchases["periodo"].tolist())
    )

    years = sorted(
        {period[:4] for period in periods},
        reverse=True,
    )

    selected_year = st.selectbox(
        "Año",
        years,
    )

    sales_year = df_sales[
        df_sales["periodo"].str.startswith(selected_year)
    ].copy()

    purchases_year = df_purchases[
        df_purchases["periodo"].str.startswith(selected_year)
    ].copy()

    # --------------------------------------------------------
    # KPI
    # --------------------------------------------------------

    total_sales = sales_year["monto_neto"].sum()
    total_purchases = purchases_year["monto_neto"].sum()
    difference = total_sales - total_purchases

    st.subheader(f"Resumen Financiero {selected_year}")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Ventas Netas",
        f"${total_sales / 1_000_000:,.1f} M",
    )

    col2.metric(
        "Compras Netas",
        f"${total_purchases / 1_000_000:,.1f} M",
    )

    col3.metric(
        "Diferencia",
        f"${difference / 1_000_000:,.1f} M",
    )

    # --------------------------------------------------------
    # Monthly chart
    # --------------------------------------------------------

    monthly_sales = (
        sales_year
        .groupby("periodo")["monto_neto"]
        .sum()
    )

    monthly_purchases = (
        purchases_year
        .groupby("periodo")["monto_neto"]
        .sum()
    )

    monthly = pd.DataFrame({
        "Ventas": monthly_sales,
        "Compras": monthly_purchases,
    }).fillna(0)

    monthly.index = monthly.index.str[-2:]

    st.subheader("Ventas vs Compras")

    st.line_chart(
        monthly / 1_000_000,
        y_label="Millones CLP",
    )