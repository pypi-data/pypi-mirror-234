import math
import random
import uuid
from time import sleep

from cval_lib.connection import CVALConnection
from cval_lib.models.detection import DetectionSamplingOnPremise
from cval_lib.models.embedding import FrameEmbeddingModel, EmbeddingModel


def get_frames(num_images: int, num_bboxes: int, emb_sz: int, categ_sz: int):
    _predictions = []
    _embeddings = []
    for i in range(num_images):
        emb = []
        scr = []
        image_name = str(uuid.uuid4().hex)
        for boxs in range(num_bboxes):
            _id = uuid.uuid4().hex
            scr.append(
                {
                    "embedding_id": _id,
                    "score": math.cos(random.random()),
                    "category_id": random.randint(0, categ_sz),
                },
            )
            emb.append(
                EmbeddingModel(**{
                    "embedding_id": _id,
                    "embedding": list(map(lambda x: random.random(), range(emb_sz))),
                })
            )

        _embeddings.append(
            FrameEmbeddingModel(**{
                "frame_id": image_name,
                "embeddings": emb,
            }),
        )
        _predictions.append(
            {
                "frame_id": image_name,
                "predictions": scr,
            },
        )
    return _embeddings, _predictions


embeddings, predictions = get_frames(100, 1, 500, 1)
USER_API_KEY = 'USER_API_KEY'
detector = CVALConnection(USER_API_KEY)
ds_id = detector.dataset().create(name='asd', description='1a2')
print(ds_id)
print(detector.embedding(dataset_id=ds_id, part_of_dataset='training').upload_many(embeddings))
task_id = detector.detection().on_premise_sampling(
    DetectionSamplingOnPremise(
        num_of_samples=20,
        dataset_id=ds_id,
        selection_strategy='clustering',
        frames=predictions,
        bbox_selection_policy='sum',
    )
).task_id

result = None
sleep_sec = 1
while result is None:
    result = detector.result().get(task_id).result
    print(f'Polling... {sleep_sec}')
    sleep(sleep_sec)
    sleep_sec *= 2

print(result)
