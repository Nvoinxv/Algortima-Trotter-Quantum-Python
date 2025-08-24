from TrotterAlgorithm.core.ComplexNumber import ComplexNumbers
import random

# Sama seperti projek sebelum nya sebenarnya ini implementasi ke projek sebelum nya
# Membuat kelas qubits:

class MultiQubitState:
    """
    Membuat global multi-qubit state dari single-qubit class.
    Tetap mempertahankan qubit single sebagai building block.
    """
    def __init__(self, amplitudes):
        """
        amplitudes: list of ComplexNumbers untuk setiap basis state |0..0>, |0..1>, ..., |1..1>
        Panjang harus 2^n
        """
        self.n_qubits = len(amplitudes).bit_length() - 1
        self.amplitudes = amplitudes  # amplitudo global
        self.normalize()
    
    def normalize(self):
        norm = sum([amp.Modulus()**2 for amp in self.amplitudes]) ** 0.5
        if norm == 0:
            raise ValueError("Amplitudo semua nol!")
        self.amplitudes = [ComplexNumbers(amp.real / norm, amp.imajiner / norm)
                           for amp in self.amplitudes]

    def measure(self):
        import random
        probs = [amp.Modulus()**2 for amp in self.amplitudes]
        r = random.random()
        cumulative = 0
        for i, p in enumerate(probs):
            cumulative += p
            if r < cumulative:
                # collapse ke state i
                new_amplitudes = [ComplexNumbers(0,0) for _ in self.amplitudes]
                new_amplitudes[i] = ComplexNumbers(1,0)
                self.amplitudes = new_amplitudes
                return i
        return len(probs)-1  # fallback

    def apply_unitary(self, U):
        """
        U: matrix 2^n x 2^n dengan ComplexNumbers
        """
        new_ampl = []
        for i in range(len(self.amplitudes)):
            val = ComplexNumbers(0,0)
            for j in range(len(self.amplitudes)):
                val += U[i][j] * self.amplitudes[j]
            new_ampl.append(val)
        self.amplitudes = new_ampl
        self.normalize()

    def __str__(self):
        return "MultiQubitState: " + ", ".join([str(a) for a in self.amplitudes])