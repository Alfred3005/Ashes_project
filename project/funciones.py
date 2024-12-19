
#----------------------------------------------------------------------------------------------------------------------------------------------------------
def sign_in(self, name, username, description):
    # Verificar que los campos no estén vacíos y no sean igual a "_"
    if name.strip() == "" or name.strip() == "_" or \
            username.strip() == "" or username.strip() == "_" or \
            description.strip() == "" or description.strip() == "_":
        print("Por favor, complete todos los campos correctamente")
        return

    # Actualizar los valores del diccionario
    info["u_name"] = username
    info["name"] = name
    info["emotion_sc"] = 3

    # Guardar los cambios en el archivo JSON
    with open(DATA_FILE, "w") as file:
        json.dump(info, file)

    print('Nombre:', name)
    print('Nombre de usuario:', username)
    print("Tu escencia es:", description)
    print(info)

    self.root.current_screen.name = "main"

#---------------------------------------------------------------------------------------------------------------------------------------------------------------



def sd_gnrt(prompt, output_dir):
    """    #funcion generadora de imgenes."""
    from diffusers import AutoPipelineForText2Image
    import torch
    import os
    # Inicializar el pipeline si no está cargado
    if 'pipe' not in globals():
        global pipe
        pipe = AutoPipelineForText2Image.from_pretrained("stabilityai/sd-turbo", torch_dtype=torch.float16, variant="fp16")
        pipe.to("cuda")

    # Crear el directorio de salida si no existe
    os.makedirs(output_dir, exist_ok=True)

    # Generar la imagen
    image = pipe(prompt=prompt, num_inference_steps=1, guidance_scale=0.0).images[0]

    # Guardar la imagen
    file_name = "daily.png"
    image.save(os.path.join(output_dir, file_name))
    sentiment_score= a_sentimientos(prompt=prompt)

    return print(os.path.join(output_dir, file_name), sentiment_score, prompt)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------

def show_image_generated(image_source, prompt):
    """funcion que muestra la imagen generada"""
    from kivymd.uix.dialog import MDDialog
    from kivymd.uix.button import MDFlatButton
    from kivymd.uix.boxlayout import MDBoxLayout
    from kivy.uix.image import AsyncImage
    # Crear el contenido del diálogo
    content = create_image_content(image_source, prompt)

    # Crear el botón para cerrar el diálogo
    close_button = MDFlatButton(text='Cerrar')

    # Crear el diálogo
    dialog = MDDialog(
        title='Tu post',
        type="custom",
        content_cls=content,
        buttons=[close_button],
    )

    # Configurar la acción para cerrar el diálogo
    close_button.on_release = lambda: dialog.dismiss()

    # Mostrar el diálogo
    dialog.open()



def create_image_content(image_source, prompt):
    from kivymd.uix.label import MDLabel
    from kivymd.uix.boxlayout import MDBoxLayout
    from kivy.uix.image import Image
    box = MDBoxLayout(orientation='vertical')

    # Usar Image en lugar de AsyncImage
    image = Image(source=image_source, size_hint_y=0.7, allow_stretch=True)
    box.add_widget(image)

    prompt_label = MDLabel(text=prompt, size_hint_y=0.3)
    box.add_widget(prompt_label)

    return box

#------------------------------------------------------------------------------------------------------------------------------------------------

def a_sentimientos(prompt):
    from transformers import AutoTokenizer, AutoModelForSequenceClassification
    import torch

    tokenizer = AutoTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')

    model = AutoModelForSequenceClassification.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')

    tokens = tokenizer.encode(str(prompt), return_tensors='pt')

    result = model(tokens)

    result.logits

    score= int(torch.argmax(result.logits))+1

    return score





