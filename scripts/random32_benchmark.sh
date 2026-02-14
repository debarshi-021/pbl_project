#!/usr/bin/env bash
set -euo pipefail

ITERATIONS=20
OUTPUT_FILE="data/random32_benchmark.txt"

mkdir -p "$(dirname "$OUTPUT_FILE")"
: > "$OUTPUT_FILE"

echo "Benchmarking TPM2 getrandom 32 bytes for ${ITERATIONS} iterations..."
for i in $(seq 1 "$ITERATIONS"); do
  elapsed=$(/usr/bin/time -f "%e" sh -c 'tpm2_getrandom 32 >/dev/null 2>&1' 2>&1)
  echo "$elapsed" >> "$OUTPUT_FILE"
  echo "Iteration $i: ${elapsed}s"
done

echo "Done. Results saved to $OUTPUT_FILE"
