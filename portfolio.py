from pathlib import Path
import flet as ft
import webbrowser
import threading
import time

ASSET_DIR = Path(__file__).resolve().parent


def asset_path(filename):
    return str(ASSET_DIR / filename)


def is_hovered(event):
    return str(getattr(event, "data", "")).lower() == "true"


if hasattr(ft, "BoxFit"):
    FIT_COVER = ft.BoxFit.COVER
elif hasattr(ft, "ImageFit"):
    FIT_COVER = ft.ImageFit.COVER
else:
    FIT_COVER = "cover"

# Compatibility: lightweight PageView shim when missing on some Flet versions
if not hasattr(ft, "PageView"):
    class _CompatPageView(ft.Container):
        def __init__(self, controls=None, selected_index=0, horizontal=False, keep_page=False, snap=False, pad_ends=False, width=None, height=None, on_change=None, **kwargs):
            self.controls = list(controls or [])
            self.selected_index = selected_index
            self.on_change = on_change
            self._row = ft.Row(controls=self.controls, spacing=0)
            super().__init__(content=self._row, width=width, height=height, **kwargs)

        def next_page(self):
            if self.selected_index < len(self.controls) - 1:
                self.selected_index += 1
                if callable(self.on_change):
                    ev = type("E", (), {"control": self})()
                    self.on_change(ev)

        def previous_page(self):
            if self.selected_index > 0:
                self.selected_index -= 1
                if callable(self.on_change):
                    ev = type("E", (), {"control": self})()
                    self.on_change(ev)

    ft.PageView = _CompatPageView

# Provide a simple icons shim for Flet versions that don't expose ft.icons
if not hasattr(ft, "icons"):
    class _CompatIcons:
        ARROW_BACK = "arrow_back"
        ARROW_FORWARD = "arrow_forward"
        SWAP_HORIZ = "swap_horiz"
        CLOSE = "close"
    
    class _CompatIconsWrapper:
        Icons = _CompatIcons()
    
    ft.icons = _CompatIconsWrapper()
    if not hasattr(ft, "Icons"):
        ft.Icons = _CompatIcons()


def main(page: ft.Page):
    page.title = "Web Portfolio"
    page.padding = 0
    page.scroll = "auto"
    page.bgcolor = "#1C1C1C"

    main_column = ft.Column(controls=[], spacing=0)
    content = ft.Container(
        border_radius=30,
        clip_behavior="antiAlias",
        expand=True,
        bgcolor="#1C1C1C",
        image=ft.DecorationImage(
            src=asset_path("Iron man.jpg"),
            fit=FIT_COVER,
            opacity=0.25,
        ),
        animate_opacity=ft.Animation(400, "easeInOut"),
        opacity=1,
        content=main_column,
    )

    main_content = main_column

    def fade_transition(func):
        """Fade out, switch content, fade in"""
        def wrapper(e):
            content.opacity = 0
            page.update()
            import time
            time.sleep(0.15)
            func(e)
            content.opacity = 1
            page.update()
        return wrapper

    def make_link_handler(url):
        def handler(e):
            # Open links in a background thread to avoid blocking the UI
            threading.Thread(target=webbrowser.open_new_tab, args=(url,), daemon=True).start()
        return handler

    def home(e):
        name_field = ft.TextField(label="Name", border_color="white", color="white", cursor_color="white")
        email_field = ft.TextField(label="Email", border_color="white", color="white")
        msg_field = ft.TextField(label="Message", multiline=True, min_lines=3, border_color="white", color="white")
        title_hover = {"hovered": False}

        def on_title_hover(event):
            title_hover["hovered"] = is_hovered(event)
            page.update()

        main_content.controls.clear()

        base_text_style = {"font_family": "Arial", "size": 18, "weight": "w500"}
        info_style = {"size": 18, "color": "yellow", "text_align": "center", "font_family": "Arial"}

        slide_status = ft.Text("Slide 1 / 3", size=16, color="#AAAAAA")

        def on_slide_change(e):
            slide_status.value = f"Slide {e.control.selected_index + 1} / {len(slide_view.controls)}"
            page.update()

        slide_view = ft.PageView(
            controls=[
                ft.Container(
                    content=ft.Column([
                        ft.Text("Project Showcase", size=22, weight="bold", color="white"),
                        ft.Text("Modern UI components, smooth animations, and responsive design.", size=16, color="#CCCCCC", text_align="center"),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER, spacing=8),
                    padding=20,
                    border_radius=20,
                    bgcolor="#232323",
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Text("Firebase Backend", size=22, weight="bold", color="white"),
                        ft.Text("Secure cloud data sync and real-time app integration.", size=16, color="#CCCCCC", text_align="center"),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER, spacing=8),
                    padding=20,
                    border_radius=20,
                    bgcolor="#232323",
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Text("Interactive Experience", size=22, weight="bold", color="white"),
                        ft.Text("Hover effects, clickable images, and animated transitions.", size=16, color="#CCCCCC", text_align="center"),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER, spacing=8),
                    padding=20,
                    border_radius=20,
                    bgcolor="#232323",
                ),
            ],
            selected_index=0,
            keep_page=True,
            horizontal=True,
            snap=True,
            pad_ends=True,
            width=700,
            height=240,
            on_change=on_slide_change,
        )

        slide_view_container = ft.Container(
            content=slide_view,
            padding=10,
            border_radius=20,
            animate_opacity=ft.Animation(250, "easeInOut"),
            animate_scale=ft.Animation(250, "easeInOut"),
            opacity=1,
            scale=1.0,
        )

        def update_slide_status():
            slide_status.value = f"Slide {slide_view.selected_index + 1} / {len(slide_view.controls)}"
            page.update()

        def slide_button_pulse():
            slide_view_container.scale = 0.97
            slide_view_container.opacity = 0.85
            page.update()
            time.sleep(0.12)
            slide_view_container.scale = 1.0
            slide_view_container.opacity = 1.0
            page.update()

        def slide_prev(e):
            slide_view.previous_page()
            update_slide_status()
            threading.Thread(target=slide_button_pulse, daemon=True).start()

        def slide_next(e):
            slide_view.next_page()
            update_slide_status()
            threading.Thread(target=slide_button_pulse, daemon=True).start()

        def icon_hover(event):
            event.control.scale = 1.1 if is_hovered(event) else 1.0
            page.update()

        # Build home column and profile section with pulse animation on load
        # define profile container first so we can reference it in the column controls
        profile_container = ft.Container(
            content=ft.Image(
                src=asset_path("Gehas.jpeg"),
                width=300,
                height=300,
                border_radius=150,
                fit="cover"
            ),
            margin=ft.Margin(left=0, top=40, right=0, bottom=0),
            shadow=ft.BoxShadow(blur_radius=30, color="#FF6B3566", spread_radius=2),
            border_radius=150,
            tooltip="Open LinkedIn profile",
            on_click=make_link_handler("https://www.linkedin.com/in/gehas-iimene-2463412a1/"),
        )

        home_container = ft.Container(
            padding=ft.Padding(left=24, right=24, top=20, bottom=20),
            alignment=ft.alignment.top_center,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=24,
                controls=[
                    profile_container,
                    ft.Text(
                        "Welcome to my portfolio",
                        size=36,
                        weight="bold",
                        color="white",
                        text_align="center",
                        font_family="Arial",
                        animate_scale=ft.Animation(300, "easeInOut"),
                        scale=1.03 if title_hover["hovered"] else 1.0,
                        animate_opacity=ft.Animation(300, "easeInOut"),
                        opacity=0.95 if title_hover["hovered"] else 1.0,
                        tooltip="Hover for a smooth intro animation",
                    ),
                    ft.Divider(color="#FF6B35", height=3, thickness=5),

                    ft.Container(
                        content=ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=14,
                            controls=[
                                ft.Text("Portfolio Slideshow", size=20, weight="bold", color="#FF6B35", font_family="Arial"),
                                ft.Text("Explore the highlights below by clicking the arrows.", size=18, color="#DDDDDD", font_family="Arial", text_align="center"),
                                slide_view_container,
                                ft.Row(
                                    controls=[
                                        ft.IconButton(
                                            ft.icons.Icons.ARROW_BACK,
                                            icon_color="white",
                                            icon_size=22,
                                            on_click=slide_prev,
                                            on_hover=icon_hover,
                                            animate_scale=ft.Animation(150, "easeInOut"),
                                            scale=1.0,
                                        ),
                                        slide_status,
                                        ft.IconButton(
                                            ft.icons.Icons.ARROW_FORWARD,
                                            icon_color="white",
                                            icon_size=22,
                                            on_click=slide_next,
                                            on_hover=icon_hover,
                                            animate_scale=ft.Animation(150, "easeInOut"),
                                            scale=1.0,
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    spacing=28,
                                ),
                            ],
                        ),
                        padding=ft.Padding(left=30, top=20, right=30, bottom=20),
                        bgcolor="#1F1F1F",
                        border_radius=20,
                        width=760,
                        alignment=ft.alignment.center,
                    ),

                    ft.Container(
                        bgcolor="#2A2A2A",
                        border_radius=16,
                        padding=ft.Padding(left=40, top=20, right=40, bottom=20),
                        shadow=ft.BoxShadow(blur_radius=15, color="#00000055"),
                        width=760,
                        alignment=ft.alignment.center,
                        content=ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=6,
                            controls=[
                                ft.Text("Gehas Iimene", weight="bold", **info_style),
                                ft.Text("Student No: 224134949", **info_style),
                                ft.Text("Module: Computer Programming I", **info_style),
                                ft.Text("Course: Electrical Engineering", **info_style),
                                ft.Text("Year: 2026", **info_style),
                            ]
                        )
                    ),

                    ft.Divider(color="#FF6B35", height=40),

                    ft.Text("Introduction", size=24, weight="bold", color="#FF6B35", font_family="Arial"),
                    ft.Container(
                        content=ft.Text(
                            "Welcome to my portfolio. I am Gehas Iimene, an Electrical Engineering student at the University of Namibia with a passion for technology, programming, and innovation. Here, you will find projects and academic work that reflect my journey in applying engineering concepts to real-world challenges in electronics, power systems, and software development.",
                            size=18,
                            color="white",
                            font_family="Arial",
                            text_align="center",
                        ),
                        padding=ft.Padding(left=20, top=0, right=20, bottom=0),
                        width=760,
                        alignment=ft.alignment.center,
                    ),

                    ft.Divider(color="#FF6B35", height=55),

                    ft.Text("Contact", size=30, weight="bold", color="#FF6B35"),
                    ft.Container(
                        padding=20,
                        width=900,
                        alignment=ft.alignment.center,
                        content=ft.ResponsiveRow(
                            alignment=ft.MainAxisAlignment.CENTER,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[

                                ft.Container(
                                    col={"sm": 12, "md": 6},
                                    content=ft.Text(
                                        "I’m passionate about engineering, innovation, and continuous learning. If you’d like to discuss electrical systems, programming, internships, or potential collaborations, feel free to send me a message — I’d love to hear from you.",
                                        size=16,
                                        color="white",
                                        text_align="center" if page.width < 600 else "left"
                                    ),
                                    padding=20,
                                ),

                                ft.Container(
                                    col={"sm": 12, "md": 5},
                                    padding=30,
                                    bgcolor="#2A2A2A",
                                    border_radius=30,
                                    content=ft.Column(
                                        spacing=20,
                                        controls=[
                                            name_field,
                                            email_field,
                                            msg_field,
                                            ft.FilledButton(
                                                "Send Message",
                                                style=ft.ButtonStyle(bgcolor="#FF6B35", color="white"),
                                                width=float("inf"),
                                                on_click=make_link_handler(
                                                    f"mailto:gehasiimene@gmail.com?subject=Message from {name_field.value}&body=From: {email_field.value}%0D%0A%0D%0A{msg_field.value}"
                                                )
                                            ),
                                        ]
                                    ),
                                ),

                            ],
                        ),
                    ),

                    ft.Divider(color="#FF6B35", height=60),
                    ft.Text(
                        "© 2026 Gehas Iimene | Computer Programming I Portfolio",
                        color="#AAAAAA",
                        size=13,
                        italic=True
                    ),
                    ft.Container(height=20)
                ]
            )
        )

        # Pulse animation for profile image on load
        def _pulse_profile():
            for _ in range(2):
                profile_container.scale = 1.03
                page.update()
                time.sleep(0.35)
                profile_container.scale = 1.0
                page.update()
                time.sleep(0.25)
        threading.Thread(target=_pulse_profile, daemon=True).start()

        page.update()


    def timeline(e):
        HEADER_SIZE = 34
        WEEK_SIZE = 20
        CONTENT_SIZE = 15
        ACCENT_COLOR = "#FF6B35"
        TEXT_COLOR = "white"
        SUBTLE_COLOR = "#CCCCCC"

        progress_values = [1.0, 0.9, 0.85, 0.8, 0.75]
        week_index = [0]

        def week_entry(title, task):
            val = progress_values[week_index[0] % len(progress_values)]
            week_index[0] += 1
            return ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text(title, size=WEEK_SIZE, weight="bold", color=ACCENT_COLOR, expand=True),
                        ft.Text(f"{int(val*100)}%", size=13, color=ACCENT_COLOR, weight="bold"),
                    ]),
                    ft.ProgressBar(
                        value=val,
                        bgcolor="#2A2A2A",
                        color=ACCENT_COLOR,
                        height=6,
                        border_radius=3,
                    ),
                    ft.Text(task, size=CONTENT_SIZE, color=TEXT_COLOR),
                    ft.Divider(height=20, thickness=1, color="#FFFFFF1F"),
                ], spacing=8),
                padding=ft.Padding(left=0, top=10, right=0, bottom=5),
                animate=ft.Animation(300, "easeOut"),
            )

        main_content.controls.clear()
        timeline_content = [
            ft.Text("Project Timeline", size=HEADER_SIZE, weight="bold", color=TEXT_COLOR),
            ft.Container(
                content=ft.Text(
                    "As the Firebase Manager of Group 14, I was responsible for the backend infrastructure of the MineOps application.  "
                    "My focus included setting up and managing the Firebase database, handling real-time data synchronization, and  "
                    "ensuring secure and reliable data flow between the app and the cloud.",
                    size=CONTENT_SIZE,
                    color=SUBTLE_COLOR,
                ),
                margin=ft.Margin(left=0, top=20, right=0, bottom=30)
            ),
        ]

        milestones = [
            ("Week 1: Firebase Setup", "Configured Firebase project architecture, authentication, and database structure."),
            ("Week 2: Database Management", "Designed and managed Firestore/Realtime Database collections and security rules."),
            ("Week 3: Authentication & Security", "Implemented user authentication, access control, and Firebase security policies."),
            ("Week 4: Cloud Functions & Optimization", "Integrated Firebase Cloud Functions and optimized backend performance."),
            ("Week 5: Deployment & Monitoring", "Managed hosting deployment, analytics, testing, and real-time system monitoring."),
        ]

        for week_title, description in milestones:
            timeline_content.append(week_entry(week_title, description))
        main_content.controls.append(
            ft.Container(
                content=ft.Column(timeline_content, scroll="hidden"),
                padding=ft.Padding(left=40, top=40, right=40, bottom=40),
                expand=True
            )
        )

        page.update()



    def github(e):
        HEADER_SIZE = 34
        SUBHEADER_SIZE = 20
        CONTENT_SIZE = 15
        ACCENT_COLOR = "#FF6B35"
        TEXT_COLOR = "white"
        SUBTLE_COLOR = "#CCCCCC"

        main_content.controls.clear()

        github_content = [
            ft.Text("GitHub Evidence", size=HEADER_SIZE, weight="bold", color=TEXT_COLOR),
            ft.Container(
                content=ft.Text(
                    "As the Firebase Manager for Group 14, I was responsible for managing and maintaining the Firebase backend infrastructure for MineOPPs. "
                    "This included configuring authentication services, managing the database structure, monitoring real-time data flow, and ensuring secure and efficient integration between the application and Firebase services. "
                    "focused on maintaining a reliable, organized, and scalable backend environment "
                    "that supported effective collaboration within the group.",
                    size=CONTENT_SIZE,
                    color=SUBTLE_COLOR,
                ),
                margin=ft.Margin(left=0, top=20, right=0, bottom=30)
            ),

            ft.Divider(height=10, thickness=1, color="#FFFFFF1F"),
            ft.Text("Project Repository", size=SUBHEADER_SIZE, weight="bold", color=TEXT_COLOR),
            ft.Text(
                "Access the complete source code and commit history below:",
                size=CONTENT_SIZE,
                color=TEXT_COLOR
            ),
            
            ft.Container(
                content=ft.FilledButton(
                    "View Repository on GitHub",
                    style=ft.ButtonStyle(
                        color="white",
                        bgcolor="#FF6B35",
                        padding=20,
                        shape=ft.RoundedRectangleBorder(radius=12),
                    ),
                    on_click=make_link_handler("https://github.com/gehasiimene-cpu")
                ),
                padding=ft.Padding(left=0, top=15, right=0, bottom=30)
            ),

            ft.Divider(height=10, thickness=1, color="#FFFFFF1F"),

            ft.Text("Development Screenshots", size=SUBHEADER_SIZE, weight="bold", color=TEXT_COLOR),
            ft.Text(
                "Visual evidence of commit history and code structure.",
                size=CONTENT_SIZE,
                color=SUBTLE_COLOR
            ),
        ]

        main_content.controls.append(
            ft.Container(
                content=ft.Column(github_content, scroll="auto"),
                padding=ft.Padding(left=40, top=40, right=40, bottom=40),
                expand=True
            )
        )

        page.update()


    def certificates(e):
        # Styling Configuration
        HEADER_SIZE = 34
        CONTENT_SIZE = 15
        ACCENT_COLOR = "#FF6B35"
        TEXT_COLOR = "white"
        SUBTLE_COLOR = "#CCCCCC"

        def cert_card(img_path, url):
            """Creates a certificate tile and links it to a URL."""
            return ft.Container(
                content=ft.Image(
                    src=img_path,
                    border_radius=10,
                    fit="cover"
                ),
                padding=20,
                bgcolor="#2A2A2A", 
                border_radius=25,
                shadow=ft.BoxShadow(blur_radius=15, color="#00000042"),
                col={"sm": 15, "md": 12},
                tooltip="Open certificate link",
                on_click=make_link_handler(url),
            )

        main_content.controls.clear()
        cert_images = [
            asset_path("cert1.png"), asset_path("cert2.png"),
            asset_path("cert3.png"), asset_path("cert4.png"),
            asset_path("cert5.png"), asset_path("cert6.png"),
        ]
        cert_links = [
            "https://1drv.ms/b/c/52cc87a4880a9a7a/IQAQv1Sq8K9jTY3-ToS7FgfoASLS-1P_2nFHmsrsAYSZjCs?e=MneDy1",
            "https://1drv.ms/b/c/52cc87a4880a9a7a/IQBL7x6vNKBQT6Mqf6B2wp5vAWbdhv_8x6X3om_45ynhizM?e=tgQxkY",
            "https://1drv.ms/b/c/52cc87a4880a9a7a/IQBWAvolDPJ5TIdNjxdtUF74Aec9HY3IlIJfo5A29dx05Ls?e=zk4ZlK",
            "https://1drv.ms/b/c/52cc87a4880a9a7a/IQB2EBEvmI-CQpcMx2CGNbkJAWXtdzhNG70EdU8968RP6zQ?e=CsvZ4p",
            "https://1drv.ms/b/c/52cc87a4880a9a7a/IQDHbgsmKqAmQLLlTRVZfsxAAaa0C9Q2g1KI46dF454CZgk?e=luBiKt",
            "https://1drv.ms/b/c/52cc87a4880a9a7a/IQACPX00bUC-RZedw3Gqx-q4AbIsSSTb2CCEj4gUqXvLa6I?e=EfQu34",
        ]
        cert_content = [
            ft.Text("MATLAB Achievement Hub", size=HEADER_SIZE, weight="bold", color=TEXT_COLOR),
            ft.Container(
                content=ft.Text(
                    "Proof of completion for 6 specialized MathWorks Learning Center courses. "
                    "These certifications validate my technical proficiency in engineering "
                    "computations and algorithm development.",
                    size=CONTENT_SIZE,
                    color=SUBTLE_COLOR,
                ),
                margin=ft.Margin(left=0, top=10, right=0, bottom=20)
            ),

            ft.ResponsiveRow(
                controls=[
                    cert_card(img, url)
                    for img, url in zip(cert_images, cert_links)
                ],
                spacing=30,
                run_spacing=30,
            )
        ]

        main_content.controls.append(
            ft.Container(
                content=ft.Column(cert_content, scroll="auto"),
                padding=ft.Padding(left=30, top=30, right=30, bottom=30),
                expand=True
            )
        )

        page.update()


 

    # webbrowser already imported at top

    def video(e):
        # Styling Configuration
        HEADER_SIZE = 30
        SUBHEADER_SIZE = 20
        CONTENT_SIZE = 15
        ACCENT_COLOR = "#FF6B35"
        TEXT_COLOR = "white"
        SUBTLE_COLOR = "#CCCCCC"

        def card_hover(event):
            event.control.scale = 1.025 if is_hovered(event) else 1.0
            event.control.shadow = ft.BoxShadow(
                blur_radius=22 if is_hovered(event) else 12,
                color="#FF6B3577" if is_hovered(event) else "#00000055",
            )
            page.update()
        
        def module_card(title, description, math_formula):
            """Creates a card for engineering modules to fill space"""
            return ft.Container(
                content=ft.Column([
                    ft.Text(title, size=18, weight="bold", color=ACCENT_COLOR),
                    ft.Text(description, size=CONTENT_SIZE, color=TEXT_COLOR),
                    ft.Container(
                        content=ft.Text(math_formula, italic=True, color="#1C1C1C", size=13),
                        padding=10,
                        bgcolor="#FFFFFF1A",
                        border_radius=5
                    ),
                ], spacing=10),
                padding=20,
                bgcolor="#232323",
                border=ft.Border(left=ft.BorderSide(1, "#FF6B3555"), top=ft.BorderSide(1, "#FF6B3555"), right=ft.BorderSide(1, "#FF6B3555"), bottom=ft.BorderSide(1, "#FF6B3555")),
                border_radius=12,
                shadow=ft.BoxShadow(blur_radius=12, color="#00000055"),
                animate=ft.Animation(200, "easeOut"),
                animate_scale=ft.Animation(180, "easeOut"),
                scale=1.0,
                on_hover=card_hover,
                col={"sm": 12, "md": 6, "lg": 4}
            )

        main_content.controls.clear()

        video_content = [
            ft.Text("Project Demonstrations", size=HEADER_SIZE, weight="bold", color=TEXT_COLOR),
            ft.Text(
                "Technical showcase of mobile development, Firebase integration, and engineering concepts.",
                size=CONTENT_SIZE, color=SUBTLE_COLOR
            ),
            
            ft.Container(
                content=ft.FilledButton(
                    "Watch Full Showcase on YouTube",
                    style=ft.ButtonStyle(bgcolor=ACCENT_COLOR, color=TEXT_COLOR),
                    on_click=make_link_handler("https://youtube.com"),
                ),
                margin=ft.Margin(left=0, top=10, right=0, bottom=20)
            ),

            ft.Container(
                content=ft.Column([
                    ft.Text("MineOps APK App Overview", size=SUBHEADER_SIZE, weight="bold", color=ACCENT_COLOR),
                    ft.Text(
                        "The MineOps Android APK is a mobile engineering support application developed for the Group 14 project. "
                        "It brings mining-operation data, engineering calculations, project records, and Firebase-backed storage into one app experience. "
                        "The app was designed to help users record operational information, view important project details, and interact with live data from the cloud.",
                        size=CONTENT_SIZE,
                        color=TEXT_COLOR,
                    ),
                    ft.Text(
                        "In the video demonstration, the important points to show are the app navigation, Firebase data flow, user input screens, "
                        "calculation features, and how the APK represents the final mobile version of the project.",
                        size=CONTENT_SIZE,
                        color=SUBTLE_COLOR,
                    ),
                ], spacing=10),
                padding=20,
                bgcolor="#232323",
                border=ft.Border(left=ft.BorderSide(1, "#FF6B3555"), top=ft.BorderSide(1, "#FF6B3555"), right=ft.BorderSide(1, "#FF6B3555"), bottom=ft.BorderSide(1, "#FF6B3555")),
                border_radius=12,
                shadow=ft.BoxShadow(blur_radius=12, color="#00000055"),
                animate=ft.Animation(200, "easeOut"),
                animate_scale=ft.Animation(180, "easeOut"),
                scale=1.0,
                on_hover=card_hover,
            ),

            ft.Divider(height=30, thickness=1, color="#FFFFFF1F"),

            ft.Text("MineOps APK Module Contributions", size=SUBHEADER_SIZE, weight="bold", color=TEXT_COLOR),
            ft.ResponsiveRow([
                module_card(
                    "Material Costing Module",
                    "In the MineOps APK, this module supports material and resource cost entries for mining-related operations.",
                    "APK feature: Quantity × Unit Cost + Overheads"
                ),
                module_card(
                    "Mining Operations Module",
                    "This APK section focuses on tracking production values and syncing operational records through Firebase.",
                    "APK feature: Actual Output / Planned Output"
                ),
                module_card(
                    "Site Infrastructure Module",
                    "The app includes support for recording site-related information that connects engineering checks with mobile data entry.",
                    "APK feature: Site data + engineering notes"
                ),
                module_card(
                    "APK System Architecture",
                    "This contribution covers the app navigation, screen flow, Firebase connection, and final Android APK packaging.",
                    "APK feature: UI screens + cloud backend"
                ),
            ], spacing=20, run_spacing=20) # 'run_spacing' adds vertical gaps between rows
        ]

        main_content.controls.append(
            ft.Container(
                content=ft.Column(video_content, scroll="auto", spacing=20),
                padding=ft.Padding(left=30, top=30, right=30, bottom=30),
                expand=True
            )
        )

        page.update()




    def blog(e):
        HEADER_SIZE = 30
        SUBHEADER_SIZE = 20
        CONTENT_SIZE = 15
        ACCENT_COLOR = "#FF6B35"
        TEXT_COLOR = "white"
        SUBTLE_COLOR = "#CCCCCC"

        def card_hover(event):
            event.control.scale = 1.02 if is_hovered(event) else 1.0
            event.control.shadow = ft.BoxShadow(
                blur_radius=20 if is_hovered(event) else 10,
                color="#FF6B3566" if is_hovered(event) else "#00000044",
            )
            page.update()

        def close_dialog(e, dialog):
            dialog.open = False
            page.update()

        def show_blog_post(title, content_text):
            dialog = ft.AlertDialog(
                title=ft.Text(title, weight="bold", size=SUBHEADER_SIZE, color=TEXT_COLOR),
                content=ft.Column([
                    ft.Text(content_text, size=CONTENT_SIZE, color=TEXT_COLOR),
                ], spacing=10),
                actions=[
                    ft.TextButton("Close", on_click=lambda e: close_dialog(e, dialog), style=ft.ButtonStyle(color=ACCENT_COLOR)),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )
            page.dialog = dialog
            dialog.open = True
            page.update()

        def blog_post_preview(title, description, full_text):
            """Helper to create professional blog entry summaries"""
            return ft.Container(
                content=ft.Column([
                    ft.Text(title, size=SUBHEADER_SIZE, weight="bold", color=ACCENT_COLOR),
                    ft.Text(description, size=CONTENT_SIZE, color=TEXT_COLOR),
                    ft.TextButton(
                        "Read full post...",
                        style=ft.ButtonStyle(color=ACCENT_COLOR),
                        on_click=lambda e: show_blog_post(title, full_text),
                    ),
                ], spacing=5),
                margin=ft.Margin(left=0, top=0, right=0, bottom=20),
                padding=ft.Padding(left=15, top=15, right=15, bottom=15),
                border=ft.Border(left=ft.BorderSide(1, "#FF6B3555"), top=ft.BorderSide(1, "#FF6B3555"), right=ft.BorderSide(1, "#FF6B3555"), bottom=ft.BorderSide(1, "#FF6B3555")),
                border_radius=10,
                bgcolor="#232323",
                animate=ft.Animation(200, "easeOut"),
                animate_scale=ft.Animation(180, "easeOut"),
                scale=1.0,
                on_hover=card_hover,
                shadow=ft.BoxShadow(blur_radius=10, color="#00000044"),
            )

        def technical_blog_video_card():
            video_name = "WhatsApp Video 2026-06-14 at 04.23.27.mp4"
            video_path = asset_path(video_name)
            if not Path(video_path).exists():
                video_path = asset_path(f"2026 portfolio website/{video_name}")

            def open_video(e):
                threading.Thread(
                    target=webbrowser.open_new_tab,
                    args=(Path(video_path).resolve().as_uri(),),
                    daemon=True,
                ).start()

            video_controls = [
                ft.Text("MineOps APK Demonstration Video", size=SUBHEADER_SIZE, weight="bold", color=ACCENT_COLOR),
                ft.Text(
                    "This video shows the MineOps APK in action, including the mobile interface, project flow, and app demonstration evidence for the technical blog.",
                    size=CONTENT_SIZE,
                    color=TEXT_COLOR,
                ),
            ]

            if Path(video_path).exists() and hasattr(ft, "Video") and hasattr(ft, "VideoMedia"):
                video_controls.append(
                    ft.Video(
                        playlist=[ft.VideoMedia(video_path)],
                        aspect_ratio=16 / 9,
                        autoplay=False,
                        muted=False,
                    )
                )
            else:
                video_controls.append(
                    ft.Text(
                        "Video preview is not available in this Flet version, but you can open the local video below.",
                        size=CONTENT_SIZE,
                        color=SUBTLE_COLOR,
                    )
                )

            video_controls.append(
                ft.FilledButton(
                    "Open Video",
                    style=ft.ButtonStyle(bgcolor=ACCENT_COLOR, color=TEXT_COLOR),
                    on_click=open_video,
                )
            )

            return ft.Container(
                content=ft.Column(video_controls, spacing=12),
                margin=ft.Margin(left=0, top=0, right=0, bottom=20),
                padding=ft.Padding(left=15, top=15, right=15, bottom=15),
                border=ft.Border(left=ft.BorderSide(1, "#FF6B3555"), top=ft.BorderSide(1, "#FF6B3555"), right=ft.BorderSide(1, "#FF6B3555"), bottom=ft.BorderSide(1, "#FF6B3555")),
                border_radius=10,
                bgcolor="#232323",
                animate=ft.Animation(200, "easeOut"),
                animate_scale=ft.Animation(180, "easeOut"),
                scale=1.0,
                on_hover=card_hover,
                shadow=ft.BoxShadow(blur_radius=10, color="#00000044"),
            )

        main_content.controls.clear()

        blog_content = [
            ft.Text("Technical Blog", size=HEADER_SIZE, weight="bold", color=TEXT_COLOR),
            ft.Container(
                content=ft.Text(
                    "Exploring the intersection of software engineering and mobile development. "
                    "Below is a collection of insights regarding the implementation, challenges, "
                    "and solutions encountered during the MineOps development lifecycle.",
                    size=CONTENT_SIZE,
                    color=SUBTLE_COLOR,
                ),
                margin=ft.Margin(left=0, top=10, right=0, bottom=30)
            ),

            technical_blog_video_card(),

            blog_post_preview(
                "MineOps APK App Overview",
                "MineOps is the Android APK application produced for the Group 14 project. It combines mobile navigation, Firebase cloud storage, engineering data handling, and project-specific calculation features into one practical app. The APK represents the final installable version of the project and shows how our software work can be used on a real mobile device.",
                "MineOps is the Android APK application produced for the Group 14 project. The app was built to support mining and engineering workflows by allowing users to work with operational information, project records, and calculation-based features from a mobile interface. My contribution focused strongly on the Firebase side of the system, including database structure, real-time data synchronization, and making sure the mobile app could communicate reliably with the backend. The APK is important because it turns the project from source code into something that can actually be installed, opened, tested, and demonstrated on an Android device.",
            ),
            blog_post_preview(
                "Mobile Development & Flet",
                "Building this portfolio was my first real experience with mobile and desktop UI development using Python and the Flet framework. I learned how to structure pages, handle navigation between sections, and design responsive layouts that adapt to different screen sizes. One of the biggest challenges was understanding how Flet manages state and updates the UI in real time. Through trial and error, I gained a solid understanding of how front-end development works outside of traditional web technologies, and how Python can be used to build fully functional, visually appealing applications.",
                "Building this portfolio was my first real experience with mobile and desktop UI development using Python and the Flet framework. I learned how to structure pages, handle navigation between sections, and design responsive layouts that adapt to different screen sizes. One of the biggest challenges was understanding how Flet manages state and updates the UI in real time. Through trial and error, I gained a solid understanding of how front-end development works outside of traditional web technologies, and how Python can be used to build fully functional, visually appealing applications.",
            ),
            blog_post_preview(
                "Firebase Integration",
                "As the Firebase Manager for Group 14, my role was to design and maintain the backend infrastructure of the MineOps application. I set up the Firebase Realtime Database, configured authentication, and ensured that data flowed securely between the app and the cloud. One key challenge was structuring the database in a way that made it easy for other team members to read and write data without conflicts. This experience gave me a deep appreciation for how backend systems support front-end functionality, and how important it is to plan your data structure before writing a single line of code.",
                "As the Firebase Manager for Group 14, my role was to design and maintain the backend infrastructure of the MineOps application. I set up the Firebase Realtime Database, configured authentication, and ensured that data flowed securely between the app and the cloud. One key challenge was structuring the database in a way that made it easy for other team members to read and write data without conflicts. This experience gave me a deep appreciation for how backend systems support front-end functionality, and how important it is to plan your data structure before writing a single line of code.",
            ),
            blog_post_preview(
                "Git Workflow & Collaboration",
                "Working on the MineOps project as part of Group 14 introduced me to the importance of version control in a team environment. Using Git and GitHub, I learned how to create branches, commit changes, push updates, and merge code without overwriting my teammates' work. Managing a shared repository with multiple contributors taught me discipline in writing clear commit messages and reviewing changes before merging. This workflow is something I now consider an essential skill for any software or engineering project.",
                "Working on the MineOps project as part of Group 14 introduced me to the importance of version control in a team environment. Using Git and GitHub, I learned how to create branches, commit changes, push updates, and merge code without overwriting my teammates' work. Managing a shared repository with multiple contributors taught me discipline in writing clear commit messages and reviewing changes before merging. This workflow is something I now consider an essential skill for any software or engineering project.",
            ),
        ]

        main_content.controls.append(
            ft.Container(
                content=ft.Column(blog_content, scroll="auto"),
                padding=ft.Padding(left=30, top=30, right=30, bottom=30),
                expand=True
            )
        )

        page.update()
   


    navbar = ft.Container(
        bgcolor="#232323",
        padding=ft.Padding(left=20, top=12, right=20, bottom=12),
        shadow=ft.BoxShadow(blur_radius=12, color="#00000066", offset=ft.Offset(0, 3)),
        content=ft.Row(
            controls=[
                ft.Row(
                    controls=[
                        ft.FilledButton("Home", style=ft.ButtonStyle(bgcolor="#2A2A2A", color="white", shape=ft.RoundedRectangleBorder(radius=8), overlay_color="#FF6B3533"), on_click=fade_transition(home)),
                        ft.FilledButton("Timeline", style=ft.ButtonStyle(bgcolor="#2A2A2A", color="white", shape=ft.RoundedRectangleBorder(radius=8), overlay_color="#FF6B3533"), on_click=fade_transition(timeline)),
                        ft.FilledButton("GitHub", style=ft.ButtonStyle(bgcolor="#2A2A2A", color="white", shape=ft.RoundedRectangleBorder(radius=8), overlay_color="#FF6B3533"), on_click=fade_transition(github)),
                        ft.FilledButton("Certificates", style=ft.ButtonStyle(bgcolor="#2A2A2A", color="white", shape=ft.RoundedRectangleBorder(radius=8), overlay_color="#FF6B3533"), on_click=fade_transition(certificates)),
                        ft.FilledButton("Video", style=ft.ButtonStyle(bgcolor="#2A2A2A", color="white", shape=ft.RoundedRectangleBorder(radius=8), overlay_color="#FF6B3533"), on_click=fade_transition(video)),
                        ft.FilledButton("Technical Blog", style=ft.ButtonStyle(bgcolor="#2A2A2A", color="white", shape=ft.RoundedRectangleBorder(radius=8), overlay_color="#FF6B3533"), on_click=fade_transition(blog)),
                    ],
                    spacing=8
                ),
                ft.Row(
                    controls=[
                        ft.TextButton(
                            content=ft.Row([ft.Image(src=asset_path("LinkedIn.png"), width=18, height=18), ft.Text("LinkedIn", color="white", size=13)], spacing=4),
                            on_click=make_link_handler("https://www.linkedin.com/in/gehas-iimene-2463412a1/"),
                        ),
                        ft.TextButton(
                            content=ft.Row([ft.Image(src=asset_path("gmail.png"), width=18, height=18), ft.Text("Email", color="white", size=13)], spacing=4),
                            on_click=make_link_handler("mailto:gehasiimene@gmail.com"),
                        ),
                        ft.TextButton(
                            content=ft.Row([ft.Image(src=asset_path("OIP.webp"), width=18, height=18), ft.Text("Student Email", color="white", size=13)], spacing=4),
                            on_click=make_link_handler("mailto:224134949@students.unam.na"),
                        ),
                    ],
                    spacing=8
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )
    )

    # Splash overlay (entry welcome)
    splash = ft.Container(
        expand=True,
        bgcolor="#001F3F",
        content=ft.Column(
            controls=[
                ft.Text("Gehas Iimene", size=48, weight="bold", color="white"),
            ],
            alignment=ft.alignment.center,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=8,
        ),
        opacity=1,
        animate_opacity=ft.Animation(600, "easeInOut"),
    )

    ui_column = ft.Column(
        controls=[
            navbar,
            ft.Container(content=content, padding=ft.Padding(left=30, top=20, right=30, bottom=30), expand=True),
        ],
        spacing=0,
        expand=True,
    )

    main_stack = ft.Stack(
        controls=[
            ui_column,
            splash,
        ]
    )

    page.add(main_stack)

    # show home content
    home(None)

    # fade out splash after 2.2s
    def _hide_splash():
        time.sleep(2.2)
        splash.opacity = 0
        page.update()
        # wait for the opacity animation to finish, then remove splash from hit testing
        time.sleep(0.65)
        try:
            splash.visible = False
        except Exception:
            # fallback: make it non-interactive
            splash.hit_testable = False
        page.update()
    threading.Thread(target=_hide_splash, daemon=True).start()



if __name__ == "__main__":
    # Start the Flet app (desktop/native view)
    ft.app(main)
