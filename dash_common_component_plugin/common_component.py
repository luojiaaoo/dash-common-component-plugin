from dash import hooks
from typing import Iterable
import feffery_antd_components as fac
import feffery_utils_components as fuc
from dash import dcc
from dash import set_props
from yarl import URL
from . import PACKAGE_NAME

_globel_get_location = fuc.FefferyLocation(id=f'{PACKAGE_NAME}/global-url-location')  # 全局url监听组件，仅仅起到监听的作用
_globel_set_location = dcc.Location(id=f'{PACKAGE_NAME}/global-dcc-url', refresh=False)  # 全局url控制组件
_globel_message_container = fac.Fragment(id=f'{PACKAGE_NAME}/global-message-container')  # 注入全局消息提示容器
_globel_notification_container = fac.Fragment(id=f'{PACKAGE_NAME}/global-notification-container')  # 注入全局通知信息容器
_globel_execute_javascript = fuc.FefferyExecuteJs(id=f'{PACKAGE_NAME}/global-execute-js-output')  # 注入全局js执行组件
_globel_reload = fuc.FefferyReload(id=f'{PACKAGE_NAME}/global-reload')  # 注入强制网页刷新组件


def inject_layout(favicon_filepath=None):
    @hooks.layout()
    def update_layout(layout):
        """inject common component to layout"""
        common_components = [
            *([fuc.FefferySetFavicon(favicon='/assets/logo.ico')] if favicon_filepath is not None else []),
            _globel_get_location,
            _globel_set_location,
            _globel_message_container,
            _globel_notification_container,
            _globel_execute_javascript,
            _globel_reload,
        ]
        if isinstance(layout, Iterable):
            layout = layout + common_components  # list type
        else:
            layout.children += common_components  # single component type
        return layout


def dash_common_component_plugin(favicon_filepath=None):
    # Inject common component to Dash app layout
    inject_layout(favicon_filepath=favicon_filepath)


def set_location(url):
    """Only supports refreshing the address bar within the site."""
    parsed_url = URL(url=url)
    set_props(_globel_set_location._id_str, {'pathname': parsed_url.path})
    set_props(_globel_set_location._id_str, {'search': f'?{t}' if (t := parsed_url.query_string) else ''})


def reload():
    """Reload the current page."""
    set_props(_globel_reload._id_str, {'reload': True})


def redirect(url):
    """Relocate to a new URL, with full page refresh."""
    set_props(_globel_execute_javascript._id_str, {'jsString': f"window.location.assign('{url}');"})


def run_js(js_string):
    """Run javascript code."""
    set_props(_globel_execute_javascript._id_str, {'jsString': js_string})
