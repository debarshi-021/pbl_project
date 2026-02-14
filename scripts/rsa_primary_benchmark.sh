#!/usr/bin/env bash
set -euo pipefail

ITERATIONS=20
OUTPUT_FILE="data/rsa_primary_benchmark.txt"

mkdir -p "$(dirname "$OUTPUT_FILE")"
: > "$OUTPUT_FILE"

echo "Benchmarking TPM2 RSA-2048 primary key creation for ${ITERATIONS} iterations..."
for i in $(seq 1 "$ITERATIONS"); do
  rm -f rsa_primary.ctx
  elapsed=$(/usr/bin/time -f "%e" sh -c 'tpm2_createprimary -C o -G rsa -c rsa_primary.ctx >/dev/null 2>&1' 2>&1)
  echo "$elapsed" >> "$OUTPUT_FILE"
  echo "Iteration $i: ${elapsed}s"
done

rm -f rsa_primary.ctx

echo "Done. Results saved to $OUTPUT_FILE"
