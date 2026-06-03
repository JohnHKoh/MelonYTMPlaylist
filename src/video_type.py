from enum import StrEnum

class VideoType(StrEnum):
    ATV = "MUSIC_VIDEO_TYPE_ATV"
    OMV = "MUSIC_VIDEO_TYPE_OMV"
    UGC = "MUSIC_VIDEO_TYPE_UGC"
    UNKNOWN = "UNKNOWN"

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN
