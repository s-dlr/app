import streamlit as st

if __name__ == "__main__":
    st.header("Choix du nom de l'équipe")
    button_login = st.button("Log in")
    team = st.text_input("équipe", "astrolabe")
    if button_login:
        st.session_state["equipe"] = team
