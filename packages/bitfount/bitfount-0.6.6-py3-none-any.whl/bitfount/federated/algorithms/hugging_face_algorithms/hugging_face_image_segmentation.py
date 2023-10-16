"""Hugging Face Image Segmentation Algorithm."""
from __future__ import annotations

import os
from pathlib import Path
import typing
from typing import (
    TYPE_CHECKING,
    Any,
    ClassVar,
    Dict,
    List,
    Literal,
    Mapping,
    Optional,
    Tuple,
    Union,
    cast,
)

import PIL
import cv2  # type: ignore[import] # Reason: No Stubs for module
from marshmallow import fields
from marshmallow.validate import OneOf
import numpy as np
import pandas as pd
from transformers import (
    AutoImageProcessor,
    AutoModelForImageSegmentation,
    pipeline,
    set_seed,
)

from bitfount.config import BITFOUNT_OUTPUT_DIR
from bitfount.data.datasources.base_source import BaseSource
from bitfount.federated.algorithms.base import (
    BaseAlgorithmFactory,
    BaseModellerAlgorithm,
    BaseWorkerAlgorithm,
)
from bitfount.federated.logging import _get_federated_logger
from bitfount.types import T_FIELDS_DICT
from bitfount.utils import DEFAULT_SEED, delegates

if TYPE_CHECKING:
    from bitfount.federated.privacy.differential import DPPodConfig

logger = _get_federated_logger(__name__)

_Subtask = Literal["semantic", "instance", "panoptic"]


class _ModellerSide(BaseModellerAlgorithm):
    """Modeller side of the HuggingFaceImageSegmentationInference algorithm."""

    def initialise(self, task_id: Optional[str] = None, **kwargs: Any) -> None:
        """Nothing to initialise here."""
        pass

    def run(self, results: Mapping[str, Any], log: bool = False) -> Dict[str, Any]:
        """Simply returns results."""
        if log:
            for pod_name, response in results.items():
                for _, response_ in enumerate(response):
                    logger.info(f"{pod_name}: {response_['mask_labels']}")

        return dict(results)


class _WorkerSide(BaseWorkerAlgorithm):
    """Worker side of the HuggingFaceImageSegmentationInference algorithm."""

    def __init__(
        self,
        model_id: str,
        image_column_name: str,
        batch_size: int = 1,
        subtask: Optional[_Subtask] = None,
        threshold: float = 0.9,
        mask_threshold: float = 0.5,
        overlap_mask_area_threshold: float = 0.5,
        seed: int = DEFAULT_SEED,
        alpha: float = 0.3,
        save_path: Union[str, os.PathLike] = BITFOUNT_OUTPUT_DIR,
        dataframe_output: bool = False,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.model_id = model_id
        self.image_column_name = image_column_name
        self.batch_size = batch_size
        self.subtask = subtask
        self.threshold = threshold
        self.mask_threshold = mask_threshold
        self.overlap_mask_area_threshold = overlap_mask_area_threshold
        self.seed = seed
        self.save_path = Path(save_path)
        self.alpha = alpha
        self.dataframe_output = dataframe_output

    def initialise(
        self,
        datasource: BaseSource,
        pod_dp: Optional[DPPodConfig] = None,
        pod_identifier: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """Initialises the model and tokenizer."""
        # TODO: [BIT-3097] Resolve initialise without DP
        if pod_dp:
            logger.warning("The use of DP is not supported, ignoring set `pod_dp`.")
        self.initialise_data(datasource=datasource)
        set_seed(self.seed)
        self.image_processor = AutoImageProcessor.from_pretrained(self.model_id)
        self.model = AutoModelForImageSegmentation.from_pretrained(self.model_id)

        self.pipe = pipeline(
            "image-segmentation",
            model=self.model,
            image_processor=self.image_processor,
        )

    @staticmethod
    def _draw_masks_fromDict(
        image: Path, masks_generated: List[Dict[str, Any]], alpha: float = 0.3
    ) -> Tuple[Any, List[Dict[str, Any]]]:
        """Draw the segmentation masks on the original image.

        Args:
            image: The path to the original image.
            masks_generated: The dictionary with predictions returned
                by the huggingface model.
            alpha: The weight of the first image. Defaults to 0.3.

        """
        # Convert to RGB to account for pngs which add the extra alpha layer
        img = PIL.Image.open(image).convert("RGB")
        orig_image = np.array(img).reshape(img.size[0], img.size[1], 3).copy()
        masked_image = orig_image.copy()
        for i in range(len(masks_generated)):
            masked_image = np.where(
                np.repeat(
                    np.array(masks_generated[i]["mask"]).astype(int)[:, :, np.newaxis],
                    3,
                    axis=2,
                ),
                np.random.choice(range(256), size=3),
                masked_image,
            )

            masked_image = masked_image.astype(np.uint8)
            # Remove masks from prediction dictionary,
            # we will add the path for the image with mask instead
            masks_generated[i].pop("mask")
        return (
            cv2.addWeighted(orig_image, alpha, masked_image, 1 - alpha, 0),
            masks_generated,
        )

    def run(self) -> Union[pd.DataFrame, np.ndarray]:
        """Runs the pipeline to generate text."""
        datasource_images_list = self.datasource.get_column(
            self.image_column_name
        ).tolist()
        preds = self.pipe(
            datasource_images_list,
            batch_size=self.batch_size,
            subtask=self.subtask,
            treshold=self.threshold,
            mask_threshold=self.mask_threshold,
            overlap_mask_area_threshold=self.overlap_mask_area_threshold,
        )
        # Predictions from the above pipeline are returned as a nested
        # list of dictionaries. Each list of dictionaries corresponds
        # to the scores, different labels and masks for a specific datapoint.
        # Since there can be multiple objects in an image, there is no way to
        # nicely output all labels and prediction scores into a csv, hence
        # we make the list for each datapoint into a string and output it
        # together with the path to the image with the masks drawn on it.
        predictions = cast(list, preds)
        # First, draw segmentation on the original image. Images are then
        # saved in the given `save_path` as `<original_filename>-with_mask.png`.
        final_img_path_list = []
        final_prediction_list = []
        for index, item_predictions in enumerate(predictions):
            if len(item_predictions) > 0:
                seg_image, final_predictions = self._draw_masks_fromDict(
                    datasource_images_list[index], item_predictions, self.alpha
                )
                filename = (
                    datasource_images_list[index].split("/")[-1].split(".")[0]
                    + "-with-mask.png"
                )
                img_filename = self.save_path / filename
                # cv2.imwrite expects a string as filename
                cv2.imwrite(str(img_filename), seg_image)
                final_img_path_list.append(img_filename)
                final_prediction_list.append(str(final_predictions))
            else:
                final_img_path_list.append("no mask found")
                final_prediction_list.append("no mask found")
        if self.dataframe_output:
            return pd.DataFrame(
                {
                    "predictions": [str(item) for item in final_prediction_list],
                    "image_with_mask_path": final_img_path_list,
                }
            )
        else:
            return np.column_stack((final_prediction_list, final_img_path_list))


@delegates()
class HuggingFaceImageSegmentationInference(BaseAlgorithmFactory):
    """Inference for pre-trained Hugging Face image segmentation models.

    Perform segmentation (detect masks & classes) in the image(s) passed as inputs.

    Args:
        model_id: The model id to use for image segmentation inference.
            The model id is of a pretrained model hosted inside a model
            repo on huggingface.co. Accepts resnet models.
        image_column_name: The image column on which the inference should be done.
        batch_size: The batch size for inference. Defaults to 1.
        subtask: Segmentation task to be performed, choose [`semantic`,
            `instance` and `panoptic`] depending on model capabilities.
            If not set, the pipeline will attempt to resolve in the
            following order: `panoptic`, `instance`, `semantic`.
        threshold: Probability threshold to filter out predicted masks.
            Defaults to 0.9.
        mask_threshold: Threshold to use when turning the predicted
            masks into binary values. Defaults to 0.5.
        overlap_mask_area_threshold: Mask overlap threshold to eliminate
            small, disconnected segments. Defaults to 0.5.
        alpha: the alpha for the mask overlay.
        seed: Sets the seed of the algorithm. For reproducible behavior
            it defaults to 42.
        save_path: The folder path where the images with masks drawn
            on them should be saved. Defaults to the current working directory.
        dataframe_output: Whether to output the prediction results in a
            dataframe format. Defaults to `False`.

    Attributes:
        model_id: The model id to use for image segmentation inference.
            The model id is of a pretrained model hosted inside a model
            repo on huggingface.co. Accepts resnet models.
        image_column_name: The image column on which the inference should be done.
        batch_size: The batch size for inference. Defaults to 1.
        subtask: Segmentation task to be performed, choose [`semantic`,
            `instance` and `panoptic`] depending on model capabilities.
            If not set, the pipeline will attempt to resolve in the
            following order: `panoptic`, `instance`, `semantic`.
        threshold: Probability threshold to filter out predicted masks.
            Defaults to 0.9.
        mask_threshold: Threshold to use when turning the predicted
            masks into binary values. Defaults to 0.5.
        overlap_mask_area_threshold: Mask overlap threshold to eliminate
            small, disconnected segments. Defaults to 0.5.
        alpha: the alpha for the mask overlay.
        seed: Sets the seed of the algorithm. For reproducible behavior
            it defaults to 42.
        save_path: The folder path where the images with masks drawn
            on them should be saved. Defaults to the current working directory.
        dataframe_output: Whether to output the prediction results in a
            dataframe format. Defaults to `False`.
    """

    def __init__(
        self,
        model_id: str,
        image_column_name: str,
        subtask: Optional[_Subtask] = None,
        threshold: float = 0.9,
        mask_threshold: float = 0.5,
        overlap_mask_area_threshold: float = 0.5,
        seed: int = DEFAULT_SEED,
        batch_size: int = 1,
        save_path: Union[str, os.PathLike] = BITFOUNT_OUTPUT_DIR,
        alpha: float = 0.3,
        dataframe_output: bool = False,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.model_id = model_id
        self.image_column_name = image_column_name
        self.batch_size = batch_size
        self.subtask = subtask
        self.threshold = threshold
        self.mask_threshold = mask_threshold
        self.overlap_mask_area_threshold = overlap_mask_area_threshold
        self.seed = seed
        self.alpha = alpha
        self.save_path = save_path
        self.dataframe_output = dataframe_output

    fields_dict: ClassVar[T_FIELDS_DICT] = {
        "model_id": fields.Str(required=True),
        "image_column_name": fields.Str(required=True),
        "batch_size": fields.Int(required=False),
        "subtask": fields.String(
            validate=OneOf(typing.get_args(_Subtask)), allow_none=True
        ),
        "threshold": fields.Float(required=False),
        "mask_threshold": fields.Float(required=False),
        "overlap_mask_area_threshold": fields.Float(required=False),
        "seed": fields.Int(required=False, missing=DEFAULT_SEED),
        "save_path": fields.Str(required=False, missing=BITFOUNT_OUTPUT_DIR),
        "alpha": fields.Float(required=False),
        "dataframe_output": fields.Bool(required=False, missing=False),
    }

    def modeller(self, **kwargs: Any) -> _ModellerSide:
        """Returns the modeller side of the HuggingFaceImageSegmentationInference algorithm."""  # noqa: B950
        return _ModellerSide(**kwargs)

    def worker(self, **kwargs: Any) -> _WorkerSide:
        """Returns the worker side of the HuggingFaceImageSegmentationInference algorithm."""  # noqa: B950
        return _WorkerSide(
            model_id=self.model_id,
            image_column_name=self.image_column_name,
            batch_size=self.batch_size,
            subtask=self.subtask,
            threshold=self.threshold,
            mask_threshold=self.mask_threshold,
            overlap_mask_area_threshold=self.overlap_mask_area_threshold,
            save_path=self.save_path,
            alpha=self.alpha,
            seed=self.seed,
            dataframe_output=self.dataframe_output,
            **kwargs,
        )
