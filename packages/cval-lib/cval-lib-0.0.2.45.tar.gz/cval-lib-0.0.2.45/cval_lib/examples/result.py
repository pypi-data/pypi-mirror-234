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
    user_api_key = '11a6006a98793bb5086bbf6f6808dd6bd9a706a38ddb36c58a484991263e8535'
    cval = CVALConnection(user_api_key)
    print(cval.result().get('ecb8a52b-9bc0-4e56-a496-e69ce74cc0ec'))
    print(cval.result().get(cval.result().get_many()[0].task_id))
