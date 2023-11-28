from dash import Dash, html, dcc
import pandas as pd
import plotly.graph_objects as go

def load_rainfall_data_1990_2005():
    """Loads rainfall data for 1990-2005."""
    return pd.read_csv("static/data/1990-2005_AverageRainfall_Makaroa.csv")

def load_rainfall_data_2022():
    """Loads rainfall data for 2022."""
    return pd.read_csv("static/data/MonthlyRainfall_Makaroa_2022.csv")

def prepare_rainfall_chart_data(data_df_1990_2005, data_df_2022):
    """Prepares data for the rainfall bar chart."""
    rainfall_data_1990_2005 = data_df_1990_2005.iloc[0, 3:]
    rainfall_data_2022 = data_df_2022.iloc[0, 2:]
    
    months = rainfall_data_1990_2005.index.tolist()
    values_1990_2005 = rainfall_data_1990_2005.values.tolist()
    values_2022 = rainfall_data_2022.values.tolist()

    return months, values_1990_2005, values_2022

def create_rainfall_bar_chart(months, values_1990_2005, values_2022):
    """Creates a bar chart for rainfall data with comparative years."""
    fig = go.Figure()
    
    # Adding 1990-2005 average data as blue bars
    fig.add_trace(go.Bar(
        x=months, 
        y=values_1990_2005, 
        name='1990-2005 average rainfall',
        marker_color='#364fc7'  # Blue color
    ))

    # Adding 2022 data as grey bars
    fig.add_trace(go.Bar(
        x=months, 
        y=values_2022, 
        name='Monthly rainfall',
        marker_color='#ced4da'  # Grey color
    ))

    # Updating the layout of the chart
    fig.update_layout(
        title={
            'text': 'Makarora - 2022',
            'x': 0.5,  # Centering the title
            'xanchor': 'center'
        },
        xaxis=dict(
            tickfont_size=14,
            showgrid=False  # Hiding vertical grid lines
        ),
        yaxis=dict(
            title='Rainfall (mm)',
            titlefont_size=16,
            tickfont_size=14,
            dtick=50,  # Displaying a tick every 50mm
            gridcolor='#dee2e6'  # Showing horizontal grid lines in grey
        ),
        legend=dict(
            x=0.5,  # Centering the legend horizontally
            y=-0.1,
            xanchor='center',
            orientation='h',  # Setting legend orientation to horizontal
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='group',
        bargap=0.15,  # Space between bars of different groups
        bargroupgap=0,  # No space between bars of the same group
        plot_bgcolor='rgba(0,0,0,0)'  # Transparent background
    )

    # Adjusting bar width
    fig.update_traces(width=0.4)  # bar width

    return fig



def create_app():
    """Creates and configures the Dash app."""
    app = Dash(__name__)

    # Load data
    data_df_1990_2005 = load_rainfall_data_1990_2005()
    data_df_2022 = load_rainfall_data_2022()

    # Prepare data
    months, values_1990_2005, values_2022 = prepare_rainfall_chart_data(data_df_1990_2005, data_df_2022)

    # Create bar chart
    fig_bar_chart = create_rainfall_bar_chart(months, values_1990_2005, values_2022)

    # Setup layout
    app.layout = html.Div(children=[
        html.Div([
            dcc.Graph(id='rainfall-bar-chart', figure=fig_bar_chart)
        ])
    ])

    return app



if __name__ == '__main__':
    app = create_app()
    app.run_server(debug=True, host='0.0.0.0', port=8050)

