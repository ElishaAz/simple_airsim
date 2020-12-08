import enum

import airsim


class ImageType(enum.Enum):
    def __init__(self, airsim_val):
        self.airsim_val = airsim_val

    DEPTH = (airsim.ImageType.DepthVis,)
    SEGMENTATION = (airsim.ImageType.Segmentation,)
    VISUAL = (airsim.ImageType.Scene,)
    DISPARITY = (airsim.ImageType.DisparityNormalized,)
    NORMALS = (airsim.ImageType.SurfaceNormals,)


class ReturnType(enum.Enum):
    def __init__(self, id: int, format: str, with_alpha: bool):
        self.with_alpha = with_alpha
        self.format = format
        self.id = id

    RGB_A = (1, "RGB", True)
    RGB = (2, "RGB", False)
    BGR_A = (3, "BGR", True)
    BGR = (4, "BGR", False)
