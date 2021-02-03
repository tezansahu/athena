# Project Athena

Project Athena is a python-based playground to understand & visualize Computer Graphics Curves interactively. It can be used to visualize [Bezier Curves](https://en.wikipedia.org/wiki/B%C3%A9zier_curve) & [B-Splines](https://en.wikipedia.org/wiki/B-spline) in 2D & 3D by specifying the control points.


## ❗❗ [Check out the app](https://project-athena-v1.herokuapp.com/) ❗❗

> _**Note:** The app currently implements the visualization of only Bezier Curves. Same for B-Splines will be made available soon._

## Running Locally

### Setup

```bash
# Create & activate a virtual environment
$ conda create --name athena
$ conda activate athena

# Clone the repository
(athena)$ git clone https://github.com/tezansahu/athena.git

# Install the required packages
(athena)$ conda install -c conda-forge --file requirements.txt
```

### Usage

```bash
(athena)$ streamlit run app.py
```