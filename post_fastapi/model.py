from typing import Optional

from sqlmodel import Field, Session, SQLModel, create_engine, select
from post import Post

class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int] = None

hero1 = Hero(name="aaa", secret_name="AAA")
hero2 = Hero(name="bbb", secret_name="BBB")
hero3 = Hero(name="CCC", secret_name="CCC")

post1 = Post(id=2, user="user1", title="title", content="ldskfjlkjse")

engine = create_engine("sqlite:///database.db")

# SQLModel.metadata.create_all(engine)

# with Session(engine) as session:
#     session.add(post1)
#     session.commit()


with Session(engine) as session:
    session.add(post1)
    session.commit()

    statement = select(Post)
    hero = session.exec(statement).all()
    print(hero)