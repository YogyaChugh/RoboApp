import asyncio
import base64
import json
import tempfile
import time

import cv2
import flet as ft
import flet_lottie as fl
import requests
from deep_translator import GoogleTranslator
from gtts import gTTS

URL = "https://api-yct9.onrender.com/upload"
FILE_PATH = "listened_audio.wav"
DONE = False
CONNECTED = False
LANGUAGES_DICT = {}


# Function to convert OpenCV image to base64
def cv2_to_base64(img):
    _, buffer = cv2.imencode(".jpg", img)
    return base64.b64encode(buffer).decode("utf-8")


def translation_page_column(page):
    returning_column = ft.Column()
    stackbro = ft.Stack()

    # Function to return all languages in form of drop-down
    def get_options():
        options = []
        with open("assets/languages.json") as f:
            LANGUAGES = json.load(f)["LANGUAGES"]
            for lang in LANGUAGES:
                options.append(
                    ft.DropdownOption(
                        key=LANGUAGES[lang].capitalize(),
                        content=ft.Text(value=LANGUAGES[lang].capitalize()),
                    )
                )
                LANGUAGES_DICT[LANGUAGES[lang]] = lang
        return options

    text_field_part_1 = ft.TextField(
        autocorrect=True,
        border_radius=10,
        capitalization=ft.TextCapitalization.SENTENCES,
        enable_suggestions=True,
        hint_text="Enter some text here ....",
        min_lines=4,
        multiline=True,
        bgcolor="#ffffff",
        border="none",
    )
    text_field_part_2 = ft.TextField(
        autocorrect=True,
        border_radius=10,
        capitalization=ft.TextCapitalization.SENTENCES,
        enable_suggestions=True,
        value="Translated Text will appear here ....",
        min_lines=4,
        multiline=True,
        bgcolor="#ffffff",
        border="none",
        read_only=True,
    )

    language_dropdown_1 = ft.Dropdown(
        editable=True,
        label="Language",
        options=get_options(),
        enable_filter=True,
        enable_search=True,
        menu_height=200,
        width=150,
        bgcolor="#ffffff",
    )
    language_dropdown_2 = ft.Dropdown(
        editable=True,
        label="Language",
        options=get_options(),
        enable_filter=True,
        enable_search=True,
        menu_height=200,
        width=150,
        bgcolor="#ffffff",
    )

    def close_it(e):
        page.close(dialog)

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Row(
            [
                ft.Icon(ft.Icons.INFO_OUTLINE, color=ft.Colors.BLUE_500),
                ft.Text("Information", weight=ft.FontWeight.BOLD),
            ]
        ),
        content=ft.Text(
            "Please enter some text for\ntranslation to specified language",
            text_align=ft.TextAlign.CENTER,
        ),
        actions=[ft.TextButton("OK", on_click=close_it)],
        actions_alignment=ft.MainAxisAlignment.CENTER,
        shape=ft.RoundedRectangleBorder(radius=15),
    )
    loading = fl.Lottie(
        src="https://lottie.host/e56fe72a"
        "-4567-4195-8fd9-0b2b7cf07fc5/PS40sQkMiL.json",
        reverse=False,
        animate=True,
    )
    loading = ft.Column(
        [loading],
        alignment=ft.MainAxisAlignment.END,
        # Vertical centering
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        # Horizontal centering
    )
    ph = ft.PermissionHandler()
    page.overlay.append(ph)
    page.update()
    lottie_listening = ft.Column(
        [
            fl.Lottie(
                "https://lottie.host/edf8944e-9765-"
                "45a3-b265-800be153dba4/QXUAumZWxI.json",
                fit=ft.ImageFit.COVER,
            )
        ],
        width=70,
        height=50,
    )

    async def stop_recording(e):
        text_field.content.controls[2].controls[0].controls.pop()
        text_field.content.controls[2].controls[0].controls.pop()
        text_field.content.controls[2].controls[0].controls.append(mic_start)
        page.update()
        try:
            await ft.audio_rec.stop_recording_async(10)
        except Exception as errr:
            print(errr)
        with open(FILE_PATH, "rb") as f:
            files = {"file": (FILE_PATH, f)}
            try:
                response = requests.post(URL, files=files)
            except Exception as err:
                response = {"error": str(err)}
                text_field_part_1.value = str(err)
            if "error" in response:
                print(response["error"])
                page.update()
                return
            text_field_part_1.value = str(response.json()["text"])
            page.update()

    async def start_recording(e):
        if not await ft.audio_rec.has_permission_async():
            ph.request_permission(ft.PermissionType.MICROPHONE)
        a = text_field.content.controls[2].controls[0]
        a.controls.pop()
        a.controls.append(mic_stop)
        a.controls.append(lottie_listening)
        page.update()
        try:
            await ft.audio_rec.start_recording_async("listened_audio.wav")
        except Exception:
            pass
        return

    mic_start = ft.IconButton(ft.Icons.MIC, on_click=start_recording)
    mic_stop = ft.IconButton(ft.Icons.MIC, on_click=stop_recording)

    def process_translate(e):
        if language_dropdown_2.value is None:
            dialog.content.value = (
                "Please specify the target language\nfor translation."
            )
            page.open(dialog)
            return
        elif text_field_part_1.value == "":
            dialog.content.value = "Text Field Empty"
            page.open(dialog)
            return
        stackbro.controls.append(loading)
        page.update()
        translated_text = ""
        if language_dropdown_1.value is None:
            lang = LANGUAGES_DICT[language_dropdown_2.value.lower()]
            translator = GoogleTranslator(source="auto", target=lang)
        else:
            translator = GoogleTranslator(
                source=LANGUAGES_DICT[language_dropdown_1.value.lower()],
                target=LANGUAGES_DICT[language_dropdown_2.value.lower()],
            )
        translated_text = translator.translate(text_field_part_1.value)
        stackbro.controls.remove(loading)
        text_field_part_2.value = translated_text
        page.update()

    # Row containing the main translator
    carder = ft.Row(
        [
            ft.Container(
                language_dropdown_1,
                bgcolor="#ffffff",
            ),
            ft.Icon(ft.Icons.SWAP_HORIZ_OUTLINED),
            ft.Container(
                language_dropdown_2,
                bgcolor="#ffffff",
            ),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    # Container for translation
    centered_layout = ft.Container(
        content=carder,
        alignment=ft.alignment.center,  # Centers the content inside
        expand=True,  # Ensures full-screen usage
    )

    def copy(e):
        page.set_clipboard(text_field_part_2.value)

    def speak(e):
        if text_field_part_2.value == "Translated Text will appear here ....":
            return

        text = text_field_part_2.value
        lang = LANGUAGES_DICT[language_dropdown_2.value.lower()]

        # Generate speech and save to a temporary file
        tts = gTTS(text, lang=lang)
        temp_audio_path = tempfile.NamedTemporaryFile(suffix=".mp3", delete=0)
        temp_audio_path = temp_audio_path.name
        tts.save(temp_audio_path)

        # Play audio using Flet
        page.add(ft.Audio(temp_audio_path, autoplay=True))
        page.update()

    text_field = ft.Container(
        ft.Column(
            [
                text_field_part_1,
                ft.Divider(height=20, thickness=2, color="grey"),
                ft.Row(
                    [
                        ft.ElevatedButton(
                            "Translate",
                            style=ft.ButtonStyle(
                                color="#ffffff",
                                bgcolor="#000055",
                                padding=ft.Padding(10, 10, 10, 10),
                            ),
                            on_click=process_translate,
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    # Ensures left & right positioning
                ),
            ]
        ),
        border_radius=5,
        padding=8,
        bgcolor="#ffffff",
    )
    vol = ft.Icons.VOLUME_UP_OUTLINED
    text_field_2 = ft.Container(
        ft.Column(
            [
                text_field_part_2,
                ft.Divider(height=20, thickness=2, color="grey"),
                ft.Row(
                    [
                        ft.Row(
                            [
                                ft.IconButton(ft.Icons.COPY, on_click=copy),
                                ft.IconButton(vol, on_click=speak),
                            ],
                            tight=True,
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    # Ensures left & right positioning
                ),
            ]
        ),
        border_radius=5,
        padding=8,
        bgcolor="#ffffff",
    )
    page.update()

    returning_column.controls.append(centered_layout)
    returning_column.controls.append(text_field)
    returning_column.controls.append(text_field_2)
    stackbro.controls.append(returning_column)
    return stackbro


def translation_page_appbar():
    translation_app_bar = ft.AppBar(
        leading=ft.Icon(ft.Icons.G_TRANSLATE_OUTLINED),
        leading_width=50,
        title=ft.Text("Translate"),
        center_title=False,
        bgcolor="#ffffff",
    )
    return translation_app_bar


def main(page: ft.Page):
    page.title = "RoboControl"
    page.scroll = "adaptive"
    page.on_scroll_interval = 10
    page.adaptive = True
    page.bgcolor = "#FFF0F0F0"
    page.window.width = 450
    page.window.height = 822

    # Main Top Bar
    home_appbar = ft.AppBar(
        leading=ft.Icon(ft.Icons.ROCKET_LAUNCH),
        leading_width=50,
        title=ft.Text("RoboControl"),
        center_title=False,
        bgcolor="#ffffff",
        actions=[
            ft.IconButton(ft.Icons.NOTIFICATIONS, adaptive=True),
            ft.IconButton(ft.Icons.PERSON_3, adaptive=True),
        ],
    )
    ic = ft.Icons.TRANSLATE_OUTLINED
    navbar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.HOME, label="Home"),
            ft.NavigationBarDestination(
                icon=ft.Icons.VIDEOGAME_ASSET_ROUNDED, label="Control"
            ),
            ft.NavigationBarDestination(icon=ft.Icons.MAP_SHARP, label="Maps"),
            ft.NavigationBarDestination(icon=ic, label="Translate"),
        ],
        adaptive=True,
        animation_duration=10,
        selected_index=0,
        bgcolor="#ffffff",
    )

    # Navigation Bar at bottom of Page
    page.navigation_bar = navbar

    # Funcion for changing the selected index at bottom of page
    def change_the_nav_url(e):
        page.navigation_bar.selected_index = int(e.control.data)
        changedbro()
        page.update()

    # Welcome Card For Home Page
    w = "#ffffff"
    b = "#000000"
    icc = ft.Icons.KEYBOARD_DOUBLE_ARROW_LEFT_OUTLINED
    home_card = ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text("Welcome to RoboControl", color=w, size=30),
                    ft.Text(
                        "Your personal robot companion management system",
                        color="#ffffff",
                    ),
                    ft.Row(
                        controls=[
                            ft.ElevatedButton(
                                "Quick Start",
                                icon=icc,
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=5)
                                ),
                                adaptive=True,
                            ),
                            ft.ElevatedButton(
                                "Guide",
                                bgcolor="#080e0a",
                                color="#ffffff",
                                icon=ft.Icons.BOOK,
                                icon_color="#ffffff",
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=5),
                                    side=ft.BorderSide(color=w, width=1),
                                ),
                                adaptive=True,
                            ),
                        ]
                    ),
                ]
            ),
            padding=20,
        ),
        color="#080e0a",
    )

    icong = ft.Icons.SETTINGS
    mapico = ft.Icons.MAP_OUTLINED
    # Container containing navigation for different pages #ON HOME PAGE
    home_part2 = ft.Container(
        margin=10,
        content=ft.Column(
            controls=[
                ft.Text("Quick Actions", size=20, weight=ft.FontWeight.BOLD),
                ft.GridView(
                    controls=[
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Icon(ft.Icons.WIFI, size=30, color=b),
                                    ft.Text("Connect Robot", size=20),
                                    ft.Text("Pair your device"),
                                ],
                            ),
                            border_radius=ft.BorderRadius(20, 20, 20, 20),
                            padding=15,
                            bgcolor="#ffffff",
                            on_click=change_the_nav_url,
                            data=1,
                        ),
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Icon(mapico, size=30, color=b),
                                    ft.Text("Start Mapping", size=20),
                                    ft.Text("Find routes"),
                                ],
                            ),
                            border_radius=ft.BorderRadius(20, 20, 20, 20),
                            padding=15,
                            bgcolor="#ffffff",
                            on_click=change_the_nav_url,
                            data=2,
                        ),
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Icon(
                                        ft.Icons.TRANSLATE_OUTLINED,
                                        size=30,
                                        color="#000000",
                                    ),
                                    ft.Text("Translate", size=20),
                                    ft.Text("Understand in your own language"),
                                ],
                            ),
                            border_radius=ft.BorderRadius(20, 20, 20, 20),
                            padding=15,
                            bgcolor="#ffffff",
                            on_click=change_the_nav_url,
                            data=3,
                        ),
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Icon(icong, size=30, color=b),
                                    ft.Text("Settings", size=20),
                                    ft.Text("Configure robot"),
                                ],
                            ),
                            border_radius=ft.BorderRadius(20, 20, 20, 20),
                            padding=15,
                            bgcolor="#ffffff",
                        ),
                    ],
                    expand=1,
                    runs_count=2,
                    spacing=10,
                    run_spacing=10,
                    max_extent=200,
                ),
            ]
        ),
    )
    connecting_button = ft.TextButton("Connect")
    # Dictionary containing all page_contents dude
    cb = connecting_button
    ha = home_appbar
    temp = asyncio.run(qr_code_scanner(page, navbar, ha, cb))

    def add_qr_code(e):
        page.controls.clear()
        page.navigation_bar = None
        page.appbar = temp[0]
        page.add(temp[1])
        page.padding = ft.Padding(50, 200, 50, 100)
        page.bgcolor = "#000000"
        page.update()
        asyncio.create_task(temp[2]())
        print("came here!")

    connecting_button.on_click = add_qr_code
    connecting_column_on_button = ft.Column(
        [connecting_button],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.MainAxisAlignment.CENTER,
    )
    page_contents = {
        0: ft.Column(controls=[home_card, home_part2]),
        1: connecting_column_on_button,
        3: translation_page_column(page),
    }

    # function to set changed page
    def changedbro(e=None):
        page.controls.clear()
        temp = page.navigation_bar.selected_index
        page.add(page_contents.get(temp, ft.Text("Coming Soon")))
        if page.navigation_bar.selected_index == 3:
            page.add(translation_page_appbar())
        page.appbar = home_appbar
        page.padding = 10
        page.bgcolor = "#FFF0F0F0"
        page.navigation_bar = navbar
        if (
            page.navigation_bar.selected_index != 0
            and page.navigation_bar.selected_index != 1
        ):
            page.appbar = None
        if page.navigation_bar.selected_index == 1:
            page.appbar = connected_robot()[0]
            page.padding = ft.Padding(150, 300, 50, 100)
        else:
            page.padding = 10
        page.update()

    page.navigation_bar.on_change = changedbro
    page.add(home_appbar, home_card, home_part2)  # default page - Home
    # asyncio.run(temp[2])
    page.update()


def connected_robot():
    w = ft.FontWeight.BOLD
    wh = "white"
    top_bar = ft.AppBar(
        title=ft.Text("RoboUnit-X1", color=wh, size=20, weight=w),
        bgcolor="#1e293b",
        actions=[ft.Icon(ft.Icons.WIFI)],
    )
    bf = ft.Icons.BATTERY_FULL
    wifi = ft.Icons.SIGNAL_WIFI_4_BAR
    c = "#22c55e"
    cc = "#3b82f6"
    ccc = "#facc15"
    status_card = ft.Card(
        content=ft.Container(
            content=ft.Row(
                controls=[
                    ft.Column(
                        [
                            ft.Icon(bf, color="green", size=30),
                            ft.Text("Battery", color="white", size=14),
                            ft.Text("None", color=c, size=16, weight=w),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Column(
                        [
                            ft.Icon(wifi, color="blue", size=30),
                            ft.Text("Signal", color="white", size=14),
                            ft.Text("None", color=cc, size=16, weight=w),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Column(
                        [
                            ft.Icon(ft.Icons.MEMORY, color="purple", size=30),
                            ft.Text("Memory", color="white", size=14),
                            ft.Text("None", color=ccc, size=16, weight=w),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
            ),
            padding=20,
            bgcolor="#1e293b",
            border_radius=12,
            shadow=ft.BoxShadow(blur_radius=10, color="#0f172a"),
        )
    )

    control_card = ft.Card(
        content=ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        [
                            ft.IconButton(
                                ft.Icons.ARROW_UPWARD,
                                icon_color="white",
                                bgcolor="#334155",
                                style=ft.ButtonStyle(icon_size=30),
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Row(
                        [
                            ft.IconButton(
                                ft.Icons.ARROW_BACK,
                                icon_color="white",
                                bgcolor="#334155",
                                style=ft.ButtonStyle(icon_size=30),
                            ),
                            ft.IconButton(
                                ft.Icons.STOP_CIRCLE,
                                icon_color="red",
                                icon_size=50,
                                bgcolor="#991b1b",
                                style=ft.ButtonStyle(icon_size=30),
                            ),
                            ft.IconButton(
                                ft.Icons.ARROW_FORWARD,
                                icon_color="white",
                                bgcolor="#334155",
                                style=ft.ButtonStyle(icon_size=30),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Row(
                        [
                            ft.IconButton(
                                ft.Icons.ARROW_DOWNWARD,
                                icon_color="white",
                                bgcolor="#334155",
                                style=ft.ButtonStyle(icon_size=30),
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=12,
            ),
            padding=25,
            bgcolor="#1e293b",
            border_radius=12,
            height=300,
            shadow=ft.BoxShadow(blur_radius=10, color="#0f172a"),
        )
    )

    return [top_bar, status_card, control_card]


async def qr_code_scanner(page, navbar, home_appbar, connecting_button):
    ro = ft.Rotate(angle=1.57)
    image_display = ft.Image(fit=ft.ImageFit.CONTAIN, rotate=ro)
    qr_result_text = ft.Text(value="Scan a QR code...", size=20)

    def camera_loop():
        cap = cv2.VideoCapture(0)
        detector = cv2.QRCodeDetector()

        while True:
            try:
                ret, frame = cap.read()
                if not ret:
                    continue

                # Resize for consistent display
                frame = cv2.resize(frame, (640, 480))

                # Detect and decode QR code
                data, bbox, _ = detector.detectAndDecode(frame)
                if data:
                    qr_result_text.value = f"QR Code: {data}"
                    print(f"QR CODE: {data}")
                    page.update()

                # Convert frame to base64 and update UI
                img_b64 = cv2_to_base64(frame)
                image_display.src_base64 = img_b64
                page.update()
            except Exception:
                pass

            # Slight delay for UI responsiveness
            time.sleep(0.03)

    def close_scanning(e):
        page.controls.clear()
        page.navigation_bar = navbar
        page.appbar = home_appbar
        navbar.selected_index = 1
        page.padding = 10
        page.bgcolor = "#FFF0F0F0"
        page.add(connecting_button)
        page.update()

    wh = "#ffffff"
    cl = ft.Icons.CLOSE
    access = ft.Icons.SETTINGS_ACCESSIBILITY_OUTLINED
    app_bar = ft.AppBar(
        leading=ft.IconButton(cl, icon_color=wh, on_click=close_scanning),
        leading_width=50,
        center_title=False,
        bgcolor="#000000",
        actions=[
            ft.IconButton(ft.Icons.INFO_OUTLINE, icon_color=wh),
            ft.IconButton(access, icon_color=wh),
        ],
    )

    qr_scanner = ft.Container(
        width=250,
        height=250,
        border_radius=10,
        border=ft.border.all(4, "limegreen"),
        bgcolor="black",
        content=image_display,
    )

    # Full-page layout with both vertical & horizontal centering
    centered_layout = ft.Column(
        controls=[
            ft.Row(
                controls=[qr_scanner],
                alignment=ft.MainAxisAlignment.CENTER,  # Horizontal centering
                expand=True,
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,  # Vertical centering
        expand=True,
    )
    return [app_bar, centered_layout, camera_loop]


ft.app(main)
