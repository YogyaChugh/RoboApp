from flet import *
import math
import folium
import json
import googletrans
import time
from gtts import gTTS
import soundfile as sf
import sounddevice as sd
import numpy as np
import tempfile
DONE = False
LANGUAGES_DICT={}

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
    loading = Lottie(
        src="https://lottie.host/e56fe72a-4567-4195-8fd9-0b2b7cf07fc5/PS40sQkMiL.json",
        reverse=False,
        animate=True,
    )
    loading = Column(
        [loading],
        alignment=MainAxisAlignment.END,  # Vertical centering
        horizontal_alignment=CrossAxisAlignment.CENTER  # Horizontal centering
    )
    def process_translate(e):
        global LANGUAGES_DICT
        translator = googletrans.Translator()
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
        if language_dropdown_1.value==None:
            temp = translator.translate(text_field_part_1.value,dest=LANGUAGES_DICT[str(language_dropdown_2.value.lower())])
        else:
            temp = translator.translate(text_field_part_1.value,src=LANGUAGES_DICT[str(language_dropdown_1.value.lower())],dest=LANGUAGES_DICT[str(language_dropdown_2.value.lower())])
        stackbro.controls.remove(loading)
        text_field_part_2.value = temp.text
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
        text = text_field_part_2.value
        lang = LANGUAGES_DICT[language_dropdown_2.value.lower()]
    
        tts = gTTS(text, lang=lang)
    
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            temp_audio_path = temp_audio.name  # Get temp file path
            temp_audio.close()  # Close the file before writing
    
            tts.save(temp_audio_path)  # Now save works
    
        print(f"Saved at: {temp_audio_path}")  # Debugging
    text_field = Container(
        Column(
            [
                text_field_part_1,
                Divider(height=20, thickness=2, color="grey"),
                Row(
                    [
                        Row(
                            [IconButton(Icons.CAMERA_ALT), IconButton(Icons.MIC)],
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

    #Navigation Bar at bottom of Page
    page.navigation_bar = NavigationBar(
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
    page_contents = {
        0: Column(controls=[home_card,home_part2]),
        3: translation_page_column(page)
    }

    #function to set changed page
    def changedbro(e=None):
        page.controls.clear()
        page.add(home_appbar,page_contents.get(page.navigation_bar.selected_index,Text("Coming Soon")))
        if page.navigation_bar.selected_index!=0:
            page.remove(home_appbar)
        if page.navigation_bar.selected_index==3:
            page.add(translation_page_appbar())
        page.update()

    page.navigation_bar.on_change = changedbro
    page.add(home_appbar,home_card,home_part2) #default page - Home
    #page.bgcolor = "#000000"
    #temp = qr_code_scanner()
    #page.add(temp[0])
    #page.add(temp[1])
    #page.add(Text("Hi bro !",color="#ffffff"))
    page.update()


def qr_code_scanner():
    app_bar = AppBar(
        leading=IconButton(Icons.CLOSE, icon_color="#ffffff"),
        leading_width=50,
        center_title=False,
        bgcolor="#000000",
        actions=[
            IconButton(Icons.INFO_OUTLINE, icon_color="#ffffff"),
            IconButton(Icons.SETTINGS_ACCESSIBILITY_OUTLINED, icon_color="#ffffff")
        ]
    )

    new_cont = Container(
        alignment=alignment.bottom_right,
        gradient=LinearGradient(
            begin=alignment.top_left,
            end=Alignment(0.8, 1),
            colors=[
                "0xff1f005c",
                "0xff5b0060",
                "0xff870160",
                "0xffac255e",
                "0xffca485c",
                "0xffe16b5c",
                "0xfff39060",
                "0xffffb56b",
            ],
            tile_mode=GradientTileMode.MIRROR,
            rotation=math.pi / 3,
        ),
        width=150,
        height=150,
        border_radius=5
    )

    # Wrapping new_cont inside a Column for vertical centering
    centered_layout = Column(
        controls=[Container(content=new_cont, alignment=alignment.center)],
        alignment=CrossAxisAlignment.START,  # Centers content vertically
        horizontal_alignment=CrossAxisAlignment.CENTER,
        expand=True  # Allows column to take full space
    )

    return [app_bar, centered_layout]

app(main)