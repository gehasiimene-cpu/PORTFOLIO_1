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
    page.bgcolor = "#040506"

    bg_image_path = asset_path("Iron man.jpg")

    main_column = ft.Column(controls=[], spacing=0)
    content = ft.Container(
        border_radius=30,
        clip_behavior="antiAlias",
        expand=True,
        bgcolor="#FFFFFF",
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
        name_field = ft.TextField(label="Name", border_color="#001F3F", color="#001F3F", cursor_color="#001F3F")
        email_field = ft.TextField(label="Email", border_color="#001F3F", color="#001F3F")
        msg_field = ft.TextField(label="Message", multiline=True, min_lines=3, border_color="#001F3F", color="#001F3F")
        profile_hover = {"hovered": False}
        title_hover = {"hovered": False}

        def on_profile_hover(event):
            profile_hover["hovered"] = is_hovered(event)
            page.update()

        def on_title_hover(event):
            title_hover["hovered"] = is_hovered(event)
            page.update()

        main_content.controls.clear()

        base_text_style = {"font_family": "Arial", "size": 18, "weight": "w500"}
        info_style = {"size": 18, "color": "yellow", "text_align": "center", "font_family": "Arial"}

        slide_status = ft.Text("Slide 1 / 3", size=16, color="#6E7D89")

        def on_slide_change(e):
            slide_status.value = f"Slide {e.control.selected_index + 1} / {len(slide_view.controls)}"
            page.update()

        def prev_slide(e):
            slide_view.previous_page()
            page.update()

        def next_slide(e):
            slide_view.next_page()
            page.update()

        slide_view = ft.PageView(
            controls=[
                ft.Container(
                    content=ft.Column([
                        ft.Text("Project Showcase", size=22, weight="bold", color="#001F3F"),
                        ft.Text("Modern UI components, smooth animations, and responsive design.", size=16, color="#607080", text_align="center"),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER, spacing=8),
                    padding=20,
                    border_radius=20,
                    bgcolor="#F4F7FB",
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Text("Firebase Backend", size=22, weight="bold", color="#001F3F"),
                        ft.Text("Secure cloud data sync and real-time app integration.", size=16, color="#607080", text_align="center"),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER, spacing=8),
                    padding=20,
                    border_radius=20,
                    bgcolor="#F4F7FB",
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Text("Interactive Experience", size=22, weight="bold", color="#001F3F"),
                        ft.Text("Hover effects, clickable images, and animated transitions.", size=16, color="#607080", text_align="center"),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER, spacing=8),
                    padding=20,
                    border_radius=20,
                    bgcolor="#F4F7FB",
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

        main_content.controls.append(
            ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=30,
                controls=[
                    # Profile Section
                    ft.Container(
                        content=ft.Image(
                            src=asset_path("Gehas.jpeg"),
                            width=300,
                            height=300,
                            border_radius=150,
                            fit="cover"
                        ),
                        margin=ft.Margin(left=0, top=40, right=0, bottom=0),
                        shadow=ft.BoxShadow(blur_radius=30, color="#001F3F66", spread_radius=2),
                        border_radius=150,
                        tooltip="Open LinkedIn profile",
                        on_click=make_link_handler("https://www.linkedin.com/in/gehas-iimene-2463412a1/"),
                        on_hover=on_profile_hover,
                        animate_scale=ft.Animation(250, "easeInOut"),
                        scale=1.05 if profile_hover["hovered"] else 1.0,
                    ),

                    ft.Container(
                        content=ft.Text(
                            "Welcome to My Portfolio",
                            size=36,
                            weight="bold",
                            color="#001F3F",
                            text_align="center",
                            font_family="Arial",
                        ),
                        on_hover=on_title_hover,
                        animate_scale=ft.Animation(300, "easeInOut"),
                        scale=1.03 if title_hover["hovered"] else 1.0,
                        animate_opacity=ft.Animation(300, "easeInOut"),
                        opacity=0.95 if title_hover["hovered"] else 1.0,
                        tooltip="Hover for a smooth intro animation",
                    ),

                    ft.Divider(color="#001F3F", height=3, thickness=5),

                    ft.Container(
                        content=ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=14,
                            controls=[
                                ft.Text("Portfolio Slideshow", size=20, weight="bold", color="#001F3F", font_family="Arial"),
                                ft.Text("Explore the highlights below by using the side arrows.", size=18, color="#607080", font_family="Arial", text_align="center"),
                                ft.Row(
                                    controls=[
                                        ft.Container(
                                            content=slide_view,
                                            width=700,
                                            height=240,
                                        ),
                                        ft.Container(
                                            content=ft.Column(
                                                controls=[
                                                    ft.IconButton(
                                                        ft.icons.Icons.ARROW_BACK,
                                                        icon_color="#001F3F",
                                                        icon_size=28,
                                                        on_click=prev_slide,
                                                        tooltip="Previous slide",
                                                    ),
                                                    slide_status,
                                                    ft.IconButton(
                                                        ft.icons.Icons.ARROW_FORWARD,
                                                        icon_color="#001F3F",
                                                        icon_size=28,
                                                        on_click=next_slide,
                                                        tooltip="Next slide",
                                                    ),
                                                ],
                                                alignment=ft.MainAxisAlignment.CENTER,
                                                spacing=18,
                                            ),
                                            padding=ft.Padding(left=20, right=0),
                                            height=240,
                                            alignment=ft.alignment.center,
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    spacing=20,
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                            ],
                        ),
                        padding=ft.Padding(left=30, top=20, right=30, bottom=20),
                        bgcolor="#F4F7FB",
                        border_radius=20,
                        width=940,
                        alignment=ft.alignment.center,
                    ),

                    ft.Container(
                        bgcolor="#F4F7FB",
                        border_radius=16,
                        padding=ft.Padding(left=40, top=20, right=40, bottom=20),
                        shadow=ft.BoxShadow(blur_radius=15, color="#00000055"),
                        width=940,
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

                    ft.Divider(color="#001F3F", height=40),

                    ft.Text("Introduction", size=24, weight="bold", color="#001F3F", font_family="Arial"),
                    ft.Container(
                        content=ft.Text(
                            "Welcome to my portfolio. I am Gehas Iimene, an Electrical Engineering student at the University of Namibia with a passion for technology, programming, and innovation. Here, you will find projects and academic work that reflect my journey in applying engineering concepts to real-world challenges in electronics, power systems, and software development.",
                            size=18,
                            color="#001F3F",
                            font_family="Arial",
                            text_align="center",
                        ),
                        padding=ft.Padding(left=20, top=0, right=20, bottom=0),
                        width=940,
                        alignment=ft.alignment.center,
                    ),

                    ft.Divider(color="#001F3F", height=55),

                    ft.Text("Contact", size=30, weight="bold", color="#001F3F"),
                    ft.Container(
                        padding=20,
                        width=940,
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
                                        color="#001F3F",
                                        text_align="center" if page.width < 600 else "left"
                                    ),
                                    padding=20,
                                ),

                                ft.Container(
                                    col={"sm": 12, "md": 5},
                                    padding=30,
                                    bgcolor="#F4F7FB",
                                    border_radius=30,
                                    content=ft.Column(
                                        spacing=20,
                                        controls=[
                                            name_field,
                                            email_field,
                                            msg_field,
                                            ft.FilledButton(
                                                "Send Message",
                                                style=ft.ButtonStyle(bgcolor="#F4F7FB", color="#001F3F"),
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

                    ft.Divider(color="#001F3F", height=60),
                    ft.Text(
                        "© 2026 Gehas Iimene | Computer Programming I Portfolio",
                        color="#6E7D89",
                        size=13,
                        italic=True
                    ),
                    ft.Container(height=20)
                ]
            )
        )

        set_chat_visible(True, update_ui=False)
        page.update()


    def timeline(e):
        HEADER_SIZE = 34
        WEEK_SIZE = 20
        CONTENT_SIZE = 15
        ACCENT_COLOR = "#001F3F"
        TEXT_COLOR = "#001F3F"
        SUBTLE_COLOR = "#607080"

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
                        bgcolor="#F4F7FB",
                        color=ACCENT_COLOR,
                        height=6,
                        border_radius=3,
                    ),
                    ft.Text(task, size=CONTENT_SIZE, color=TEXT_COLOR),
                    ft.Divider(height=20, thickness=1, color="#001F3F1F"),
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

        set_chat_visible(False, update_ui=False)
        page.update()



    def github(e):
        HEADER_SIZE = 34
        SUBHEADER_SIZE = 20
        CONTENT_SIZE = 15
        ACCENT_COLOR = "#001F3F"
        TEXT_COLOR = "#001F3F"
        SUBTLE_COLOR = "#607080"

        repo_url = "https://github.com/makotajr06/UNAM-I3691CP-SyntaxCrew-MineOps"

        main_content.controls.clear()

        github_content = [
            ft.Text("GitHub Evidence", size=HEADER_SIZE, weight="bold", color=TEXT_COLOR),
            ft.Container(
                content=ft.Text(
                    "As the Firebase Manager for Group 14, I was responsible for managing and maintaining the Firebase backend infrastructure for MineOps. "
                    "This included configuring authentication services, managing the database structure, monitoring real-time data flow, and ensuring secure and efficient integration between the application and Firebase services. "
                    "focused on maintaining a reliable, organized, and scalable backend environment "
                    "that supported effective collaboration within the group.",
                    size=CONTENT_SIZE,
                    color=SUBTLE_COLOR,
                ),
                margin=ft.Margin(left=0, top=20, right=0, bottom=30)
            ),

            ft.Divider(height=10, thickness=1, color="#001F3F1F"),
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
                        color="#001F3F",
                        bgcolor="#F4F7FB",
                        padding=20,
                        shape=ft.RoundedRectangleBorder(radius=12),
                    ),
                    on_click=make_link_handler("https://github.com/makotajr06/UNAM-I3691CP-SyntaxCrew-MineOps")
                ),
                padding=ft.Padding(left=0, top=15, right=0, bottom=30)
            ),

            ft.Divider(height=10, thickness=1, color="#001F3F1F"),

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

        set_chat_visible(False, update_ui=False)
        page.update()


    def certificates(e):
        # Styling Configuration
        HEADER_SIZE = 34
        CONTENT_SIZE = 15
        ACCENT_COLOR = "#001F3F"
        TEXT_COLOR = "#001F3F"
        SUBTLE_COLOR = "#607080"

        def cert_card(img_path, url):
            """Creates a certificate tile and links it to a URL."""
            return ft.Container(
                content=ft.Image(
                    src=img_path,
                    border_radius=10,
                    fit="cover"
                ),
                padding=20,
                bgcolor="#F4F7FB", 
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

        set_chat_visible(False, update_ui=False)
        page.update()


 

    # webbrowser already imported at top

    def video(e):
        # Styling Configuration
        HEADER_SIZE = 30
        SUBHEADER_SIZE = 20
        CONTENT_SIZE = 15
        ACCENT_COLOR = "#001F3F"
        TEXT_COLOR = "#001F3F"
        SUBTLE_COLOR = "#607080"
        
        youtube_url = "https://youtube.com"

        def card_hover(event):
            event.control.scale = 1.025 if is_hovered(event) else 1.0
            event.control.shadow = ft.BoxShadow(
                blur_radius=22 if is_hovered(event) else 12,
                color="#001F3F66" if is_hovered(event) else "#00000055",
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
                bgcolor="#F4F7FB",
                border=ft.Border(left=ft.BorderSide(1, "#001F3F55"), top=ft.BorderSide(1, "#001F3F55"), right=ft.BorderSide(1, "#001F3F55"), bottom=ft.BorderSide(1, "#001F3F55")),
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
                bgcolor="#F4F7FB",
                border=ft.Border(left=ft.BorderSide(1, "#001F3F55"), top=ft.BorderSide(1, "#001F3F55"), right=ft.BorderSide(1, "#001F3F55"), bottom=ft.BorderSide(1, "#001F3F55")),
                border_radius=12,
                shadow=ft.BoxShadow(blur_radius=12, color="#00000022"),
                animate=ft.Animation(200, "easeOut"),
                animate_scale=ft.Animation(180, "easeOut"),
                scale=1.0,
                on_hover=card_hover,
            ),

            ft.Divider(height=30, thickness=1, color="#001F3F1F"),

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
        ACCENT_COLOR = "#001F3F"
        TEXT_COLOR = "#001F3F"
        SUBTLE_COLOR = "#607080"

        def card_hover(event):
            event.control.scale = 1.02 if is_hovered(event) else 1.0
            event.control.shadow = ft.BoxShadow(
                blur_radius=20 if is_hovered(event) else 10,
                color="#001F3F55" if is_hovered(event) else "#00000044",
            )
            page.update()

        def blog_post_preview(title, description):
            """Helper to create professional blog entry summaries"""
            return ft.Container(
                content=ft.Column([
                    ft.Text(title, size=SUBHEADER_SIZE, weight="bold", color=ACCENT_COLOR),
                    ft.Text(description, size=CONTENT_SIZE, color=TEXT_COLOR),
                    ft.TextButton("Read full post...", style=ft.ButtonStyle(color=ACCENT_COLOR)),
                ], spacing=5),
                margin=ft.Margin(left=0, top=0, right=0, bottom=20),
                padding=ft.Padding(left=15, top=15, right=15, bottom=15),
                border=ft.Border(left=ft.BorderSide(1, "#001F3F55"), top=ft.BorderSide(1, "#001F3F55"), right=ft.BorderSide(1, "#001F3F55"), bottom=ft.BorderSide(1, "#001F3F55")),
                border_radius=10,
                bgcolor="#F4F7FB",
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

            blog_post_preview(
                "MineOps APK App Overview",
                "MineOps is the Android APK application produced for the Group 14 project. It combines mobile navigation, Firebase cloud storage, engineering data handling, and project-specific calculation features into one practical app. The APK represents the final installable version of the project and shows how our software work can be used on a real mobile device."
            ),
            blog_post_preview(
                "Mobile Development & Flet", 
                "A deep dive into building responsive UIs using Python and the Flet framework."
            ),
            blog_post_preview(
                "Firebase Integration", 
                "How we managed real-time data and authentication for MineOps."
            ),
            blog_post_preview(
                "Git Workflow & Collaboration", 
                "Lessons learned while managing a multi-developer repository on GitHub."
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
   


    def button_hover(e):
        e.control.scale = 1.05 if e.data else 1.0
        page.update()

    navbar = ft.Container(
        bgcolor="#05111F",
        padding=ft.Padding(left=20, top=12, right=20, bottom=12),
        shadow=ft.BoxShadow(blur_radius=12, color="#00000080", offset=ft.Offset(0, 3)),
        content=ft.Row(
            controls=[
                ft.Row(
                    controls=[
                        ft.FilledButton("Home", style=ft.ButtonStyle(bgcolor="#0D2B45", color="#FFFFFF", shape=ft.RoundedRectangleBorder(radius=8), overlay_color="#FF6B3588"), on_click=fade_transition(home), on_hover=button_hover, animate_scale=ft.Animation(150, "easeInOut"), scale=1.0),
                        ft.FilledButton("Timeline", style=ft.ButtonStyle(bgcolor="#0D2B45", color="#FFFFFF", shape=ft.RoundedRectangleBorder(radius=8), overlay_color="#FF6B3588"), on_click=fade_transition(timeline), on_hover=button_hover, animate_scale=ft.Animation(150, "easeInOut"), scale=1.0),
                        ft.FilledButton("GitHub", style=ft.ButtonStyle(bgcolor="#0D2B45", color="#FFFFFF", shape=ft.RoundedRectangleBorder(radius=8), overlay_color="#FF6B3588"), on_click=fade_transition(github), on_hover=button_hover, animate_scale=ft.Animation(150, "easeInOut"), scale=1.0),
                        ft.FilledButton("Certificates", style=ft.ButtonStyle(bgcolor="#0D2B45", color="#FFFFFF", shape=ft.RoundedRectangleBorder(radius=8), overlay_color="#FF6B3588"), on_click=fade_transition(certificates), on_hover=button_hover, animate_scale=ft.Animation(150, "easeInOut"), scale=1.0),
                        ft.FilledButton("Video", style=ft.ButtonStyle(bgcolor="#0D2B45", color="#FFFFFF", shape=ft.RoundedRectangleBorder(radius=8), overlay_color="#FF6B3588"), on_click=fade_transition(video), on_hover=button_hover, animate_scale=ft.Animation(150, "easeInOut"), scale=1.0),
                        ft.FilledButton("Technical Blog", style=ft.ButtonStyle(bgcolor="#0D2B45", color="#FFFFFF", shape=ft.RoundedRectangleBorder(radius=8), overlay_color="#FF6B3588"), on_click=fade_transition(blog), on_hover=button_hover, animate_scale=ft.Animation(150, "easeInOut"), scale=1.0),
                    ],
                    spacing=8
                ),
                ft.Row(
                    controls=[
                        ft.TextButton(
                            content=ft.Row([ft.Image(src=asset_path("LinkedIn.png"), width=18, height=18), ft.Text("LinkedIn", color="#FFFFFF", size=13)], spacing=4),
                            on_click=make_link_handler("https://www.linkedin.com/in/gehas-iimene-2463412a1/"),
                            on_hover=button_hover,
                            animate_scale=ft.Animation(150, "easeInOut"),
                            scale=1.0,
                        ),
                        ft.TextButton(
                            content=ft.Row([ft.Image(src=asset_path("gmail.png"), width=18, height=18), ft.Text("Email", color="#FFFFFF", size=13)], spacing=4),
                            on_click=make_link_handler("mailto:gehasiimene@gmail.com"),
                            on_hover=button_hover,
                            animate_scale=ft.Animation(150, "easeInOut"),
                            scale=1.0,
                        ),
                        ft.TextButton(
                            content=ft.Row([ft.Image(src=asset_path("OIP.webp"), width=18, height=18), ft.Text("Student Email", color="#FFFFFF", size=13)], spacing=4),
                            on_click=make_link_handler("mailto:224134949@students.unam.na"),
                            on_hover=button_hover,
                            animate_scale=ft.Animation(150, "easeInOut"),
                            scale=1.0,
                        ),
                    ],
                    spacing=8
                )
            ],
            alignment="spaceBetween"
        )
    )

    # --- UI Theme / Colors ---
    PRIMARY_COLOR = "#001F3F"
    WHITE = "#FFFFFF"
    ACCENT = "#FF6B35"
    page.bgcolor = "#040506"

    # --- Chat widget state & helpers ---
    chat_open = {"value": False}
    chat_position = {"value": "right"}
    chat_messages = ft.Column(spacing=8, scroll="auto")

    def add_bot_message(text: str):
        chat_messages.controls.append(
            ft.Container(
                content=ft.Text(text, color=PRIMARY_COLOR),
                padding=ft.Padding(10, 8, 10, 8),
                bgcolor=WHITE,
                border_radius=10,
                alignment=ft.alignment.center_right if False else None,
            )
        )

    def add_user_message(text: str):
        chat_messages.controls.append(
            ft.Container(
                content=ft.Text(text, color=WHITE),
                padding=ft.Padding(10, 8, 10, 8),
                bgcolor=PRIMARY_COLOR,
                border_radius=10,
            )
        )

    # Simple FAQ bot logic
    def bot_reply(user_text: str):
        text = user_text.lower()
        if "project" in text or "projects" in text:
            return "You can view my projects under the Projects/Video/GitHub sections — would you like me to open Projects?"
        if "about" in text or "education" in text or "skills" in text:
            return "I'm an Electrical Engineering student with experience in Python, Firebase, and mobile UIs. Ask me about specific projects!"
        if "contact" in text or "email" in text:
            return "You can contact me at gehasiimene@gmail.com or 224134949@students.unam.na"
        return "I can show Projects, About Me, or Contact. Try the quick replies below."

    def on_quick_reply(e, action: str):
        add_user_message(action)
        page.update()
        # small delay then bot reply
        def _reply():
            time.sleep(0.2)
            add_bot_message(bot_reply(action))
            page.update()
        threading.Thread(target=_reply, daemon=True).start()

    # Chat input
    chat_input = ft.TextField(hint_text="Type a message...", expand=True)

    def send_chat(e=None):
        txt = chat_input.value or ""
        if not txt.strip():
            return
        add_user_message(txt)
        chat_input.value = ""
        page.update()
        def _reply():
            time.sleep(0.25)
            add_bot_message(bot_reply(txt))
            page.update()
        threading.Thread(target=_reply, daemon=True).start()

    def close_chat(e):
        set_chat_visible(False)

    def set_chat_visible(visible: bool, update_ui: bool = True):
        chat_open["value"] = visible
        chat_floating.visible = visible
        if update_ui:
            page.update()

    def move_chat(e):
        if chat_position["value"] == "right":
            chat_position["value"] = "left"
            chat_floating.left = 20
            chat_floating.right = None
        else:
            chat_position["value"] = "right"
            chat_floating.right = 20
            chat_floating.left = None
        page.update()

    # Build chat panel
    chat_panel = ft.Container(
        width=340,
        height=420,
        bgcolor=WHITE,
        border_radius=12,
        shadow=ft.BoxShadow(blur_radius=20, color="#00000055"),
        padding=ft.Padding(12, 12, 12, 12),
        content=ft.Column(
            controls=[
                ft.Row([
                    ft.Text("Chat with Gehas", weight="bold", color=PRIMARY_COLOR),
                    ft.Row([
                        ft.IconButton(ft.icons.Icons.SWAP_HORIZ, icon_color=PRIMARY_COLOR, on_click=move_chat, tooltip="Move chat"),
                        ft.IconButton(ft.icons.Icons.CLOSE, icon_color=PRIMARY_COLOR, on_click=close_chat, tooltip="Minimize chat"),
                    ], spacing=0),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(),
                ft.Container(content=chat_messages, expand=True, padding=ft.Padding(0, 6, 0, 6)),
                ft.Row(
                    controls=[
                        ft.ElevatedButton("View Projects", on_click=lambda e: on_quick_reply(e, "View Projects"), bgcolor=PRIMARY_COLOR, color=WHITE),
                        ft.ElevatedButton("About Me", on_click=lambda e: on_quick_reply(e, "About Me"), bgcolor=PRIMARY_COLOR, color=WHITE),
                        ft.ElevatedButton("Contact Gehas", on_click=lambda e: on_quick_reply(e, "Contact Gehas"), bgcolor=PRIMARY_COLOR, color=WHITE),
                    ], spacing=6)
            ], spacing=8
        ),
    )

    # Splash overlay
    splash = ft.Container(
        expand=True,
        alignment=ft.alignment.center,
        bgcolor=PRIMARY_COLOR,
        content=ft.Column(
            controls=[
                ft.Text("Gehas Iimene", size=48, weight="bold", color=WHITE),
                ft.Text("Electrical Engineering Student", size=20, color=WHITE),
            ],
            alignment="center",
            horizontal_alignment="center",
            spacing=10,
        ),
        opacity=1,
        animate_opacity=ft.Animation(600, "easeInOut"),
    )

    # Build the main UI inside a Stack so we can overlay splash and a floating chatbox
    ui_column = ft.Column(
        controls=[
            navbar,
            ft.Container(content=content, padding=ft.Padding(left=30, top=20, right=30, bottom=30), expand=True),
        ],
        spacing=0,
        expand=True,
    )

    # Position the chat panel at bottom-right
    chat_floating = ft.Container(
        content=chat_panel,
        right=20,
        bottom=20,
        visible=False,
    )

    main_stack = ft.Stack(
        expand=True,
        controls=[
            ft.Container(
                expand=True,
                image=ft.DecorationImage(src=bg_image_path, fit=FIT_COVER),
            ),
            ft.Container(expand=True, bgcolor="#00000088"),
            ui_column,
            chat_floating,
            splash,
        ]
    )

    page.add(main_stack)

    # Show initial home content
    home(None)

    # Start splash fade-out and chat greeting in background threads
    def _start_entry_effects():
        # wait then fade out splash
        time.sleep(1.6)
        splash.opacity = 0
        page.update()
        time.sleep(0.65)
        splash.visible = False
        splash.hit_testable = False
        page.update()
        # initial chat greeting
        add_bot_message("Hi! Welcome to Gehas's portfolio — what can I help you with today?")
        page.update()

    threading.Thread(target=_start_entry_effects, daemon=True).start()


if __name__ == "__main__":
    # Start the Flet app (desktop/native view by default)
    ft.app(target=main)

