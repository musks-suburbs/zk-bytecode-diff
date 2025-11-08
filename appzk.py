# app.py
import os
import sys
import time
import json
import argparse
from typing import Dict, Any, Optional
from web3 import Web3
from eth_utils import keccak

DEFAULT_RPC = os.environ.get("RPC_URL", "https://mainnet.infura.io/v3/YOUR_INFURA_KEY")

def get_contract_bytecode(w3: Web3, address: str, block: Optional[str] = "latest") -> bytes:
    """
    Fetch the on-chain bytecode for a given contract address.
    """
    try:
        address = Web3.to_checksum_address(address)
        code = w3.eth.get_code(address, block_identifier=block)
        return code
    except Exception as e:
        raise RuntimeError(f"Error fetching bytecode: {e}")

def compare_bytecodes(bytecode_a: bytes, bytecode_b: bytes) -> Dict[str, Any]:
    """
    Compare two bytecodes and return a diff summary.
    """
    hash_a = Web3.keccak(bytecode_a).hex() if bytecode_a else "0x0"
    hash_b = Web3.keccak(bytecode_b).hex() if bytecode_b else "0x0"
    identical = bytecode_a == bytecode_b
    diff_length = abs(len(bytecode_a) - len(bytecode_b))
    return {
        "identical": identical,
        "hash_a": hash_a,
        "hash_b": hash_b,
        "diff_length": diff_length
    }

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="zk-bytecode-diff — compare on-chain bytecode between two contracts to check deployment soundness across chains or versions."
    )
    p.add_argument("--rpc", default=DEFAULT_RPC, help="EVM RPC URL (default from RPC_URL)")
    p.add_argument("--address-a", required=True, help="First contract address")
    p.add_argument("--address-b", required=True, help="Second contract address to compare")
    p.add_argument("--block", default="latest", help="Block number or tag for comparison (default: latest)")
    p.add_argument("--timeout", type=int, default=30, help="RPC timeout in seconds (default: 30)")
    p.add_argument("--json", action="store_true", help="Emit results in JSON format")
    return p.parse_args()

def main() -> None:
    start_time = time.time()
    args = parse_args()

    # Basic RPC sanity check
    if not args.rpc.startswith("http"):
        print("❌ Invalid RPC URL format. It must start with 'http' or 'https'.")
        sys.exit(1)

    w3 = Web3(Web3.HTTPProvider(args.rpc, request_kwargs={"timeout": args.timeout}))
    if not w3.is_connected():
        print("❌ RPC connection failed. Check your RPC_URL or --rpc argument.")
        sys.exit(1)

    print("🔧 zk-bytecode-diff")
    print(f"🔗 RPC: {args.rpc}")
    try:
        print(f"🧭 Chain ID: {w3.eth.chain_id}")
    except Exception:
        pass
    print(f"🏷️ Comparing:")
    print(f"   A: {args.address_a}")
    print(f"   B: {args.address_b}")
    print(f"🧱 Block: {args.block}")

    try:
        bytecode_a = get_contract_bytecode(w3, args.address_a, args.block)
        bytecode_b = get_contract_bytecode(w3, args.address_b, args.block)
    except Exception as e:
        print(f"❌ {e}")
        sys.exit(2)

    diff = compare_bytecodes(bytecode_a, bytecode_b)

    print(f"🔹 Hash (A): {diff['hash_a']}")
    print(f"🔸 Hash (B): {diff['hash_b']}")
    if diff["identical"]:
        print("✅ Bytecodes are identical.")
    else:
        print(f"⚠️ Bytecodes differ! Length delta: {diff['diff_length']} bytes")

    elapsed = time.time() - start_time
    print(f"⏱️ Completed in {elapsed:.2f}s")

    if args.json:
        out = {
            "rpc": args.rpc,
            "chain_id": None,
            "address_a": Web3.to_checksum_address(args.address_a),
            "address_b": Web3.to_checksum_address(args.address_b),
            "block": args.block,
            "result": diff,
            "elapsed_seconds": round(elapsed, 2)
        }
        try:
            out["chain_id"] = w3.eth.chain_id
        except Exception:
            pass
        print(json.dumps(out, ensure_ascii=False, indent=2))

    sys.exit(0 if diff["identical"] else 2)

if __name__ == "__main__":
    main()
