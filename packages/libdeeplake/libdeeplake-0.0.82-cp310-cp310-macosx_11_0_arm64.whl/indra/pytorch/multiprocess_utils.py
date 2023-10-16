from deeplake.core.serialize import bytes_to_text
from deeplake.integrations.pytorch.common import convert_sample_to_data
from indra.pytorch.util import (
    transform_collate_batch,
)
from indra.pytorch.exceptions import (
    StopChildProcess,
)

from multiprocessing import current_process
from typing import List, Optional
from PIL import Image
import dill as pickle
import os
import io


def combine_compressed_bytes(
    batch,
    pil_compressed_tensors: Optional[List[str]] = None,
    json_tensors: Optional[List[str]] = None,
    list_tensors: Optional[List[str]] = None,
):
    all_byte_tensors = set(pil_compressed_tensors + json_tensors + list_tensors)
    sb, eb, all_bts = 0, 0, []
    for sample in batch:
        for tensor in all_byte_tensors:
            if isinstance(sample[tensor], bytes):
                sample_bts = sample.pop(tensor)
                all_bts.append(sample_bts)
                eb += len(sample_bts)
                sample[tensor] = (sb, eb)
                sb = eb
            elif isinstance(sample[tensor], list):
                sb_eb_list = []
                for item in sample[tensor]:
                    sample_bts = item
                    all_bts.append(sample_bts)
                    eb += len(sample_bts)
                    sb_eb_list.append((sb, eb))
                    sb = eb
                sample[tensor] = sb_eb_list

    # combine all_bts into one bytearray
    all_bts = bytearray(b"".join(all_bts))
    return all_bts, batch


def bytes_to_batch(
    batch,
    all_bts,
    pil_compressed_tensors: Optional[List[str]] = None,
    json_tensors: Optional[List[str]] = None,
    list_tensors: Optional[List[str]] = None,
):
    data_bytes = memoryview(all_bts)
    all_byte_tensors = set(pil_compressed_tensors + json_tensors + list_tensors)
    pil_compressed_tensors = set(pil_compressed_tensors)
    json_tensors = set(json_tensors)
    list_tensors = set(list_tensors)
    for sample in batch:
        for tensor in all_byte_tensors:
            if tensor in pil_compressed_tensors:
                decompress_fn = lambda x: Image.open(io.BytesIO(x))
            elif tensor in json_tensors:
                decompress_fn = lambda x: bytes_to_text(x, "json")
            elif tensor in list_tensors:
                decompress_fn = lambda x: bytes_to_text(x, "list")

            if isinstance(sample[tensor], tuple):
                sb, eb = sample[tensor]
                sample[tensor] = decompress_fn(data_bytes[sb:eb])
            elif isinstance(sample[tensor], list):
                sb_eb_list = sample[tensor]
                sample[tensor] = [
                    decompress_fn(data_bytes[sb:eb]) for sb, eb in sb_eb_list
                ]
            else:
                # will only happen for Image tensors that are tiled
                sample[tensor] = Image.fromarray(sample[tensor])
    return batch


def early_transform_collate(inp):
    (
        data_in_queue,
        data_out_queue,
        ignore_errors,
        transform_fn,
        collate_fn,
        upcast,
        pil_compressed_tensors,
        json_tensors,
        list_tensors,
        raw_tensors,
        htype_dict,
        ndim_dict,
        tensor_info_dict,
    ) = inp
    raw_tensor_set = set(raw_tensors) - set(json_tensors) - set(list_tensors)
    transform_fn = None if transform_fn is None else pickle.loads(transform_fn)
    collate_fn = None if collate_fn is None else pickle.loads(collate_fn)
    while 1:
        try:
            batch = data_in_queue.get()
            if isinstance(batch, StopIteration):
                process = current_process()
                data_out_queue.put(batch)
                print(f'Worker: {process.name} successfully stopped')
                break
            elif isinstance(batch, StopChildProcess):
                process = current_process()
                print(f'Worker: {process.name} successfully stopped')
                break
            else:
                if batch is None:
                    data_out_queue.put(None)
                    continue
                all_bts, batch = batch
                if all_bts is not None:
                    batch = bytes_to_batch(
                        batch,
                        all_bts,
                        pil_compressed_tensors,
                        json_tensors,
                        list_tensors,
                    )
                if htype_dict:
                    for sample in batch:
                        convert_sample_to_data(
                            sample, htype_dict, ndim_dict, tensor_info_dict
                        )
                out = transform_collate_batch(
                    batch, transform_fn, collate_fn, upcast, raw_tensor_set
                )
                data_out_queue.put(out)
        except Exception as e:
            data_out_queue.put(e)
            if ignore_errors:
                continue
            else:
                print(f"Stopping process {os.getpid()} due to exception {e}")
                break
