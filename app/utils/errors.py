# ==========================================================
#  RippleWriter Studio — Friendly Error Messaging
# ==========================================================

class RWErrorCodes:
    """Standard RippleWriter error codes."""
    YAML_NOT_FOUND = "RW-YAML-001"
    YAML_PARSE_ERROR = "RW-YAML-002"
    NETWORK_UNAVAILABLE = "RW-NET-001"
    RSS_FETCH_FAILED = "RW-RSS-001"


def friendly_yaml_error(path: str) -> str:
    """
    Returns a friendly, user-facing error message for missing YAML files.
    """
    return (
        f"**{RWErrorCodes.YAML_NOT_FOUND}: Missing YAML file**\n\n"
        f"RippleWriter could not find the required settings file:\n"
        f"`{path}`\n\n"
        "Fix:\n"
        "• Make sure the file exists in the `/app/yaml/system/` folder.\n"
        "• If you recently moved folders, restart RippleWriter.\n"
    )


def friendly_yaml_parse_error(path: str, details: str) -> str:
    return (
        f"**{RWErrorCodes.YAML_PARSE_ERROR}: YAML Format Issue**\n\n"
        f"RippleWriter found the file but could not read it:\n"
        f"`{path}`\n\n"
        f"Details: `{details}`\n\n"
        "Fix:\n"
        "• Look for indentation mistakes or missing colons.\n"
        "• Validate the YAML using an online linter.\n"
    )


def friendly_network_error(details: str) -> str:
    return (
        f"**{RWErrorCodes.NETWORK_UNAVAILABLE}: Network Problem**\n\n"
        "RippleWriter could not connect to the internet to fetch news feeds.\n"
        f"Details: `{details}`\n\n"
        "Fix:\n"
        "• Check your internet connection.\n"
        "• Some corporate/VPN networks block RSS.\n"
        "• Try again in a few minutes.\n"
    )


def friendly_rss_error(source: str, details: str) -> str:
    return (
        f"**{RWErrorCodes.RSS_FETCH_FAILED}: RSS Fetch Failed**\n\n"
        f"Source: `{source}`\n"
        f"Details: `{details}`\n\n"
        "Fix:\n"
        "• The news service may be temporarily offline.\n"
        "• It may require HTTPS-only.\n"
        "• RSS URLs sometimes change — check the settings file.\n"
    )
