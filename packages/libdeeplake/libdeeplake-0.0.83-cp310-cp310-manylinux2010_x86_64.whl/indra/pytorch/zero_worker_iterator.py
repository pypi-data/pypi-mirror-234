from typing import Callable, List, Optional
from indra.pytorch.buffered_loader import BufferedLoader
from indra.pytorch.util import (
    transform_collate_batch,
    create_folder,
)
from indra.pytorch.exceptions import (
    TransformExceptionWrapper,
    CollateExceptionWrapper,
)

from indra.pytorch.common import collate_fn as default_collate
from deeplake.integrations.pytorch.common import convert_sample_to_data
from deeplake.core.serialize import bytes_to_text
from uuid import uuid4


from PIL import Image
import traceback

import io
import os

class ZeroWorkerIterator:
    def __init__(
        self,
        dataloader,
        htype_dict: Optional[dict] = None,
        ndim_dict: Optional[dict] = None,
        tensor_info_dict: Optional[dict] = None,
        pil_compressed_tensors: Optional[List[str]] = None,
        raw_tensors: Optional[List[str]] = None,
        json_tensors: Optional[List[str]] = None,
        list_tensors: Optional[List[str]] = None,
        upcast: bool = True,
        transform_fn: Optional[Callable] = None,
        collate_fn: Optional[Callable] = default_collate,
        ignore_errors: bool = True,
        verbose: bool = False,
    ):
        """
        Returns an iterator for single process iteration

        Args:
            htype_dict (dict): Dictionary of the tensors and their corresponding htypes. Only populated for tensors which have data as decode_method.
            ndim_dict (dict): Dictionary of the tensors and their corresponding ndims. Only populated for tensors which have data as decode_method.
            tensor_info_dict (dict): Dictionary of the tensors and their corresponding tensor_info. Only populated for tensors which have data as decode_method and have htype class_label.
            pil_compressed_tensors (List[str], optional) Subset of raw tensors, these will be decompressed by python workers into PIL images.
            raw_tensors (List[str], optional) List of the tensors that needs to return raw data instead of decompression.
                Defaults to ``None`` if raw_tensors is None then all the tensors will send decompression data
                E.g raw_tensors['images'] then only the images tensor data will be sent as a row array
            json_tensors (List[str], optional) Subset of raw tensors, these will be decompressed by python workers into jsons.
            list_tensors (List[str], optional) Subset of raw tensors, these will be decompressed by python workers into lists.
            upcast (bool) flag that is showing whether we need to upcast object if dtype is not supported this is needed only for
                pytorch as it is not support all the dtypes. Defaults to True.
            transform_fn (Callable, optional) Callable object which is needed to be applyed on each sample on batch. Defaults to None.
            collate_fn (callable, optional): merges a list of samples to form a
                mini-batch of Tensor(s).  Used when using batched loading from a
                map-style dataset.
            ignore_errors(bool) shows whether need to ignore the errors appearing during transformation
        """
        self.dataloader = dataloader
        self.htype_dict = htype_dict
        self.ndim_dict = ndim_dict
        self.tensor_info_dict = tensor_info_dict
        self.pil_compressed_tensors = pil_compressed_tensors
        self.raw_tensors = raw_tensors
        self.json_tensors = json_tensors
        self.list_tensors = list_tensors
        self.upcast = upcast
        self.transform_fn = transform_fn
        self.collate_fn = collate_fn
        self.iter_pos = None
        self.raw_tensor_set = (
            set(self.raw_tensors) - set(self.json_tensors) - set(self.list_tensors)
        )  # tensors to be returned as bytes
        self.ignore_errors = ignore_errors
        self.skipped = 0
        self.processed = 0
        self.verbose=verbose
        self.pid = os.getpid()
        if self.verbose:
            create_folder(path="libdeeplake_logs")
            file_name = f"libdeeplake_logs/log_{self.pid}_{str(uuid4())[:4]}.txt"
            self.file = open(file_name, "a")
            self.file.write(f"ZeroWorkerIterator iterator created {self.pid}\n")
        else:
            self.file=None

    def __iter__(self):
        if self.file:
            self.file.write(f"ZeroWorkerIterator initialized {self.pid}\n")
        if isinstance(self.dataloader, BufferedLoader):
            self.dataloader.dataloader().reset()
        else:
            self.dataloader.reset()

        self.skipped = 0
        self.processed = 0
        self.iter_pos = iter(self.dataloader)
        return self

    def __next__(self):
        return self.get_data()

    def __len__(self) -> int:
        return len(self.dataloader)

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return f"ZeroWorkerIterator length {self.length} num_workers {self.num_workers} batch_size {self.batch_size} shuffle {self.shuffle}"

    def _next_data(self):
        batch = next(self.iter_pos)
        for sample in batch:
            for tensor in self.pil_compressed_tensors:
                if isinstance(sample[tensor], (list, tuple)):
                    sample[tensor] = list(
                        Image.open(io.BytesIO(t)) for t in sample[tensor]
                    )
                else:
                    sample[tensor] = Image.open(io.BytesIO(sample[tensor]))
            for tensor in self.json_tensors:
                sample[tensor] = bytes_to_text(sample[tensor], "json")
            for tensor in self.list_tensors:
                sample[tensor] = bytes_to_text(sample[tensor], "list")
            if self.htype_dict:
                convert_sample_to_data(
                    sample, self.htype_dict, self.ndim_dict, self.tensor_info_dict
                )
        return batch

    def get_data(self):
        while True:
            self.processed += 1
            batch = self._next_data()
            try:
                return transform_collate_batch(
                    batch,
                    self.transform_fn,
                    self.collate_fn,
                    self.upcast,
                    self.raw_tensor_set,
                )
            except Exception as ex:
                if self.file:
                    self.file.write(f"ZeroWorkerIterator {self.pid} exception happened {ex}\n")
                self.handle_exception(ex)
                if self.ignore_errors:
                    continue
                else:
                    raise

    def handle_exception(self, ex):
        self.processed -= 1
        if isinstance(
            ex,
            (
                TransformExceptionWrapper,
                CollateExceptionWrapper,
            ),
        ):
            ex.processed = self.processed
            ex.skipped = self.skipped
            if self.ignore_errors:
                print(f"An exception happened during data handling exception: {ex} processed batches {ex.processed} skipped batched {ex.skipped}")
            else:
                traceback.print_tb(ex.exception.__traceback__)
        else:
            if self.ignore_errors:
                print(
                    f"An exception happened during data handling exception: {ex} processed batches {self.processed}"
                )
            else:
                traceback.print_tb(ex)
        self.skipped += 1

    def close(self):
        return
