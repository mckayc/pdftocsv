from flask import Flask, request, render_template, redirect, url_for, jsonify, send_file
import os
import fitz  # PyMuPDF
import csv
import io

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def parse_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    # Placeholder for grouping logic
    groups = {1: text[:100], 2: text[100:200]}  # Example groupings
    return groups

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'pdfFile' not in request.files:
        return jsonify(success=False, message='No file part')
    file = request.files['pdfFile']
    if file.filename == '':
        return jsonify(success=False, message='No selected file')
    if file and allowed_file(file.filename):
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        # Parse PDF and group elements
        groups = parse_pdf(file_path)
        # Save groups to session or database
        # Placeholder: save groups to a global variable
        global pdf_groups
        pdf_groups = groups
        return jsonify(success=True)
    return jsonify(success=False, message='File not allowed')

@app.route('/groups')
def groups():
    return render_template('groups.html', groups=pdf_groups)

@app.route('/export', methods=['POST'])
def export_csv():
    groups = request.json
    # Create CSV
    csv_buffer = io.StringIO()
    csv_writer = csv.writer(csv_buffer)
    headers = [groups[key] for key in sorted(groups.keys())]
    csv_writer.writerow(headers)
    # Example data rows
    data_rows = [['data1', 'data2'], ['data3', 'data4']]
    csv_writer.writerows(data_rows)
    csv_buffer.seek(0)
    return send_file(io.BytesIO(csv_buffer.read().encode('utf-8')),
                     mimetype='text/csv',
                     as_attachment=True,
                     attachment_filename='output.csv')

if __name__ == '__main__':
    app.run(debug=True)
