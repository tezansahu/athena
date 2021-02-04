import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objs as go

DIMS = {
    "2D": 2,
    "3D": 3
}

def show():
    st.title('B-Spline')
    
    dims = DIMS[st.sidebar.radio("Choose the space", ["2D", "3D"])]

    st.sidebar.title("Spline Settings")
    n = st.sidebar.selectbox("Number of Control Points:", np.arange(2, 11, 1), index=1) - 1
    k = st.sidebar.selectbox("Degree of B-Spline:", np.arange(1, n+1, 1), index= 0 if n==1 else 1)
    
    # Define the Knot Vector
    knot_type = st.sidebar.radio("Category of Knot Vector:", ["Uniform", "Uniform Open"])
    m = (n + 1) + k

    # Generic Knot Vector: [t_0, t_1, ..., t_k, ..., t_n+1, ...t_m]
    if knot_type == "Uniform":
        knots = np.arange(0, m+1, 1)                            # [0, 1, ..., k, ..., n+1, ..., m]
    elif knot_type == "Uniform Open":
        knots = np.arange(0, m+1, 1)
        knots[:k] = knots[k]
        knots[n+2:] = knots[n+1]                                # First (k+1) values = k & last (k+1) values = n+1
    
    show_knots = st.sidebar.checkbox("Show Knot Vector")
    if show_knots:
        knot_vec = "["
        knot_vec += "".join([f"{i}, " for i in knots])
        knot_vec = "]".join(knot_vec.rsplit(", ", 1))
        st.sidebar.markdown(f"__Knot Vector:__ {knot_vec}")

    T = np.linspace(knots[k], knots[n+1], 101)                  # Domain on which the B-Spline is defined

    # Set the Control Points
    V = np.zeros((n+1,dims))
    st.sidebar.markdown(f"## Set Control Points:")
    for i in range(n+1):

        st.sidebar.write(f'__Control Point V<sub>{i}</sub>:__', unsafe_allow_html=True)

        V[i, 0] = st.sidebar.number_input("X: ", key=f"x_{i}")
        V[i, 1] = st.sidebar.number_input("Y: ", key=f"y_{i}")
        
        if dims == 3:
            V[i, 2] = st.sidebar.number_input("Z: ", key=f"z_{i}")

    pts = calc_bspline(k, T, V, knots, knot_type)

    show_bspline(pts, V)


def get_basis_func(i, k, knots, t):
    # Base case [for N(i, 0)(t)]
    if k == 0:
        if knots[i] <= t < knots[i+1]:
            return 1
        else:
            return 0
        # if knot_type == "Uniform" and knots[i] <= t < knots[i+1]:
        #     return 1
        # elif knot_type == "Uniform Open" and knots[i] <= t <= knots[i+1]:
        #     return 1
        # else:
        #     return 0

    # Recursive formulation to obtain basis function [N(i,k)(t)]
    else:
        if knots[i+k] == knots[i]:
            term1 = 0
        else:
            term1 = ((t - knots[i])/(knots[i+k] - knots[i])) * get_basis_func(i, k-1, knots, t)

        if knots[i+k+1] == knots[i+1]:
            term2 = 0
        else:
            term2 = ((knots[i+k+1] - t)/(knots[i+k+1] - knots[i+1])) * get_basis_func(i+1, k-1, knots, t)
        
        return term1 + term2


def calc_bspline(k, T, V, knots, knot_type):
    pts = np.zeros((T.shape[0], V.shape[1]))        # Store points on the B-Spline

    for t_i, t in enumerate(T):
        for i, ct_pt in enumerate(V):
            pts[t_i] += ct_pt * get_basis_func(i, k, knots, t)
    
    # Enforcing boundary conditions
    if knot_type == "Uniform":
        pts[0] = (V[0] + V[1])/2
        pts[T.shape[0]-1] = (V[-1] + V[-2])/2
    elif knot_type == "Uniform Open":
        pts[0] = V[0]
        pts[T.shape[0]-1] = V[-1]

    return pts

def show_bspline(pts, V):
    # 2D Plot
    if pts.shape[1] == 2:
        control_pts = pd.DataFrame(data=V, columns=["x", "y"])
        bspline_pts = pd.DataFrame(data=pts, columns=["x", "y"])
        fig = go.Figure(
            data = [
                go.Scatter(
                    name="B-Spline",
                    x=bspline_pts["x"],
                    y=bspline_pts["y"],
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
            ],
        )
        fig.update_layout(
            title="2D B-Spline Using Given Control Points",
            xaxis_title="X Axis",
            yaxis_title="Y Axis",
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # 3D Plot
    elif pts.shape[1] == 3:
        control_pts = pd.DataFrame(data=V, columns=["x", "y", "z"])
        bspline_pts = pd.DataFrame(data=pts, columns=["x", "y", "z"])

        fig = go.Figure([
            go.Scatter3d(
                name="B-Spline",
                x=bspline_pts["x"],
                y=bspline_pts["y"],
                z=bspline_pts["z"],
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
            title="3D B-Spline Using Given Control Points",
            width=900,
            height=600,
        )
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.error("Something went wrong! Please recheck the settings")