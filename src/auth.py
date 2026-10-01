import streamlit as st
from supabase import create_client


@st.cache_resource
def get_supabase():
    return create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_KEY"],
    )


def sign_in(email: str, password: str):
    """Authenticate a VALORA user with Supabase Auth."""

    supabase = get_supabase()

    return supabase.auth.sign_in_with_password(
        {
            "email": email,
            "password": password,
        }
    )


def sign_out():
    """Close the current VALORA session."""

    supabase = get_supabase()

    try:
        supabase.auth.sign_out()
    except Exception:
        pass

    for key in (
        "authenticated",
        "user_id",
        "email",
        "access_token",
    ):
        st.session_state.pop(key, None)