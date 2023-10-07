<!-- TOP OF README ANCHOR -->
<a name="top"></a>
<!-- PROJECT LOGO -->
<br />
<div align="center">
  <p>
    <img src="https://github.com/fangorntreabeard/cval-lib/blob/main/images/logo.jpg?raw=true" alt="Cval logo" width="155" height="155">
  </p>
<h3 align="center">CVAL REST API LIBRARY</h3>
  <p align="center">
    A library designed to interact with the REST-API cval.ai
    <br/>
    <b>
      <a href="https://github.com/fangorntreabeard/cval-lib/tree/main/docs"> Library docs </a> 
      ·
      <a href="https://cval.ai">REST API docs</a>
      ·
      <a href="https://colab.research.google.com/drive/1f93b-aCv4MacngujLVUcQBJ9T1mJZBKH?usp=sharing"> Google Colaboratory Demo </a>
      ·
      <a href="https://github.com/fangorntreabeard/cval-lib/issues">Report Bug</a>
   </b>
  </p>
</div>

# About

With CVAL, you can iteratively **improve your models** by following our active learning loop.

* **First**, manually or semi-automatically annotate a random set of images.

* **Next**, train your model and use uncertainty and diversity methods to score the remaining images for annotation.

* **Then**, manually or semi-automatically annotate the images marked as more confident to increase the accuracy of the model.

Repeat this process until you achieve an acceptable quality of the model.

# Getting started

To start using the CVAL Rest API, you need to **obtain** a **client/user API key**. 
Once you have your API key, you can use it to authenticate your requests and interact with the CVAL Rest API endpoints. 
Refer to our API documentation for detailed information on available endpoints, request formats, and response structures.

## Installation

#### Unix and Mac
```shell
python3 -m pip install cval-lib
```
or downloaded:

```shell
python3 -m pip install cval-lib.tar
```

#### Windows
```powershell
python -m pip install cval-lib
```
or downloaded:
```shell
python3 -m pip install cval-lib.tar
```

#### Submodule
```shell
git submodule add https://github.com/fangorntreabeard/cval-lib.git cval
```
## Architecture
The library architecture consists of **three layers**:
1. _A layer of protocols and abstract handlers_. Responsible for the use of a particular library. If an error is found, it is enough to simply change one method.
2. _A layer of handlers._ These are all the methods that are present in the API. Are based on abstract
3. _Model layer._ If the data structure changes, only this layer changes.

## Examples

##### Set your user_api_key

```python3
from cval_lib.connection import CVALConnection
USER_API_KEY = 'awesome_api_key'
cval = CVALConnection(USER_API_KEY)
```

> The same actions are available with the rest of the entities, but there are some nuances, for example, somewhere there is the use of models, and somewhere only parameters. But anyway, these examples well reflect possible scenarios when working with cval. The most typical api scenario is a dataset, so let's start with it.

### Dataset
 > Within the framework of the created system, datasets are spaces in which data for machine learning is stored.
 Creating a dataset is similar to creating a folder.
##### Create dataset
```python3
# :NOTE: To avoid incomprehensibility of errors, it is recommended to use  CVALConnection
ds_id = cval.dataset().create(name='on-premise-scheme-ds', description='')
print(ds_id)
```

##### Update dataset
```python3
ds = cval.dataset()
print(ds.update(ds_id, description='any string data'))
# :NOTE: the dataset can store the state (ds_id)
ds.update(name='sample name')
```

##### Get dataset
```python3
print(ds.get())
```

> A further example of using the library concerns embedding. Since embedding is a large data object and the method of its creation is completely defined by the user, the embedding method works through query schemes (models).

### Embeddings

> Embeddings are vector representations of images obtained using pytorch or any other library

##### Create embeddings

```python3
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
```


##### Upload & check embeddings

```python3
emb = cval.embedding(ds_id, 'training')
emb.upload_many(embeddings)
print(emb.get_many())
```

> The following example is used to invoke active learning
 
### Active learning

##### Get predictions data

```python3
from random import random
import uuid
from cval_lib.models.detection import BBoxScores, FramePrediction

# :NOTE: example only
frames_predictions = list(
    map(
        lambda x: FramePrediction(
            frame_id=str(uuid.uuid4().hex),
            predictions=list(
                map(lambda x: BBoxScores(category_id=str(uuid.uuid4()), score=random()), range(100)))
        ),
        range(10)
    )
)
print(frames_predictions)

```

##### Construct config

```python3
from cval_lib.models.detection import DetectionSamplingOnPremise
request = DetectionSamplingOnPremise(
 num_of_samples=200, 
 bbox_selection_policy='min', 
 selection_strategy='margin', 
 sort_strategy='ascending',
 frames=frames_predictions,
)
```

##### Run active learning
```python3
emb = cval.detection()
print(emb.on_premise_sampling(request))
```
> The following method is most relevant when we are dealing with long-term tasks and, accordingly, with asynchronous interaction.
##### Polling
> refers to actively sampling the status of an external device by a client program as a synchronous activity.

```python3
import uuid
from random import random
from time import sleep

from cval_lib.connection import CVALConnection
from cval_lib.models.detection import DetectionSamplingOnPremise, FramePrediction, BBoxScores

frames_predictions = list(
        map(
            lambda x: FramePrediction(
                frame_id=str(uuid.uuid4().hex),
                predictions=list(map(lambda _: BBoxScores(category_id=str(uuid.uuid4()), score=random()), range(100)))
            ),
            range(1000)
        )
    )

request = DetectionSamplingOnPremise(
        num_of_samples=200,
        bbox_selection_policy='min',
        selection_strategy='margin',
        sort_strategy='ascending',
        frames=frames_predictions,
    )
emb = cval.detection()
print(emb.on_premise_sampling(request))

result = None
sleep_sec = 1
while result is None:
    result = emb.result.get().result
    print(f'Polling... {sleep_sec} s')
    sleep(sleep_sec)
    sleep_sec *= 2

print(result)
```
