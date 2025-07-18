from dash import hooks, html
from typing import Iterable
import feffery_antd_components as fac
import feffery_utils_components as fuc
from dash import dcc
from . import PACKAGE_NAME


def inject_common_components(favicon_filepath: str = None):
    @hooks.layout()
    def update_layout(layout):
        """inject common component to layout"""
        common_components = [
            *(
                [fuc.FefferySetFavicon(favicon="/assets/logo.ico")]
                if favicon_filepath is not None
                else []
            ),
            # 全局url监听组件，仅仅起到监听的作用
            fuc.FefferyLocation(id=f"{PACKAGE_NAME}/global-url-location"),
            # 全局url控制组件
            dcc.Location(id=f"{PACKAGE_NAME}/global-dcc-url", refresh=False),
            # 注入全局消息提示容器
            fac.Fragment(id=f"{PACKAGE_NAME}/global-message-container"),
            # 注入全局通知信息容器
            fac.Fragment(id=f"{PACKAGE_NAME}/global-notification-container"),
            # 注入js执行
            fuc.FefferyExecuteJs(id=f"{PACKAGE_NAME}/global-execute-js-output"),
            # 注入强制网页刷新组件
            fuc.FefferyReload(id=f"{PACKAGE_NAME}/global-reload"),
            # URL初始化中继组件，触发root_router回调执行
            dcc.Store(id=f"{PACKAGE_NAME}/global-url-init-load"),
        ]
        if isinstance(layout, Iterable):
            layout = layout + common_components  # list type
        else:
            layout.children += common_components  # single component type
        return layout
