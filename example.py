import dash
from dash import Output, Input
from dash.exceptions import PreventUpdate
import feffery_antd_components as fac

import dash_common_component_plugin

# 激活
dash_common_component_plugin.activate()

app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
)

app.layout = lambda: [
    fac.AntdButton('刷新地址栏', id='button-test-set_location'),
]


@app.callback(
    Input('button-test-set_location', 'nClicks'),
    prevent_initial_callbacks=True,
)
def update_location(n_clicks):
    dash_common_component_plugin.UtilLocation.set_location(
        pathname=f'/{n_clicks}',
        query={'a': n_clicks, 'b': n_clicks},
    )


if __name__ == '__main__':
    app.run(debug=True)
