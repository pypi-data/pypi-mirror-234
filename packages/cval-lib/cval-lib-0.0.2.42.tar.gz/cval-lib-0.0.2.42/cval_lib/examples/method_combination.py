import math
import random
import uuid
from pprint import pprint
from time import sleep

from cval_lib.connection import CVALConnection
from cval_lib.models.detection import DetectionSamplingOnPremise
from cval_lib.models.embedding import FrameEmbeddingModel, EmbeddingModel


def get_scores(num_images: int, num_bboxes: int, categ_sz: int):
    _predictions = []
    for i in range(num_images):
        scr = []
        image_name = str(uuid.uuid4().hex)
        for boxs in range(num_bboxes):
            _id = uuid.uuid4().hex
            scr.append(
                {
                    'embedding_id': uuid.uuid4().hex,
                    "score": math.cos(random.random()),
                    "category_id": random.randint(0, categ_sz),
                },
            )
        _predictions.append(
            {
                "frame_id": image_name,
                "predictions": scr,
            },
        )
    return _predictions


def get_embeddings(_frames: list[str], _predictions, emb_sz=500):
    _embeddings = []
    for i in _frames:
        for j in _predictions:
            if i == j.get('frame_id'):
                emb = [
                    EmbeddingModel(**{
                        "embedding_id": k.get('embedding_id'),
                        "embedding": list(map(lambda x: random.random(), range(emb_sz))),
                    }) for k in j.get('predictions')
                ]

                _embeddings.append(
                    FrameEmbeddingModel(**{
                        "frame_id": j.get('frame_id'),
                        "embeddings": emb,
                    }),
                )
    return _embeddings


predictions = get_scores(500, 14, 1)

USER_API_KEY = 'USER_API_KEY'
detector = CVALConnection(USER_API_KEY)
ds_id = detector.dataset().create(name='asd', description='1a2')
print(ds_id)

task_id = detector.detection().on_premise_sampling(
    DetectionSamplingOnPremise(
        num_of_samples=20,
        dataset_id=ds_id,
        selection_strategy='entropy',
        sort_strategy='ascending',
        bbox_selection_policy='sum',
        frames=predictions,
    )
).task_id

result = None
sleep_sec = 1


while result is None:
    result = detector.result().get(task_id).result
    print(f'Polling... {sleep_sec}')
    sleep(sleep_sec)
    sleep_sec *= 2

pprint(result)

detector.embedding(dataset_id=ds_id, part_of_dataset='training').upload_many(get_embeddings(result, predictions))
task_id = detector.detection().on_premise_sampling(
    DetectionSamplingOnPremise(
        num_of_samples=2,
        dataset_id=ds_id,
        mc_task_id=task_id,
        selection_strategy='clustering',
        frames=list(filter(lambda x: x.get('frame_id') in result, predictions)),
    )
).task_id


result = None
sleep_sec = 1
while result is None:
    result = detector.result().get(task_id).result
    print(f'Polling... {sleep_sec}')
    sleep(sleep_sec)
    sleep_sec *= 2
pprint(result)
