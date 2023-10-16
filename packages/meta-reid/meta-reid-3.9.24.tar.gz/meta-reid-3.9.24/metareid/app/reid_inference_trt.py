import os
import cv2
import tqdm
import glob
import numpy as np
from ..utils import fast_dot
from ..model_zoo import TrtEngine


def list_files(target_dir, pattern):
    file_pattern = target_dir + "/" + pattern
    files = glob.glob(file_pattern)
    return files


def list_dirs(target_dir):
    result = []
    for item in os.listdir(target_dir):
        if os.path.isdir(os.path.join(target_dir, item)):
            result.append(item)
    return result


class ReidInferenceTrt:
    def __init__(self,
                 trt_file="models/baseline_R50.trt",
                 new_size=(224, 224),
                 gpu_idx=0,
                 batch_size=24,
                 class_nums=19,
                 use_gpu=False,
                 total_memory=5000,
                 query_file_path='models/query_files.npy',
                 query_name_path='models/query_names.npy',
                 query_feature_path='models/query_features.npy',
                 query_image_path='models/query_images.npy'):
        self.new_size = new_size
        self.model = TrtEngine(trt_file, gpu_idx=gpu_idx, batch_size=batch_size)
        self.query_file_path = query_file_path
        self.query_name_path = query_name_path
        self.query_feature_path = query_feature_path
        self.query_image_path = query_image_path
        self.total_memory = total_memory
        self.query_files, self.query_names, self.query_features, self.query_images = self.load_features()
        self.use_gpu = use_gpu
        self.invert_index = self.get_invert_index(n_list=class_nums) if self.use_gpu else None

    def predict(self, image):
        # rgb
        if not isinstance(image, list): image = [image]
        return self.model.inference_on_images(image, self.new_size)

    def load_features(self, ):
        query_files, query_names, query_features, query_images = None, None, None, None
        if os.path.exists(self.query_file_path):
            query_files = np.load(self.query_file_path)
        if os.path.exists(self.query_name_path):
            query_names = np.load(self.query_name_path)
        if os.path.exists(self.query_feature_path):
            query_features = np.load(self.query_feature_path)
        if os.path.exists(self.query_image_path):
            query_images = np.load(self.query_image_path)

        return query_files, query_names, query_features, query_images

    def update_features(self, query_file: str, query_name: str, query_feature: np.ndarray, query_image: np.ndarray):
        if True in np.isnan(query_feature):
            print(query_file)
            return

        if self.query_names is not None:
            self.query_files = np.append(self.query_files, query_file)
            self.query_names = np.append(self.query_names, query_name)
            self.query_features = np.vstack([self.query_features, query_feature])
            self.query_images = np.vstack([self.query_images, query_image])
        else:
            self.query_files = np.array([query_file])
            self.query_names = np.array([query_name])
            self.query_features = query_feature
            self.query_images = query_image

        if len(self.query_names) > self.total_memory:
            t = len(self.query_names) - self.total_memory
            self.query_files = self.query_files[t:]
            self.query_names = self.query_names[t:]
            self.query_features = self.query_features[t:]
            self.query_images = self.query_images[t:]

    def remove_features(self, idx):
        if len(self.query_names) > idx:
            self.query_files = self.query_files[idx + 1:]
            self.query_names = self.query_names[idx + 1:]
            self.query_features = self.query_features[idx + 1:]
            self.query_images = self.query_images[idx + 1:]

    def save_features(self):
        np.save(self.query_file_path, self.query_files)
        np.save(self.query_name_path, self.query_names)
        np.save(self.query_feature_path, self.query_features)
        np.save(self.query_image_path, self.query_images)

    def save_folder(self, img_dir):
        query_name = img_dir.split('/')[-1]
        img_files = list_files(img_dir, "*.jpg")
        for img_file in tqdm.tqdm(img_files):
            query_image = cv2.imread(img_file)[:, :, ::-1]
            query_feature = self.predict(query_image)
            self.update_features(os.path.basename(img_file), query_name, query_feature, query_image)

    def save_folders(self, root_dir):
        dirs = list_dirs(root_dir)
        for d in dirs:
            self.save_folder(os.path.join(root_dir, d))

        self.save_features()

    def index(self, features, min_score, recall_num=1):
        if self.query_features is None:
            return [[]] * len(features), [[]] * len(features)

        if self.use_gpu:
            D, I = self.invert_index.search(features, recall_num)

            return I[0].tolist(), D[0].tolist()
        else:
            max_idxes, maximums = [], []
            index_cossims = fast_dot(features, self.query_features.T)
            for index_cossim in index_cossims:
                if len(self.query_features) > recall_num:
                    max_idx = np.intersect1d(np.where(index_cossim > np.sort(index_cossim)[-recall_num - 1]),
                                             np.where(index_cossim > min_score))
                else:
                    max_idx = np.where(index_cossim > min_score)[0]
                maximum = index_cossim[max_idx]
                max_idxes.append(max_idx)
                maximums.append(maximum)

            return max_idxes, maximums

    def get_invert_index(self, n_list=19):
        import faiss

        d = len(self.query_features[0])
        quantizer = faiss.IndexFlatL2(d)
        index = faiss.IndexIVFFlat(quantizer, d, n_list, faiss.METRIC_L2)
        assert not index.is_trained
        index.train(self.query_features)
        assert index.is_trained
        index.add(self.query_features)
        index.nprobe = 700

        return index
