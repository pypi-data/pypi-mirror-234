import copy
import json
import os
from pathlib import Path
from random import sample
from typing import Union

from cval_lib.models.frame import FrameModel


class Annotation:
    def __init__(self, path_to_coco_train: Union[str, Path]):
        self.path_to_dataset = path_to_coco_train
        with open(path_to_coco_train) as f:
            self.annotation = json.load(f)
        self.categories = self.annotation['categories']
        self.annotations = self.annotation['annotations']
        self.images = self.annotation['images']
        self.info = self.annotation['info']
        self.licenses = self.annotation['licenses']
        self.photo_ids = list(set(map(lambda x: x['image_id'], self.annotations)))

    def __len__(self):
        return len(self.photo_ids)

    def make_random(
            self,
            num_of_frames: int,
            current_label: int = 1,
    ):
        if num_of_frames < 0:
            return
        all_photo_id = sample(self.photo_ids, k=num_of_frames)
        new_annotation = []
        for row in self.annotations:
            if all([
                row['category_id'] == current_label,
                row['image_id'] in all_photo_id,
            ]):
                row_copy = copy.deepcopy(row)
                row_copy['segmentation'] = []
                new_annotation.append(row_copy)

        good_images_ids = list(set(map(lambda x: x['image_id'], new_annotation)))
        print('zero file {} / {}'.format(len(good_images_ids), num_of_frames))
        new_image = []

        for row in self.images:
            if row['id'] in all_photo_id:
                new_image.append(copy.deepcopy(row))

        with open(Path(self.path_to_dataset).parent.joinpath('first.json'), 'w') as f:
            f.write(json.dumps(self.new_coco_dataset(new_annotation, new_image)))
        return Path(self.path_to_dataset).parent.joinpath('first.json')

    def new_coco_dataset(self, new_annotation, new_image):
        return dict(
            annotations=new_annotation,
            images=new_image,
            categories=self.categories,
            info=self.info,
            licenses=self.licenses,
        )

    def make_al(
            self,
            list_files: list[str],
            step: int,
            current_label: int = 1
    ):
        new_image = []
        a = []
        for row in self.images:
            if row['file_name'] in list_files:
                a.append(row['id'])
                copy_row = copy.deepcopy(row)
                new_image.append(copy_row)

        new_annotation = []
        for row in self.annotations:
            if row['category_id'] == current_label and row['image_id'] in a:
                copy_row = copy.deepcopy(row)
                copy_row['segmentation'] = []
                new_annotation.append(copy_row)

        print('file {}, {} / {}'.format(
            step,
            len(list(set(map(lambda x: x['image_id'], new_annotation)))),
            len(list_files))
        )

        with open(Path(self.path_to_dataset).parent.joinpath(f'{step}.json'), 'w') as f:
            f.write(json.dumps(self.new_coco_dataset(new_annotation, new_image)))
        return Path(self.path_to_dataset).parent.joinpath(f'{step}.json')


def covert_from_coco(path_to_coco: Union[str, Path, os.PathLike], ):
    with open(path_to_coco, 'r') as f:
        return [
            FrameModel(
                img_external_id=image['coco_url'].split('/')[-1].replace('.jpg', ''),
                img_link=image['coco_url']
            ) for image in json.load(f)['images']
        ]
