import os

from bec_lib.core.bec_errors import ServiceConfigError


class FileWriterMixin:
    """File writer mixin class"""

    def __init__(self, service_config: dict) -> None:
        """
        Initialize the file writer mixin class.

        Args:
            service_config (dict): File writer service config. Must at least contain a base_path.
        """
        self._base_path = self._get_base_path_from_config(service_config)

    def _get_base_path_from_config(self, service_config: str):
        if not service_config:
            raise ServiceConfigError("Service config must contain a file writer definition.")
        if not service_config.get("base_path"):
            raise ServiceConfigError("File writer config must define a base path.")
        return os.path.abspath(os.path.expanduser(service_config.get("base_path")))

    def get_scan_directory(self, scan_number: int, scan_bundle: int, leading_zeros: int = None):
        """
        Get the scan directory for a given scan number and scan bundle.

        Args:
            scan_bundle (int): Scan bundle size
            scan_number (int): Scan number
            leading_zeros (int, optional): Number of leading zeros. Defaults to None.

        Returns:
            str: Scan directory

        Examples:
            >>> get_scan_directory(100, 1234)
            'S1200-1299/S1234'
            >>> get_scan_directory(1000, 1234, 5)
            'S1200-1299/S1234'
        """
        if leading_zeros is None:
            leading_zeros = len(str(scan_bundle))
        floor_dir = scan_number // scan_bundle * scan_bundle
        return f"S{floor_dir:0{leading_zeros}d}-{floor_dir+scan_bundle-1:0{leading_zeros}d}/S{scan_number:0{leading_zeros}d}"

    def compile_full_filename(
        self,
        scan_number: int,
        suffix: str,
        scan_bundle=1000,
        leading_zeros=5,
        create_dir=True,
    ) -> str:
        """
        Compile a full filename for a given scan number and suffix.

        Args:
            scan_number (int): Scan number
            suffix (str): Filename suffix including extension
            scan_bundle (int, optional): Scan bundle size. Defaults to 1000.
            leading_zeros (int, optional): Number of leading zeros. Defaults to 5.
            create_dir (bool, optional): Create the directory if it does not exist. Defaults to True.

        Returns:
            str: Full filename
        """
        scan_dir = self.get_scan_directory(scan_number, scan_bundle, leading_zeros)
        full_file = os.path.join(
            self._base_path,
            "data",
            scan_dir,
            f"S{scan_number:0{leading_zeros}d}_{suffix}",
        )
        if create_dir:
            os.makedirs(os.path.dirname(full_file), exist_ok=True)
        return full_file
