import streamlit as st

from src.auth import get_supabase


def get_authorized_companies():

    supabase = get_supabase()

    # Restore the authenticated Supabase session
    supabase.auth.set_session(
        st.session_state.access_token,
        st.session_state.refresh_token,
    )

    response = (
        supabase
        .table("user_companies")
        .select(
            "company_id, role, active, "
            "companies(id, rut, razon_social, nombre_fantasia)"
        )
        .eq("active", True)
        .execute()
    )

    return response.data