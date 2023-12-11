from . import schemas
from fastapi import Depends, HTTPException, status, APIRouter, Response
import jwt
import os
from fastapi import File, UploadFile
from models import User, UserModel, History

def ChatGPT(path, name) -> bool: pass
def GigaChat(model_path, output_file_name, user_upload): pass
SECRET = 'allelleo'

def genearte_user_path_to_csv(username: str):
    work_dir = os.path.join('static', 'user_store')
    user_folder = os.path.join(work_dir, str(username))
    save_to = os.path.join(user_folder, 'train_files')
    print(save_to)
    return save_to 

controller = APIRouter()

@controller.post('/sign-up')
async def create_user(username: str, first_name: str, last_name:str, email: str, password:str):
    user = User(
        username=username,
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password
    )
    await user.save()
    work_dir = os.path.join('static', 'user_store')
    
    os.mkdir(os.path.join(work_dir, str(user.username)))
    
    user_folder = os.path.join(work_dir, str(user.username))
    
    folders = [
        'train_files', 'models', 'predict_files', 'predictions'
    ]
    for f in folders:
        os.mkdir(os.path.join(user_folder, f))
    
    
    return True


@controller.post('/sign-in')
async def login(username: str, password: str):
    user = await User.get(username=username)
    if user.password == password:
        return {"token": jwt.encode(
            {'user_id': user.id}, SECRET, algorithm='HS256'
        )}
    return None


@controller.get('/me')
async def me(token:str):
    user_id = jwt.decode(token, SECRET, algorithms=['HS256']).get('user_id')
    user = await User.get(id=user_id)
    return user

@controller.post('/create_model')
async def create_model(token: str, model_title:str, file: UploadFile = File(...), ):
    # TODO : check file is csv
    user_id = jwt.decode(token, SECRET, algorithms=['HS256']).get('user_id')
    user = await User.get(id=user_id)
    try:
        path_to_save = genearte_user_path_to_csv(user.username)
        
        contents = file.file.read()
        with open(f"{path_to_save}/{file.filename}", 'wb') as f:
            f.write(contents)
        
        model = await UserModel.create(
            title=model_title
        )
        await user.models.add(model)
        await user.save()
        
        res = ChatGPT(file_path=f"{path_to_save}/{file.filename}", model_name=model_title)
        return {
            'status': res
        }
        
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

    return {"message": f"Successfully uploaded {file.filename}"}

@controller.get('/inference')
async def inference(token: str, model_name:str, output_file_name: str, file: UploadFile = File(...)):
    user_id = jwt.decode(token, SECRET, algorithms=['HS256']).get('user_id')
    user = await User.get(id=user_id)
    
    try:
        path_to_save = os.path.join(genearte_user_path_to_csv(user.username), '..', 'predict_files')
        
        contents = file.file.read()
        with open(f"{path_to_save}/{file.filename}", 'wb') as f:
            f.write(contents)
        
        models = await user.models.all()
        current = None
        for model in models:
            if model.title == model_name:
                current = model
                break
        
        model_path = os.path.join('static', 'user_store',user.username, 'models', current.title)
        user_upload = f"{path_to_save}/{file.filename}"
        
        GigaChat(model_path, output_file_name, user_upload)
        
        h = History(model_name=model_name, output_file_name=output_file_name+'.csv', user_upload=user_upload)
        await h.save()
        await user.history.add(h)
        await user.save()
        
        return {
            'file': os.path.join('static', 'user_store',user.username, 'predictions', output_file_name+'.csv')
        }
        
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

    return {"message": f"Successfully uploaded {file.filename}"}

@controller.get('/reset_password')
async def reset_password(token: str, old_password:str, new_password:str):
    user_id = jwt.decode(token, SECRET, algorithms=['HS256']).get('user_id')
    user = await User.get(id=user_id)
    if user.password == old_password:
        user.password = new_password
        await user.save()
        return True
    return False

@controller.get('/history')
async def get_history(token: str):
    user_id = jwt.decode(token, SECRET, algorithms=['HS256']).get('user_id')
    user = await User.get(id=user_id)
    data = []
    
    history = await user.history.all()
    for his in history:
        data.append(await his.json())
    
    return data