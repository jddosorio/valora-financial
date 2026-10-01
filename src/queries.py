import streamlit as st

from src.auth import get_supabase


def _authenticated_client():
    """Create a Supabase client using the current Streamlit session."""

    supabase = get_supabase()

    supabase.auth.set_session(
        st.session_state.access_token,
        st.session_state.refresh_token,
    )

    return supabase


@st.cache_data(ttl=300)
def get_sales(company_id: str):
    """Get authorized RCV sales."""

    supabase = _authenticated_client()

    response = (
        supabase
        .table("rcv_ventas")
        .select(
            "periodo, fecha_documento, rut_cliente, razon_social, "
            "monto_neto, iva, monto_total"
        )
        .eq("company_id", company_id)
        .order("fecha_documento")
        .execute()
    )

    return response.data


@st.cache_data(ttl=300)
def get_purchases(company_id: str):
    """Get authorized RCV purchases."""

    supabase = _authenticated_client()

    response = (
        supabase
        .table("rcv_compras")
        .select(
            "periodo, fecha_documento, rut_proveedor, razon_social, "
            "monto_neto, iva_recuperable, monto_total"
        )
        .eq("company_id", company_id)
        .order("fecha_documento")
        .execute()
    )

    return response.data