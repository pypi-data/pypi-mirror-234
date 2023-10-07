from typing import Union

import pydantic
import pytest

from kognic.io.model.scene.cameras.cameras import Cameras
from kognic.io.model.scene.cameras.cameras import Frame as CFrame
from kognic.io.model.scene.cameras_sequence import CamerasSequence
from kognic.io.model.scene.cameras_sequence import Frame as CSFrame
from kognic.io.model.scene.metadata.metadata import MetaData


def build_scene(metadata: Union[MetaData, dict]):
    return Cameras(external_id="ext-id", frame=CFrame(images=list()), metadata=metadata)


def build_sequence_scene(metadata: Union[MetaData, dict]):
    frame = CSFrame(metadata=metadata, frame_id="frame-id", relative_timestamp=0)
    return CamerasSequence(external_id="ext-id", frames=[frame])


def run_test(metadata: Union[MetaData, dict]):
    scene = build_scene(metadata)
    scene_dict = scene.to_dict()
    metadata_dict = metadata.dict() if isinstance(metadata, MetaData) else metadata
    assert scene_dict["metadata"] == metadata_dict


def run_frame_test(metadata: Union[MetaData, dict]):
    scene = build_sequence_scene(metadata)
    scene_dict = scene.to_dict()
    metadata_dict = metadata.dict() if isinstance(metadata, MetaData) else metadata
    assert scene_dict["frames"][0]["metadata"] == metadata_dict


def test_serialize_empty_metadata():
    run_test(dict())


def test_serialize_region_metadata():
    metadata = MetaData(region="sweden")
    run_test(metadata)


def test_serialize_snake_metadata():
    metadata = {"some_key": "some_value"}
    run_test(metadata)


def test_serialize_camel_metadata():
    metadata = {"someKey": "someValue"}
    run_test(metadata)


def test_serialize_metadata_with_nested_list():
    metadata = {"someKey": ["someValue"]}
    with pytest.raises(pydantic.ValidationError) as e_info:
        build_scene(metadata)


def test_serialize_metadata_with_nested_dict():
    metadata = {"someKey": {"nested-key": "nested-value"}}
    with pytest.raises(pydantic.ValidationError) as e_info:
        build_scene(metadata)


def test_serialize_empty_frame_metadata():
    run_frame_test(dict())


def test_serialize_snake_frame_metadata():
    metadata = {"some_key": "some_value"}
    run_frame_test(metadata)


def test_serialize_camel_frame_metadata():
    metadata = {"someKey": "someValue"}
    run_frame_test(metadata)
