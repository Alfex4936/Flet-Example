import webbrowser
from typing import Optional

import flet
from flet import (
    Card,
    CircleAvatar,
    Column,
    Container,
    FloatingActionButton,
    Icon,
    Image,
    KeyboardEvent,
    ListTile,
    ListView,
    NavigationRail,
    NavigationRailDestination,
    Page,
    PopupMenuButton,
    PopupMenuItem,
    ProgressRing,
    Row,
    SnackBar,
    Text,
    TextButton,
    TextField,
    VerticalDivider,
    alignment,
    control_event,
    icons,
    padding,
)

from utils.parser import Ajou, Error, Notice, NoticeFilter


def main(page: Page) -> None:
    tb4 = TextField()

    def on_keyboard(e: KeyboardEvent):
        if e.ctrl and e.key == "F":
            tb4 = TextField(
                label="무슨 공지를 보고 싶으신가요?",
                hint_text="검색할 것",
                autofocus=True,
                on_submit=lambda s: build_notice_page(NoticeFilter(keyword=tb4.value)),  # type: ignore
            )
            if len(row.controls) > 1:
                row.controls.pop()

            row.controls.append(tb4)
            page.update()

        print(
            f"Key: {e.key}, Shift: {e.shift}, Control: {e.ctrl}, Alt: {e.alt}, Meta: {e.meta}"
        )

    def build_notice_page(filter: Optional[NoticeFilter] = None):
        while len(row.controls) > 1:
            row.controls.pop()

        snack_bar_text = "공지 불러오는 중..."
        if filter and filter.keyword:
            snack_bar_text = f'"{filter.keyword}" 검색하는 중...'

        page.snack_bar = SnackBar(
            Text(snack_bar_text),
            bgcolor="#0066b3",
        )
        page.snack_bar.open = True
        page.update()
        print("Parsing...")

        # page.add(row)

        ajou = Ajou()
        data = ajou.parser(filter=filter)
        lv = ListView(expand=1, spacing=20, padding=20, auto_scroll=False)

        if data is Error:
            lv.controls = [Text(f"Error: {Error.name}")]
            row.controls.append(lv)
            page.update()
            return

        for notice in data:  # type: ignore
            match notice.category:
                case "학사":
                    notice_icon = icons.SCHOOL_ROUNDED
                case "비교과":
                    notice_icon = icons.INFO_ROUNDED
                case "장학":
                    notice_icon = icons.INFO_ROUNDED
                case "학술":
                    notice_icon = icons.NEWSPAPER_ROUNDED
                case "입학":
                    notice_icon = icons.TRANSIT_ENTEREXIT_ROUNDED
                case "취업":
                    notice_icon = icons.WORK_ROUNDED
                case "사무":
                    notice_icon = icons.BUSINESS_CENTER_ROUNDED
                case "기타":
                    notice_icon = icons.ANNOUNCEMENT_ROUNDED
                case "행사":
                    notice_icon = icons.FESTIVAL
                case "파란학기제":
                    notice_icon = icons.CLASS_ROUNDED
                case "학사일정":
                    notice_icon = icons.CLASS_ROUNDED
                case _:
                    notice_icon = icons.MORE_VERT

            item = Card(
                content=Container(
                    width=500,
                    content=Column(
                        [
                            ListTile(
                                leading=Icon(notice_icon),
                                title=Text(notice.title),
                                subtitle=Text(
                                    f"{notice.category} | {notice.date} | {notice.writer}"
                                ),
                                data=notice.link,
                                on_click=lambda e: webbrowser.open(e.data, new=2),
                                trailing=PopupMenuButton(
                                    icon=icons.MORE_VERT_ROUNDED,
                                    tooltip="더보기",
                                    items=[
                                        PopupMenuItem(text="공유하기"),
                                    ],
                                ),
                            ),
                        ],
                        spacing=0,
                    ),
                    padding=padding.symmetric(vertical=10),
                )
            )

            lv.controls.append(item)

        # lv.controls = [
        #     Text(
        #         f"{i + 1}. {n.title} ({n.date})", size=18, selectable=True, data=n.link
        #     )
        #     for i, n in enumerate(data)  # type: ignore
        # ]

        row.controls.append(lv)

        page.snack_bar.open = False
        page.update()

    def build_timetable():
        row.controls.append(ProgressRing())
        page.update()

        lv = ListView(expand=1, spacing=20, padding=20, auto_scroll=False)

        item = Card(
            content=Container(
                width=500,
                content=Column(
                    [
                        ListTile(
                            title=Text("One-line list tile"),
                        ),
                        ListTile(title=Text("One-line dense list tile"), dense=True),
                        ListTile(
                            leading=Icon(icons.SETTINGS),
                            title=Text("One-line selected list tile"),
                            selected=True,
                        ),
                        ListTile(
                            leading=Image(src="/icons/icon-192.png", fit="contain"),
                            title=Text("One-line with leading control"),
                        ),
                        ListTile(
                            title=Text("One-line with trailing control"),
                            trailing=PopupMenuButton(
                                icon=icons.MORE_VERT,
                                items=[
                                    PopupMenuItem(text="Item 1"),
                                    PopupMenuItem(text="Item 2"),
                                ],
                            ),
                        ),
                        ListTile(
                            leading=Icon(icons.ALBUM),
                            title=Text("One-line with leading and trailing controls"),
                            trailing=PopupMenuButton(
                                icon=icons.MORE_VERT,
                                items=[
                                    PopupMenuItem(text="Item 1"),
                                    PopupMenuItem(text="Item 2"),
                                ],
                            ),
                        ),
                        ListTile(
                            leading=Icon(icons.SNOOZE),
                            title=Text("Two-line with leading and trailing controls"),
                            subtitle=Text("Here is a second title."),
                            trailing=PopupMenuButton(
                                icon=icons.MORE_VERT,
                                items=[
                                    PopupMenuItem(text="Item 1"),
                                    PopupMenuItem(text="Item 2"),
                                ],
                            ),
                        ),
                    ],
                    spacing=0,
                ),
                padding=padding.symmetric(vertical=10),
            )
        )

        lv.controls.append(item)
        row.controls.pop()
        row.controls.append(lv)
        page.update()

    page.title = "아주대학교"
    page.vertical_alignment = "center"
    page.on_keyboard_event = on_keyboard

    def change_menu(index: int):
        while len(row.controls) > 1:
            row.controls.pop()

        match index:
            case 0:
                build_notice_page()
            case 1:
                build_timetable()

        print("come here")

    page.on_keyboard_event = on_keyboard

    a1 = CircleAvatar(
        foreground_image_url="https://user-images.githubusercontent.com/2356749/187013722-c2b6dcf4-f3d5-4701-995c-bdb7907946c2.png",
        # content=Text("FF"),
    )

    rail = NavigationRail(
        selected_index=0,
        label_type="all",
        extended=False,
        min_width=100,
        min_extended_width=400,
        leading=a1,
        group_alignment=-0.9,
        destinations=[
            NavigationRailDestination(
                icon_content=Icon(icons.CHECKLIST_OUTLINED),
                selected_icon_content=Icon(icons.CHECKLIST_ROUNDED),
                label="공지",
            ),
            NavigationRailDestination(
                icon_content=Icon(icons.BOOKMARK_BORDER),
                selected_icon_content=Icon(icons.BOOKMARK),
                label="학사 일정",
            ),
            NavigationRailDestination(
                icon=icons.SETTINGS_OUTLINED,
                selected_icon_content=Icon(icons.SETTINGS),
                label_content=Text("설정"),
            ),
        ],
        on_change=lambda e: change_menu(e.control.selected_index),
    )

    row = Row(
        [
            rail,
            # VerticalDivider(width=1),
            # Column([Text("Body!")], alignment="center", expand=True),
        ],
        expand=True,
        # alignment="center",
        vertical_alignment="center",
    )

    page.add(row)

    change_menu(0)


if __name__ == "__main__":
    flet.app(target=main)
    # ajou = Ajou()
    # # print(ajou.parser())

    # filter = NoticeFilter(nums=50)
    # # filter.set_category("학사")
    # # filter.set_keyword("졸업")
    # ajou.parser(filter=filter)
