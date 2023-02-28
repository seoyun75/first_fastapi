from inmemory import NoticeDB
from notice import Notice
from fastapi import FastAPI
 
app = FastAPI()

@app.get("/")
async def root():
    notice_list = NoticeDB()
    print(notice_list.notice_list)
    return {"message" : "Hello"}

@app.post("/create_notice")
async def create_notice(notice : Notice):
    notice_list = NoticeDB().notice_list
    notice_list[len(notice_list)+1] = notice
    return notice

@app.get("/get_list")
async def get_list():
    
    return NoticeDB().notice_list

@app.get("/get_notice/{id}")
async def get_notice(id:int):
    return NoticeDB().notice_list[id]
