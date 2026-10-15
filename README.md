# NeuralCore MetalPatch: MLX-LM ArraysCache deferred-advance experiment

## Overview
An experimental modification to `mlx_lm/models/cache.py` (`ArraysCache`) intended to avoid persistent chains of lazy Metal/MLX array operations during repeated cache advancement. It retains publicly observable `lengths` and `left_padding` metadata via properties, defers integer advances, and flushes pending updates at state boundaries. This may reduce repeated metadata allocations, but **does not establish that a full-model Metal resource leak is fixed**.

## Upstream reference
- Project: https://github.com/ml-explore/mlx-lm
- Pinned upstream commit: `ba8a08fd2ed72bbc53de84f89933f91fe4743e4a`
- File: `mlx_lm/models/cache.py`
- Original upstream SHA-256: `c96cb169fd5e0ec4584a162dd61dc62ab08ccdca03a9850f8a491ce6809145e6`
- Current packaged patched source SHA-256: `4183088f8504e55353bbd5db16d43e8a32d9e68773d7cce1f1097c785186b465`.
- Investigation 029 README historically recorded SHA-256 `25c43a69b74e6dc5111217be452126acff7efa50799da9136500702be5ca41`, which does **not** match the current file. The discrepancy is preserved for review before upstream submission; do not assert these are identical versions.

## Contents
- `arrays_cache.diff`: unified patch against pinned MLX-LM source.
- `cache.patched.py`: complete candidate `cache.py` for inspection; **do not replace installed libraries blindly**.
- `test_patch.py`, `windows_test_log.txt`: offline property and lifecycle regression evidence.
- `MetalPatch_Mac_Test.zip`: Apple Silicon MLX smoke/regression package (`run_on_mac.command`, `test_mlx_cache.py`, reference sources and README).

## Testing completed
- Windows/NumPy stand-in testing: Investigation 029 8/8 passed; Investigation 030 additional 5/5 passed, including nonempty merge/extract and Qwen-style metadata access.
- User-run Apple Silicon MLX 0.29.3 tests on macOS 27.0.1 arm64: `interleaved`, `filter`, `extend`, `state_roundtrip`, `setters`, `repeated_advances` all reported PASS. A second run requested 20,000 advances and also reported six PASS categories, failures 0. These are user-provided terminal results; raw Mac JSON logs are not included in this package.

## Important limitations
- No confirmed full Qwen3.5-397B inference test, measured GPU resource counts, sustained leak elimination, speed improvement or upstream acceptance.
- Apple test results show functional regression success, not proof of resource-leak resolution.
- `mx.eval` synchronization, transient lazy-expression allocations and compatibility with future MLX-LM versions require review.
- Pinned upstream commit may differ from current main; rebase and review before upstream pull request.
- Do not upload private research archives, owner passwords, certificate keys or unrelated NeuralCore data.

## Suggested upstream workflow
Review diff, reproduce tests, compare memory/Metal allocation under a real workload, and open a focused pull request against MLX-LM if upstream maintainers find the approach useful. Include exact source revision and known limitations.

## License
This is a modification of upstream MLX-LM source. Preserve upstream copyright and license terms. Consult the upstream repository's LICENSE for redistribution requirements.
