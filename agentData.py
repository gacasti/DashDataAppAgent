# pip install dash
# to run: python dashDemo3Data.py
# View on your browser at http://127.0.0.1:8050/
#
# TO RUN, open anaconda and open the terminal from the base:root environment
# Then change directory to where this progra is on the computer
# Maybe: "cd C:\Users\gilma_acc68ku\OneDrive\Documents\TechCareers\CPRG008_003\CPRG100-PythonData\code>"
# Then, run the command: python dashDemo3Data.py
# After, go to a browser and load the graph on port:8050 (localhost:8050)
#
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash_html_components import Br
from numpy import append
import plotly.express as px
import dash_table
import pandas as pd
from readDB import ReadMongoData as db
import plotly.graph_objects as pgo

# To run locally
# app = dash.Dash("app")
# app = dash_app.Dash("app")

# To run as service in Azure or similar
dash_app = dash.Dash(__name__)
app = dash_app.server

df = db.booking_sales_by_customer_by_agent
df1 = db.booking_sales_by_region_by_agent
df2 = db.booking_details_by_packages

df1["Agent Name"] = df1["AgtFirstName"].astype(
    str) + " " + df1["AgtLastName"].astype(str)

df2["Agent Name"] = df1["AgtFirstName"].astype(
    str) + " " + df1["AgtLastName"].astype(str)

# Convert the Decimal128 columns to float to work for the dash_table.DataTable
df[["BasePrice",
    "AgencyCommission"]] = df[["BasePrice",
                               "AgencyCommission"]].astype(str).astype(float)

df1[["BasePrice",
     "AgencyCommission"]] = df1[["BasePrice",
                                 "AgencyCommission"]].astype(str).astype(float)

df2[["BasePrice",
     "AgencyCommission"]] = df2[["BasePrice",
                                 "AgencyCommission"]].astype(str).astype(float)

# Create a sunburst graph to show total sales by supplier by region
fig1 = px.sunburst(df1, path=['Agent Name', 'RegionName'], values='BasePrice')

# Create a histogram to count of bookings by agent
fig2 = px.histogram(df1,
                    x="Agent Name",
                    y="BookingId",
                    histfunc="count",
                    title="Total Bookings Per Agent")
fig2.update_traces(xbins_size="M3")
fig2.update_xaxes(showgrid=True,
                  ticklabelmode="period",
                  dtick="M3",
                  tickformat="%b\n%Y")
fig2.update_layout(bargap=0.1)
# fig2.add_trace(
#     pgo.Scatter(mode="markers",
#                 x=df1["AgentName"],
#                 y=df["BookingId"],
#                 name="Quarterly"))
#
# Create a histogram to show most popular packages
fig5 = px.histogram(df2,
                    x="PkgName",
                    y="BookingId",
                    histfunc="count",
                    title="Total Bookings Per Package",
                    color_discrete_map={
                        0: 'red',
                        1: 'blue',
                        2: 'purple',
                        3: 'green'
                    })

fig7 = px.histogram(df2,
                    x="PkgName",
                    y="BasePrice",
                    nbins=10,
                    color="Agent Name",
                    title="Packages By Agent")

# fig2.update_traces(xbins_size="M3")
# fig2.update_xaxes(showgrid=True,
#                   ticklabelmode="period",
#                   dtick="M3",
#                   tickformat="%b\n%Y")
# fig2.update_layout(bargap=0.1)

# Summary for destinations
df_group_agent = df.groupby(["AgtEmail"]).count()[["BookingId"]]
fig = px.bar(df_group_agent, x=df_group_agent.index, y="BookingId")

# Selecting and renaming of columns for data frame table
new_column_names = [
    'Region', 'Supplier', 'Booking Description', 'Destination', 'Base Price'
]
df_column_names = [
    'RegionName', 'SupName', 'Description', 'Destination', 'BasePrice'
]

app.layout = html.Div(children=[
    html.A(href='/', children='Home'),
    html.H1(children='Travel Experts data'),
    html.Div(children=['Total Bookings by Agent']),
    html.Br(),
    # dash_table.DataTable(
    #     id='mytable',
    #     columns=[{
    #         'name': col,
    #         'id': df_column_names[idx]
    #     } for (idx, col) in enumerate(new_column_names)],
    #     data=df1.to_dict('records'),
    #     page_size=20
    dash_table.DataTable(id='mytable',
                         columns=[{
                             "name": i,
                             "id": i
                         } for i in df1.columns],
                         data=df1.to_dict('records'),
                         page_size=30),
    dcc.Graph(figure=fig1),
    dcc.Graph(figure=fig5),
    dcc.Graph(figure=fig7),
    dcc.Graph(figure=fig2)
])

if __name__ == '__main__':
    dash.app.run_server(debug=True)

# To run locally comment out the if statement above
# and then the following line should be: app.run_server(debug=True)
