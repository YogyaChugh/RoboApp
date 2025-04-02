from flet import *

def main(page: Page):
    page.title="RoboControl"
    page.scroll = "adaptive"
    page.on_scroll_interval = 10
    page.adaptive = True
    page.bgcolor = "#FFE0E0E0"

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

    #Dictionary containing all page_contents dude
    page_contents = {
        0: Column(controls=[home_card,home_part2]),
        1: Column(controls=[robot_card])
    }

    #function to set changed page
    def changedbro(e=None):
        page.controls.clear()
        page.add(home_appbar,page_contents.get(page.navigation_bar.selected_index,Text("Coming Soon")))
        if page.navigation_bar.selected_index!=0:
            page.remove(home_appbar)
        page.update()

    page.navigation_bar.on_change = changedbro
    page.add(home_appbar,home_card,home_part2) #default page - Home
    page.update()


app(main)