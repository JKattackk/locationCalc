import numpy as np
import pandas as pd

# Generate a large random dataset
N = 5000
df = pd.DataFrame({
    'x': np.random.normal(size=N),
    'y': np.random.normal(size=N),
    'z': np.random.normal(size=N)
})

import datashader as ds
import datashader.transfer_functions as tf

# Project onto x,y plane and count density
cvs = ds.Canvas(plot_width=800, plot_height=800)
agg = cvs.points(df, 'x', 'y')
x_coords = agg.coords['x'].values
y_coords = agg.coords['y'].values
X, Y = np.meshgrid(x_coords, y_coords)

# Flatten everything to match agg.values
X = X.flatten()
Y = Y.flatten()
densities = agg.values.flatten()

# Keep only nonzero-density cells
mask = densities > 0
X = X[mask]
Y = Y[mask]
densities = densities[mask]

# Repeat points proportional to density (cap for performance)
max_points = 200_000  # limit for plotly
prob = densities / densities.sum()
sample_idx = np.random.choice(len(X), size=max_points, p=prob)

x_sample = X[sample_idx]
y_sample = Y[sample_idx]
z_sample = np.random.choice(df['z'], size=max_points, replace=True)


import plotly.graph_objects as go

fig = go.Figure(data=[go.Scatter3d(
    x=x_sample,
    y=y_sample,
    z=z_sample,
    mode='markers',
    marker=dict(size=2, opacity=0.5)
)])

fig.update_layout(
    scene=dict(
        xaxis_title='X',
        yaxis_title='Y',
        zaxis_title='Z'
    ),
    title="3D Scatter (Datashader + Plotly)"
)

fig.show()