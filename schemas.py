from typing import Optional

from pydantic import BaseModel


class MetricaIn(BaseModel):
    servidor: str
    ip_local: str
    internet: str
    latencia_ms: float
    cpu_porcentaje: float
    ram_porcentaje: float
    ram_usada_gb: float
    ram_total_gb: float
    disco_porcentaje: float
    disco_usado_gb: float
    disco_total_gb: float
    uptime_segundos: int
    os: Optional[str] = None
    os_version: Optional[str] = None
    arquitectura: Optional[str] = None
    usuario: Optional[str] = None
    mac_address: Optional[str] = None
    python_version: Optional[str] = None
