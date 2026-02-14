#!/usr/bin/env bash
set -euo pipefail

ITERATIONS=20
OUTPUT_FILE="data/rsa_sign_benchmark.txt"
MESSAGE_FILE="data/test_message.txt"

mkdir -p "$(dirname "$OUTPUT_FILE")"
: > "$OUTPUT_FILE"

echo "TPM2 RSA signing benchmark payload" > "$MESSAGE_FILE"

# Prepare RSA signing key once; benchmark only the sign operation.
rm -f rsa_primary.ctx rsa_key.pub rsa_key.priv rsa_key.ctx rsa_signature.bin
tpm2_createprimary -C o -G rsa -c rsa_primary.ctx >/dev/null 2>&1
tpm2_create -C rsa_primary.ctx -G rsa2048 -u rsa_key.pub -r rsa_key.priv >/dev/null 2>&1
tpm2_load -C rsa_primary.ctx -u rsa_key.pub -r rsa_key.priv -c rsa_key.ctx >/dev/null 2>&1

echo "Benchmarking TPM2 RSA signing for ${ITERATIONS} iterations..."
for i in $(seq 1 "$ITERATIONS"); do
  elapsed=$(/usr/bin/time -f "%e" sh -c 'tpm2_sign -c rsa_key.ctx -g sha256 -d data/test_message.txt -f plain -s rsassa -o rsa_signature.bin >/dev/null 2>&1' 2>&1)
  echo "$elapsed" >> "$OUTPUT_FILE"
  echo "Iteration $i: ${elapsed}s"
done

rm -f rsa_primary.ctx rsa_key.pub rsa_key.priv rsa_key.ctx rsa_signature.bin

echo "Done. Results saved to $OUTPUT_FILE"
