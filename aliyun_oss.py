import tempfile
import uuid

import numpy as np
import oss2
from PIL import Image


class UploadAliyunOSS:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE", ),
                "object_prefix": ("STRING", {}),
                "access_key": ("STRING", {}),
                "secret_key": ("STRING", {}),
                "endpoint": ("STRING", {}),
                "bucket": ("STRING", {}),
            },
        }

    RETURN_TYPES = ()
    FUNCTION = "upload_aliyun_oss"

    OUTPUT_NODE = True

    CATEGORY = "image"

    def upload_aliyun_oss(self, images, object_prefix, access_key, secret_key, endpoint, bucket):
        auth = oss2.Auth(access_key, secret_key)
        bucket = oss2.Bucket(auth, endpoint, bucket)
        results = list()

        for image in images:
            i = 255. * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))

            with tempfile.NamedTemporaryFile(suffix=".png") as f:
                img.save(f.name)
                obj_name = object_prefix+f'{uuid.uuid4()}.png'

                bucket.put_object_from_file(
                    obj_name, f.name, {"content-type": "image/png"})
                results.append({"object_name": obj_name})

        return {"ui": {"images": results}}
