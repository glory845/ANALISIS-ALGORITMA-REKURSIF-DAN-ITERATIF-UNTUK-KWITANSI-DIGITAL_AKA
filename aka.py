import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt

from flask import Flask, render_template, request
import time

app = Flask(__name__, template_folder="front")

kata = ["", "Satu", "Dua", "Tiga", "Empat", "Lima", "Enam", "Tujuh", "Delapan", "Sembilan",
    "Sepuluh", "Sebelas"]


# Fungsi Rekursif

def terbilang_rekursif(n):
    if n < 12:
        return kata[n]
    if n < 20:
        return kata[n - 10] + " Belas"
    if n < 100:
        return (
            kata[n // 10] + " Puluh " + terbilang_rekursif(n % 10)
            if n % 10 != 0 else
            kata[n // 10] + " Puluh"
        )
    if n < 200:
        return "Seratus " + terbilang_rekursif(n - 100)
    if n < 1000:
        return (
            kata[n // 100] + " Ratus " + terbilang_rekursif(n % 100)
            if n % 100 != 0 else
            kata[n // 100] + " Ratus"
        )
    if n < 2000:
        return "Seribu " + terbilang_rekursif(n - 1000)
    if n < 1_000_000:
        return (
            terbilang_rekursif(n // 1000) + " Ribu " + terbilang_rekursif(n % 1000)
            if n % 1000 != 0 else
            terbilang_rekursif(n // 1000) + " Ribu"
        )
    if n < 1_000_000_000:
        return (
            terbilang_rekursif(n // 1_000_000) + " Juta " + terbilang_rekursif(n % 1_000_000)
            if n % 1_000_000 != 0 else
            terbilang_rekursif(n // 1_000_000) + " Juta"
        )
    if n < 1_000_000_000_000:
        return (
            terbilang_rekursif(n // 1_000_000_000) + " Miliar " +
            terbilang_rekursif(n % 1_000_000_000)
            if n % 1_000_000_000 != 0 else
            terbilang_rekursif(n // 1_000_000_000) + " Miliar"
        )
    if n < 1_000_000_000_000_000:
        return (
            terbilang_rekursif(n // 1_000_000_000_000) + " Triliun " +
            terbilang_rekursif(n % 1_000_000_000_000)
            if n % 1_000_000_000_000 != 0 else
            terbilang_rekursif(n // 1_000_000_000_000) + " Triliun"
        )

    return "Angka Terlalu Besar"


# Fungsi Iteratif

def terbilang_iteratif(n):
    if n == 0:
        return "Nilai Tidak Ada"

    kata = ["", "Satu", "Dua", "Tiga", "Empat", "Lima",
            "Enam", "Tujuh", "Delapan", "Sembilan",
            "Sepuluh", "Sebelas"]

    def terbilang_kecil(x):
        hasil = ""

        if x < 12:
            return kata[x]

        if x < 20:
            return kata[x - 10] + " Belas"

        if x < 100:
            hasil = kata[x // 10] + " Puluh"
            if x % 10 != 0:
                hasil += " " + kata[x % 10]
            return hasil

        if x < 200:
            hasil = "Seratus"
            if x - 100 != 0:
                hasil += " " + terbilang_kecil(x - 100)
            return hasil

        if x < 1000:
            hasil = kata[x // 100] + " Ratus"
            if x % 100 != 0:
                hasil += " " + terbilang_kecil(x % 100)
            return hasil

    satuan = [
        (1_000_000_000_000, " Triliun"),
        (1_000_000_000, " Miliar"),
        (1_000_000, " Juta"),
        (1_000, " Ribu"),
        (1, "")
    ]

    hasil = ""

    for nilai, nama in satuan:
        bagian = n // nilai
        if bagian > 0:
            if nilai == 1000 and bagian == 1:
                hasil += "Seribu"
            else:
                hasil += terbilang_kecil(bagian) + nama
            n %= nilai
            if n > 0:
                hasil += " "

    return hasil.strip()


# =====================
# ROUTE UTAMA
# =====================
@app.route("/", methods=["GET", "POST"])
def index():
    hasil_rek = ""
    hasil_iter = ""
    waktu_rek = None
    waktu_iter = None

    if request.method == "POST":
        n = int(request.form["angka"])
        ITERASI = 2000

        hasil_rek = terbilang_rekursif(n)
        hasil_iter = terbilang_iteratif(n)

        ukuran_input = sorted(set([n]))
        waktu_rekursif = []
        waktu_iteratif = []

        for nilai in ukuran_input:
            start = time.perf_counter()
            for _ in range(ITERASI):
                terbilang_rekursif(nilai)
            waktu_rekursif.append((time.perf_counter() - start) / ITERASI)

            start = time.perf_counter()
            for _ in range(ITERASI):
                terbilang_iteratif(nilai)
            waktu_iteratif.append((time.perf_counter() - start) / ITERASI)

        # =====================
        # MEMBUAT GRAFIK TITIK
        # =====================
        plt.figure()

        plt.plot(ukuran_input, waktu_rekursif,
                marker='o', linestyle='', label='Rekursif')

        plt.plot(ukuran_input, waktu_iteratif,
                marker='o', linestyle='', label='Iteratif')

        plt.title("Perbandingan Waktu Eksekusi Rekursif vs Iteratif")
        plt.xlabel("Ukuran Input")
        plt.ylabel("Waktu Eksekusi (detik)")
        plt.legend()
        plt.grid(True)

        plt.savefig("static/grafik.png")
        plt.close()


        waktu_rek = waktu_rekursif[-1]
        waktu_iter = waktu_iteratif[-1]

    return render_template(
        "index.html",
        rek=hasil_rek + " Rupiah",
        ite=hasil_iter + " Rupiah",
        wr=waktu_rek,
        wi=waktu_iter
    )


if __name__ == "__main__":
    app.run(debug=True)
