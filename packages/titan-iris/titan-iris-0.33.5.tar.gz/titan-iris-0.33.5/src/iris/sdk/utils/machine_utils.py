"""Utilities for checking the machine's hardware and software configuration."""
import cpuinfo


def is_intel_cpu_with_mkl_support():
    """Check if the CPU is Intel and supports MKL."""
    cpu_info = cpuinfo.get_cpu_info()
    if "vendor_id_raw" in cpu_info:
        is_intel_cpu = cpu_info["vendor_id_raw"] == "GenuineIntel"
    else:
        is_intel_cpu = False
    return is_intel_cpu
