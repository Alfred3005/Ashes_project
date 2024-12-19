from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.uix.image import Image
from kivy.uix.image import AsyncImage

KV = '''
BoxLayout:
    orientation: 'vertical'
    MDRaisedButton:
        text: "Open Dialog"
        on_release: app.show_dialog()
'''

class MyApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def show_dialog(self):
        # Crear la imagen
        #image = Image(source='./project/imgs/add_button.png') # Reemplaza 'tu_imagen.jpg' con el nombre de tu archivo de imagen
        image = AsyncImage(source='./project/imgs/add_button.png')

        # Crear el cuadro de diálogo
        self.dialog = MDDialog(
            title="Título del cuadro de diálogo",
            type="custom",
            content_cls=image,
            buttons=[
                MDFlatButton(
                    text="CANCELAR", 
                    on_release=self.close_dialog
                ),
                MDFlatButton(
                    text="ACEPTAR", 
                    on_release=self.close_dialog
                ),
            ],
        )
        self.dialog.open()

    def close_dialog(self, *args):
        self.dialog.dismiss()

MyApp().run()
