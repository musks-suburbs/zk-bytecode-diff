# zk-bytecode-diff

## Overview
**zk-bytecode-diff** is a command-line tool that compares on-chain smart contract bytecode between two addresses, verifying whether the deployed code is **identical**.  
This is especially useful in zk or cryptographic ecosystems like **Aztec** or **Zama**, where cross-chain soundness and reproducible deployments are crucial.

## Features
- Compare two contract bytecodes on any EVM-compatible chain  
- Compute and display keccak256 hashes of both contracts  
- Detect bytecode length mismatches and report differences  
- Output results in human-readable or JSON format  
- Supports historical block lookups  

## Installation
1. Install Python 3.9+  
2. Install dependencies:
   pip install web3 eth-utils
3. Set or pass your RPC endpoint:
   export RPC_URL=https://mainnet.infura.io/v3/YOUR_KEY

## Usage
Compare two contracts at the latest block:
   python app.py --address-a 0xContractA --address-b 0xContractB

Compare specific block bytecodes:
   python app.py --address-a 0xContractA --address-b 0xContractB --block 21000000

Emit JSON output for pipelines:
   python app.py --address-a 0xContractA --address-b 0xContractB --json

## Example Output
🔧 zk-bytecode-diff  
🔗 RPC: https://mainnet.infura.io/v3/YOUR_KEY  
🧭 Chain ID: 1  
🏷️ Comparing:  
   A: 0x00000000219ab540356cBB839Cbe05303d7705Fa  
   B: 0x00000000219ab540356cBB839Cbe05303d7705Fb  
🧱 Block: latest  
🔹 Hash (A): 0x3b44a77f8b43d4a77f8b43d4a77f8b43d4a77f8b43d4a77f8b43d4a77f8b43d4  
🔸 Hash (B): 0x3b44a77f8b43d4a77f8b43d4a77f8b43d4a77f8b43d4a77f8b43d4a77f8b43d5  
⚠️ Bytecodes differ! Length delta: 128 bytes  
⏱️ Completed in 0.53s  

## Notes
- If a contract’s bytecode is empty (e.g., EOA), the hash will be `0x0`.  
- Works for L1 and L2 networks — just switch the RPC endpoint.  
- Use in CI/CD pipelines to enforce identical deployments across environments.  
- Useful for Aztec/Zama rollup verifiers, bridges, and cross-chain proofs.  
- Always use a fixed block number for deterministic audits.  
- Exit codes:  
  `0` → Identical bytecode  
  `2` → Mismatch or error.  

