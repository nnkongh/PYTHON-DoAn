import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from blog import mail

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _,f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path,'static/myAva',picture_fn)
    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    
    return picture_fn

def send_reset_email(user):
    from blog import mail
    token = user.get_reset_token()
    msg = Message('Gửi yêu cầu reset mật khẩu',sender='haukong1308@gmail.com',recipients=[user.email])
    msg.body = f'''ĐỂ RESET MẬT KHẨU, HÃY ẤN VÀO LINK NÀY: {url_for('users.reset_token',token = token, _external=True)}
    NẾU KHÔNG GỬI YÊU CẦU THÌ MẬT KHẨU SẼ KHÔNG ĐƯỢC THAY ĐỔI
    '''
    mail.send(msg)
