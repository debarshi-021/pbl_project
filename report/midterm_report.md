# Midterm Report: TPM 2.0 Performance Analysis for PBL

## Abstract
Trusted Platform Module (TPM) 2.0 is widely used as a hardware root of trust for integrity measurement, key protection, and secure cryptographic workflows. Despite strong security properties, practical deployment requires understanding runtime overheads in real systems. This midterm report presents a structured performance study of core TPM 2.0 commands: PCR read, random number generation, primary key creation, and digital signing using RSA and ECC. We define a reproducible benchmark methodology based on repeated measurements (20 iterations per command), standardized timing instrumentation (`/usr/bin/time -f "%e"`), and controlled command output suppression to minimize noise. Preliminary analysis focuses on expected relative trends and an initial analytical performance model that decomposes latency into command dispatch, TPM queueing, cryptographic computation, and context management costs. The work establishes a foundation for final-stage quantitative evaluation and comparative discussion of security-performance tradeoffs in TPM-enabled architectures.

## 1. Introduction
Modern trusted computing relies on hardware-assisted security primitives to protect secrets and verify system state. TPM 2.0 serves this role by isolating key material and implementing attestation-relevant operations. In practical deployments, however, security operations compete with throughput and latency constraints, especially in embedded systems, edge platforms, and enterprise endpoints.

The core research question is: **What is the operational latency profile of commonly used TPM 2.0 commands, and how can these measurements inform system design choices?**

This project studies representative operations spanning read, random, key lifecycle, and signing tasks. The objective is not only to produce benchmark numbers, but to create a reusable experimental pipeline and explain results through a simple, interpretable performance model.

## 2. Background
TPM 2.0 is a tamper-resistant cryptographic subsystem that exposes a command interface for integrity and key management functions.

### 2.1 Key TPM Concepts
- **PCR (Platform Configuration Register)**: Stores integrity measurements of firmware/software components.
- **Hierarchy and Primary Keys**: TPM objects are rooted in hierarchies (owner, platform, endorsement). Primary keys anchor object trees.
- **Random Number Generator**: Provides hardware-backed random bytes through TPM command interface.
- **TPM Signing**: Enables signatures with private keys that remain protected within TPM-controlled boundaries.

### 2.2 Why Performance Matters
In measured boot pipelines, remote attestation, and secure update frameworks, TPM operations can lie on critical execution paths. Poorly characterized latency can increase boot time, delay service startup, or create bottlenecks in high-frequency signing workflows.

## 3. Brief Literature Context
Prior work in trusted computing often emphasizes TPM security guarantees, attestation protocols, and secure key storage. Performance discussion is usually secondary and frequently platform-specific. Studies that report command timing generally observe:
- notable variance across TPM vendors,
- higher latency for key creation than read/random operations,
- non-negligible software stack overhead (driver/resource manager/user-space tools).

This project contributes an educational and reproducible benchmark artifact tailored to PBL objectives, while aligning with established empirical benchmarking principles.

## 4. Methodology

### 4.1 Experimental Design
The benchmark suite includes seven operations:
1. PCR read (`tpm2_pcrread sha256:0`)
2. Random 32 bytes (`tpm2_getrandom 32`)
3. Random 256 bytes (`tpm2_getrandom 256`)
4. RSA primary key creation (`tpm2_createprimary -C o -G rsa`)
5. ECC primary key creation (`tpm2_createprimary -C o -G ecc256`)
6. RSA signing of static payload
7. ECC signing of static payload

Each operation runs 20 iterations to capture baseline distribution behavior.

### 4.2 Measurement Procedure
- Timing is collected using `/usr/bin/time -f "%e"`.
- Benchmark command output is redirected to `/dev/null` to avoid output-related distortion.
- Scripts write clean elapsed-time values to text files in the `data/` directory.
- A CSV template standardizes downstream analysis.

### 4.3 Reproducibility Controls
- Fixed command parameters for all runs.
- Explicit script-level file cleanup for key/context artifacts.
- Single benchmark operation per script for isolation.
- Linux shell implementation for portability.

## 5. Results and Preliminary Analysis
At midterm stage, the focus is methodology validation and preliminary expectation framing rather than finalized numerical claims.

### 5.1 Anticipated Relative Ordering
Expected low-to-high latency trend:
1. PCR read
2. Random 32
3. Random 256
4. RSA/ECC sign
5. RSA/ECC primary creation

This ordering follows command complexity and TPM internal resource usage.

### 5.2 Sources of Variability
- OS scheduler interference
- TPM internal queue contention
- Resource manager behavior
- Virtualization overhead (if in VM)
- Thermal/power management effects

### 5.3 Data Readiness
The repository includes:
- runnable scripts for all seven operations,
- raw output text files generated per operation,
- unified CSV schema for aggregation and plotting.

## 6. Performance Model
We propose the latency decomposition:

\[
T_{op} = T_{dispatch} + T_{queue} + T_{crypto} + T_{context} + \epsilon
\]

Interpretation:
- **Dispatch**: user-space command marshalling and kernel handoff.
- **Queue**: TPM command serialization delays.
- **Crypto**: operation-dependent hardware cryptographic execution.
- **Context**: object/session creation, loading, and cleanup overhead.
- **Noise term** \(\epsilon\): background-system perturbations.

For signing workflows, a refined expression can separate setup cost:

\[
T_{sign,total} = T_{key\_prep} + n \cdot T_{sign,per\_op}
\]

This supports design choices such as key reuse versus frequent regeneration.

## 7. Discussion
The midterm milestone demonstrates that the project has moved beyond conceptual framing to an operational benchmarking framework. The scripts are immediately executable in TPM-capable Linux environments and enforce consistent measurement discipline.

Educationally, the project illustrates a core systems-security insight: stronger trust guarantees often come with measurable latency costs. Engineering decisions should therefore be evidence-based, balancing security value against service-level performance constraints.

## 8. Conclusion
This midterm report establishes the experimental backbone for TPM 2.0 performance analysis. A complete benchmark pipeline has been prepared with standardized scripts, controlled timing, and structured data outputs. Preliminary modeling and expected trends provide a clear analytical direction. The final phase will populate the dataset, produce comparative visualizations, conduct deeper statistical analysis, and derive design recommendations.

## 9. Future Work
1. Execute full benchmark runs on target TPM hardware and, if available, software TPM for comparison.
2. Compute descriptive statistics (mean, median, standard deviation, confidence intervals).
3. Plot command-wise boxplots and cumulative distribution curves.
4. Compare RSA vs ECC tradeoffs under identical workload assumptions.
5. Evaluate warm-start vs cold-start behavior and context reuse effects.
6. Extend study to additional TPM operations (quote, unseal, policy session commands).

---

**Repository Artifacts Supporting This Report**
- Benchmark scripts in `scripts/`
- Data template in `data/benchmark_data_template.csv`
- Analysis scaffolding for final report preparation
