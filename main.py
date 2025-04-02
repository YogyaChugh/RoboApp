from flet import *
import math

LANGUAGES = {
    'af': 'afrikaans',
    'sq': 'albanian',
    'am': 'amharic',
    'ar': 'arabic',
    'hy': 'armenian',
    'az': 'azerbaijani',
    'eu': 'basque',
    'be': 'belarusian',
    'bn': 'bengali',
    'bs': 'bosnian',
    'bg': 'bulgarian',
    'ca': 'catalan',
    'ceb': 'cebuano',
    'ny': 'chichewa',
    'zh-cn': 'chinese (simplified)',
    'zh-tw': 'chinese (traditional)',
    'co': 'corsican',
    'hr': 'croatian',
    'cs': 'czech',
    'da': 'danish',
    'nl': 'dutch',
    'en': 'english',
    'eo': 'esperanto',
    'et': 'estonian',
    'tl': 'filipino',
    'fi': 'finnish',
    'fr': 'french',
    'fy': 'frisian',
    'gl': 'galician',
    'ka': 'georgian',
    'de': 'german',
    'el': 'greek',
    'gu': 'gujarati',
    'ht': 'haitian creole',
    'ha': 'hausa',
    'haw': 'hawaiian',
    'iw': 'hebrew',
    'he': 'hebrew',
    'hi': 'hindi',
    'hmn': 'hmong',
    'hu': 'hungarian',
    'is': 'icelandic',
    'ig': 'igbo',
    'id': 'indonesian',
    'ga': 'irish',
    'it': 'italian',
    'ja': 'japanese',
    'jw': 'javanese',
    'kn': 'kannada',
    'kk': 'kazakh',
    'km': 'khmer',
    'ko': 'korean',
    'ku': 'kurdish (kurmanji)',
    'ky': 'kyrgyz',
    'lo': 'lao',
    'la': 'latin',
    'lv': 'latvian',
    'lt': 'lithuanian',
    'lb': 'luxembourgish',
    'mk': 'macedonian',
    'mg': 'malagasy',
    'ms': 'malay',
    'ml': 'malayalam',
    'mt': 'maltese',
    'mi': 'maori',
    'mr': 'marathi',
    'mn': 'mongolian',
    'my': 'myanmar (burmese)',
    'ne': 'nepali',
    'no': 'norwegian',
    'or': 'odia',
    'ps': 'pashto',
    'fa': 'persian',
    'pl': 'polish',
    'pt': 'portuguese',
    'pa': 'punjabi',
    'ro': 'romanian',
    'ru': 'russian',
    'sm': 'samoan',
    'gd': 'scots gaelic',
    'sr': 'serbian',
    'st': 'sesotho',
    'sn': 'shona',
    'sd': 'sindhi',
    'si': 'sinhala',
    'sk': 'slovak',
    'sl': 'slovenian',
    'so': 'somali',
    'es': 'spanish',
    'su': 'sundanese',
    'sw': 'swahili',
    'sv': 'swedish',
    'tg': 'tajik',
    'ta': 'tamil',
    'te': 'telugu',
    'th': 'thai',
    'tr': 'turkish',
    'uk': 'ukrainian',
    'ur': 'urdu',
    'ug': 'uyghur',
    'uz': 'uzbek',
    'vi': 'vietnamese',
    'cy': 'welsh',
    'xh': 'xhosa',
    'yi': 'yiddish',
    'yo': 'yoruba',
    'zu': 'zulu',
}

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

    def change_the_nav_url(e):
        page.navigation_bar.selected_index=int(e.control.data)
        changedbro()
        page.update()

    # Card For Home Page
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

    #Container containing navigation for different pages
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

    #Card for Robot | Which Robot bro ??
    robot_card = Container(
        Row(
            [
                Text("Robot 01"),
                ElevatedButton("Connect")
            ],
        ),
        bgcolor="#FFB0BEC5"
    )

    #Function to return all languages in form of drop-down
    def get_options():
        options = []
        for lang in LANGUAGES:
            options.append(
                DropdownOption(
                    key=LANGUAGES[lang].capitalize(),
                    content=Text(
                        value=LANGUAGES[lang].capitalize()
                    ),
                )
            )
        return options

    #Row containing the main translator
    carder = Row(
            [
                Container(
                    Dropdown(
                        editable=True,
                        label="Language",
                        options=get_options(),
                        enable_filter=True,
                        enable_search=True,
                        menu_height=200,
                        width=150,
                        bgcolor="#ffffff"
                    ),
                    bgcolor="#ffffff",
                    border_radius=4
                ),
                IconButton(Icons.SWAP_HORIZ_OUTLINED,adaptive=True,bgcolor="#ffffff"),
                Container(
                    Dropdown(
                        editable=True,
                        label="Language",
                        options=get_options(),
                        enable_filter=True,
                        enable_search=True,
                        menu_height=200,
                        width=150,
                        bgcolor="#ffffff"
                    ),
                    bgcolor="#ffffff",
                    border_radius=4
                )
            ],
            alignment=MainAxisAlignment.CENTER
        )
    
    #Container for translation
    centered_layout = Container(
        content=carder,
        alignment=alignment.center,  # Centers the content inside
        expand=True,  # Ensures full-screen usage
    )
    
    translation_app_bar = AppBar(
        leading=Icon(Icons.G_TRANSLATE_OUTLINED),
        leading_width=50,
        title= Text("Translate"),
        center_title=False,
        bgcolor="#ffffff"
    )

    text_field = Column(
        [
            TextField(
                autocorrect=True,
                border_radius=10,
                capitalization=TextCapitalization.SENTENCES,
                enable_suggestions=True,
                hint_text="Enter some text here ....",
                min_lines=4,
                multiline=True,
                bgcolor="#ffffff",
                border="none"
            ),
            Divider(height=20, thickness=2, color="black")
        ]
    )
    text_field = Container(
        text_field,
        border=border.all(2, "gray"),  # Outer border like a TextField
        border_radius=5,
        padding=8,
        bgcolor="#ffffff"
    )
    #Dictionary containing all page_contents dude
    page_contents = {
        0: Column(controls=[home_card,home_part2]),
        1: Column(controls=[robot_card]),
        3: Column([centered_layout,text_field])
    }

    #function to set changed page
    def changedbro(e=None):
        page.controls.clear()
        page.add(home_appbar,page_contents.get(page.navigation_bar.selected_index,Text("Coming Soon")))
        if page.navigation_bar.selected_index!=0:
            page.remove(home_appbar)
        if page.navigation_bar.selected_index==3:
            page.add(translation_app_bar)
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