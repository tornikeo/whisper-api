from typing import Union
from fastapi import FastAPI
import gradio as gr
from starlette.responses import RedirectResponse
import os
from uuid import uuid4
import uvicorn

CUSTOM_PATH = "/gradio"

app = FastAPI()


def gradio_fn(webcam_video_path = None, upload_video_path = None):
    video_path = upload_video_path if upload_video_path is not None else webcam_video_path
    assert video_path is not None
    # output_video_path = NamedTemporaryFile(suffix=".mp4", delete=False).name
    os.makedirs("workdir",exist_ok=True)
    output_video_path = f"workdir/video_{str(uuid4())[:8]}.mp4"
    stats = run_inference(video_path, output_video_file_path=output_video_path)
    final_count, confidence, pred_period, infer_time, running_counts = stats
    return final_count, confidence, output_video_path


io = gr.Interface(
    fn = gradio_fn,
    inputs=[
        gr.Video(label="Repeating webcam video", source="webcam", format="mp4", mirror_webcam=False,),
        gr.Video(label="Repeating uploaded video", source="upload", format="mp4", mirror_webcam=False,),
    ],
    outputs=[
        gr.Number(label="Repetition Count", precision=0),
        gr.Number(label="Confidence Score", precision=3), 
        gr.Video(label="Video with counter", format="mp4"),
    ],
    examples=[ 
        [ "assets/repnet/jumping_jacks.mp4", "assets/jumping_jacks.mp4",],
        [ "assets/pull_ups.mp4", "assets/pull_ups.mp4",],
    ],
    cache_examples=True,
)
gradio_app = gr.routes.App.create_app(io)

app.mount(CUSTOM_PATH, gradio_app)

@app.get("/")
def redirect():
    # url = app.url_path_for("/gradio")
    response = RedirectResponse(url="/gradio")
    return response

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)