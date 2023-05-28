from pathlib import Path

root_path: Path = Path(__file__).parent.parent.resolve()
lib_path: Path = Path(root_path, 'source')

lib_path.mkdir(parents=True, exist_ok=True)
