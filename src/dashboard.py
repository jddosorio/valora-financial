import pandas as pd
import streamlit as st

from src.queries import get_sales, get_purchases


def show_dashboard():

    company_id = st.session_state.company_id
    company_name = st.session_state.company_name
    company_rut = st.session_state.company_rut

    sales = get_sales(company_id)
    purchases = get_purchases(company_id)

    df_sales = pd.DataFrame(sales)
    df_purchases = pd.DataFrame(purchases)

    if df_sales.empty and df_purchases.empty:
        st.warning("No existen datos financieros disponibles.")
        return

    st.title(company_name)
    st.markdown(f"**RUT:** {company_rut}")

    # --------------------------------------------------------
    # Period
    # --------------------------------------------------------

    df_sales["period_date"] = pd.to_datetime(
        df_sales["periodo"],
        format="%Y%m",
    )

    df_purchases["period_date"] = pd.to_datetime(
        df_purchases["periodo"],
        format="%Y%m",
    )

    latest_date = max(
        df_sales["period_date"].max(),
        df_purchases["period_date"].max(),
    )

    period_options = {
        "Últimos 6 meses": 6,
        "Últimos 12 meses": 12,
        "Últimos 18 meses": 18,
        "Últimos 24 meses": 24,
    }

    selected_period = st.selectbox(
        "Período",
        list(period_options.keys()),
        index=1,
    )

    months = period_options[selected_period]

    start_date = latest_date - pd.DateOffset(
        months=months - 1
    )

    sales_period = df_sales[
        df_sales["period_date"].between(
            start_date,
            latest_date,
        )
    ].copy()

    purchases_period = df_purchases[
        df_purchases["period_date"].between(
            start_date,
            latest_date,
        )
    ].copy()

    # --------------------------------------------------------
    # KPI
    # --------------------------------------------------------


    total_sales = sales_period["monto_neto"].sum()
    total_purchases = purchases_period["monto_neto"].sum()
    difference = total_sales - total_purchases

    st.subheader(
        f"Resumen Financiero — {selected_period}"
    )

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
        sales_period
        .groupby("periodo")["monto_neto"]
        .sum()
    )

    monthly_purchases = (
        purchases_period
        .groupby("periodo")["monto_neto"]
        .sum()
    )

    monthly = pd.DataFrame({
        "Ventas": monthly_sales,
        "Compras": monthly_purchases,
    }).fillna(0)

    # Show month and year on X axis
    monthly.index = pd.to_datetime(
        monthly.index,
        format="%Y%m",
    ).strftime("%b %y")

    st.subheader("Ventas vs Compras")

    st.line_chart(
        monthly / 1_000_000,
        y_label="Millones CLP",
        use_container_width=True,
    )