if __name__ == '__main__':
    import random
    import uuid

    from cval_lib.connection import CVALConnection
    from cval_lib.models.detection import (
        DetectionSamplingOnPremise,
        FramePrediction,
        BBoxScores,
    )


    def generate_random_array(sz):
        random_numbers = tuple(map(lambda x: random.random(), range(sz)))
        normalized_numbers = [i/sum(random_numbers) for i in random_numbers]
        return normalized_numbers


    nc = 10
    prediction_per_frame = 100
    frames = 100

    USER_API_KEY = 'USER_API_KEY'

    req = DetectionSamplingOnPremise(
        bbox_selection_policy='max',
        sort_strategy='ascending',
        selection_strategy='entropy',
        probs_weights=list(generate_random_array(nc)),
        num_of_samples=1024,
        frames=[
            FramePrediction(
                frame_id=uuid.uuid4().hex,
                predictions=[
                    BBoxScores(
                        probabilities=list(generate_random_array(nc)),
                    )
                    for _ in range(prediction_per_frame)
                ]
            )
            for _ in range(frames)
        ]
    )

    with CVALConnection(USER_API_KEY) as cval:
        print(cval.detection().on_premise_sampling(req))
