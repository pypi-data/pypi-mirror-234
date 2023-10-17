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


if __name__ == '__main__':
    from cval_lib.connection import CVALConnection

    # set up your user_api_key
    user_api_key = 'USER_API_KEY'
    # set up session
    cval = CVALConnection(user_api_key)
    # choose strategy
    ds = cval.dataset()
    # create your dataset
    ds_id = ds.create()
    print(ds_id)
    # update your dataset
    update = ds.update(name='any')
    print('', update)
    # watch changes
    get = ds.get()
    print(get)
    # also you can use dataset_id for watch changes
    get = ds.get(ds_id)
    print(get)
    # get all datasets
    print(ds.get_all())
