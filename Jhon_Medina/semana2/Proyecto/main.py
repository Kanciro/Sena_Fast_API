from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from models import UserCreate, UserResponse, TaskBase
from datetime import datetime

app = FastAPI(title="Mi Primera API")

db_users = {}
user_id_counter = 0

@app.get("/")
def hello_world() -> dict:
    return {"message": "¡Mi primera API FastAPI!"}

app = FastAPI(title="Mi Primera API")

# Simulación de base de datos en memoria
db_users = {}
user_id_counter = 0

@app.get("/")
def hello_world() -> dict:
    """Retorna un mensaje de bienvenida."""
    return {"message": "¡Mi primera API FastAPI!"}



@app.post("/users", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate):
    global user_id_counter
    
    if any(u['email'] == user.email for u in db_users.values()):
        raise HTTPException(status_code=400, detail="Email already registered")

 
    user_id_counter += 1
    new_user_data = user.model_dump()
    new_user_data["id"] = user_id_counter
    new_user_data["registration_date"] = datetime.now()
    
 
    db_users[user_id_counter] = new_user_data

    return UserResponse(**new_user_data)


@app.get("/users", response_model=list[UserResponse])
async def list_users():
    return [UserResponse(**user) for user in db_users.values()]


@app.get("/users/{user_id}", response_model=UserResponse)
async def search_user_id(user_id:int):
    user = db_users.get(user_id)
    return UserResponse(**user)

@app.put("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user: UserCreate):
    if user_id not in db_users:
        raise HTTPException(status_code=404, detail="User not found")
    updated_user_data = user.model_dump()
    updated_user_data["id"] = user_id
    updated_user_data["registration_date"] = db_users[user_id]["registration_date"]
    db_users[user_id] = updated_user_data
    return UserResponse(**updated_user_data)



@app.patch("/users/{user_id}", response_model=UserResponse)
async def actualizar_usuario_parcial(user_id:int, user: UserCreate):
    if user_id not in db_users:
        raise HTTPException(status_code=404, detail="no se encontro el usuario")
    usuario_existente = db_users[user_id]
    usuario_existente.update(user.model_dump(exclude_unset=True))
    db_users[user_id] = usuario_existente
    return UserResponse(**usuario_existente)

@app.delete("/users/{user_id}", response_model=UserResponse)
async def eliminat_usuario(user_id :int):
    if user_id not in db_users:
        raise HTTPException(status_code=404, detail="User not found")
    deleted_user = db_users.pop(user_id)
    return UserResponse(**deleted_user)

@app.get("/users/search", response_model=UserResponse)
async def search_user(email: Optional[str], name: Optional[str]):
    for user in db_users.values():
        if (email and user["email"] == email) or (name and user["name"]== name):
            return UserResponse(**user)

@app.get("/users/{user_id}/tasks", response_model=UserResponse)
async def get_user_tasks(user_id: int):
    """Retorna las tareas asignadas a un usuario específico."""
    if user_id not in db_users:
        raise HTTPException(status_code=404, detail="User not found")

    tasks = [task_id for task_id, task in TaskBase.items() if task["assigned_to"] == user_id]
    return {"user_id": user_id, "tasks": tasks}

@app.patch("/users/{user_id}/lasrt_access")
async def update_last_access(user_id: int):
    if user_id not in db_users:
        raise HTTPException(status_code=404, detail="User not found")
    db_users[user_id]["last_access"] = datetime.now()
    return {"message": "Last access updated successfully", "user_id": user_id} 




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)