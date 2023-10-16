from itertools import repeat
from typing import Callable, List, Optional
from indra.pytorch.buffered_loader import BufferedLoader
from indra.pytorch.common import collate_fn as default_collate
from indra.pytorch.multiprocess_utils import (
    combine_compressed_bytes,
    early_transform_collate,
)
from indra.pytorch.util import (
    process_initializer,
    create_folder,
)
from indra.pytorch.exceptions import (
    TransformExceptionWrapper,
    CollateExceptionWrapper,
    StopChildProcess,
)
from multiprocessing import Pool, Manager, Queue
import warnings
import os
import dill as pickle
import traceback
from uuid import uuid4


class MultiprocessIterator:
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
        prefetch_factor: int = 10,
        transform_fn: Optional[Callable] = None,
        collate_fn: Optional[Callable] = default_collate,
        worker_init_fn: Optional[Callable] = None,
        num_workers: int = 0,
        persistent_workers: bool = False,
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
            prefetch_factor (int) Number of samples loaded in advance by workers. Defaults to 10
            transform_fn (Callable, optional) Callable object which is needed to apply on each sample on batch. Defaults to None.
            collate_fn (callable, optional): merges a list of samples to form a
                mini-batch of Tensor(s).  Used when using batched loading from a
                map-style dataset.
            worker_init_fn (Callable, optional) function to initialise the child processes. Defaults to None.
            num_workers (int, optional): how many subprocesses to use for data
                loading. ``0`` means that the data will be loaded in the main process.
                (default: ``0``)
            persistent_workers (bool): If ``True``, the data loader will not shutdown the worker processes after a dataset has been consumed once. Defaults to ``False``.
            ignore_errors(bool) shows whether need to ignore the errors appearing during transformation
        """
        self.dataloader = dataloader
        self.htype_dict = htype_dict
        self.ndim_dict = ndim_dict
        self.tensor_info_dict = tensor_info_dict
        self.pil_compressed_tensors = pil_compressed_tensors
        self.raw_tensors = raw_tensors
        self.prefetch_factor = prefetch_factor
        self.json_tensors = json_tensors
        self.list_tensors = list_tensors
        self.upcast = upcast
        self.transform_fn = transform_fn
        self.collate_fn = collate_fn
        self.worker_init_fn = worker_init_fn or None
        self.num_workers = num_workers
        self.persistent_workers = persistent_workers or False
        self.num_prefetch_tasks = self.prefetch_factor * self.num_workers
        self.length = len(dataloader)
        self.current_pos = 0
        self.iter_pos = 0
        self.workers_initialized = False
        self.ignore_errors = ignore_errors
        self.skipped = 0
        self.processed = 0

        self.pool = None
        self.manager = None

        self.verbose=verbose
        self.pid = os.getpid()
        if self.verbose:
            create_folder(path="libdeeplake_logs")
            file_name = f"libdeeplake_logs/log_{self.pid}_{str(uuid4())[:4]}.txt"
            self.file = open(file_name, "a")
            self.file.write(f"class MultiprocessIterator created {self.pid}\n")
        else:
            self.file=None

    def __iter__(self):
        if self.file:
            self.file.write(f"class MultiprocessIterator initialized {self.pid}\n")
        if self.current_pos != 0:
            if isinstance(self.dataloader, BufferedLoader):
                self.dataloader.dataloader().reset()
            else:
                self.dataloader.reset()

        if self.persistent_workers and self.pool is not None:
            self.clear_queues()

        self.reset_positions()
        self.iter_dl = iter(self.dataloader)
        if self.pool is not None:
            if not self.persistent_workers:
                self.send_stop_signals_to_subprocesses()
                self.close()
                self.start_processes()
            self.run_workers()
            self.fill_prefetch_jobs()

        return self

    def __len__(self):
        return self.length

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return f"MultiprocessIterator length {self.length} num_workers {self.num_workers} batch_size {self.batch_size} shuffle {self.shuffle}"

    def __del__(self):
        self.free_resources()

    def __next__(self):
        if self.pool is None:
            if self.file:
                self.file.write(f"class MultiprocessIterator next call restart workers {self.pid}\n")
            self.start_processes()
            self.run_workers()
            self.fill_prefetch_jobs()
            if self.file:
                self.file.write(f"class MultiprocessIterator next call restart workers finished {self.pid}\n")
        elif (
            self.pool is not None
            and self.persistent_workers
            and not self.workers_initialized
        ):
            if self.file:
                self.file.write(f"class MultiprocessIterator next call reuse workers {self.pid}\n")
            self.run_workers()
            self.fill_prefetch_jobs()
            if self.file:
                self.file.write(f"class MultiprocessIterator next call reuse workers finished {self.pid}\n")
        return self.get_data()

    def reset_positions(self):
        self.current_pos = 0
        self.iter_pos = 0
        self.skipped = 0
        self.processed = 0

    def clear_queues(self):
        if self.file:
            self.file.write(f"class MultiprocessIterator clear queues {self.pid}\n")
        for item in self.data_in_queues:
            while not item.empty():
                item.get_nowait()

        for item in self.data_out_queues:
            while not item.empty():
                item.get_nowait()

        if self.file:
            self.file.write(f"class MultiprocessIterator clear queues finished {self.pid}\n")

    def fetch_next_job(self):
        while True:
            try:
                wid = self.current_pos % self.num_workers
                if self.file:
                    self.file.write(f"class MultiprocessIterator libdeeplake next pid: {self.pid}\n")
                batch = next(self.iter_dl)
                if self.pil_compressed_tensors:
                    all_bts, batch = combine_compressed_bytes(
                        batch,
                        self.pil_compressed_tensors,
                        self.json_tensors,
                        self.list_tensors,
                    )
                else:
                    all_bts = None
                batch = (all_bts, batch)
                if self.file:
                    self.file.write(f"class MultiprocessIterator self.data_in_queues[{wid}].put start {self.pid}\n")
                self.data_in_queues[wid].put(batch)
                if self.file:
                    self.file.write(f"class MultiprocessIterator self.data_in_queues[{wid}].put finish {self.pid}\n")
                self.current_pos += 1
                return True
            except StopIteration:
                if self.file:
                    self.file.write(f"class MultiprocessIterator StopIteration during stat fetching {self.pid}\n")
                for j in range(self.num_workers):
                    self.data_in_queues[j].put(StopIteration())
                return False
            except Exception as ex:
                if self.file:
                    self.file.write(f"class MultiprocessIterator Exception during data fetching, {str(ex)} {self.pid}\n")
                print(f"Exception during data fetching, {str(ex)}")
                continue

    def fill_prefetch_jobs(self):
        while self.current_pos <= self.num_prefetch_tasks:
            if not self.fetch_next_job():
                break

    def adjust_environment(self):
        child_env = os.environ.copy()

        # This code is referred from https://github.com/pytorch/pytorch/blob/master/torch/distributed/run.py
        if self.num_workers >= 1 and "OMP_NUM_THREADS" not in os.environ:
            omp_num_threads = 1
            warnings.warn(
                f"Setting OMP_NUM_THREADS environment variable for each process "
                f"to be {omp_num_threads} in default, to avoid your system being "
                f"overloaded, please further tune the variable for optimal "
                f"performance in your application as needed."
            )
            child_env["OMP_NUM_THREADS"] = str(omp_num_threads)
            os.environ["OMP_NUM_THREADS"] = str(omp_num_threads)

        if self.num_workers >= 1 and "MKL_NUM_THREADS" not in os.environ:
            mkl_num_threads = 1
            warnings.warn(
                f"Setting MKL_NUM_THREADS environment variable for each process "
                f"to be {mkl_num_threads} in default, to avoid your system being "
                f"overloaded, please further tune the variable for optimal "
                f"performance in your application as needed."
            )

            child_env["MKL_NUM_THREADS"] = str(mkl_num_threads)
            os.environ["MKL_NUM_THREADS"] = str(mkl_num_threads)

        return child_env

    def start_processes(self):
        if self.pool is not None:
            return
        
        if self.file:
            self.file.write(f"MultiprocessIterator start_process {self.pid}\n")

        child_env = self.adjust_environment()
        id_queue = Queue(maxsize=self.num_workers)
        for i in range(self.num_workers):
            id_queue.put(i)

        self.pool = Pool(
            processes=self.num_workers,
            initializer=process_initializer,
            initargs=(child_env, self.worker_init_fn, id_queue),
        )

        if self.manager is None:
            self.manager = Manager()

        self.data_in_queues = [self.manager.Queue() for _ in range(self.num_workers)]
        self.data_out_queues = [self.manager.Queue() for _ in range(self.num_workers)]

    def run_workers(self):
        transform_fn = (
            None if self.transform_fn is None else pickle.dumps(self.transform_fn)
        )
        collate_fn = None if self.collate_fn is None else pickle.dumps(self.collate_fn)
        inp = list(
            zip(
                self.data_in_queues,
                self.data_out_queues,
                repeat(self.ignore_errors),
                repeat(transform_fn),
                repeat(collate_fn),
                repeat(self.upcast),
                repeat(self.pil_compressed_tensors),
                repeat(self.json_tensors),
                repeat(self.list_tensors),
                repeat(self.raw_tensors),
                repeat(self.htype_dict),
                repeat(self.ndim_dict),
                repeat(self.tensor_info_dict),
            )
        )
        self.workers_initialized = True
        self.pool.map_async(early_transform_collate, inp)

    def get_data(self):
        out = None

        while True:
            self.processed += 1
            wid = self.iter_pos % self.num_workers
            if self.file:
                self.file.write(f"MultiprocessIterator.__next__ iter_pos: {self.iter_pos} processed: {self.processed} wid: {wid} is_queue_empty: {self.data_out_queues[wid].empty()}\n")
            out = self.data_out_queues[wid].get()
            if isinstance(out, StopIteration):
                if self.file:
                    self.file.write(f"MultiprocessIterator StopIteration received {self.pid}\n")
                # get StopIteration from other workers too, to empty the queues
                for j in range(self.num_workers):
                    if j != wid:
                        self.data_out_queues[j].get()
                if not self.persistent_workers:
                    self.send_stop_signals_to_subprocesses()
                    self.close()
                self.workers_initialized = False
                if self.file:
                    self.file.write(f"MultiprocessIterator StopIteration finished {self.pid}\n")
                raise StopIteration
            elif isinstance(out, StopChildProcess):
                warnings.warn("Invalid state was reached, please contact Activeloop for further assistance.")
                if self.file:
                    self.file.write(f"MultiprocessIterator StopChildProcess received {self.pid}\n")
                self.fetch_next_job()   
                self.iter_pos += 1
                if self.file:
                    self.file.write(f"MultiprocessIterator StopChildProcess finished {self.pid}\n")
                raise StopIteration
            elif isinstance(out, Exception):
                self.handle_exception(out)
                if self.ignore_errors:
                    self.fetch_next_job()
                    self.iter_pos += 1
                    continue
                else:
                    raise out
            if self.current_pos < self.length:
                self.fetch_next_job()
            elif self.current_pos == self.length:
                try:
                    batch = next(self.iter_dl)
                except StopIteration:
                    # send StopIteration (stop signal) to all workers
                    for j in range(self.num_workers):
                        self.data_in_queues[j].put(StopIteration())
            self.iter_pos += 1
            return out

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

    def send_stop_signals_to_subprocesses(self):
        if self.pool is not None:
            for idx in range(self.num_workers):
                self.data_in_queues[idx].put(StopChildProcess())

    def close(self):
        if self.pool is not None:
            if self.file:
                self.file.write(f"MultiprocessIterator iterator close is called {self.pid}\n")
            self.pool.close()
            self.pool.join()
            if self.file:
                self.file.write(f"MultiprocessIterator iterator close is finished {self.pid}\n")
            self.pool = None

    def free_resources(self):
        self.send_stop_signals_to_subprocesses()
        self.close()
        if self.manager is not None:
            self.manager.shutdown()
            self.manager = None

    @staticmethod
    def _clean_up_worker(obj):
        obj.free_resources()
