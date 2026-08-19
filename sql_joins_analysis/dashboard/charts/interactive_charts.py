import plotly.graph_objects as go
import numpy as np

def create_metric_chart(df):
    """
    Creates an interactive time-series chart with Plotly updatemenus for metric selection,
    date-range selectors, custom tooltips, and anomaly highlighting.
    """
    fig = go.Figure()
    
    # Define the 3 metrics we want to toggle between (from agg_daily_revenue)
    metrics = [
        {'col': 'total_revenue', 'name': 'Total Revenue ($)', 'format': '$%{y:,.2f}'},
        {'col': 'order_count', 'name': 'Order Count', 'format': '%{y:,.0f}'},
        {'col': 'avg_order_value', 'name': 'Avg Order Value ($)', 'format': '$%{y:,.2f}'}
    ]
    
    # Add traces for all metrics, but only make the first one visible initially
    for i, m in enumerate(metrics):
        # Calculate simple Z-score for anomaly detection (insight integration)
        mean = df[m['col']].mean()
        std = df[m['col']].std()
        # Handle cases with no variance
        if std == 0 or np.isnan(std):
            is_anomaly = [False] * len(df)
        else:
            # Highlight points > 1.5 standard deviations (lower threshold due to small sample size)
            is_anomaly = abs((df[m['col']] - mean) / std) > 1.5
            
        colors = ['#EF553B' if anomaly else '#636EFA' for anomaly in is_anomaly]
        marker_sizes = [12 if anomaly else 6 for anomaly in is_anomaly]
        
        # Add custom hover text for anomalies
        hover_texts = [
            '⚠️ Anomaly Detected' if anomaly else 'Normal Activity' 
            for anomaly in is_anomaly
        ]
        
        fig.add_trace(
            go.Scatter(
                x=df['aggregation_date'],
                y=df[m['col']],
                mode='lines+markers',
                name=m['name'],
                visible=(i == 0),
                marker=dict(color=colors, size=marker_sizes, line=dict(width=1, color='white')),
                line=dict(width=2, color='#636EFA'),
                text=hover_texts,
                hovertemplate=(
                    '<b>%{x|%b %d, %Y}</b><br>' +
                    f"{m['name']}: {m['format']}<br>" +
                    '<i>%{text}</i>' +
                    '<extra></extra>'
                )
            )
        )
        
    # Create dropdown buttons using updatemenus
    buttons = []
    for i, m in enumerate(metrics):
        visibility = [False] * len(metrics)
        visibility[i] = True
        
        button = dict(
            label=m['name'],
            method='update',
            args=[
                {'visible': visibility},
                {'yaxis': {'title': m['name']}}
            ]
        )
        buttons.append(button)
        
    # Add updatemenus and rangeselector (zoom/pan date selection)
    fig.update_layout(
        title='Business Metric Trend (Anomalies Highlighted in Red)',
        updatemenus=[dict(
            active=0,
            buttons=buttons,
            x=0.01,
            xanchor='left',
            y=1.15,
            yanchor='top'
        )],
        xaxis=dict(
            title='Date',
            rangeselector=dict(
                buttons=list([
                    dict(count=7, label='1W', step='day', stepmode='backward'),
                    dict(count=1, label='1M', step='month', stepmode='backward'),
                    dict(count=3, label='3M', step='month', stepmode='backward'),
                    dict(step='all', label='All')
                ])
            ),
            rangeslider=dict(visible=True),
            type='date'
        ),
        yaxis=dict(title=metrics[0]['name']),
        template='plotly_white',
        margin=dict(t=100) # Give space for dropdown
    )
    
    return fig
