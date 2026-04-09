import numpy as np

def bind(a, b):
    """Standard Circular Convolution (Binding)."""
    return np.fft.ifft(np.fft.fft(a) * np.fft.fft(b)).real.astype(np.float32)

def unbind(a, b):
    """Standard Circular Correlation (Unbinding/Inference)."""
    # Circular correlation is convolution with the involution of b
    b_inv = np.concatenate([b[:1], b[1:][::-1]])
    return bind(a, b_inv)

def fractional_bind(base, alpha=0.5):
    """Fractional Binding via frequency-domain scaling."""
    f = np.fft.fft(base)
    mag = np.abs(f)
    phase = np.angle(f)

    # Scale both magnitude and phase
    # This is equivalent to f**alpha in the complex domain
    f_alpha = (mag ** alpha) * np.exp(1j * phase * alpha)

    return np.fft.ifft(f_alpha).real.astype(np.float32)

def normalize(v):
    norm = np.linalg.norm(v)
    if norm < 1e-8:
        return v
    return v / norm
