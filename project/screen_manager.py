#export DISPLAY=host.docker.internal:0.0

import json
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.uix.label import Label


from kivy.factory import Factory
import datetime


# Importar la función historias desde el archivo widgets.py
from widgets import historias, feed, post_display

Window.size = (300, 500)
# Definir la ubicación del archivo de datos
DATA_FILE = "/app/project/char/main_c/info.json"

# Verificar si el archivo existe y cargar los datos
try:
    with open(DATA_FILE, "r") as file:
        info = json.load(file)
except FileNotFoundError:
    fecha_hora_actual = datetime.datetime.now()
    info = {"u_name": "_", "name": "", "emotion_sc": 0, "i_date": ""}
    fecha_inicial = fecha_hora_actual.date()


# Obtener la fecha y hora actual
fecha_hora_actual = datetime.datetime.now()


# Leer la fecha inicial del diccionario
fecha_inicial_str = info.get("i_date", "")

# Comprobar si la cadena de fecha inicial está vacía
if fecha_inicial_str:
    # Convertir la cadena de texto en un objeto datetime.date si no está vacía
    i_date = datetime.datetime.strptime(fecha_inicial_str, "%Y-%m-%d").date()
else:
    # Si está vacía, usar la fecha actual como fecha inicial
    i_date = datetime.datetime.now().date()


fecha_actual = fecha_hora_actual.date()
hora_actual = fecha_hora_actual.time()
dia_actual = (fecha_actual - i_date).days + 1

# Definir el contenido del archivo kv
Builder.load_file("screens.kv")


class MyScreenManager(ScreenManager):
    pass

class SignInScreen(Screen):
    pass

class PostScreen(Screen):
    def on_enter(self):
        post_display(self.ids.p_feed, dia=dia_actual)


class MainScreen(Screen):
    def on_enter(self):
        with open(DATA_FILE, "r") as file:
            info = json.load(file)


        print(dia_actual)
        print(hora_actual)
        #agregamos los creadores de widgets
        chat_logs = App.get_running_app().root.get_screen('chatroom').ids.chat_logs
        historias(self.ids.r_historias, dia=dia_actual, chat_logs=chat_logs)
        feed(self.ids.r_feed , dia= dia_actual)

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, BooleanProperty


class ChatMessageBubble(BoxLayout):
    sent_by_user = BooleanProperty(False)
    text = StringProperty('')

class ChatScreen(Screen):
    ChatMessageBubble = Factory.ChatMessageBubble

    def add_message_to_chat(self, message):
        # Esta función añade un mensaje al chat_logs layout
        self.ids.chat_logs.add_widget(Label(text=message))

    def send_message(self):
        # Get the message from the TextInput
        message = self.ids.message_input.text

        # If there's a message, add it to the chat logs and clear the TextInput
        if message.strip():
            user_bubble = ChatMessageBubble(sent_by_user=True,
                                            text=message)  # Create a ChatMessageBubble for the user's message
            self.ids.chat_logs.add_widget(user_bubble)  # Add the user's message bubble to chat_logs

            # Add the sample response after the user's message
            sample_bubble = ChatMessageBubble(sent_by_user=False,
                                              text="Sample message")  # Create a ChatMessageBubble for the sample message
            self.ids.chat_logs.add_widget(sample_bubble)  # Add the sample message bubble to chat_logs

            self.ids.message_input.text = ""  # Clear the TextInput


from funciones import sd_gnrt
class MyApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "DeepOrange"
        self.theme_cls.theme_style = "Dark"
        screen_manager = MyScreenManager()
        screen_manager.add_widget(SignInScreen(name="signin"))
        screen_manager.add_widget(MainScreen(name="main"))
        screen_manager.add_widget(ChatScreen(name="chatroom"))
        screen_manager.add_widget(PostScreen(name='post_screen'))

        if info["u_name"] == "_":
            screen_manager.current = "signin"
        else:
            screen_manager.current = "main"

        return screen_manager

    def sign_in(self, name, username, description):
        # Verificar que los campos no estén vacíos y no sean igual a "_"
        if name.strip() == "" or name.strip() == "_" or \
                username.strip() == "" or username.strip() == "_" or \
                description.strip() == "" or description.strip() == "_":
            print("Por favor, complete todos los campos correctamente")
            return
        else:
            # Actualizar los valores del diccionario
            info["u_name"] = username
            info["name"] = name
            info["emotion_sc"] = 3
            info["i_date"]= str(fecha_inicial)

            # Guardar los cambios en el archivo JSON
            with open(DATA_FILE, "w") as file:
                json.dump(info, file)

            print('Nombre:', name)
            print('Nombre de usuario:', username)
            print("Tu escencia es:", description)
            print(info)


            self.root.current= "main"
    dialog = None
    text_field = None

    def switch_to_main(self):
        self.root.current = "main"

    def show_dialog(self):
        import os

        # Construir la ruta del archivo
        daily_image_path = os.path.join("./project/char/main_c/Days", str(dia_actual), "daily.png")

        # Verificar si el archivo daily.png existe
        if os.path.exists(daily_image_path):
            # Si existe, cambia a la ventana PostScreen
            screen_manager = App.get_running_app().root
            screen_manager.current = 'post_screen'

            # Obtener una referencia a PostScreen
            post_screen = screen_manager.get_screen('post_screen')

            # Actualizar el widget en PostScreen que mostrará la imagen
            post_screen.ids.p_feed.source = daily_image_path
        else:
            # Si no existe, muestra el diálogo como estaba predeterminado
            if not self.dialog:
                self.text_field = MDTextField()
                box = MDBoxLayout(orientation='vertical')
                box.add_widget(self.text_field)
                self.dialog = MDDialog(
                    title='IMAGINA',
                    type="custom",
                    content_cls=box,
                    buttons=[
                        MDFlatButton(
                            text='CANCEL',
                            on_release=lambda obj: self.close_dialog()
                        ),
                        MDFlatButton(
                            text='OK',
                            on_release=lambda obj: self.save_input(obj)
                        )
                    ],
                )
            self.dialog.open()

    def close_dialog(self):
        if self.dialog:
            self.dialog.dismiss()




#------------------------------------------------------------------------------------------------------------------------------------------------

    def save_input(self, obj):
        import os
        
        h_prompt = self.text_field.text

        # Construir la ruta de salida usando os.path.join
        output_dir = os.path.join("/app/project/char/main_c/Days", str(dia_actual))
        sd_gnrt(h_prompt, output_dir=output_dir)

        # Asumiendo que la imagen se guarda en image_path
        image_path = os.path.join(output_dir, "daily.png")

        # Obtener una referencia al ScreenManager de tu aplicación
        screen_manager = App.get_running_app().root

        # Cambiar a la ventana PostScreen
        screen_manager.current = 'post_screen'

        # Obtener una referencia a PostScreen
        post_screen = screen_manager.get_screen('post_screen')

        # Aquí, necesitas actualizar el widget en PostScreen que mostrará la imagen.
        # Esto depende de cómo hayas estructurado PostScreen y sus widgets.
        # Por ejemplo, si tienes un widget Image con id 'image_widget' en PostScreen, podrías hacer:
        post_screen.ids.p_feed.source = image_path
        

        self.close_dialog()
            
MyApp().run()

