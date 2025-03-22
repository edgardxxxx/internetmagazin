from fastapi import FastAPI, Response
from fastapi.params import Depends 
from fastapi.staticfiles import StaticFiles 
from fastapi.middleware.cors import CORSMiddleware
import unicorn  
 
from router.adroyterhtml import routere
from router.html import index1
from tovar.operation import router
from texxt.test import test1
from tovar.panel import router as addindex
from auth.userproverka import routerp
from auth.user_tovar import user_korzina
  
app = FastAPI(
    title="Trading App"
)


app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/css", StaticFiles(directory="css"), name="css")
app.mount("/js", StaticFiles(directory="js"), name="js")


app.include_router(user_korzina)
app.include_router(routere)
app.include_router(index1)
app.include_router(router)  
app.include_router(addindex)
app.include_router(routerp)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
 
if __name__== "__main__":
    unicorn.run("main:app", reload=True)