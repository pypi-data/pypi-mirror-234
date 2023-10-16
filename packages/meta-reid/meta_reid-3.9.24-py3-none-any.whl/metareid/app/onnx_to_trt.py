from ..model_zoo import EngineBuilder


class Onnx2Trt:
    def __init__(self,
                 onnx_file="models/hand.onnx",
                 trt_file="models/hand.trt",
                 precision="fp16",
                 verbose=False,
                 workspace=4,
                 end2end=False,
                 conf=0.01,
                 iou=0.45,
                 max_det=100,
                 v8=False):
        self.onnx_file = onnx_file
        self.trt_file = trt_file
        self.precision = precision
        self.verbose = verbose
        self.workspace = workspace
        self.calib_input = False
        self.calib_cache = "calibration.cache"
        self.calib_num_images = 5000
        self.calib_batch_size = 8
        self.end2end = end2end
        self.conf = conf
        self.iou = iou
        self.max_det = max_det,
        self.v8 = v8

    def convert(self):
        builder = EngineBuilder(self.verbose, self.workspace)
        builder.create_network(self.onnx_file, self.end2end, self.conf, self.iou, self.max_det, v8=self.v8)
        builder.create_engine(self.trt_file, self.precision, self.calib_input, self.calib_cache, self.calib_num_images,
                              self.calib_batch_size)
