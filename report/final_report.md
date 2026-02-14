# Final Report: Comprehensive TPM 2.0 Performance Analysis for PBL

## Abstract
This final report presents a complete performance benchmarking framework for key TPM 2.0 operations relevant to trusted computing workflows. The project measures and analyzes command latency for PCR reads, random number generation, RSA and ECC primary key creation, and asymmetric signing. A reproducible Linux-based toolchain was implemented using `tpm2-tools` and standardized timing capture via `/usr/bin/time -f "%e"` over 20 iterations per operation. Beyond presenting an executable benchmark suite, the report formalizes a latency decomposition model, interprets expected behavior across command classes, and discusses system-design implications for secure boot, attestation, and protected signing services. The repository artifacts are intended for direct reuse in educational and pre-production evaluation contexts.

## 1. Introduction
Hardware roots of trust are foundational to modern platform security. TPM 2.0 supports integrity measurement, secure key storage, and cryptographic operations with hardware-backed protections. While the security benefits are well established, integration into real systems requires careful attention to runtime cost.

This project addresses the practical question:

> How do core TPM 2.0 operations differ in latency, and how can those differences guide architecture-level decisions in secure systems?

The deliverable is both analytical and operational: (i) a full benchmark pipeline and (ii) a structured interpretation model for the measured behavior.

## 2. Project Objectives
The project pursued five concrete objectives:
1. Define a representative set of TPM commands covering integrity, entropy, key generation, and signing.
2. Implement robust benchmark scripts with consistent timing and minimal measurement contamination.
3. Organize outputs into reusable data artifacts for statistical and visual analysis.
4. Construct a performance model that maps observed latency to stack-level contributors.
5. Produce documentation suitable for academic reporting and presentation.

## 3. Technical Background

### 3.1 TPM 2.0 in Brief
TPM 2.0 is a discrete or integrated security coprocessor offering:
- cryptographic key protection,
- integrity-related registers (PCRs),
- random number generation,
- command-authorized cryptographic services.

### 3.2 Operations Selected for Benchmarking
The seven selected operations were chosen for practical relevance:
- **PCR read**: common in measured-state validation pipelines.
- **Random generation (32 and 256 bytes)**: supports nonce/key material provisioning.
- **Primary key creation (RSA/ECC)**: representative of high-overhead setup operations.
- **RSA/ECC signing**: representative of recurring trust-sensitive cryptographic tasks.

### 3.3 Expected Cost Drivers
Latency is influenced by both hardware and software layers:
- userspace tool invocation overhead,
- kernel/resource-manager mediation,
- TPM command serialization,
- cryptographic engine execution,
- transient object context handling.

## 4. Experimental Environment
A Linux VM/host with TPM 2.0 capability was targeted. Required components:
- `tpm2-tools`
- shell runtime (`bash`)
- GNU `/usr/bin/time`
- accessible TPM resource manager path

To ensure portability, scripts avoid non-standard shell features and keep dependencies minimal.

## 5. Methodology

### 5.1 Measurement Protocol
For each operation:
- execute exactly **20 iterations**,
- measure elapsed wall time with `/usr/bin/time -f "%e"`,
- suppress operation output to `/dev/null`,
- record one clean numeric value per line in `data/*.txt`.

### 5.2 Script Design Choices
- Single-purpose script per operation for isolation.
- Deterministic artifact paths for easy automation.
- Pre/post cleanup of context and key files.
- Static payload file for signing comparability.

### 5.3 Data Schema
`data/benchmark_data_template.csv` defines aligned columns:
- `PCR_Read`
- `Random_32`
- `Random_256`
- `RSA_Primary`
- `ECC_Primary`
- `RSA_Sign`
- `ECC_Sign`

This format supports direct import into spreadsheet tools, Python notebooks, or R scripts.

## 6. Implementation Summary

### 6.1 Repository Structure
- `scripts/`: executable benchmark drivers.
- `data/`: raw timing outputs and aggregation template.
- `report/`: academic writeups.
- `presentation/`: slide planning artifact.
- top-level `README.md` and `LICENSE`.

### 6.2 Benchmark Scripts
Implemented scripts:
1. `pcr_benchmark.sh`
2. `random32_benchmark.sh`
3. `random256_benchmark.sh`
4. `rsa_primary_benchmark.sh`
5. `ecc_primary_benchmark.sh`
6. `rsa_sign_benchmark.sh`
7. `ecc_sign_benchmark.sh`

Each script is executable and ready for Linux TPM environments.

## 7. Results and Analysis Framework

### 7.1 Qualitative Outcome Pattern
Although exact values depend on hardware/stack configuration, the expected qualitative pattern is:
- low latency: PCR read, random-32
- medium latency: random-256, signing
- high latency: primary key creation

### 7.2 RSA vs ECC Considerations
Potential trends:
- ECC may show lower latency than RSA for some operations on certain TPM implementations.
- Implementation-specific firmware and command serialization behavior can invert this trend.
- Therefore, empirical measurement on target hardware remains essential.

### 7.3 Statistical Post-Processing Plan
For each column/operation:
- compute mean, median, min, max,
- compute standard deviation and coefficient of variation,
- create boxplots and violin plots,
- examine outliers and possible warm-up effects.

### 7.4 Interpretation Strategy
Map statistical features to system implications:
- **Mean latency**: expected service time.
- **Tail latency**: worst-case responsiveness risk.
- **Variance**: predictability under load.

## 8. Performance Model
Primary model:

\[
T_{op} = T_{dispatch} + T_{queue} + T_{crypto} + T_{context} + \epsilon
\]

Where:
- \(T_{dispatch}\): userspace invocation and marshalling.
- \(T_{queue}\): TPM scheduling/serialization delays.
- \(T_{crypto}\): command-intrinsic cryptographic processing.
- \(T_{context}\): object/session setup and teardown.
- \(\epsilon\): environmental noise.

For repeated signing:

\[
T_{sign,total}(n) = T_{setup} + n\cdot T_{sign}
\]

This explains why one-time key preparation amortization matters in real services.

## 9. Discussion

### 9.1 Security-Performance Tradeoff
TPM-backed operations intentionally prioritize key isolation and trust guarantees, often at a latency premium relative to software-only cryptography. This premium is acceptable for many security-critical workflows, but should be measured before deploying into time-sensitive paths.

### 9.2 Practical Engineering Guidance
- Reuse loaded keys when safe and possible.
- Separate setup-time and per-operation costs in performance budgets.
- Avoid unnecessary high-frequency key-creation events.
- Profile on deployment hardware, not only in development VMs.

### 9.3 Limitations
- Current artifact provides framework and expected analytical approach; numeric claims must come from actual run data on target TPMs.
- Results can vary by vendor firmware, kernel version, and resource manager configuration.

## 10. Conclusion
This project delivers a complete and reusable TPM 2.0 benchmarking repository suitable for PBL evaluation and further research extension. The implementation standardizes timing capture, operation selection, and data organization. The analysis model and reporting artifacts provide a strong basis for rigorous, reproducible performance evaluation.

By combining script-level reproducibility with systems-level interpretation, the project supports informed decisions about where and how TPM primitives should be integrated in secure computing pipelines.

## 11. Future Work
1. Execute repeated multi-day runs for stability analysis.
2. Compare discrete TPM vs firmware TPM.
3. Add attestation-related operations (`tpm2_quote`, policy sessions, unseal).
4. Automate CSV population from raw `.txt` outputs.
5. Build a notebook for statistical analysis and publication-ready plots.
6. Investigate command batching and concurrency effects.

## 12. Reproducibility Checklist
- [x] Seven benchmark scripts implemented.
- [x] 20-iteration standardization.
- [x] Uniform time-measurement method.
- [x] Output suppression for cleaner timing.
- [x] Structured data template included.
- [x] Documentation and reporting artifacts included.

---

## Appendix A: Example Execution Sequence
```bash
chmod +x scripts/*.sh
./scripts/pcr_benchmark.sh
./scripts/random32_benchmark.sh
./scripts/random256_benchmark.sh
./scripts/rsa_primary_benchmark.sh
./scripts/ecc_primary_benchmark.sh
./scripts/rsa_sign_benchmark.sh
./scripts/ecc_sign_benchmark.sh
```

## Appendix B: Suggested Analysis Commands
```bash
paste -d, \
  data/pcr_benchmark.txt \
  data/random32_benchmark.txt \
  data/random256_benchmark.txt \
  data/rsa_primary_benchmark.txt \
  data/ecc_primary_benchmark.txt \
  data/rsa_sign_benchmark.txt \
  data/ecc_sign_benchmark.txt > data/benchmark_data_filled.csv
```
