import gradio as gr
import numpy as np

# Example for loading and displaying 3D mesh files
# def load_mesh(mesh_file_name):
#     return mesh_file_name

# demo = gr.Interface(
#     fn = load_mesh,
#     inputs=gr.Model3D(),
#     outputs=gr.Model3D(
#         clear_color=[0.0] * 4,
#         label="3D Model"
#     ),
#     examples=[
#         ['app/assets/models/Fox/Fox.glb']
#     ],
#     cache_examples=True
# )

# Multi input/output function
# def greet(name, is_morning, temperature):
#     salutation = "Good morning" if is_morning else "Good evening"
#     greeting = f"{salutation} {name}. It is {temperature} degrees today"
#     celsius = (temperature - 32) * 5 / 9
#     return greeting, round(celsius, 2)
# demo = gr.Interface(
#     fn = greet,
#     inputs = ["text", "checkbox", gr.Slider(0,100)],
#     outputs = ["text", "number"],
# )

def sepia(input_img):
    sepia_filter = np.array([
        [0.393, 0.769, 0.189], 
        [0.349, 0.686, 0.168], 
        [0.272, 0.534, 0.131]
    ])
    print('HIT!')
    sepia_img = input_img.dot(sepia_filter.T)
    sepia_img /= sepia_img.max()
    return sepia_img

demo = gr.Interface(
    fn=sepia, 
    inputs=[gr.Image(shape=(200,200))],
    outputs=["image"]
)

if __name__ == "__main__":
    demo.launch()   