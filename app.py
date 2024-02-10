
# app.py

from flask import Flask, render_template, request

app = Flask(__name__)

def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            return file.readlines()
    except FileNotFoundError:
        return [f"Error: File {file_path} not found"]
    except PermissionError:
        return [f"Error: Permission denied while trying to access {file_path}"]
    except Exception as e:
        return [f"An unexpected error occurred: {e}"]

@app.route('/file/')
@app.route('/file/<filename>')
def display_file(filename='file1'):
    file_path = f'{filename}.txt'
    try:
        lines = read_file(file_path)

        start_line = request.args.get('start_line', type=int)
        end_line = request.args.get('end_line', type=int)

        if start_line is not None and end_line is not None:
            try:
                lines = lines[start_line - 1:end_line]
            except Exception as e:
                return render_template('error_template.html', error=f"Error processing lines: {e}")

        content = '<br>'.join(lines)
        return render_template('file_template.html', content=content)

    except Exception as e:
        return render_template('error_template.html', error=f"An unexpected error occurred: {e}")

if __name__ == '__main__':
    app.run(debug=True)
