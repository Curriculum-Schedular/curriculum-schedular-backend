from typing import List
from uuid import UUID, uuid4
from fastapi import FastAPI, HTTPException, File, UploadFile
from wrangler import CurriculumWrangler


app = FastAPI()


@app.get("/")
def root():
    return {"status": "OK"}


# Profile Page requests this endpoint to fetch courses taken by any given user
@app.get("/api/v1/users/{user_id}/taken-courses")
def get_taken_courses(user_id: str):
    return {user_id: "OK"}


# @app.post("/api/v1/users")
# async def register_user(user: User):
# db.append(user)
# return {"id": user.id}


# @app.delete("/api/v1/users/{user_id}")
# async def delete_user(user_id: UUID):
# for user in db:
#     if user.id == user_id:
#         db.remove(user)
#         return

# raise HTTPException(
#     status_code=404, detail=f"user with id: {user_id} does not exist"
# )


# @app.put("/api/v1/users/{user_id}")
# async def update_user(user_update: UserUpdateRequest, user_id: UUID):
#     for user in db:
#         if user.id == user_id:
#             if user_update.first_name is not None:
#                 user.first_name = user_update.first_name
#             if user_update.last_name is not None:
#                 user.last_name = user_update.last_name
#             if user_update.middle_name is not None:
#                 user.middle_name = user_update.middle_name
#             if user_update.roles is not None:
#                 user.roles = user_update.roles

#             return
#     raise HTTPException(
#         status_code=404, detail=f"user with id: {user_id} does not exist"
#     )


@app.post("/api/v1/upload-curriculum")
def upload_file(file: UploadFile = File(...)):
    # df = pd.read_csv(file.file)
    wrangler = CurriculumWrangler(file)
    wrangler.load_curriculum()
    print(file.filename)
    return wrangler.transform_curriculum()

    # file.file.close()
    # file_input = file.file.read()
    # file_input.save("local.xlsx")
    # return {"filename": file.filename}
