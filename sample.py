# from pydantic import BaseModel
# from uuid import UUID, uuid4

# class SuperHero(BaseModel):
#     id: UUID = uuid4()
#     alias: str
#     name: str
#     rating: int

# data = [
#     {'alias':'Spider-Man','name':'Peter Parker','rating':10},
#     {'alias':'Spider-Woman','name':'Jessica Drew','rating':10},
#     {'alias':'Agent Venom','name':'Eddie Brock','rating':9},
#     {'alias':'Dr. Strange','name':'Stephan Strange','rating':9}
# ]

# ROSTER = { h['alias']: SuperHero(**h) for h in data}
# print(ROSTER)
from pydantic import BaseModel
from uuid import UUID, uuid4

class SuperHero(BaseModel):
    id: UUID
    alias: str
    name: str
    rating: int

data = [
    {'alias':'Spider-Man','name':'Peter Parker','rating':10},
    {'alias':'Spider-Woman','name':'Jessica Drew','rating':10},
    {'alias':'Agent Venom','name':'Eddie Brock','rating':9},
    {'alias':'Dr. Strange','name':'Stephan Strange','rating':9}
]

ROSTER = {}
for h in data:
    sh_id = uuid4()
    ROSTER[sh_id] = SuperHero(id=sh_id,**h)