import random
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

def generate_employee_data():
    departments = ['Engineering', 'HR', 'Marketing', 'Sales', 'Product']
    employee_ids = range(1, 51)
    data = []

    for emp_id in employee_ids:
        department = random.choice(departments)
        hours_worked = random.uniform(5, 9)
        productivity = random.uniform(60, 100)
        status = random.choice(['Active', 'Idle', 'On Break'])
        data.append({
            'Employee ID': emp_id,
            'Department': department,
            'Hours Worked': round(hours_worked, 2),
            'Productivity (%)': round(productivity, 2),
            'Status': status
        })

    return pd.DataFrame(data)

# Create Dash App
app = dash.Dash(__name__)

app.layout = html.Div(style={'backgroundColor': '#e6f0ff', 'padding': '20px', 'maxWidth': '1600px', 'margin': 'auto'}, children=[
    html.H1("Neuro Tech Enclave Pvt Ltd - Employee Data Dashboard", style={'textAlign': 'center'}),

    html.Div([
        dcc.Graph(id='bar-chart', style={'height': '400px'}),
        dcc.Graph(id='pie-chart', style={'height': '400px'}),
    ], style={'display': 'inline-block', 'width': '48%', 'verticalAlign': 'top'}),

    html.Div([
        dcc.Graph(id='line-chart', style={'height': '400px'}),
        dcc.Graph(id='scatter-chart', style={'height': '400px'}),
    ], style={'display': 'inline-block', 'width': '48%', 'verticalAlign': 'top'}),

    html.Div([
        dcc.Graph(id='histogram-chart', style={'height': '400px'}),
        dcc.Graph(id='box-chart', style={'height': '400px'}),
    ], style={'display': 'inline-block', 'width': '48%', 'verticalAlign': 'top'}),

    html.Div([
        dcc.Graph(id='area-chart', style={'height': '400px'}),
        dcc.Graph(id='bar-chart-department', style={'height': '400px'}),
    ], style={'display': 'inline-block', 'width': '48%', 'verticalAlign': 'top'}),

    html.Div([
        dcc.Graph(id='heatmap-chart', style={'height': '400px'}),
    ], style={'display': 'inline-block', 'width': '100%', 'verticalAlign': 'top'}),

    dcc.Interval(id='interval-component', interval=5*1000, n_intervals=0)
])

@app.callback(
    [Output('bar-chart', 'figure'),
     Output('pie-chart', 'figure'),
     Output('line-chart', 'figure'),
     Output('scatter-chart', 'figure'),
     Output('histogram-chart', 'figure'),
     Output('box-chart', 'figure'),
     Output('area-chart', 'figure'),
     Output('bar-chart-department', 'figure'),
     Output('heatmap-chart', 'figure')],
    [Input('interval-component', 'n_intervals')]
)
def update_graphs(n):

    df = generate_employee_data()

    # Bar Chart: Average Hours Worked by Department
    bar_fig = px.bar(df.groupby('Department')['Hours Worked'].mean().reset_index(),
                     x='Department', y='Hours Worked', title="Avg Hours Worked by Dept")

    # Pie Chart: Employee Status Distribution
    pie_fig = px.pie(df, names='Status', title="AI Driven Employee Status Distribution")

    # Line Chart: Productivity by Employee
    line_fig = px.line(df, x='Employee ID', y='Productivity (%)', title="Productivity per Employee")

    # Scatter Chart: Hours Worked vs Productivity
    scatter_fig = px.scatter(df, x='Hours Worked', y='Productivity (%)', color='Department',
                             title="Scatter: Hours Worked vs Productivity")

    # Histogram: Distribution of Hours Worked
    histogram_fig = px.histogram(df, x='Hours Worked', title="Histogram: Distribution of Hours Worked")

    # Box Plot: Hours Worked by Department
    box_fig = px.box(df, x='Department', y='Hours Worked', title="Box Plot: Hours Worked by Department")

    # Area Chart: Total Hours Worked over Employees
    area_fig = px.area(df.groupby('Employee ID')['Hours Worked'].sum().reset_index(),
                       x='Employee ID', y='Hours Worked', title="Area Chart: Total Hours Worked")

    # Bar Chart: Average Productivity by Department
    bar_fig_department = px.bar(df.groupby('Department')['Productivity (%)'].mean().reset_index(),
                                 x='Department', y='Productivity (%)', title="Avg Productivity by Dept")

    # Heatmap: Correlation between Hours Worked and Productivity
    heatmap_data = df[['Hours Worked', 'Productivity (%)']]
    heatmap_fig = px.density_heatmap(heatmap_data, x='Hours Worked', y='Productivity (%)',
                                      title="Heatmap: Hours Worked vs Productivity")

    return (bar_fig, pie_fig, line_fig, scatter_fig, histogram_fig,
            box_fig, area_fig, bar_fig_department, heatmap_fig)

if __name__ == '__main__':
    app.run_server(debug=True)
