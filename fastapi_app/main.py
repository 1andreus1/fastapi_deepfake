from fastapi import FastAPI

from deepfake_app.router import router

app = FastAPI(
    title='DeepFake'
)

app.include_router(
    router
)

