from email.message import Message
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, EmailField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired, EqualTo
import boto3

dynamodb=boto3.resource('dynamodb',aws_access_key_id = "AKIAZZLNU35XHUHRKG6M",aws_secret_access_key = "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",region_name="us-east-1")

from boto3.dynamodb.conditions import Key, Attr

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/files'
s3=boto3.client('s3',aws_access_key_id = "AKIAZZLNU35XHUHRKG6M",aws_secret_access_key = "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")

BUCKET_NAME = "hariuploadfile"
class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")
    email1 = EmailField("email1", validators=[InputRequired(message = 'Atleast one email id required')])
    email2 = EmailField("email2")
    email3 = EmailField("email3")
    email4 = EmailField("email4")
    email5 = EmailField("email5")

@app.route('/', methods=['GET',"POST"])
@app.route('/home', methods=['GET',"POST"])
def home():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data # First grab the file
        file_name = secure_filename(file.filename)
        table = dynamodb.Table('filedetails')
        email1 = form.email1.data
        email2 = form.email2.data
        email3 = form.email3.data
        email4 = form.email4.data
        email5 = form.email5.data
        
        table.put_item(
                Item={
                       'filename': file_name, 
                       'emails': [email1, email2, email3, email4, email5]
                       
                      }
        )
        
        
        file.save(file_name)
        s3.upload_file(Bucket=BUCKET_NAME, Filename=file_name, Key=file_name)   
        return "File has been uploaded."
    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)