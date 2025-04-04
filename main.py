from flet import *
import flet_lottie as fl
import flet_audio as fa
import cv2
import base64
import threading
import time
import numpy as np
import json
import asyncio
from deep_translator import GoogleTranslator
from gtts import gTTS
import tempfile
import requests

URL = "https://api-yct9.onrender.com/upload"
FILE_PATH = "listened_audio.wav"
DONE = False
LANGUAGES_DICT={}

# Function to convert OpenCV image to base64
def cv2_to_base64(img):
    _, buffer = cv2.imencode('.jpg', img)
    return base64.b64encode(buffer).decode('utf-8')

def translation_page_column(page):
    returning_column = Column()
    stackbro = Stack()
    #Function to return all languages in form of drop-down
    def get_options():
        options = []
        with open('assets/languages.json') as f:
            LANGUAGES = json.load(f)['LANGUAGES']
            for lang in LANGUAGES:
                options.append(
                    DropdownOption(
                        key=LANGUAGES[lang].capitalize(),
                        content=Text(
                            value=LANGUAGES[lang].capitalize()
                        ),
                    )
                )
                global LANGUAGES_DICT
                LANGUAGES_DICT[LANGUAGES[lang]]=lang
        return options
    
    text_field_part_1=TextField(
                    autocorrect=True,
                    border_radius=10,
                    capitalization=TextCapitalization.SENTENCES,
                    enable_suggestions=True,
                    hint_text="Enter some text here ....",
                    min_lines=4,
                    multiline=True,
                    bgcolor="#ffffff",
                    border="none"
                )
    text_field_part_2 = TextField(
                    autocorrect=True,
                    border_radius=10,
                    capitalization=TextCapitalization.SENTENCES,
                    enable_suggestions=True,
                    value="Translated Text will appear here ....",
                    min_lines=4,
                    multiline=True,
                    bgcolor="#ffffff",
                    border="none",
                    read_only=True
                )
    
    language_dropdown_1 = Dropdown(
                        editable=True,
                        label="Language",
                        options=get_options(),
                        enable_filter=True,
                        enable_search=True,
                        menu_height=200,
                        width=150,
                        bgcolor="#ffffff"
                    )
    language_dropdown_2 = Dropdown(
                        editable=True,
                        label="Language",
                        options=get_options(),
                        enable_filter=True,
                        enable_search=True,
                        menu_height=200,
                        width=150,
                        bgcolor="#ffffff"
                    )
    
    def close_it(e):
        page.close(dialog)
    dialog = AlertDialog(
            modal=True,
            title=Row(
                [
                    Icon(Icons.INFO_OUTLINE, color=Colors.BLUE_500),
                    Text("Information", weight=FontWeight.BOLD)
                ]
            ),
            content=Text(
                "Please enter some text for\ntranslation to the specified language",
                text_align=TextAlign.CENTER,
            ),
            actions=[
                TextButton("OK",on_click=close_it)
            ],
            actions_alignment=MainAxisAlignment.CENTER,
            shape=RoundedRectangleBorder(radius=15),
        )
    loading = fl.Lottie(
        src="https://lottie.host/e56fe72a-4567-4195-8fd9-0b2b7cf07fc5/PS40sQkMiL.json",
        reverse=False,
        animate=True,
    )
    loading = Column(
        [loading],
        alignment=MainAxisAlignment.END,  # Vertical centering
        horizontal_alignment=CrossAxisAlignment.CENTER  # Horizontal centering
    )
    ph = PermissionHandler()
    page.overlay.append(ph)
    page.update()
    lottie_listening = Column([fl.Lottie("https://lottie.host/edf8944e-9765-45a3-b265-800be153dba4/QXUAumZWxI.json",fit=ImageFit.COVER)],width=70,height=50)

    async def stop_recording(e):
        text_field.content.controls[2].controls[0].controls.pop()
        text_field.content.controls[2].controls[0].controls.pop()
        text_field.content.controls[2].controls[0].controls.append(mic_start)
        page.update()
        try:
            await audio_rec.stop_recording_async(10)
        except Exception as e:
            print(e)
        with open(FILE_PATH, "rb") as f:
            files = {"file": (FILE_PATH, f)}
            try:
                response = requests.post(URL, files=files)
            except Exception as e:
                print(e)
                response = {'error':str(e)}
                text_field_part_1.value = str(e)
            if 'error' in response:
                print(response['error'])
                page.update()
                return
            text_field_part_1.value = str(response.json()['text'])
            page.update()
    async def start_recording(e):
        if not await audio_rec.has_permission_async():
            ph.request_permission(PermissionType.MICROPHONE)
        text_field.content.controls[2].controls[0].controls.pop()
        text_field.content.controls[2].controls[0].controls.append(mic_stop)
        text_field.content.controls[2].controls[0].controls.append(lottie_listening)
        page.update()
        try:
            await audio_rec.start_recording_async("listened_audio.wav")
        except Exception as e:
            print(e)
        return
    mic_start = IconButton(Icons.MIC,on_click=start_recording)
    mic_stop = IconButton(Icons.MIC,on_click=stop_recording)
    def process_translate(e):
        global LANGUAGES_DICT
        if language_dropdown_2.value==None:
            dialog.content.value="Please specify the target language\nfor translation."
            page.open(dialog)
            return
        elif text_field_part_1.value=="":
            dialog.content.value="Please enter some text for\ntranslation to the specified language"
            page.open(
                dialog
            )
            return
        temp = ""
        stackbro.controls.append(loading)
        page.update()
        translated_text = ""
        if language_dropdown_1.value==None:
            translator = GoogleTranslator(source="auto", target=LANGUAGES_DICT[language_dropdown_2.value.lower()])
        else:
            translator = GoogleTranslator(source=LANGUAGES_DICT[language_dropdown_1.value.lower()], target=LANGUAGES_DICT[language_dropdown_2.value.lower()])
        translated_text = translator.translate(text_field_part_1.value)
        stackbro.controls.remove(loading)
        text_field_part_2.value = translated_text
        page.update()

    #Row containing the main translator
    carder = Row(
            [
                Container(
                    language_dropdown_1,
                    bgcolor="#ffffff",
                ),
                Icon(Icons.SWAP_HORIZ_OUTLINED),
                Container(
                    language_dropdown_2,
                    bgcolor="#ffffff",
                )
            ],
            alignment=MainAxisAlignment.SPACE_BETWEEN
        )
    
    #Container for translation
    centered_layout = Container(
        content=carder,
        alignment=alignment.center,  # Centers the content inside
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
        temp_audio_path = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False).name
        tts.save(temp_audio_path)

        # Play audio using Flet
        page.add(Audio(temp_audio_path,autoplay=True))
        page.update()

    text_field = Container(
        Column(
            [
                text_field_part_1,
                Divider(height=20, thickness=2, color="grey"),
                Row(
                    [
                        Row(
                            [mic_start],
                            tight=True
                        ),
                        ElevatedButton("Translate",style=ButtonStyle(color="#ffffff",bgcolor="#000055",padding=Padding(10,10,10,10)),on_click=process_translate)
                    ],
                    alignment=MainAxisAlignment.SPACE_BETWEEN  # Ensures left & right positioning
                )
            ]
        ),
        border_radius=5,
        padding=8,
        bgcolor="#ffffff"
    )
    text_field_2 = Container(
        Column(
            [
                text_field_part_2,
                Divider(height=20, thickness=2, color="grey"),
                Row(
                    [
                        Row(
                            [IconButton(Icons.COPY,on_click=copy), IconButton(Icons.VOLUME_UP_OUTLINED,on_click=speak)],
                            tight=True
                        )
                    ],
                    alignment=MainAxisAlignment.SPACE_BETWEEN  # Ensures left & right positioning
                )
            ]
        ),
        border_radius=5,
        padding=8,
        bgcolor="#ffffff"
    )

    audio_rec = AudioRecorder(
        audio_encoder=AudioEncoder.WAV
    )
    page.overlay.append(audio_rec)
    page.update()

    returning_column.controls.append(centered_layout)
    returning_column.controls.append(text_field)
    returning_column.controls.append(text_field_2)
    stackbro.controls.append(returning_column)
    return stackbro

def translation_page_appbar():
    translation_app_bar = AppBar(
        leading=Icon(Icons.G_TRANSLATE_OUTLINED),
        leading_width=50,
        title= Text("Translate"),
        center_title=False,
        bgcolor="#ffffff"
    )
    return translation_app_bar

def main(page: Page):
    page.title="RoboControl"
    page.scroll = "adaptive"
    page.on_scroll_interval = 10
    page.adaptive = True
    page.bgcolor = "#FFF0F0F0"

    #Main Top Bar
    home_appbar = AppBar(
        leading=Icon(Icons.ROCKET_LAUNCH),
        leading_width=50,
        title= Text("RoboControl"),
        center_title=False,
        bgcolor="#ffffff",
        actions=[
            IconButton(Icons.NOTIFICATIONS,adaptive=True),
            IconButton(Icons.PERSON_3,adaptive=True)
        ]
    )
    navbar=NavigationBar(
        destinations=[
            NavigationBarDestination(icon=Icons.HOME,label="Home"),
            NavigationBarDestination(icon=Icons.VIDEOGAME_ASSET_ROUNDED,label="Control"),
            NavigationBarDestination(icon=Icons.MAP_SHARP,label="Maps"),
            NavigationBarDestination(icon=Icons.TRANSLATE_OUTLINED,label="Translate")
        ],
        adaptive=True,
        animation_duration=10,
        selected_index=0,
        bgcolor="#ffffff"
    )

    #Navigation Bar at bottom of Page
    page.navigation_bar = navbar

    #Funcion for changing the selected index at bottom of page
    def change_the_nav_url(e):
        page.navigation_bar.selected_index=int(e.control.data)
        changedbro()
        page.update()

    #Welcome Card For Home Page
    home_card = Card(
        content= Container(
            content= Column(
                [ Text("Welcome to RoboControl",color="#ffffff",size=30),
                 Text("Your personal robot companion management system",color="#ffffff"),
                 Row(controls=[ElevatedButton("Quick Start",icon=Icons.KEYBOARD_DOUBLE_ARROW_LEFT_OUTLINED,style=ButtonStyle(shape=RoundedRectangleBorder(radius=5)),adaptive=True)
                               ,ElevatedButton("Guide",bgcolor="#080e0a" ,color="#ffffff",icon=Icons.BOOK,icon_color="#ffffff",style=ButtonStyle(shape=RoundedRectangleBorder(radius=5),side=BorderSide(color="#ffffff",width=1),),adaptive=True)])
                ]
            ),
            padding=20
        ),
        color="#080e0a"
    )

    #Container containing navigation for different pages #ON HOME PAGE
    home_part2 = Container(
        margin=10,
        content = Column(
            controls=[
                Text("Quick Actions",size=20,weight=FontWeight.BOLD),
                GridView(
                    controls=[
                        Container(
                            content=Column(
                                controls=[
                                    Icon(Icons.WIFI,size=30,color="#000000"),
                                    Text("Connect Robot",size=20),
                                    Text("Pair your device")
                                ],
                            ),
                            border_radius = BorderRadius(20,20,20,20),
                            padding=15,
                            bgcolor="#ffffff",
                            on_click=change_the_nav_url,
                            data = 1
                        ),
                        Container(
                            content=Column(
                                controls=[
                                    Icon(Icons.MAP_OUTLINED,size=30,color="#000000"),
                                    Text("Start Mapping",size=20),
                                    Text("Find routes")
                                ],
                            ),
                            border_radius = BorderRadius(20,20,20,20),
                            padding=15,
                            bgcolor="#ffffff",
                            on_click=change_the_nav_url,
                            data = 2
                        ),
                        Container(
                            content=Column(
                                controls=[
                                    Icon(Icons.TRANSLATE_OUTLINED,size=30,color="#000000"),
                                    Text("Translate",size=20),
                                    Text("Understand in your own language")
                                ],
                            ),
                            border_radius = BorderRadius(20,20,20,20),
                            padding=15,
                            bgcolor="#ffffff",
                            on_click=change_the_nav_url,
                            data = 3
                        ),
                        Container(
                            content=Column(
                                controls=[
                                    Icon(Icons.SETTINGS,size=30,color="#000000"),
                                    Text("Settings",size=20),
                                    Text("Configure robot")
                                ],
                            ),
                            border_radius = BorderRadius(20,20,20,20),
                            padding=15,
                            bgcolor="#ffffff"
                        )
                    ],
                    expand=1,
                    runs_count=2,
                    spacing=10,
                    run_spacing=10,
                    max_extent=200
                )
            ]
        )
    )

    #Dictionary containing all page_contents dude
    temp = asyncio.run(qr_code_scanner(page,navbar,home_appbar,home_card,home_part2))
    page_contents = {
        0: Column(controls=[home_card,home_part2]),
        1: temp[1],
        3: translation_page_column(page)
    }

    #function to set changed page
    def changedbro(e=None):
        page.controls.clear()
        page.add(page_contents.get(page.navigation_bar.selected_index,Text("Coming Soon")))
        if page.navigation_bar.selected_index==3:
            page.add(translation_page_appbar())
        if page.navigation_bar.selected_index==1:
            page.appbar= temp[0]
            page.padding=Padding(50,200,50,100)
            page.bgcolor= "#000000"
        else:
            page.appbar = home_appbar
            page.padding = 10
            page.bgcolor = "#FFF0F0F0"
            page.navigation_bar = navbar
        if page.navigation_bar.selected_index!=0 and page.navigation_bar.selected_index!=1:
            page.appbar = None
        if page.navigation_bar.selected_index==1:
            page.navigation_bar = None
        page.update()

    page.navigation_bar.on_change = changedbro
    page.add(home_appbar,home_card,home_part2) #default page - Home
    #asyncio.run(temp[2])
    asyncio.create_task(temp[2]())
    page.update()


async def qr_code_scanner(page,navbar,home_appbar,home_card,home_part2):

    image_display = Image(fit=ImageFit.CONTAIN)
    qr_result_text = Text(value="Scan a QR code...", size=20)

    def camera_loop():
        cap = cv2.VideoCapture(0)
        detector = cv2.QRCodeDetector()

        while True:
            ret, frame = cap.read()
            if not ret:
                continue

            # Resize for consistent display
            frame = cv2.resize(frame, (640, 480))

            # Detect and decode QR code
            data, bbox, _ = detector.detectAndDecode(frame)
            if data:
                qr_result_text.value = f"QR Code: {data}"
                page.update()

            # Convert frame to base64 and update UI
            img_b64 = cv2_to_base64(frame)
            image_display.src_base64 = img_b64
            page.update()

            # Slight delay for UI responsiveness
            time.sleep(0.03)

    def close_scanning(e):
        page.controls.clear()
        page.navigation_bar = navbar
        page.appbar = home_appbar
        navbar.selected_index = 0
        page.padding = 10
        page.bgcolor = "#FFF0F0F0"
        page.add(home_card,home_part2)
        page.update()
    app_bar = AppBar(
        leading=IconButton(icons.CLOSE, icon_color="#ffffff",on_click=close_scanning),
        leading_width=50,
        center_title=False,
        bgcolor="#000000",
        actions=[
            IconButton(icons.INFO_OUTLINE, icon_color="#ffffff"),
            IconButton(icons.SETTINGS_ACCESSIBILITY_OUTLINED, icon_color="#ffffff")
        ]
    )

    qr_scanner = Container(
        width=250,
        height=250,
        border_radius=10,
        border=border.all(4, "limegreen"),
        bgcolor="black",
        content=image_display
    )

    # Full-page layout with both vertical & horizontal centering
    centered_layout = Column(
        controls=[
            Row(
                controls=[qr_scanner],
                alignment=MainAxisAlignment.CENTER,  # Horizontal centering
                expand=True
            ),
        ],
        alignment=MainAxisAlignment.CENTER,  # Vertical centering
        expand=True
    )
    return [app_bar, centered_layout,camera_loop]
app(main)