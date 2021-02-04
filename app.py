import streamlit as st
import src.bezier
import src.b_spline

CURVES = {
    "Bezier Curve": src.bezier,
    "B-Spline": src.b_spline
}

def main():
    st.title('Project Athena')
    st.subheader('An interactive playground to visualize Computer Graphics Curves')

    st.sidebar.title("Settings")
    selection = st.sidebar.radio("Choose the Curve to play with", list(CURVES.keys()))
    with st.spinner(f"Loading {selection} ..."):
        CURVES[selection].show()

    st.sidebar.info('_Developed with ❤️ by [Tezan Sahu](https://tezansahu.github.io/)_')

if __name__ == "__main__":
	main()