import streamlit as st

st.header("Choix du nom de l'équipe")
team = st.text_input("équipe", "astrolabe")
if st.button("Log in"):
    st.session_state["equipe"] = team
    st.switch_page("pages/page_arborescence.py")
