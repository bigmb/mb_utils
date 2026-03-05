from .check_package import check_package
from .logging import logg

__all__ = ["gpu_info"]


def gpu_info(gpu_value=0,logger=None):
    """
    Prints GPU information including name, total memory, allocated memory, reserved memory, and free memory.
    Prints for all available CUDA GPUs. If no CUDA GPU is available, it logs that information.
    Args:
        gpu_value (str, optional): Specifies which GPU(s) to display information for. 
        logger (logging.Logger, optional): Logger for logging messages. Defaults to None.
    """
    check_package("torch", "PyTorch is required to check GPU information.")
    import torch
    if torch.cuda.is_available():
        device = device = torch.device(f"cuda:{gpu_value}")
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

def get_gpus_by_least_usage(return_stats: bool = False):
    """
    Get GPUs ordered by least memory usage.

    Usage for each GPU is computed as:
        usage_ratio = (total_bytes - free_bytes) / total_bytes

    Args:
        return_stats (bool):
            - False: return only GPU indices in ascending usage order.
            - True: return list of dict stats sorted by ascending usage.

    Returns:
        list:
            - If return_stats=False: [gpu_idx0, gpu_idx1, ...]
            - If return_stats=True: [
                  {
                    "gpu_id": int,
                    "name": str,
                    "free_gb": float,
                    "used_gb": float,
                    "total_gb": float,
                    "usage_ratio": float,
                  },
                  ...
              ]
    """
    check_package("torch", "PyTorch is required to check GPU information.")
    import torch
    if not torch.cuda.is_available():
        return []

    gpu_stats = []
    for gpu_id in range(torch.cuda.device_count()):
        free_bytes, total_bytes = torch.cuda.mem_get_info(device=gpu_id)
        used_bytes = total_bytes - free_bytes

        gpu_stats.append(
            {
                "gpu_id": gpu_id,
                "name": torch.cuda.get_device_name(gpu_id),
                "free_gb": free_bytes / (1024**3),
                "used_gb": used_bytes / (1024**3),
                "total_gb": total_bytes / (1024**3),
                "usage_ratio": (used_bytes / total_bytes) if total_bytes > 0 else 1.0,
            }
        )

    gpu_stats.sort(key=lambda item: (item["usage_ratio"], -item["free_gb"]))

    if return_stats:
        return gpu_stats

    return [item["gpu_id"] for item in gpu_stats]