import streamlit as st
from src.dashboard import show_dashboard
from src.authorization import get_authorized_companies

from src.auth import sign_in, sign_out
import pandas as pd

from src.queries import get_sales, get_purchases

st.set_page_config(
    page_title="VALORA | Portal Financiero",
    page_icon="📊",
    layout="centered",
)


# ------------------------------------------------------------
# Session initialization
# ------------------------------------------------------------

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False


# ------------------------------------------------------------
# Login
# ------------------------------------------------------------

if not st.session_state.authenticated:

    st.title("VALORA")
    st.subheader("Portal Financiero")

    st.write(
        "Ingrese sus credenciales para acceder a la "
        "información financiera de su empresa."
    )

    with st.form("login_form"):

        email = st.text_input(
            "Correo electrónico",
            value="user@acme.cl"
        )

        password = st.text_input(
            "Contraseña",
            value="123456",
            type="password"
        )

        submitted = st.form_submit_button(
            "INICIAR SESIÓN",
            use_container_width=True
        )

    if submitted:

        if not email or not password:
            st.warning("Ingrese correo electrónico y contraseña.")

        else:

            try:

                response = sign_in(
                    email.strip(),
                    password,
                )

                if response.user and response.session:

                    st.session_state.authenticated = True
                    st.session_state.user_id = response.user.id
                    st.session_state.email = response.user.email
                    st.session_state.access_token = (
                        response.session.access_token
                    )
                    st.session_state.refresh_token = (
                    response.session.refresh_token
                )

                    st.rerun()

                else:
                    st.error(
                        "No fue posible iniciar sesión."
                    )

            except Exception:
                st.error(
                    "Correo electrónico o contraseña incorrectos."
                )


# ------------------------------------------------------------
# Authenticated area
# ------------------------------------------------------------

else:

    try:
        authorized = get_authorized_companies()

    except Exception as exc:
        st.error("No fue posible obtener la empresa autorizada.")
        st.exception(exc)
        st.stop()

    if not authorized:

        st.error(
            "El usuario no tiene empresas autorizadas."
        )

        if st.button("Cerrar sesión"):
            sign_out()
            st.rerun()

        st.stop()

    # --------------------------------------------------------
    # Authorized company
    # --------------------------------------------------------

    authorization = authorized[0]
    company = authorization["companies"]

    st.session_state.company_id = authorization["company_id"]
    st.session_state.company_name = company["razon_social"]
    st.session_state.company_rut = company["rut"]
    st.session_state.role = authorization["role"]
    show_dashboard()

    # --------------------------------------------------------
    # Header
    # --------------------------------------------------------

    col1, col2 = st.columns([4, 2])

    with col1:
        st.title("VALORA")
        st.caption("Portal Financiero")

    with col2:
        st.markdown(
            f"### {st.session_state.company_name}"
        )

        st.caption(
            f"RUT {st.session_state.company_rut}"
        )

        if st.button("Cerrar sesión"):
            sign_out()
            st.rerun()

    st.divider()

    # --------------------------------------------------------
    # Company portal
    # --------------------------------------------------------

    st.subheader(
        f"Bienvenido a {st.session_state.company_name}"
    )

    st.write(
        f"Usuario: **{st.session_state.email}**"
    )

    st.write(
        f"Rol: **{st.session_state.role}**"
    )

 