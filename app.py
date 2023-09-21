from flask import Flask, render_template, request, redirect, url_for
import qrcode
import os
import pyshorteners

app = Flask(__name__)

# Configuration
app.config['UPLOAD_FOLDER'] = 'static/qr_codes/'

# Initialize URL shortener
s = pyshorteners.Shortener()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten():
    long_url = request.form.get('long_url')
    if long_url:
        short_url = s.tinyurl.short(long_url)
        return render_template('index.html', short_url=short_url)
    return redirect(url_for('index'))

@app.route('/generate_qrcode', methods=['POST'])
def generate_qrcode():
    data = request.form.get('data')
    if data:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img.save(os.path.join(app.config['UPLOAD_FOLDER'], 'qr_code.png'))

        return render_template('index.html', qr_code='/static/qr_codes/qr_code.png')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

