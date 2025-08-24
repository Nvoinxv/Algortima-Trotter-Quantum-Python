# Qubit_test.py
from TrotterAlgorithm.core.Qubit import MultiQubitState
from TrotterAlgorithm.core.ComplexNumber import ComplexNumbers

# Contoh amplitudo awal (misal 2 qubit -> 4 basis states)
amplitudes = [
    ComplexNumbers(0.5, 0),
    ComplexNumbers(0.5, 0),
    ComplexNumbers(0.5, 0),
    ComplexNumbers(0.5, 0)
]

# Buat global multi-qubit state
multi_state = MultiQubitState(amplitudes)

print("State awal (normalized):")
print(multi_state)

# Tes pengukuran
print("\nHasil measurement:")
meas_result = multi_state.measure()
print("Hasil:", meas_result)
print("State setelah measurement:")
print(multi_state)

# Contoh apply unitary (identity)
identity_4x4 = [
    [ComplexNumbers(1,0), ComplexNumbers(0,0), ComplexNumbers(0,0), ComplexNumbers(0,0)],
    [ComplexNumbers(0,0), ComplexNumbers(1,0), ComplexNumbers(0,0), ComplexNumbers(0,0)],
    [ComplexNumbers(0,0), ComplexNumbers(0,0), ComplexNumbers(1,0), ComplexNumbers(0,0)],
    [ComplexNumbers(0,0), ComplexNumbers(0,0), ComplexNumbers(0,0), ComplexNumbers(1,0)]
]

multi_state.apply_unitary(identity_4x4)
print("\nState setelah apply identity (harus sama):")
print(multi_state)
