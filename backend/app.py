from flask import Flask, request, jsonify, session, send_from_directory, abort
from flask_cors import CORS
import datetime
import json
from modules.ai import check_use_case, check_regulation_objects, check_regulations
from modules.utils import extract_text_from_docx, extract_text_from_pdf, save_to_file, generate_and_return_files, generate_excel_report
import docx
import PyPDF2
import os

app = Flask(__name__, static_folder='dist')
CORS(app, supports_credentials=True, origins=["http://localhost:5174", "http://localhost:3000", "http://localhost:5173"])

# Путь для сохранения временных файлов
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

TEMP_FOLDER = 'temp'
app.config['TEMP_FOLDER'] = TEMP_FOLDER
os.makedirs(TEMP_FOLDER, exist_ok=True)

# Функция для создания пути к папке с данными по файлу
def get_file_folder(user_id, file_name):
    user_folder = os.path.join(app.config['TEMP_FOLDER'], user_id)
    file_folder = os.path.join(user_folder, file_name)
    os.makedirs(file_folder, exist_ok=True)
    return file_folder

@app.route("/home/")
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/temp/<path:filename>')
def download_report(filename):
    try:
        # Возвращаем файл с заголовком, указывающим, что это файл для скачивания
        return send_from_directory(TEMP_FOLDER, filename, as_attachment=True)
    except FileNotFoundError:
        abort(404)

@app.route('/api/check-use-case', methods=['POST'])
def check_use_case_endpoint():
    data = request.get_json()
    text = data.get('text')
    user_id = data.get('user_id')
    file_name = data.get('file_name')
        
    if not text or not user_id:
        return jsonify({"error": "Введите текст требований для анализа."}), 400
    
    try:
        # Путь к папке с данными по файлу
        file_folder = get_file_folder(user_id, file_name)
        
        print('file_folder', file_folder)

        # Анализируем use case
        res = check_use_case(text)
        
        # Сохраняем результат во временный файл
        save_to_file(file_folder, 'use_case.txt', res)

        # Генерация файлов и возвращение ссылок и текста
        docx_url, pdf_url, full_text = generate_and_return_files(file_folder, user_id)

        return jsonify({
            "docx_url": docx_url,
            "pdf_url": pdf_url,
            "full_text": res
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/check-regulation-objects', methods=['POST'])
def check_regulation_objects_endpoint():
    data = request.get_json()
    text = data.get('text')
    user_id = data.get('user_id')
    file_name = data.get('file_name')
        
    if not text or not user_id:
        return jsonify({"error": "Введите текст требований для анализа."}), 400
    
    try:
        # Путь к папке с данными по файлу
        file_folder = get_file_folder(user_id, file_name)

        # Анализируем объекты регулирования
        res = check_regulation_objects(text)
        print('res', res)
        
        # Сохраняем результат во временный файл
        save_to_file(file_folder, 'regulation_objects.txt', res)

        # Генерация файлов и возвращение ссылок и текста
        docx_url, pdf_url, full_text = generate_and_return_files(file_folder, user_id)

        return jsonify({
            "docx_url": docx_url,
            "pdf_url": pdf_url,
            "full_text": res
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/check-regulations', methods=['POST'])
def check_regulations_endpoint():
    data = request.get_json()
    text = data.get('text')
    user_id = data.get('user_id')
    file_name = data.get('file_name')
        
    if not text or not user_id:
        return jsonify({"error": "Введите текст требований для анализа."}), 400
    
    try:
        # Путь к общей папке пользователя
        user_folder = os.path.join(app.config['TEMP_FOLDER'], user_id)
        os.makedirs(user_folder, exist_ok=True)

        # Путь к папке с данными по файлу (для хранения результатов анализа)
        file_folder = get_file_folder(user_id, file_name)

        # Анализируем регламенты
        final_response, itog = check_regulations(text)

        # Структура данных для отчета Excel
        report_data = [
            [file_name, itog[0], itog[1], itog[2], final_response]  # Статус, кол-во соблюденных и несоблюденных регламентов
        ]

        # Генерация Excel-файла в общей папке пользователя
        excel_file_name = 'report.xlsx'
        generate_excel_report(user_folder, excel_file_name, report_data)

        # Генерация файлов (DOCX и PDF) в папке конкретного файла
        docx_url, pdf_url, full_text = generate_and_return_files(file_folder, user_id)

        return jsonify({
            "docx_url": docx_url,
            "pdf_url": pdf_url,
            "excel_url": f"/temp/{user_id}/{excel_file_name}",  # Корректируем ссылку на Excel-файл
            "full_text": final_response
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Эндпоинт для загрузки и обработки файлов
@app.route('/api/upload-file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "Файл не найден в запросе"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Не указан файл для загрузки"}), 400
    
    file_ext = os.path.splitext(file.filename)[1].lower()
    
    if file_ext not in ['.docx', '.pdf']:
        return jsonify({"error": "Поддерживаются только файлы PDF и DOCX"}), 400
    
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)
    
    try:
        if file_ext == '.docx':
            text = extract_text_from_docx(file_path)
        elif file_ext == '.pdf':
            text = extract_text_from_pdf(file_path)
        
        # Здесь можно передать текст для дальнейшей обработки
        return jsonify({"text": text})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        # Удаление файла после обработки
        if os.path.exists(file_path):
            os.remove(file_path)
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)