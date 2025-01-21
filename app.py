from flask import Flask, render_template, request
from math import factorial

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', page='form')

@app.route('/result', methods=['POST'])
def result():
    try:
        # Ambil input dari form
        arrival_rate = float(request.form['arrival_rate'])
        service_rate = float(request.form['service_rate'])

        if arrival_rate <= 0 or service_rate <= 0:
            return render_template('index.html', page='error', message="Input harus bernilai positif!")

        s = 2  # Jumlah loket (servers)
        rho = arrival_rate / (s * service_rate)  # Pemanfaatan pelayan per server

        # Validasi stabilitas sistem
        if rho >= 1:
            return render_template('index.html', page='error', message="Sistem tidak stabil (ρ ≥ 1).")

        # Perhitungan probabilitas sistem kosong (P0)
        term1 = sum((arrival_rate / service_rate) ** n / factorial(n) for n in range(s))
        term2 = ((arrival_rate / service_rate) ** s) / (factorial(s) * (1 - rho))
        P0 = 1 / (term1 + term2)

        # Perhitungan metrik lainnya
        Lq = (P0 * ((arrival_rate / service_rate) ** s) * rho) / (factorial(s) * (1 - rho) ** 2)
        Wq = Lq / arrival_rate
        W = Wq + (1 / service_rate)
        L = arrival_rate * W

        # Langkah-langkah perhitungan
        steps = f"""
        <h3>Langkah-langkah Perhitungan:</h3>
        <p><b>1. Hitung Traffic Intensity (ρ):</b></p>
        <p>ρ = λ / (s × μ)</p>
        <p>ρ = {arrival_rate} / ({s} × {service_rate})</p>
        <p>ρ = {rho:.4f}</p>
        <br>

        <p><b>2. Hitung Probabilitas Sistem Kosong (P₀):</b></p>
        <p>P₀ = 1 / [Σ (λ/μ)^n / n! untuk n = 0 sampai s-1] + [(λ/μ)^s / (s! × (1 - ρ))]</p>
        <p>P₀ = 1 / [{term1:.4f} + {term2:.4f}]</p>
        <p>P₀ = {P0:.4f}</p>
        <br>

        <p><b>3. Hitung Jumlah Pelanggan dalam Antrean (Lq):</b></p>
        <p>Lq = (P₀ × (λ/μ)^s × ρ) / (s! × (1 - ρ)^2)</p>
        <p>Lq = ({P0:.4f} × ({arrival_rate}/{service_rate})^{s} × {rho:.4f}) / ({factorial(s)} × (1 - {rho:.4f})^2)</p>
        <p>Lq = {Lq:.4f}</p>
        <br>

        <p><b>4. Hitung Waktu Rata-rata dalam Antrean (Wq):</b></p>
        <p>Wq = Lq / λ</p>
        <p>Wq = {Lq:.4f} / {arrival_rate}</p>
        <p>Wq = {Wq:.4f} menit</p>
        <br>

        <p><b>5. Hitung Waktu Rata-rata dalam Sistem (W):</b></p>
        <p>W = Wq + (1/μ)</p>
        <p>W = {Wq:.4f} + (1 / {service_rate})</p>
        <p>W = {W:.4f} menit</p>
        <br>

        <p><b>6. Hitung Jumlah Pelanggan dalam Sistem (L):</b></p>
        <p>L = λ × W</p>
        <p>L = {arrival_rate} × {W:.4f}</p>
        <p>L = {L:.4f}</p>
        """

        # Kirim hasil ke template
        return render_template('index.html', page='result',
                               P0=f"{P0:.4f}", Lq=f"{Lq:.2f}", Wq=f"{Wq:.2f}",
                               W=f"{W:.2f}", L=f"{L:.2f}", steps=steps)
    except ValueError:
        return render_template('index.html', page='error', message="Input tidak valid! Masukkan angka yang benar.")

if __name__ == '__main__':
    app.run(debug=True)