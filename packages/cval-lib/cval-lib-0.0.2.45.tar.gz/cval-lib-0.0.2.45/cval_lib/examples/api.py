from random import random, randint

if __name__ == '__main__':
    import uuid

    from cval_lib.models.detection import DetectionSamplingOnPremise, FramePrediction, BBoxScores
    from cval_lib.api import CVALEntrypoint

    USER_API_KEY = ...
    ENTRY = CVALEntrypoint(USER_API_KEY)
    frames_predictions = list(
        map(
            lambda x: FramePrediction(
                frame_id=str(uuid.uuid4().hex),
                predictions=list(map(lambda _: BBoxScores(category_id=randint(0, 100), score=random()), range(10)))
            ),
            range(10)
        )
    )
    result = ENTRY.execute(
        request=DetectionSamplingOnPremise(
            num_of_samples=200,
            bbox_selection_policy='min',
            selection_strategy='margin',
            sort_strategy='ascending',
            frames=frames_predictions,
        )
    )
    print(result.result)
