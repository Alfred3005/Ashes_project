from char.main_c.Friends import amigos

from kivymd.uix.imagelist import MDSmartTile
from kivymd.uix.button import MDIconButton
from kivy.uix.label import Label
from kivy.utils import get_color_from_hex

import os



def show_image_dialog(image_source, text_content, chat_logs):
    from kivy.uix.popup import Popup
    from kivy.uix.button import Button
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.image import AsyncImage
    from kivy.uix.textinput import TextInput
    from kivy.uix.label import Label
    from kivy.app import App

    """ Mostrar un cuadro de diálogo con una imagen y un texto.
    """

    # Crear el contenido del cuadro de diálogo
    box = BoxLayout(orientation='vertical')

    # Añadir la imagen al cuadro de diálogo
    image = AsyncImage(source=image_source, size_hint_y=0.7, allow_stretch=True)
    box.add_widget(image)

    # Añadir el campo de texto al cuadro de diálogo
    input_field = TextInput(size_hint_y=0.2, hint_text="Enter your text here")
    box.add_widget(input_field)

    # Añadir el botón de envío al cuadro de diálogo
    send_button = Button(text="SEND", size_hint_y=0.1)
    box.add_widget(send_button)

    # Crear el cuadro de diálogo con el contenido definido
    popup = Popup(title=text_content, content=box, size_hint=(0.9, 0.9), separator_color=(1, 0.5, 0, 1))

    # Función para guardar el texto y cerrar el cuadro de diálogo
    def save_text_and_close(instance):
        if input_field.text.strip():
            respuesta_historia = input_field.text
            chat_logs.add_widget(Label(text=respuesta_historia))
            # Cambiar a la pantalla ChatScreen
            app_instance = App.get_running_app()
            app_instance.root.current = 'chatroom'
        popup.dismiss()

    send_button.bind(on_release=save_text_and_close)

    popup.open()
def historias(r_historias, dia, chat_logs):  # Agregamos chat_logs como argumento
    pos_h_horizontal = 0.4
    for amigo in amigos:
        widget = MDSmartTile(
            radius=24,
            box_radius=[0, 0, 24, 24],
            box_color=[0, 1, 0, 0],
            source=amigos[amigo] + "/avatar.jpeg",
            pos_hint={"center_x": pos_h_horizontal, "center_y": 0.5},
            size_hint=(None, None),
            size=("50dp", "50dp"),
        )
        pos_h_horizontal += 0.23

        # Llamar a show_image_dialog al liberar el widget
        image_source = amigos[amigo] + "/Days/"+str(dia)+"/post.jpg"
        text_content = "Oink <3"
        widget.bind(on_release=lambda instance, src=image_source: show_image_dialog(src, text_content, chat_logs))

        r_historias.add_widget(widget)

        # Add a label for the username
        label = Label(
            text=amigo,
            pos_hint={"center_x": pos_h_horizontal - 0.22, "center_y": 0.15},
            font_size=10
        )
        r_historias.add_widget(label)


def feed(r_feed, dia):
    directorio = "/app/project/days/" + str(dia)
    archivos = os.listdir(directorio)
    archivos_jpeg = [archivo for archivo in archivos if archivo.endswith(".jpeg")]

    def toggle_heart_icon(instance):
        if instance.icon == "heart-outline":
            instance.icon = "heart"
        else:
            instance.icon = "heart-outline"

    for imagen in archivos_jpeg:
        ruta_imagen = os.path.join(directorio, imagen)
        widget = MDSmartTile(
            radius=24,
            box_radius=[0, 0, 24, 24],
            box_color=get_color_from_hex("#d86200"),
            pos_hint= {'center_x': 0.5},
            size_hint=(None, None),
            size=("280dp", "320dp"),
            overlap=False,
            source=ruta_imagen
        )

#Widget---------------------------------------------------------------------------------------------------------------
        button1 = MDIconButton(
            icon="heart-outline",
            theme_icon_color="Custom",
            icon_color=(1, 0, 0, 1),
            pos_hint={"center_y": 0.5, "center_x": 0.2}
        )
        button1.bind(on_release=toggle_heart_icon)
        widget.add_widget(button1)

        button2 = MDIconButton(
            icon="heart-outline",
            theme_icon_color="Custom",
            icon_color=(1, 0, 0, 1),
            pos_hint={"center_y": 0.5, "center_x": 0.5}
        )
        button2.bind(on_release=toggle_heart_icon)
        widget.add_widget(button2)

        button3 = MDIconButton(
            icon="heart-outline",
            theme_icon_color="Custom",
            icon_color=(1, 0, 0, 1),
            pos_hint={"center_y": 0.5, "center_x": 0.7}
        )
        button3.bind(on_release=toggle_heart_icon)
        widget.add_widget(button3)

        button4 = MDIconButton(
            icon="heart-outline",
            theme_icon_color="Custom",
            icon_color=(1, 0, 0, 1),
            pos_hint={"center_y": 0.5, "center_x": 0.9}
        )
        button4.bind(on_release=toggle_heart_icon)
        widget.add_widget(button4)

        label = Label(
            text="plz",
            bold=True,
            color=(1, 1, 1, 1)
        )
        widget.add_widget(label)


        r_feed.add_widget(widget)

# ----------------------------------------------------------------------------------------------------------------------

def post_display(p_feed, dia):
    from funciones import a_sentimientos
    directorio = "./project/char/main_c/Days/" + str(dia)  
    archivos = os.listdir(directorio)
    archivos_jpeg = [archivo for archivo in archivos if archivo.endswith(".png")]

    def toggle_heart_icon(instance):
        if instance.icon == "heart-outline":
            instance.icon = "heart"
        else:
            instance.icon = "heart-outline"

    for imagen in archivos_jpeg:
        ruta_imagen = os.path.join(directorio, imagen)
        widget = MDSmartTile(
            radius=24,
            box_radius=[0, 0, 24, 24],
            box_color=get_color_from_hex("#d86200"),
            pos_hint= {'center_x': 0.5},
            size_hint=(None, None),
            size=("280dp", "320dp"),
            overlap=False,
            source=ruta_imagen
        )

#Widget---------------------------------------------------------------------------------------------------------------
        button1 = MDIconButton(
            icon="heart-outline",
            theme_icon_color="Custom",
            icon_color=(1, 0, 0, 1),
            pos_hint={"center_y": 0.5, "center_x": 0.2}
        )
        button1.bind(on_release=toggle_heart_icon)
        widget.add_widget(button1)

        button2 = MDIconButton(
            icon="heart-outline",
            theme_icon_color="Custom",
            icon_color=(1, 0, 0, 1),
            pos_hint={"center_y": 0.5, "center_x": 0.5}
        )
        button2.bind(on_release=toggle_heart_icon)
        widget.add_widget(button2)

        button3 = MDIconButton(
            icon="heart-outline",
            theme_icon_color="Custom",
            icon_color=(1, 0, 0, 1),
            pos_hint={"center_y": 0.5, "center_x": 0.7}
        )
        button3.bind(on_release=toggle_heart_icon)
        widget.add_widget(button3)

        button4 = MDIconButton(
            icon="heart-outline",
            theme_icon_color="Custom",
            icon_color=(1, 0, 0, 1),
            pos_hint={"center_y": 0.5, "center_x": 0.9}
        )
        button4.bind(on_release=toggle_heart_icon)
        widget.add_widget(button4)

        label = Label(
            text="plz",
            bold=True,
            color=(1, 1, 1, 1)
        )
        widget.add_widget(label)


        p_feed.add_widget(widget)
        






