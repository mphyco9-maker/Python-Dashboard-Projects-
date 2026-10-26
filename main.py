import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import numpy as np


np.random.seed(42)

categories = ['Electronics', 'Clothing', 'Home & Kitchen', 'Books', 'Toys']
regions = ['North', 'South', 'East', 'West']
channels = ['Online Store', 'Retail Store', 'Distributor']
segments = ['Corporate', 'Wholesale', 'Consumer']
dates = pd.date_range(start='2026-01-01', periods=10, freq='ME')

records = []
for date in dates:
    for reg in regions:
        for ch in channels:
            for cat in categories:
                
                seg = np.random.choice(segments, p=[0.4, 0.35, 0.25])
                ad_spend = np.random.randint(600, 4500)
                units = int(ad_spend * np.random.uniform(0.08, 0.22) + np.random.randint(10, 50))
                price = np.random.randint(30, 120)
                revenue = units * price
                profit = revenue * np.random.uniform(0.18, 0.36)

                records.append({
                    'Date': date,
                    'Month': date.strftime('%b %Y'),
                    'Region': reg,
                    'Channel': ch,
                    'Category': cat,
                    'CustomerSegment': seg,
                    'AdSpend': ad_spend,
                    'UnitsSold': units,
                    'Revenue': round(revenue, 2),
                    'Profit': round(profit, 2)
                })

df = pd.DataFrame(records)

app = dash.Dash(__name__)

CARD_STYLE = {
    'backgroundColor': '#1e293b',
    'borderRadius': '12px',
    'padding': '18px',
    'border': '1px solid #334155'
}

app.layout = html.Div(
    style={'backgroundColor': '#0f172a', 'color': '#f8fafc', 'fontFamily': 'Segoe UI, sans-serif', 'padding': '24px'},
    children=[
        # Title Header
        html.Div(
            style={'marginBottom': '20px'},
            children=[
                html.H1("Executive Performance Analytics", style={'margin': '0 0 6px 0', 'fontSize': '26px', 'fontWeight': '600'}),
                html.P("Dynamic interactive reporting across Bar, Line, Scatter, Donut, and Pie visuals",
                       style={'margin': '0', 'color': '#94a3b8', 'fontSize': '14px'})
            ]
        ),

        html.Div(
            style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '16px', 'marginBottom': '20px', **CARD_STYLE},
            children=[
                html.Div([
                    html.Label("Filter by Region:", style={'fontSize': '13px', 'color': '#94a3b8', 'marginBottom': '6px', 'display': 'block'}),
                    dcc.Dropdown(
                        id='filter-region',
                        options=[{'label': 'All Regions', 'value': 'ALL'}] + [{'label': r, 'value': r} for r in regions],
                        value='ALL',
                        clearable=False,
                        style={'color': '#0f172a'}
                    )
                ]),
                html.Div([
                    html.Label("Filter by Sales Channel:", style={'fontSize': '13px', 'color': '#94a3b8', 'marginBottom': '6px', 'display': 'block'}),
                    dcc.Dropdown(
                        id='filter-channel',
                        options=[{'label': 'All Channels', 'value': 'ALL'}] + [{'label': ch, 'value': ch} for ch in channels],
                        value='ALL',
                        clearable=False,
                        style={'color': '#0f172a'}
                    )
                ]),
            ]
        ),

        html.Div(
            style={'display': 'grid', 'gridTemplateColumns': 'repeat(4, 1fr)', 'gap': '16px', 'marginBottom': '20px'},
            children=[
                html.Div(style={**CARD_STYLE, 'borderLeft': '4px solid #38bdf8'}, children=[
                    html.Div("Total Revenue", style={'fontSize': '12px', 'color': '#94a3b8', 'textTransform': 'uppercase'}),
                    html.Div(id='kpi-revenue', style={'fontSize': '24px', 'fontWeight': '700', 'marginTop': '4px'})
                ]),
                html.Div(style={**CARD_STYLE, 'borderLeft': '4px solid #34d399'}, children=[
                    html.Div("Net Profit", style={'fontSize': '12px', 'color': '#94a3b8', 'textTransform': 'uppercase'}),
                    html.Div(id='kpi-profit', style={'fontSize': '24px', 'fontWeight': '700', 'marginTop': '4px'})
                ]),
                html.Div(style={**CARD_STYLE, 'borderLeft': '4px solid #f472b6'}, children=[
                    html.Div("Units Sold", style={'fontSize': '12px', 'color': '#94a3b8', 'textTransform': 'uppercase'}),
                    html.Div(id='kpi-units', style={'fontSize': '24px', 'fontWeight': '700', 'marginTop': '4px'})
                ]),
                html.Div(style={**CARD_STYLE, 'borderLeft': '4px solid #fbbf24'}, children=[
                    html.Div("Profit Margin", style={'fontSize': '12px', 'color': '#94a3b8', 'textTransform': 'uppercase'}),
                    html.Div(id='kpi-margin', style={'fontSize': '24px', 'fontWeight': '700', 'marginTop': '4px'})
                ]),
            ]
        ),

        html.Div(
            style={'display': 'grid', 'gridTemplateColumns': '1.3fr 1fr', 'gap': '16px', 'marginBottom': '20px'},
            children=[
                html.Div(style=CARD_STYLE, children=[
                    dcc.Graph(id='line-chart', config={'displayModeBar': False})
                ]),
                html.Div(style=CARD_STYLE, children=[
                    dcc.Graph(id='bar-chart', config={'displayModeBar': False})
                ]),
            ]
        ),

        html.Div(
            style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr 1.4fr', 'gap': '16px'},
            children=[
                html.Div(style=CARD_STYLE, children=[
                    dcc.Graph(id='donut-chart', config={'displayModeBar': False})
                ]),
                html.Div(style=CARD_STYLE, children=[
                    dcc.Graph(id='pie-chart', config={'displayModeBar': False})
                ]),
                html.Div(style=CARD_STYLE, children=[
                    dcc.Graph(id='scatter-plot', config={'displayModeBar': False})
                ]),
            ]
        )
    ]
)


@app.callback(
    [
        Output('kpi-revenue', 'children'),
        Output('kpi-profit', 'children'),
        Output('kpi-units', 'children'),
        Output('kpi-margin', 'children'),
        Output('line-chart', 'figure'),
        Output('bar-chart', 'figure'),
        Output('donut-chart', 'figure'),
        Output('pie-chart', 'figure'),
        Output('scatter-plot', 'figure')
    ],
    [
        Input('filter-region', 'value'),
        Input('filter-channel', 'value')
    ]
)
def update_dashboard(selected_region, selected_channel):

    filtered = df.copy()
    if selected_region != 'ALL':
        filtered = filtered[filtered['Region'] == selected_region]
    if selected_channel != 'ALL':
        filtered = filtered[filtered['Channel'] == selected_channel]

    filter_label = f"({selected_region} / {selected_channel})"

    # KPI Calculations
    total_rev = filtered['Revenue'].sum()
    total_profit = filtered['Profit'].sum()
    total_units = filtered['UnitsSold'].sum()
    margin = (total_profit / total_rev * 100) if total_rev > 0 else 0

    kpi_rev_str = f"${total_rev:,.0f}"
    kpi_profit_str = f"${total_profit:,.0f}"
    kpi_units_str = f"{total_units:,}"
    kpi_margin_str = f"{margin:.1f}%"

    theme_layout = dict(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': '#cbd5e1', 'family': 'Segoe UI, sans-serif'},
        margin={'t': 45, 'l': 30, 'r': 20, 'b': 30}
    )

    monthly = filtered.groupby(['Date', 'Month', 'Category'], as_index=False)['Revenue'].sum().sort_values('Date')
    line_fig = px.line(
        monthly,
        x='Month',
        y='Revenue',
        color='Category',
        markers=True,
        title=f"Monthly Trajectory {filter_label}",
        color_discrete_sequence=px.colors.qualitative.Safe
    )
    line_fig.update_layout(**theme_layout, legend=dict(orientation='h', y=-0.2, x=0.5, xanchor='center'))

    cat_revenue = filtered.groupby('Category', as_index=False)['Revenue'].sum().sort_values('Revenue', ascending=True)
    bar_fig = px.bar(
        cat_revenue,
        x='Revenue',
        y='Category',
        orientation='h',
        title=f"Revenue by Category {filter_label}",
        color='Category',
        text_auto='.2s',
        color_discrete_sequence=px.colors.qualitative.Prism
    )
    bar_fig.update_layout(**theme_layout, showlegend=False)

    
    segment_summary = filtered.groupby('CustomerSegment', as_index=False)['Revenue'].sum()
    donut_fig = px.pie(
        segment_summary,
        names='CustomerSegment',
        values='Revenue',
        hole=0.55,
        title=f"Customer Segment % {filter_label}",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    donut_fig.update_traces(textposition='inside', textinfo='percent+label')
    donut_fig.update_layout(**theme_layout, legend=dict(orientation='h', y=-0.15, x=0.5, xanchor='center'))

   
    cat_summary = filtered.groupby('Category', as_index=False)['Revenue'].sum()
    pie_fig = px.pie(
        cat_summary,
        names='Category',
        values='Revenue',
        title=f"Product Category % {filter_label}",
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    pie_fig.update_traces(textposition='inside', textinfo='percent+label')
    pie_fig.update_layout(**theme_layout, legend=dict(orientation='h', y=-0.15, x=0.5, xanchor='center'))

   
    scatter_fig = px.scatter(
        filtered,
        x='AdSpend',
        y='Revenue',
        size='Profit',
        color='Category',
        hover_data=['CustomerSegment'],
        title=f"Ad Spend vs Revenue {filter_label}",
        color_discrete_sequence=px.colors.qualitative.Safe
    )
    scatter_fig.update_layout(**theme_layout, legend=dict(orientation='h', y=-0.25, x=0.5, xanchor='center'))

    return (
        kpi_rev_str, kpi_profit_str, kpi_units_str, kpi_margin_str,
        line_fig, bar_fig, donut_fig, pie_fig, scatter_fig
    )

if __name__ == '__main__':
    app.run(debug=True)
