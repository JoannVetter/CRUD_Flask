from flask import Flask,render_template, request, redirect, url_for, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)

app.app_context().push()

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','mp4'}
app.config['SECRET_KEY'] = 'super secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://JJ578:superpassword@JJ578.mysql.pythonanywhere-services.com'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)

class File(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)

    def __repr__(self):
        return '<File %r>' % self.name

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET','POST'])
def index():
    
    if request.method == 'POST':
        try:
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                new_stuff = File(name=filename)
                db.session.add(new_stuff)
                db.session.commit()
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return redirect('/')

            #try:
 
        # check if the post request has the file part
            
            # If the user does not select a file, the browser submits an
            # empty file without a filename.

            return "Only txt, pdf and images are allowed"
        except:
            return "Something went wrong..."
    else:
        files = File.query.order_by(File.created_at).all()
        return render_template("index.html",files=files)

@app.route('/delete/<int:id>')
def delete(id):
    current_file = File.query.get_or_404(id)

    try:
        db.session.delete(current_file)
        db.session.commit()
        if os.path.exists(app.config['UPLOAD_FOLDER']+'/'+current_file.name):
            os.remove(app.config['UPLOAD_FOLDER']+'/'+current_file.name)
        return redirect('/')
    except:
        return "There was a problem deleting data"
    

@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    current_file = File.query.get_or_404(id)

    if request.method=='POST':

        try:
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                old_name = current_file.name
                current_file.name = filename
                db.session.commit()
                os.remove(app.config['UPLOAD_FOLDER']+'/'+old_name)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return redirect('/')

            #try:
 
        # check if the post request has the file part
            
            # If the user does not select a file, the browser submits an
            # empty file without a filename.

            return "Only txt, pdf and images are allowed"
        except Exception as e:
            return str(e)

    else:
        title='Update Data'
        return(render_template("update.html",title=title,current_file=current_file))

@app.route('/uploads/<name>')
def download_file(name):
        return send_from_directory(app.config["UPLOAD_FOLDER"],name)
    

if __name__ == '__main__':

    app.debug = False
    app.run()
