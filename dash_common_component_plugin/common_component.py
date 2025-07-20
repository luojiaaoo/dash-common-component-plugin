from dash import hooks
from typing import Iterable, Dict, Optional, Literal
import feffery_antd_components as fac
import feffery_utils_components as fuc
from dash import dcc
from dash import Input, Output, State
from dash import set_props
from yarl import URL

PACKAGE_NAME = 'dash-common-component-plugin'

_globel_get_location = fuc.FefferyLocation(id=f'{PACKAGE_NAME}/global-get-location')  # 全局url监听组件，仅仅起到监听的作用
_globel_get_load_location = dcc.Store(id=f'{PACKAGE_NAME}/global-get-load-location')  # 用于临时保存刚加载页面的时候的href
_globel_set_location = dcc.Location(id=f'{PACKAGE_NAME}/global-set-url', refresh=False)  # 全局url控制组件
_globel_message_container = fac.Fragment(id=f'{PACKAGE_NAME}/global-message-container')  # 注入全局消息提示容器
_globel_notification_container = fac.Fragment(id=f'{PACKAGE_NAME}/global-notification-container')  # 注入全局通知信息容器
_globel_execute_javascript = fuc.FefferyExecuteJs(id=f'{PACKAGE_NAME}/global-execute-js-output')  # 注入全局js执行组件
_globel_reload = fuc.FefferyReload(id=f'{PACKAGE_NAME}/global-reload')  # 注入强制网页刷新组件


class OutputComponent:
    input_get_load_location = Input(_globel_get_load_location._id_str, 'data')  # 只保存刚加载页面的时候的href， 只在页面初始化的时候触发
    input_get_location = Input(_globel_get_location._id_str, 'href')  # 只要是页面的url产生变动就会触发


def activate(favicon_filepath: Optional[str] = None) -> None:
    """
    激活功能.

    Parameters:
        favicon_filepath 设置favicon文件路径。
    """

    @hooks.layout()
    def update_layout(layout):
        """注入layout"""
        common_components = [
            *([fuc.FefferySetFavicon(favicon='/assets/logo.ico')] if favicon_filepath is not None else []),
            _globel_get_location,
            _globel_set_location,
            _globel_message_container,
            _globel_notification_container,
            _globel_execute_javascript,
            _globel_reload,
        ]
        if isinstance(layout, list):
            layout = layout + common_components
        else:
            layout = [layout, *common_components]
        return layout

    # 注入浏览器回调
    # 在页面初始化的时候触发，把页面初始化的href保存到一个临时store中
    hooks.clientside_callback(
        """
            (href, trigger) => {
                return trigger === 'load' ? href : window.dash_clientside.no_update;
            }
        """,
        Output(_globel_get_load_location, 'data'),
        Input(_globel_get_location, 'href'),
        State(_globel_get_location, 'trigger'),
        prevent_initial_call=True,
    )


class UtilLocation:
    """地址工具集"""

    @staticmethod
    def set_location(pathname: str, query: Dict = None) -> None:
        """设置浏览器地址栏，不会刷新页面"""
        set_props(_globel_set_location._id_str, {'pathname': pathname})
        set_props(_globel_set_location._id_str, {'search': URL.build(query=query).__str__()})

    @staticmethod
    def reload() -> None:
        """重载当前页面"""
        set_props(_globel_reload._id_str, {'reload': True})

    @staticmethod
    def redirect(url: str) -> None:
        """重定向"""
        set_props(_globel_execute_javascript._id_str, {'jsString': f"window.location.assign('{url}');"})


class UtilJs:
    """JS工具集"""

    @staticmethod
    def run_js(js_string: str) -> None:
        """运行javascript代码"""
        set_props(_globel_execute_javascript._id_str, {'jsString': js_string})


class UtilMessage:
    """消息工具集"""

    maxCount = 3
    duration = 3

    @classmethod
    def show_message(
        cls,
        type: Literal['default', 'success', 'error', 'info', 'warning'],
        content: str,
    ) -> None:
        """显示消息"""
        message = fac.AntdMessage(
            type=type,
            content=content,
            duration=cls.duration,
            maxCount=cls.maxCount,
        )
        set_props(_globel_message_container._id_str, {'children': message})


class UtilNotification:
    """消息工具集"""

    duration = 4.5
    showProgress = True
    placement: Literal['top', 'bottom', 'topLeft', 'topRight', 'bottomLeft', 'bottomRight'] = 'topRight'

    @classmethod
    def show_notification(
        cls,
        type: Literal['default', 'success', 'error', 'info', 'warning'],
        content: str,
        description: str = None,
    ) -> None:
        """显示消息"""
        notification = fac.AntdNotification(
            type=type,
            message=content,
            description=description,
            placement=cls.placement,
            duration=cls.duration,
            showProgress=cls.showProgress,
        )
        set_props(_globel_notification_container._id_str, {'children': notification})
