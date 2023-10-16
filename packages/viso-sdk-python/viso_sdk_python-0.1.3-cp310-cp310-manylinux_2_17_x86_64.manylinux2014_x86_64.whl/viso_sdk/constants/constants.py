
# =====================================================================================================================
# architectures
class ARCHITECTURE:
    AMD64 = "amd64"
    ARMV7HF = "armv7hf"
    AARCH64 = "aarch64"


# =====================================================================================================================
# frameworks
class FRAMEWORK:
    TF = "tensorflow"
    TF_GPU = "tensorflow_gpu"
    TF_LITE = "tensorflow_lite"
    OPENVINO = "openvino"
    TORCH = "torch"
    TORCH_GPU = "torch_gpu"
    KERAS = "keras"
    CAFFE = "caffe"


# =====================================================================================================================
# devices
class DEVICE:
    DEFAULT = 'CPU'

    # tensorflow devices
    class TF:
        CPU = "CPU"
        GPU = "nGPU"  # nvidia GPU

    class OPENVINO:
        CPU = "CPU"
        MYRIAD = "MYRIAD"
        GPU = "iGPU"  # intel GPU
        GNA = "GNA"
        # FPGA = "FPGA"
        # HDDL = "HDDL"

    class TF_LITE:
        CPU = "CPU"  # CPU
        eTPU = "eTPU"  # Edge TPU
        GPU = "nGPU"

    class TORCH:
        CPU = "CPU"
        CUDA = "CUDA"

    class CAFFE:
        CPU = "CPU"

    class KERAS:
        CPU = "CPU"


# =====================================================================================================================
SUPPORT_DEVICES = {
    ARCHITECTURE.AMD64: {
        FRAMEWORK.TF: [DEVICE.TF.CPU],
        FRAMEWORK.TF_GPU: [DEVICE.TF.CPU, DEVICE.TF.GPU],
        # TENSORFLOW_LITE: [TF_LITE_CPU, TF_LITE_eTPU],  # TF_LITE_nGPU
        FRAMEWORK.OPENVINO: [DEVICE.OPENVINO.CPU, DEVICE.OPENVINO.MYRIAD, DEVICE.OPENVINO.GPU, DEVICE.OPENVINO.GNA],
        # OV_FPGA, OV_HDDL
        FRAMEWORK.TORCH: [DEVICE.TORCH.CPU],
        FRAMEWORK.TORCH_GPU: [DEVICE.TORCH.CPU, DEVICE.TORCH.CUDA],
        FRAMEWORK.CAFFE: [DEVICE.CAFFE.CPU],
        FRAMEWORK.KERAS: [DEVICE.KERAS.CPU]
    },
    ARCHITECTURE.AARCH64: {},
    ARCHITECTURE.ARMV7HF: {}
}


# =====================================================================================================================
# model types
class MODEL_TYPE:
    INTERNAL = "internal"
    TF_V1 = "TF_V1"
    TF_V2 = "TF_V2"
    TF_YOLO = "TF_YOLO"
    OPENVINO = "OPENVINO"
    TF_LITE = "TF_LITE"
    TORCH = "TORCH"
    KERAS = "KERAS"
    CAFFE = "CAFFE"


# =====================================================================================================================
# detection object attributes
class KEY:
    CLASS_ID = "class_id"
    SCORE = "confidence"
    LABEL = "label"
    TLWH = "rect"
    ROI_ID = 'roi_id'
    ROI_NAME = "roi_name"


# ----- [MQTT & REDIS] ----------------------------------------------------------
class PREFIX:

    class REDIS:
        LOCAL = "redis"
        STATUS = "viso/container_status"

    class MQTT:
        LOCAL = "viso/mqtt"
        CLOUD = "viso_cloud/mqtt"

        DEBUG = "viso_debug/mqtt"
