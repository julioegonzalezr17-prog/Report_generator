# magic_logger.py
import logging
from logging import Logger
import os
import sys
from pathlib import Path
from datetime import datetime

def get_log_dir(app_name: str = "mi_app") -> Path:
    """
    Carpeta de logs por plataforma:
    - Windows: %LOCALAPPDATA%/app_name/logs
    - Linux/Mac: ~/.local/share/app_name/logs
    """
    if sys.platform.startswith("win"):
        base = os.environ.get("LOCALAPPDATA") or os.path.expanduser("~")
    else:
        base = os.path.join(os.path.expanduser("~"), ".local", "share")
    log_dir = Path(base) / app_name / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir

def _remove_all_handlers(logger: Logger):
    """Elimina y cierra todos los handlers actuales del logger root."""
    for h in list(logger.handlers):
        logger.removeHandler(h)
        try:
            h.close()
        except Exception:
            pass

def _cleanup_old_logs(log_dir: Path, keep: int = 20, pattern: str = "*.log"):
    """
    Mantiene solo los últimos 'keep' archivos de log según fecha de modificación (descendente).
    """
    try:
        files = sorted(log_dir.glob(pattern), key=lambda p: p.stat().st_mtime, reverse=True)
        for old in files[keep:]:
            try:
                old.unlink(missing_ok=True)
            except Exception:
                pass
    except Exception:
        # Si por permisos u otros motivos no se puede limpiar, lo ignoramos silenciosamente
        pass

def setup_per_run_logging(
    app_name: str = "mi_app",
    level: int = logging.INFO,
    to_console: bool = True,
    keep_last: int = 20,         # <-- mantener 20 logs
    latest_alias: bool = True,
) -> Path:
    """
    Crea un logger 'un log por ejecución' con nombre único:
    app_name_YYYYMMDD_HHMMSS_pidXXXXX.log
    Devuelve la ruta del archivo de log activo.
    """
    logger = logging.getLogger()
    _remove_all_handlers(logger)
    logger.setLevel(level)

    log_dir = get_log_dir(app_name)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    pid = os.getpid()
    log_path = log_dir / f"{app_name}_{ts}_pid{pid}.log"

    # Formato detallado
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(threadName)s | "
        "%(funcName)s:%(lineno)d | %(message)s",
        "%Y-%m-%d %H:%M:%S",
    )

    # Archivo (modo 'w' crea el archivo inmediatamente)
    file_handler = logging.FileHandler(str(log_path), encoding="utf-8", mode="w")
    file_handler.setFormatter(formatter)
    file_handler.setLevel(level)
    logger.addHandler(file_handler)

    # Consola (opcional)
    if to_console:
        console = logging.StreamHandler(sys.stdout)
        console.setFormatter(formatter)
        console.setLevel(level)
        logger.addHandler(console)

    # Alias 'latest.log' apuntando al último (útil para abrir rápido)
    if latest_alias:
        latest = log_dir / "latest.log"
        try:
            if latest.exists():
                latest.unlink()
            # Intentamos crear hard link (en NTFS suele funcionar). Si falla, dejamos un file con referencia.
            try:
                os.link(log_path, latest)
            except Exception:
                with latest.open("w", encoding="utf-8") as f:
                    f.write(f"# Último log: {log_path}\n")
        except Exception:
            pass

    # Limpieza de logs antiguos (mantener 'keep_last')
    if keep_last and keep_last > 0:
        _cleanup_old_logs(log_dir, keep=keep_last)
    logging.getLogger("matplotlib").setLevel(logging.WARNING)
    logger.info("Logging (per-run) inicializado. Archivo: %s", log_path)
    
    logging.captureWarnings(True)
    logging.getLogger().setLevel(logging.DEBUG)

    return log_path

