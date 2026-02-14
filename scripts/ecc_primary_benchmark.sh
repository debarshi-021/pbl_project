#!/usr/bin/env bash
set -euo pipefail

ITERATIONS=20
OUTPUT_FILE="data/ecc_primary_benchmark.txt"

mkdir -p "$(dirname "$OUTPUT_FILE")"
: > "$OUTPUT_FILE"

echo "Benchmarking TPM2 ECC (NIST P-256) primary key creation for ${ITERATIONS} iterations..."
for i in $(seq 1 "$ITERATIONS"); do
  rm -f ecc_primary.ctx
  elapsed=$(/usr/bin/time -f "%e" sh -c 'tpm2_createprimary -C o -G ecc256 -c ecc_primary.ctx >/dev/null 2>&1' 2>&1)
  echo "$elapsed" >> "$OUTPUT_FILE"
  echo "Iteration $i: ${elapsed}s"
done

rm -f ecc_primary.ctx

echo "Done. Results saved to $OUTPUT_FILE"
