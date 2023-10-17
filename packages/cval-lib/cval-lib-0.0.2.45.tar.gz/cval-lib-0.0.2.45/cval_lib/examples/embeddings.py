"""
Introducing CVAL Rest API, a powerful tool for AI developers in the computer vision field.
Our service combines the concepts of human-in-the-loop and active learning to improve the quality of
your models and minimize annotation costs for classification, detection, and segmentation cases.

With CVAL, you can iteratively improve your models by following our active learning loop.
First, manually or semi-automatically annotate a random set of images.
Next, train your model and use uncertainty and diversity methods to score the remaining images for annotation.
Then, manually or semi-automatically annotate the images marked as more confident to increase the accuracy of the model.
Repeat this process until you achieve an acceptable quality of the model.

Our service makes it easy to implement this workflow and improve your models quickly and efficiently.
Try our demo notebook to see how CVAL can revolutionize your computer vision projects.

To obtain a client_api_key, please send a request to k.suhorukov@digital-quarters.com
"""
import time

if __name__ == '__main__':
    from random import random
    import uuid

    from cval_lib.connection import CVALConnection
    from cval_lib.models.embedding import EmbeddingModel, FrameEmbeddingModel

    embeddings = tuple(
        map(
            lambda x: FrameEmbeddingModel(
                frame_id=uuid.uuid4().hex,
                embeddings=[
                    EmbeddingModel(embedding_id=uuid.uuid4().hex, embedding=list(map(lambda x: random(), range(500))))]
            ),
            range(10_000)
        )
    )

    print(embeddings)
    user_api_key = '50b524bcae7b7bf77e2fcd34fefaf6c7192cbeef1ea55939d5f86a88f42bc809'
    cval = CVALConnection(user_api_key)
    ds = cval.dataset()
    emb = cval.embedding(ds.create(), 'training')
    t0 = time.time()
    emb.upload_many(embeddings)
    t1 = time.time()
    print(t1-t0)
    ds.embedding(part_of_dataset='training').get_many()
    print(emb.get_many())
