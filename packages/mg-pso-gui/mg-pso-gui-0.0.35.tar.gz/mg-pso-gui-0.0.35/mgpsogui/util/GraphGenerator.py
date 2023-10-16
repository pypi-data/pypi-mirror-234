import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import numpy as np

def best_cost_stacked(config, dataframe):
    fig = go.Figure()
        
    total_steps = len(config)
    
    # Get unique values from the round_step column of the dataframe
    for iteration in dataframe['round_step'].unique():
        # Get best_cost and completed rounds rows for this iteration
        df = dataframe[dataframe['round_step'] == iteration]
        
        step_index = ((iteration) % total_steps)
        round_index = ((iteration) // total_steps)
        
        fig.add_trace(go.Scatter(x=df['completed_rounds'], y=df['best_cost'], name='Round ' + str(round_index + 1) +  ' Step ' + str(step_index + 1)))

    fig.update_layout(
        title="",
        xaxis_title="Iteration",
        yaxis_title="Best Cost",
        font=dict(color='white'),
        paper_bgcolor='rgba(42, 42, 42, 0)',
        plot_bgcolor='rgb(62, 62, 62)',
        xaxis=dict(
            gridcolor='rgb(72, 72, 72)',
            gridwidth=1
        ),
        yaxis=dict(
            range=[0, 0.6],
            autorange='reversed',
            gridcolor='rgb(72, 72, 72)',
            gridwidth=0.1
        )
    )

    fig.write_image("./best_cost_stacked.png", width=1280, height=720)
    fig.write_html("./best_cost_stacked.html", include_plotlyjs='cdn', auto_open=False)
    with open("./best_cost_stacked.html", "r") as f:
        html = f.read()
        html = html.replace("<body>", "<body bgcolor='#2a2a2a'>")
    with open("./best_cost_stacked.html", "w") as f:
        f.write(html)
    
    return fig

def table(config, dataframe):
    # Create a plotly table with the values in the dataframe
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=list(dataframe.columns),
            font=dict(color='black'),
            align="left"
        ),
        cells=dict(
            values=[dataframe[k].tolist() for k in dataframe.columns],
            font=dict(color='black'),
            align = "left")
    )])
    
    fig.update_layout(
        title="",
        xaxis_title="Iteration",
        yaxis_title="Best Cost",
        font=dict(color='white'),
        paper_bgcolor='rgba(42, 42, 42, 0)',
        plot_bgcolor='rgb(62, 62, 62)',
        xaxis=dict(
            gridcolor='rgb(72, 72, 72)',
            gridwidth=1
        ),
        yaxis=dict(
            range=[0, 0.6],
            autorange='reversed',
            gridcolor='rgb(72, 72, 72)',
            gridwidth=0.1
        )
    )

    fig.write_image("./table.png", width=1280, height=720)
    fig.write_html("./table.html", include_plotlyjs='cdn', auto_open=False)
    with open("./table.html", "r") as f:
        html = f.read()
        html = html.replace("<body>", "<body bgcolor='#2a2a2a'>")
    with open("./table.html", "w") as f:
        f.write(html)
    
    return fig

def best_cost_by_round(config, dataframe):
    fig = go.Figure()
        
    total_steps = len(config)
    
    # Get unique values from the round_step column of the dataframe
    for iteration in dataframe['round_step'].unique():
        # Get best_cost and completed rounds rows for this iteration
        df = dataframe[dataframe['round_step'] == iteration]
        
        step_index = ((iteration) % total_steps)
        round_index = ((iteration) // total_steps)
        
        fig.add_trace(go.Scatter(x=df['completed_rounds'] + (df['total_rounds'] * round_index), y=df['best_cost'], name='Step ' + str(step_index + 1)))
        
        xx = np.max(df['completed_rounds']) + (np.max(df['total_rounds']) * round_index)
        fig.add_shape(
            type='line',
            x0=xx,
            y0=0,
            x1=xx,
            y1=1,
            yref='paper',
            line=dict(
                color='rgb(102, 102, 102)',
                width=2
            )
        )
        
        fig.add_annotation(
            x=xx + 0.5,
            y=1,
            yref='paper',
            text='Round ' + str(round_index + 1),
            showarrow=False,
            yshift=-10
        )

    fig.update_layout(
        title="",
        xaxis_title="Iteration",
        yaxis_title="Best Cost",
        font=dict(color='white'),
        paper_bgcolor='rgba(42, 42, 42, 0)',
        plot_bgcolor='rgb(62, 62, 62)',
        xaxis=dict(
            gridcolor='rgb(72, 72, 72)',
            gridwidth=1
        ),
        yaxis=dict(
            range=[0, 0.6],
            autorange='reversed',
            gridcolor='rgb(72, 72, 72)',
            gridwidth=0.1
        )
    )

    fig.write_image("./best_cost_by_round.png", width=1280, height=720)
    fig.write_html("./best_cost_by_round.html", include_plotlyjs='cdn', auto_open=False)
    with open("./best_cost_by_round.html", "r") as f:
        html = f.read()
        html = html.replace("<body>", "<body bgcolor='#2a2a2a'>")
    with open("./best_cost_by_round.html", "w") as f:
        f.write(html)
    
    return fig

def calibrated_params_by_round(config, list_of_objs):
    fig = go.Figure()
        
    total_steps = len(config)
    
    datalines = {"step": [], "round": []}
    step = 1
    round = 1
    for index, obj in enumerate(list_of_objs):
        if (obj == {}):
            continue
        for key in obj.keys():
            if key not in datalines:
                datalines[key] = []
            datalines[key].append(obj[key])
        datalines["step"].append(step)
        datalines['round'].append(round)
        step += 1
        if (step > total_steps):
            step = 1
            round += 1
    
    # Get unique values from the round_step column of the dataframe
    for key in datalines.keys():
        # Get best_cost and completed rounds rows for this iteration
        if key == 'step' or key == 'round':
            continue
        
        fig.add_trace(go.Scatter(x=datalines['round'], y=datalines[key], name=key))

    fig.update_layout(
        title="",
        xaxis_title="Round",
        yaxis_title="Particle Parameters",
        font=dict(color='white'),
        paper_bgcolor='rgba(42, 42, 42, 0)',
        plot_bgcolor='rgb(62, 62, 62)',
        xaxis=dict(
            gridcolor='rgb(72, 72, 72)',
            gridwidth=1
        ),
        yaxis=dict(
            gridcolor='rgb(72, 72, 72)',
            gridwidth=0.1
        )
    )

    fig.write_image("./calibrated_params_by_round.png", width=1280, height=720)
    fig.write_html("./calibrated_params_by_round.html", include_plotlyjs='cdn', auto_open=False)
    with open("./calibrated_params_by_round.html", "r") as f:
        html = f.read()
        html = html.replace("<body>", "<body bgcolor='#2a2a2a'>")
    with open("./calibrated_params_by_round.html", "w") as f:
        f.write(html)
    
    return fig