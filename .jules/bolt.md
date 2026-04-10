
## 2026-04-10 - [RFFT Optimization for Real-Valued Holographic Vectors]
**Learning:** Standard FFT/IFFT operations on real-valued vectors (like the D=1024 vectors used in STRATOS-OS) waste 50% of computation on redundant complex conjugates. Switching to RFFT/IRFFT provides a ~1.5x-2.3x speedup. Furthermore, complex exponentiation (np.exp(1j * angle)) is significantly slower than direct complex arithmetic (division by sqrt of magnitude) for fractional binding with alpha=0.5.
**Action:** Always prefer RFFT for real-valued holographic operations and avoid trigonometric functions in hot loops where direct complex arithmetic can achieve the same result.

## 2026-04-10 - [Fused Matrix Retrieval and Deferred Cache Persistence]
**Learning:** Looping over multiple shards for nearest-neighbor search is significantly slower than a single large matrix multiplication, even for relatively small numbers of shards. Maintaining a fused "hot" matrix for retrieval improves throughput by ~3x. Furthermore, disk I/O in high-frequency loops (like cache saving) causes severe performance degradation as the cache grows. Providing an option to defer persistence allows for much higher execution frequency.
**Action:** Always prefer vectorized operations over loops, even when data is sharded for storage. Avoid synchronous disk writes in hot execution paths.
