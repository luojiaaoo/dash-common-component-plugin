import dash
from dash import html

from dash_common_component_plugin import activate, OutputComponent, UtilLocation, UtilJs, UtilMessage, UtilNotification

# 激活
activate()

# Remember to set serve_locally=False
app = dash.Dash(__name__, serve_locally=False)

app.layout = html.Div("Test App", style={"padding": 50})

if __name__ == "__main__":
    app.run()