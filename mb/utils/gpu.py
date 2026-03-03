from .check_package import check_package
from .logging import logg

__all__ = ["gpu_info"]


def gpu_info(logger=None):
    check_package("torch", "PyTorch is required to check GPU information.")
    import torch
    if torch.cuda.is_available():
        device = torch.cuda.current_device()
        gpu_name = torch.cuda.get_device_name(device)

        total_memory = torch.cuda.get_device_properties(device).total_memory
        allocated_memory = torch.cuda.memory_allocated(device)
        reserved_memory = torch.cuda.memory_reserved(device)
        free_memory = total_memory - reserved_memory

        logg.info(f"GPU: {gpu_name}", logger=logger)
        logg.info(f"Total Memory:     {total_memory / 1e6:.2f} MB | {total_memory / 1e9:.2f} GB", logger=logger)
        logg.info(f"Allocated Memory: {allocated_memory / 1e6:.2f} MB | {allocated_memory / 1e9:.2f} GB", logger=logger)
        logg.info(f"Reserved Memory:  {reserved_memory / 1e6:.2f} MB | {reserved_memory / 1e9:.2f} GB", logger=logger)
        logg.info(f"Free Memory:      {free_memory / 1e6:.2f} MB | {free_memory / 1e9:.2f} GB", logger=logger)
    else:
        logg.info("No CUDA GPU available", logger=logger)