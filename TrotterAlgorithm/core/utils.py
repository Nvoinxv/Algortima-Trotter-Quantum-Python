import numpy as np

# Ini di gunakan buat stabilitas numerik
# Jadi gak fluktuasi gede banget tetap mempertahankan 0 - 1
# Seperti kek scaling data di AI buat preprocessing data
# Disini tugas nya stabilitas numerik, skala seragam, dan memenuhi syarat fisik
# Jadi setiap ganti ganti D dan titik dimensi itu tetap konsisten walau keubah dikit saja
# Kalau gak pakai ini, amplitudo nya bisa meledak

class NumericalUtils:
    """
    Kelas utilitas numerik untuk PDE Quantum.
    Berisi metode derivatif numerik, interpolasi, dll.
    Semua method statis agar bisa dipanggil langsung.
    """

    @staticmethod
    def central_difference(y, h, order=1):
        """
        Hitung turunan dengan skema finite difference sentral.
        y : array 1D data
        h : ukuran grid
        order : orde turunan (1 atau 2)
        """
        if order == 1:
            # d/dx f ≈ (f(x+h) - f(x-h)) / 2h
            dydx = np.zeros_like(y)
            dydx[1:-1] = (y[2:] - y[:-2]) / (2*h)
            dydx[0] = (y[1] - y[0]) / h          # forward diff
            dydx[-1] = (y[-1] - y[-2]) / h       # backward diff
            return dydx

        elif order == 2:
            # d²/dx² f ≈ (f(x+h) - 2f(x) + f(x-h)) / h²
            d2ydx2 = np.zeros_like(y)
            d2ydx2[1:-1] = (y[2:] - 2*y[1:-1] + y[:-2]) / (h**2)
            d2ydx2[0] = (y[2] - 2*y[1] + y[0]) / (h**2)    # forward
            d2ydx2[-1] = (y[-1] - 2*y[-2] + y[-3]) / (h**2)  # backward
            return d2ydx2

        else:
            raise ValueError("Order hanya mendukung 1 atau 2")

    @staticmethod
    def linear_interpolation(x, xp, yp):
        """
        Interpolasi linear: mirip np.interp tapi versi OOP.
        x : titik yang ingin diinterpolasi
        xp : array titik grid
        yp : array nilai fungsi di xp
        """
        return np.interp(x, xp, yp)

    @staticmethod
    def normalize(arr):
        """
        Normalisasi array agar jumlah totalnya = 1 (probabilitas).
        """
        total = np.sum(arr)
        if total == 0:
            return arr
        return arr / total

    @staticmethod
    def gaussian(x, mu=0.0, sigma=1.0):
        """
        Fungsi Gaussian 1D.
        """
        return np.exp(-(x-mu)**2 / (2*sigma**2)) / (sigma*np.sqrt(2*np.pi))