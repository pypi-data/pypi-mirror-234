
class MODULE:
    """
        modules container mqtt and redis ports as individual
    """
    class ROI:
        NAME = 'region-of-interest'
        class ROI_TYPE:
            POLYGON = 'polygon'
            RECTANGLE = 'rectangle'
            SECTION = 'section'

    class MULTI_OBJ_DET:
        NAME = "multiple-object-detection"

    class VIDEO_FEED:
        NAME = "video-feed"

    class CLR_REG:
        NAME = 'color-recognition'

    class REID_OBJ_TRK:
        NAME = 'reid-object-tracking'

    class OBJ_CNT:
        NAME = "object-count"


class MODULE2:
    """
        modules publish metadata in redis string together
    """
    class ROI2:
        NAME = 'roi'

        class ROI_TYPE:
            POLYGON = 'polygon'
            RECTANGLE = 'rectangle'
            SECTION = 'section'

    class VIDEO_SOURCE:
        NAME = "video-source"

    class OBJ_DET:
        NAME = "object-detection"

    class OBJ_TRK:
        NAME = 'object-tracking'

    class FRAME_VIEWER:
        NAME = "frame-viewer"
