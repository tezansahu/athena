import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

t = np.transpose(np.array([np.linspace(0, 1, 101)]))        # Values of t for plotting curve
V = np.zeros((4,2))                                         # Control Points (default: empty 4*2 matrix)

M_B = {
    2: np.array([[1, -1], [0, 1]]),
    3: np.array([[1, -2, 1], [0, 2, -2], [0, 0, 1]]),
    4: np.array([[1, -3, 3, 1], [0, 3, -6, 3], [0, 0, 3, -3], [0, 0, 0, 1]]),
    5: np.array([[1, -4, 6, -4, 1], [0, 4, -12, 12, -4], [0, 0, 6, -12, 6], [0, 0, 0, 4, -4], [0, 0, 0, 0, 1]])
}

DIMS = {
    "2D": 2,
    "3D": 3
}

def show():
    st.title('Bezier Curve')
    
    dims = DIMS[st.sidebar.radio("Choose the space", ["2D", "3D"])]

    st.sidebar.title("Control Points")
    n_plus_1 = st.sidebar.selectbox("Number of Control Points:", (2, 3, 4, 5), index=2)

    n = n_plus_1 - 1
    V = np.zeros((n_plus_1,dims))
    st.sidebar.markdown(f"__Degree of Bezier Curve:__ {n}")

    # Input for control points
    st.sidebar.markdown(f"## Set Control Points:")
    for i in range(n+1):

        st.sidebar.write(f'__Control Point V<sub>{i}</sub>:__', unsafe_allow_html=True)

        V[i, 0] = st.sidebar.number_input("X: ", key=f"x_{i}")
        V[i, 1] = st.sidebar.number_input("Y: ", key=f"y_{i}")
        
        if dims == 3:
            V[i, 2] = st.sidebar.number_input("Z: ", key=f"z_{i}")
        
    pts = calc_bezier(n, V)

    show_bezier(pts, V)

def calc_bezier(n, V):
    T = np.ones((101, 1))
    for i in range(1, n+1):
        T = np.append(np.power(t, i), T, axis=1)
    return np.matmul(np.matmul(T, M_B[n+1]), V)

def show_bezier(pts, V):
    # 2D Plot
    if pts.shape[1] == 2:
        control_pts = pd.DataFrame(data=V, columns=["x", "y"])
        bezier_pts = pd.DataFrame(data=pts, columns=["x", "y"])
        # fig = px.line(bezier_pts, x="X-axis", y="Y-axis", title="Bezier Curve Using Given Control Points")
        # fig.update_traces()
        fig = go.Figure([
            go.Scatter(
                name="Bezier Curve",
                x=bezier_pts["x"],
                y=bezier_pts["y"],
                mode="lines",
                line=dict(width=3, color="blue"),
                showlegend=True
            ),
            go.Scatter(
                name="Control Polynomial",
                x=control_pts["x"],
                y=control_pts["y"],
                mode="markers+lines",
                marker=dict(color="black", size=5),
                line=dict(color="red", width=1),
                showlegend=True
            )
        ])
        fig.update_layout(
            title="2D Bezier Curve Using Given Control Points",
            xaxis_title="X Axis",
            yaxis_title="Y Axis",
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # 3D Plot
    elif pts.shape[1] == 3:
        control_pts = pd.DataFrame(data=V, columns=["x", "y", "z"])
        bezier_pts = pd.DataFrame(data=pts, columns=["x", "y", "z"])

        fig = go.Figure([
            go.Scatter3d(
                name="Bezier Curve",
                x=bezier_pts["x"],
                y=bezier_pts["y"],
                z=bezier_pts["z"],
                mode="lines",
                line=dict(width=3, color="blue"),
                showlegend=True
            ),
            go.Scatter3d(
                name="Control Polynomial",
                x=control_pts["x"],
                y=control_pts["y"],
                z=control_pts["z"],
                mode="markers+lines",
                marker=dict(color="black", size=5),
                line=dict(color="red", width=1),
                showlegend=True
            )
        ])
        fig.update_layout(
            title="3D Bezier Curve Using Given Control Points",
            width=900,
            height=600,
        )
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.error("Something went wrong! Please recheck the settings")
