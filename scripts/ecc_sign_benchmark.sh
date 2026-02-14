#!/usr/bin/env bash
set -euo pipefail

ITERATIONS=20
OUTPUT_FILE="data/ecc_sign_benchmark.txt"
MESSAGE_FILE="data/test_message.txt"

mkdir -p "$(dirname "$OUTPUT_FILE")"
: > "$OUTPUT_FILE"

echo "TPM2 ECC signing benchmark payload" > "$MESSAGE_FILE"

# Prepare ECC signing key once; benchmark only the sign operation.
rm -f ecc_primary.ctx ecc_key.pub ecc_key.priv ecc_key.ctx ecc_signature.bin
tpm2_createprimary -C o -G ecc256 -c ecc_primary.ctx >/dev/null 2>&1
tpm2_create -C ecc_primary.ctx -G ecc256 -u ecc_key.pub -r ecc_key.priv >/dev/null 2>&1
tpm2_load -C ecc_primary.ctx -u ecc_key.pub -r ecc_key.priv -c ecc_key.ctx >/dev/null 2>&1

echo "Benchmarking TPM2 ECC signing for ${ITERATIONS} iterations..."
for i in $(seq 1 "$ITERATIONS"); do
  elapsed=$(/usr/bin/time -f "%e" sh -c 'tpm2_sign -c ecc_key.ctx -g sha256 -d data/test_message.txt -f plain -s ecdsa -o ecc_signature.bin >/dev/null 2>&1' 2>&1)
  echo "$elapsed" >> "$OUTPUT_FILE"
  echo "Iteration $i: ${elapsed}s"
done

rm -f ecc_primary.ctx ecc_key.pub ecc_key.priv ecc_key.ctx ecc_signature.bin

echo "Done. Results saved to $OUTPUT_FILE"
