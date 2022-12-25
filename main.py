import subprocess
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction


class SessionManager(Extension):
    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())


class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        options = [
            {
                "name": "Lock",
                "keyword": extension.preferences["kw_lock"],
                "icon": "lock.png",
                "cmd": "xdg-screensaver lock",
            },
            {
                "name": "Log Out",
                "keyword": extension.preferences["kw_logout"],
                "icon": "logout.png",
                "cmd": "gnome-session-quit --no-prompt",
            },
            {
                "name": "Suspend",
                "keyword": extension.preferences["kw_suspend"],
                "icon": "suspend.png",
                "cmd": "systemctl suspend",
            },
            {
                "name": "Restart",
                "keyword": extension.preferences["kw_restart"],
                "icon": "reboot.png",
                "cmd": "systemctl reboot",
            },
            {
                "name": "Power Off",
                "keyword": extension.preferences["kw_poweroff"],
                "icon": "poweroff.png",
                "cmd": "systemctl poweroff",
            },
        ]

        # Using the specific keywords
        keyword = event.get_keyword()
        preferences = list(extension.preferences.items())
        preferences.pop(0)
        for id, kw in preferences:
            if kw == keyword:
                subprocess.run(
                    next(option for option in options if option["keyword"] == kw)[
                        "cmd"
                    ],
                    shell=True,
                )
                return HideWindowAction()

        # Using the general keyword
        query = event.get_argument()
        if query:
            options = list(
                filter(lambda option: query.lower() in option["name"].lower(), options)
            )

        return RenderResultListAction(
            list(
                map(
                    lambda option: ExtensionResultItem(
                        icon=f"images/{option['icon']}",
                        name=option["name"],
                        description=f"Keyword: {option['keyword']}",
                        on_enter=ExtensionCustomAction(
                            option["cmd"],
                            keep_app_open=False,
                        ),
                    ),
                    options,
                )
            )
        )


class ItemEnterEventListener(EventListener):
    def on_event(self, event, extension):
        data = event.get_data()
        subprocess.run(data, shell=True)


if __name__ == "__main__":
    SessionManager().run()
