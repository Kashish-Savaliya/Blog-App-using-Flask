import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flask_blog import mail

def save_picture(form_picture):
    random_hex= secrets.token_hex(8)
    # This function splits the filename without extension and only file extension
    _,f_ext = os.path.splitext(form_picture.filename)
    # this saves the picture with given random hex number with f_ext as extension
    picture_fn = random_hex + f_ext

    # Saves the picture to the current package specified by app.root_path and in the profile_pics folder in static folder
    picture_path = os.path.join(current_apps.root_path,'static/profile_pics',picture_fn)

    # This resizes the large image to given size and then saves the resized image in file system
    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(picture_path)

    return picture_fn

def send_reset_email(user):
    token = user.get_reset_token()
    # print(token)
    msg = Message('Password Reset Request',sender = 'noreply@domain.com', recipients=[user.email])
    # _external is set to true so that absolute URL is returned instead of a relative URL
    msg.body = f"""To reset your password, visit the following Link:
{url_for('users.reset_token',token=token,_external=True)}

If you did not make this request then simply ignore this email and no changes will be made"""
    mail.send(msg)

