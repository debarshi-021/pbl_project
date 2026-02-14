# TPM 2.0 Performance Benchmark and Analysis for PBL

## Project Overview
This repository contains a complete, reproducible benchmark workflow for evaluating the runtime performance of common Trusted Platform Module (TPM) 2.0 operations. The project is designed for a Project-Based Learning (PBL) performance analysis study and focuses on representative cryptographic and platform trust primitives.

The benchmark suite includes:
- Platform Configuration Register (PCR) read
- Hardware random number generation (32-byte and 256-byte requests)
- RSA-2048 primary key creation
- ECC (NIST P-256) primary key creation
- RSA signing
- ECC signing

All scripts are production-ready for Linux environments that have `tpm2-tools` installed and a functional TPM 2.0 stack.

## Problem Statement
TPM 2.0 offers strong hardware-rooted security guarantees, but its practical adoption in system design depends on understanding runtime costs. In many real deployments, engineers must choose between stronger trust guarantees and acceptable latency overhead. Without empirical measurements, system architects cannot reliably estimate performance impact.

This project addresses that gap by collecting consistent execution-time measurements for key TPM operations and organizing them for comparative analysis.

## Motivation
The motivation of this study is threefold:
1. **Security engineering relevance**: TPM-backed workflows are increasingly used for measured boot, attestation, key sealing, and secure signing.
2. **Design tradeoff awareness**: Performance characteristics differ substantially across TPM commands; these differences affect architecture decisions.
3. **Educational value**: A clear and reproducible pipeline helps students and practitioners learn both TPM internals and empirical evaluation methods.

## TPM Basics (Simple Explanation)
A TPM (Trusted Platform Module) is a dedicated security processor that stores keys securely and performs cryptographic operations in a protected environment.

Key concepts used in this project:
- **PCRs**: Registers holding integrity measurements, used to represent platform state.
- **TPM RNG**: Hardware-backed random number generation.
- **Primary keys**: Root-level TPM-resident keys created under TPM hierarchies.
- **Asymmetric signing**: Digital signatures generated with private keys protected by TPM hardware.

Because operations execute via a hardware trust boundary, TPM commands typically have higher latency than pure software crypto, but provide stronger key protection and trust guarantees.

## Experimental Setup
Recommended setup for reproducibility:
- Linux VM or bare-metal Linux host
- TPM 2.0 device (hardware TPM or software TPM emulator, documented clearly if emulated)
- `tpm2-tools` installed and configured
- Resource manager/service available (`tpm2-abrmd` or kernel RM depending on platform)
- Bash shell and GNU `time` (`/usr/bin/time`)

Minimum software checks:
```bash
tpm2_getcap properties-fixed
which tpm2_pcrread tpm2_getrandom tpm2_createprimary tpm2_sign
/usr/bin/time --version
```

## Methodology
1. Each benchmark script runs **20 iterations**.
2. Timing uses `/usr/bin/time -f "%e"` (wall-clock elapsed seconds).
3. Command standard output is suppressed (`> /dev/null`) to avoid I/O noise.
4. Clean numeric timings are stored in dedicated `.txt` files under `data/`.
5. A CSV template (`benchmark_data_template.csv`) is provided for manual or scripted aggregation.

### Operations Benchmarked
- `tpm2_pcrread sha256:0`
- `tpm2_getrandom 32`
- `tpm2_getrandom 256`
- `tpm2_createprimary -C o -G rsa -c rsa_primary.ctx`
- `tpm2_createprimary -C o -G ecc256 -c ecc_primary.ctx`
- RSA sign on static payload
- ECC sign on static payload

## Benchmark Results (Summary)
At this stage, the repository provides a benchmark framework and data template rather than fixed cross-device numeric claims. Typical observed patterns (to be validated on your target platform) are:
- PCR read and low-byte RNG requests are usually among the fastest operations.
- 256-byte random generation tends to be slower than 32-byte generation.
- Primary key creation is typically much slower than read/random operations.
- Signing operations are generally faster than key creation but slower than simple reads.
- ECC operations may outperform RSA in some TPM implementations, especially for key generation and signing, but this is vendor-dependent.

## Performance Model
A simple model for per-operation latency:

\[
T_{op} = T_{cmd\_dispatch} + T_{TPM\_queue} + T_{crypto\_engine} + T_{context\_overhead} + \epsilon
\]

Where:
- \(T_{cmd\_dispatch}\): userspace-to-driver command dispatch overhead
- \(T_{TPM\_queue}\): TPM internal command scheduling/serialization delay
- \(T_{crypto\_engine}\): true cryptographic execution time
- \(T_{context\_overhead}\): object load/unload and hierarchy/context handling
- \(\epsilon\): environment noise (scheduler, virtualization, background load)

For large-sample planning, mean latency and variance from the 20-run sample can be used to estimate expected service time under target workloads.

## Observations and Conclusion
This project demonstrates how to systematically quantify TPM operation costs in a reproducible way. Even when exact numbers vary by hardware vendor and software stack, the methodology captures relative behavior across operation classes. Such data supports informed decisions in secure system design, especially where latency-sensitive and trust-critical tasks coexist.

## How to Reproduce
1. Clone the repository and enter it:
   ```bash
   git clone https://github.com/debarshi-021/pbl_project.git
   cd pbl_project
   ```
2. Ensure TPM tools and TPM service are available.
3. Make scripts executable (if needed):
   ```bash
   chmod +x scripts/*.sh
   ```
4. Run benchmarks:
   ```bash
   ./scripts/pcr_benchmark.sh
   ./scripts/random32_benchmark.sh
   ./scripts/random256_benchmark.sh
   ./scripts/rsa_primary_benchmark.sh
   ./scripts/ecc_primary_benchmark.sh
   ./scripts/rsa_sign_benchmark.sh
   ./scripts/ecc_sign_benchmark.sh
   ```
5. Inspect raw outputs in `data/*.txt` and populate/analyze `data/benchmark_data_template.csv`.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.
