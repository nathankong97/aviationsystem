import plotly.graph_objs as go
import numpy as np
from plotly.offline import download_plotlyjs, init_notebook_mode, plot,iplot

'''x=np.array([2,5,8,0,2,-8,4,3,1])
y=np.array([2,5,8,0,2,-8,4,3,1])'''


#data = [go.Scatter(x=x,y=y)]
'''fig = go.Figure(data = data,layout = go.Layout(title='Offline Plotly Testing',width = 800,height = 500,
                                           xaxis = dict(title = 'X-axis'), yaxis = dict(title = 'Y-axis')))'''

nyc_london = [dict(
    type='scattergeo',
    lat=[35.7720, 32.896801],
    lon=[140.3929, -97.038002],
    mode='lines',
    line=dict(
        width=1,
        color='red',
    ),
)]

layout = dict(
    title='London to NYC Great Circle',
    showlegend=False,
    geo=dict(
        resolution=50,
        showland=True,
        #showlakes=True,
        landcolor='rgb(243, 243, 243)',
        countrycolor='rgb(204, 204, 204)',
        #lakecolor='rgb(255, 255, 255)',
        projection=dict(type="Mercator"),
        coastlinewidth=2,
    )
)

fig = dict(data=nyc_london, layout=layout)


plot(fig, validate=False)



'''lataxis=dict(
            range=[30, 150],
            showgrid=True,
            tickmode="linear",
            dtick=10
        ),
        lonaxis=dict(
            range=[-100, 40],
            showgrid=True,
            tickmode="linear",
            dtick=20
        ),'''