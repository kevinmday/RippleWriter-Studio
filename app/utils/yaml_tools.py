from pathlib import Path
import yaml

# ------------------------------------------------------
# Resolve RippleWriter project root automatically
# ------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]

YAML_ROOT = PROJECT_ROOT / "yaml"

SYSTEM_DIR = YAML_ROOT / "system"
TEMPLATES_DIR = YAML_ROOT / "templates"
MODELS_DIR = YAML_ROOT / "models"


# ------------------------------------------------------
# Helpers
# ------------------------------------------------------
def load_yaml(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception as e:
        return {"error": str(e)}


def save_yaml(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, sort_keys=False, allow_unicode=True)


def list_yaml_files(directory):
    path = Path(directory)
    if not path.exists():
        return []
    return list(path.glob("*.yaml"))


# ------------------------------------------------------
# High-level project loaders
# ------------------------------------------------------
def list_system_files():
    return list_yaml_files(SYSTEM_DIR)

def list_templates():
    return list_yaml_files(TEMPLATES_DIR)

def list_models():
    return list_yaml_files(MODELS_DIR)


def load_system(name):
    return load_yaml(SYSTEM_DIR / name)

def load_template(name):
    return load_yaml(TEMPLATES_DIR / name)

def load_model(name):
    return load_yaml(MODELS_DIR / name)
