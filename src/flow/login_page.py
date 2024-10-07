import streamlit as st

if __name__ == "__main__":
    st.header("Choix du nom de l'équipe")
    if st.button("Log in"):
        title = st.text_input("équipe", "astrolabe")
        st.session_state.equipe = title
