import streamlit as st
import src.bezier
import src.b_spline

CURVES = {
    "Bezier Curve": src.bezier,
    "B-Spline": src.b_spline
}

def main():
    st.set_page_config(
        page_title="Project Athena",
        page_icon="📈",
        layout="centered",
        initial_sidebar_state="expanded"
    )
    st.title('Project Athena')
    st.subheader('An interactive playground to visualize Computer Graphics Curves')

    st.sidebar.title("Settings")
    selection = st.sidebar.radio("Choose the Curve to play with", list(CURVES.keys()))
    with st.spinner(f"Loading {selection} ..."):
        CURVES[selection].show()

    st.info('Developed with ❤️ by [Tezan Sahu](https://tezansahu.github.io/)')

if __name__ == "__main__":
	main()