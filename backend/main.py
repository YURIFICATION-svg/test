from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from containers import Container
from database import init_db
from user.interface.controllers.user_controller import router as user_routers
from message.interface.controllers.message_controller import router as message_routers


app = FastAPI()
app.container = Container()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yurification-svg.github.io"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

containers.wire(
    modules=[
        user.interface.controllers,user_controller,
        message.interface.controllers,message_controller,
    ]
)

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(user_routers)
app.include_router(message_routers)
