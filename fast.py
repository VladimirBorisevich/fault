from fastapi import FastAPI
from fastapi.responses import FileResponse
import os
import uvicorn
from glob import glob
from main import load_plot

picture_path = load_plot()
app = FastAPI()


@app.get("/")
def main():
    print(picture_path)
    return FileResponse(glob(os.path.join('pics/', '*.png'))[0])


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
