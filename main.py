from fastapi import FastAPI,HTTPException,Query,Path
from pydantic import BaseModel
import json
app = FastAPI()
class Student(BaseModel):
    name:str
    age:int
    language:str
    city:str
    marks:int
@app.get('/')
def retrieve():
    return {'message':'Data Loaded Successfully'}
@app.get('/student')
def retrieve_data():
    with open('students.json','r') as file:
        data = json.load(file)
    return data
@app.get('/student/{student_id}')
def retrieve_id(student_id:int):
    with open('students.json','r') as file:
        students = json.load(file)
    for student in students:
        if student['id'] == student_id:
            return student
        raise HTTPException(status_code=404,detail='Student not found')
@app.get('/student/language/{student_language}')
def retrieve_language(student_language:str):
    with open('students.json','r') as file:
        students = json.load(file)
    for student in students:
        if student['language'].lower() == student_language.lower():
            return student
        raise HTTPException(status_code=404,detail='Student not found')

@app.get('/student/language/city/')
def retrieve_language(language: str, city: str):
    with open('students.json', 'r') as file:
        students = json.load(file)

    for student in students:
        if student['language'] == language and student['city'] == city:
            return student

    raise HTTPException(
        status_code=404,
        detail='User Not Found'
    )
@app.delete('/student/delete/{student_id}')
def remove_student(student_id:int):
    with open('students.json', 'r') as file:
        students = json.load(file)
        for student in students:
            if student['id'] == student_id:
                students.remove(student)
                with open('students.json', 'w') as file:
                    json.dump(students,file,indent=4)
                return{
                    'message':'Student deleted successfully',
                    'deleted_student':student
                }
        raise HTTPException(status_code=404,detail='Student not found')
@app.post('/student/')
def create_student(student:Student):
    with open('students.json', 'r') as file:
        students = json.load(file)
    for student in students:
        if student['id'] == student.id:
            raise HTTPException(status_code=404,detail='User Already exist')
        students.append(student.model_dump())
        with open('students.json', 'w') as file:
            json.dump(students,file,indent=4)
            return{
                    'message':'Student Added successfully',
                    'student':student
                        }
@app.put('/student_update/{student_id}')
def update_student(student_id:int,student:Student):
    with open('students.json', 'r') as file:
        students = json.load(file)
    for student in students:
        if student['id'] == student_id:
            student['name'] = student.name
            student['age'] = student.age
            student['marks'] = student.marks
            student['city'] = student.city
            student['language'] = student.language
            with open('students.json', 'w') as file:
                json.dump(students,file,indent=4)
            return{
                    'message':'Student Updated successfully',
                    'student':student
                        }
class Student(BaseModel):
    name: str | None = None
    language: str | None = None
    city: str | None = None


@app.patch('/student/{student_id}')
def patch_student(student_id: int, student: Student):

    with open('students.json', 'r') as file:
        students = json.load(file)

    for s in students:
        if s['id'] == student_id:

            update_data = student.model_dump(exclude_unset=True)

            s.update(update_data)

            with open('students.json', 'w') as file:
                json.dump(students, file, indent=4)

            return {
                "message": "Student patched successfully",
                "student": s
            }

    raise HTTPException(
        status_code=404,
        detail="Student not found"
    )


from typing import Literal
@app.get('/student/order/')
def order_student(
    sort_by: Literal['name', 'age', 'language', 'marks'] = Query('marks'),
    order: Literal['asc', 'desc'] = Query('asc')
):
    with open('students.json', 'r') as file:
        students = json.load(file)

    sorted_students = sorted(
        students,
        key=lambda s: s[sort_by].lower() if isinstance(s[sort_by], str)
        else s[sort_by],
        reverse=(order == 'desc')
    )

    return sorted_students



            




    
