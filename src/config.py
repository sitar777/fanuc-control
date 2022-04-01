from src.models.fanuc import FanucPoint


class Settings:
    FANUC_HOST = "192.168.31.150"
    FANUC_PORT = 59002
    VERSION = "0.0.1"
    FANUC_HOME = FanucPoint(
        x=985,
        y=0,
        z=940,
        w=-180,
        p=0,
        r=0,
    )
    SERVER_NAME = "ZTESTSEM2"


settings = Settings()
