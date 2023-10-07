# pylint: disable=too-many-public-methods
from string import Template


class MessageEndpoints:
    # devices feedback
    _device_status = "internal/devices/status"
    _device_read = "internal/devices/read"
    _device_readback = "internal/devices/readback"
    _device_req_status = "internal/devices/req_status"
    _device_progress = "internal/devices/progress"
    _device_async_readback = Template("internal/devices/async_readback/$scanID/$device")

    # device config
    _device_config_request = "internal/devices/config_request"
    _device_config_request_response = "internal/devices/config_request_response"
    _device_server_config_update = "internal/devices/config_request_response"
    _device_server_config_update_response = "internal/devices/config_request_response"
    _device_config_update = "internal/devices/config_update"
    _device_config = "internal/devices/config"
    _device_info = "internal/devices/info"
    _device_staged = "internal/devices/staged"

    # scan queue
    _scan_queue_modification = "internal/queue/queue_modification"
    _scan_queue_modification_request = "internal/queue/queue_modification_request"
    _scan_queue_insert = "internal/queue/queue_insert"
    _scan_queue_request = "internal/queue/queue_request"
    _scan_queue_request_response = "internal/queue/queue_request_response"
    _scan_queue_status = "internal/queue/queue_status"
    _scan_queue_history = "internal/queue/queue_history"

    # scan info
    _scan_number = "scans/scan_number"
    _dataset_number = "scans/dataset_number"
    _scan_status = "scans/scan_status"
    _scan_status_list = "scans/scan_status_list"
    _available_scans = "scans/available_scans"
    _scan_segment = "scans/scan_segment"
    _scan_baseline = "scans/scan_baseline"
    _bluesky_events = "scans/bluesky-events"
    _public_scan_info = Template("public/$scanID/scan_info")
    _public_scan_segment = Template("public/$scanID/scan_segment/$pointID")
    _public_scan_baseline = Template("public/$scanID/scan_baseline")
    _public_file = Template("public/$scanID/file/$name")
    _file_event = "public/file_event"

    # instructions
    _device_instructions = "internal/devices/instructions"
    _device_rpc = "internal/devices/rpc"
    _pre_scan_macros = "internal/pre_scan_macros"
    _post_scan_macros = "internal/post_scan_macros"

    # log
    _log = "internal/log"
    _alarms = "internal/alarms"

    # service
    _services_status = "internal/services/status"
    _metrics = "internal/services/metrics"

    # misc
    _public_global_vars = "public/vars"
    _observer = "internal/observer"
    _progress = "public/progress"

    # logbook
    _logbook = "internal/logbook"

    # experiment
    _account = "internal/account"

    # data processing
    _processed_data = "public/processed_data"
    _dap_config = "internal/dap/config"
    _avilable_dap_plugins = "internal/dap/available_plugins"

    ##########

    # devices feedback
    @classmethod
    def device_status(cls, device: str):
        """
        Endpoint for device status. This endpoint is used by the device server to publish
        the device status using a BECMessage.DeviceStatus message.

        Args:
            device (str): Device name, e.g. "samx".
        """
        return f"{cls._device_status}/{device}"

    @classmethod
    def device_read(cls, device: str) -> str:
        """
        Endpoint for device readings. This endpoint is used by the device server to publish
        the device readings using a BECMessage.DeviceMessage message.

        Args:
            device (str): Device name, e.g. "samx".

        Returns:
            str: Endpoint for device readings of the specified device.
        """
        return f"{cls._device_read}/{device}"

    @classmethod
    def device_readback(cls, device: str) -> str:
        """
        Endpoint for device readbacks. This endpoint is used by the device server to publish
        the device readbacks using a BECMessage.DeviceMessage message.

        Args:
            device (str): Device name, e.g. "samx".

        Returns:
            str: Endpoint for device readbacks of the specified device.
        """
        return f"{cls._device_readback}/{device}"

    @classmethod
    def device_req_status(cls, device: str) -> str:
        """
        Endpoint for device request status. This endpoint is used by the device server to publish
        the device request status using a BECMessage.DeviceRequestStatus message.

        Args:
            device (str): Device name, e.g. "samx".

        Returns:
            str: Endpoint for device request status of the specified device.
        """
        return f"{cls._device_req_status}/{device}"

    @classmethod
    def device_progress(cls, device: str) -> str:
        """
        Endpoint for device progress. This endpoint is used by the device server to publish
        the device progress using a BECMessage.DeviceStatus message.

        Args:
            device (str): Device name, e.g. "samx".

        Returns:
            str: Endpoint for device progress of the specified device.
        """
        return f"{cls._device_progress}/{device}"

    # device config
    @classmethod
    def device_config_request(cls) -> str:
        """
        Endpoint for device config request. This endpoint can be used to
        request a modification to the device config. The request is sent using
        a BECMessage.DeviceConfigMessage message.

        Returns:
            str: Endpoint for device config request.
        """
        return cls._device_config_request

    @classmethod
    def device_config_request_response(cls, RID: str) -> str:
        """
        Endpoint for device config request response. This endpoint is used by the
        device server and scihub connector to inform about whether the device config
        request was accepted or rejected. The response is sent using a
        BECMessage.DeviceConfigMessage message.

        Args:
            RID (str): Request ID.

        Returns:
            str: Endpoint for device config request response.
        """
        return f"{cls._device_config_request_response}/{RID}"

    @classmethod
    def device_server_config_request(cls) -> str:
        """
        Endpoint for device server config request. This endpoint can be used to
        request changes to config. Typically used by the scihub connector following a
        device config request and validate a new configuration with the device server.
        The request is sent using a BECMessage.DeviceConfigMessage message.

        Returns:
            str: Endpoint for device server config request.
        """
        return cls._device_server_config_update

    @classmethod
    def device_server_config_request_response(cls, RID: str) -> str:
        """
        Endpoint for device server config request response. This endpoint is used by the
        device server to inform about whether a new configuration was accepted or rejected.
        The response is sent using a BECMessage.DeviceConfigMessage message.

        Args:
            RID (str): Request ID.

        Returns:
            str: Endpoint for device server config request response.
        """
        return f"{cls._device_server_config_update_response}/{RID}"

    @classmethod
    def device_config_update(cls) -> str:
        """
        Endpoint for device config update. This endpoint is used by the scihub connector
        to inform about a change to the device config. The update is sent using a
        BECMessage.DeviceConfigMessage message.

        Returns:
            str: Endpoint for device config update.

        """
        return cls._device_config_update

    @classmethod
    def device_config(cls) -> str:
        """
        Endpoint for device config. This endpoint is used by the scihub connector
        to set the device config.

        Returns:
            str: Endpoint for device config.
        """
        return cls._device_config

    @classmethod
    def device_info(cls, device: str) -> str:
        """
        Endpoint for device info. This endpoint is used by the device server to publish
        the device info using a BECMessage.DeviceInfo message.

        Args:
            device (str): Device name, e.g. "samx".

        Returns:
            str: Endpoint for device info of the specified device.
        """
        return f"{cls._device_info}/{device}"

    @classmethod
    def device_staged(cls, device: str) -> str:
        """
        Endpoint for the device stage status. This endpoint is used by the device server
        to publish the device stage status using a BECMessage.DeviceStatus message.
        A device is staged when it is ready to be used in a scan. A DeviceStatus of 1 means
        that the device is staged, 0 means that the device is not staged.

        Args:
            device (str): Device name, e.g. "samx".

        Returns:
            str: Endpoint for the device stage status of the specified device.
        """
        return f"{cls._device_staged}/{device}"

    @classmethod
    def device_async_readback(cls, scanID: str, device: str) -> str:
        """
        Endpoint for receiving an async device readback over Redis streams.
        This endpoint is used by the device server to publish async device
        readbacks using a BECMessage.DeviceMessage. In addition tp scan metadata,
        the message metadata contains information on how to concatenate multiple readings.
        Further keyword arguments for GUI handling might be attached.

        Args:
            scanID (str): unique scan identifier
            device (str): Device name, e.g. "mcs".

        Returns:
            str: Endpoint for the async device readback.
        """
        return cls._device_async_readback.substitute(scanID=scanID, device=device)

    # scan queue
    @classmethod
    def scan_queue_modification(cls) -> str:
        """
        Endpoint for scan queue modification. This endpoint is used to publish accepted
        scan queue modifications using a BECMessage.ScanQueueModification message.

        Returns:
            str: Endpoint for scan queue modification.
        """
        return cls._scan_queue_modification

    @classmethod
    def scan_queue_modification_request(cls) -> str:
        """
        Endpoint for scan queue modification request. This endpoint is used to request
        a scan queue modification using a BECMessage.ScanQueueModification message.
        If accepted, the modification is published using the scan_queue_modification
        endpoint.

        Returns:
            str: Endpoint for scan queue modification request.
        """
        return cls._scan_queue_modification_request

    @classmethod
    def scan_queue_insert(cls) -> str:
        """
        Endpoint for scan queue inserts. This endpoint is used to publish accepted
        scans using a BECMessage.ScanQueueMessage message.
        The message will be picked up by the scan queue manager and inserted into the
        scan queue.

        Returns:
            str: Endpoint for scan queue inserts.
        """
        return cls._scan_queue_insert

    @classmethod
    def scan_queue_request(cls) -> str:
        """
        Endpoint for scan queue request. This endpoint is used to request the new scans.
        The request is sent using a BECMessage.ScanQueueMessage message.

        Returns:
            str: Endpoint for scan queue request.
        """
        return cls._scan_queue_request

    @classmethod
    def scan_queue_request_response(cls) -> str:
        """
        Endpoint for scan queue request response. This endpoint is used to publish the
        information on whether the scan request was accepted or rejected. The response
        is sent using a ``BECMessage.ScanQueueRequestResponse`` message.

        Returns:
            str: Endpoint for scan queue request response.

        """
        return cls._scan_queue_request_response

    @classmethod
    def scan_queue_status(cls) -> str:
        """
        Endpoint for scan queue status. This endpoint is used to publish the scan queue
        status using a BECMessage.ScanQueueStatus message.

        Returns:
            str: Endpoint for scan queue status.
        """
        return cls._scan_queue_status

    @classmethod
    def scan_queue_history(cls) -> str:
        """
        Endpoint for scan queue history. This endpoint is used to keep track of the
        scan queue history using a BECMessage.ScanQueueHistory message. The endpoint is
        connected to a redis list.

        Returns:
            str: Endpoint for scan queue history.
        """
        return cls._scan_queue_history

    # scan info
    @classmethod
    def scan_number(cls) -> str:
        """
        Endpoint for scan number. This endpoint is used to publish the scan number. The
        scan number is incremented after each scan and set in redis as an integer.

        Returns:
            str: Endpoint for scan number.
        """
        return cls._scan_number

    @classmethod
    def dataset_number(cls) -> str:
        """
        Endpoint for dataset number. This endpoint is used to publish the dataset number.
        The dataset number is incremented after each dataset and set in redis as an integer.

        Returns:
            str: Endpoint for dataset number.
        """
        return cls._dataset_number

    @classmethod
    def scan_status(cls) -> str:
        """
        Endpoint for scan status. This endpoint is used to publish the scan status using
        a BECMessage.ScanStatusMessage message.

        Returns:
            str: Endpoint for scan status.
        """
        return cls._scan_status

    @classmethod
    def available_scans(cls) -> str:
        """
        Endpoint for available scans. This endpoint is used to publish the available scans
        using a direct msgpack dump of a dictionary containing the available scans.

        #TODO: Change this to a BECMessage.AvailableScans message.

        Returns:
            str: Endpoint for available scans.
        """
        return cls._available_scans

    @classmethod
    def bluesky_events(cls) -> str:
        """
        Endpoint for bluesky events. This endpoint is used by the scan bundler to
        publish the bluesky events using a direct msgpack dump of the bluesky event.

        Returns:
            str: Endpoint for bluesky events.
        """
        return cls._bluesky_events

    @classmethod
    def scan_segment(cls) -> str:
        """
        Endpoint for scan segment. This endpoint is used by the scan bundler to publish
        the scan segment using a BECMessage.ScanMessage message.

        Returns:
            str: Endpoint for scan segments.
        """
        return cls._scan_segment

    @classmethod
    def scan_baseline(cls) -> str:
        """
        Endpoint for scan baseline readings. This endpoint is used by the scan bundler to
        publish the scan baseline readings using a BECMessage.ScanBaselineMessage message.

        Returns:
            str: Endpoint for scan baseline readings.
        """
        return cls._scan_baseline

    # instructions
    @classmethod
    def device_instructions(cls) -> str:
        """
        Endpoint for device instructions. This endpoint is used by the scan server to
        publish the device instructions using a BECMessage.DeviceInstructions message.
        The device instructions are used to instruct the device server to perform
        certain actions, e.g. to move a motor.

        Returns:
            str: Endpoint for device instructions.
        """
        return cls._device_instructions

    @classmethod
    def device_rpc(cls, rpc_id: str) -> str:
        """
        Endpoint for device rpc. This endpoint is used by the device server to publish
        the result of a device rpc using a BECMessage.DeviceRPCResponse message.

        Args:
            rpc_id (str): RPC ID.

        Returns:
            str: Endpoint for device rpc.
        """
        return f"{cls._device_rpc}/{rpc_id}"

    @classmethod
    def pre_scan_macros(cls) -> str:
        """
        Endpoint for pre scan macros. This endpoint is used to keep track of the pre scan
        macros. The endpoint is connected to a redis list.

        Returns:
            str: Endpoint for pre scan macros.
        """
        return cls._pre_scan_macros

    @classmethod
    def post_scan_macros(cls) -> str:
        """
        Endpoint for post scan macros. This endpoint is used to keep track of the post scan
        macros. The endpoint is connected to a redis list.

        Returns:
            str: Endpoint for post scan macros.
        """
        return cls._post_scan_macros

    @classmethod
    def public_scan_info(cls, scanID: str) -> str:
        """
        Endpoint for scan info. This endpoint is used by the scan worker to publish the
        scan info using a BECMessage.ScanInfo message. In contrast to the scan_info endpoint,
        this endpoint is specific to a scan and has a retentioni time of 30 minutes.

        Args:
            scanID (str): Scan ID.

        Returns:
            str: Endpoint for scan info.

        """
        return cls._public_scan_info.substitute(scanID=scanID)

    @classmethod
    def public_scan_segment(cls, scanID: str, pointID: int) -> str:
        """
        Endpoint for public scan segments. This endpoint is used by the scan bundler to
        publish the scan segment using a BECMessage.ScanMessage message. In contrast to the
        scan_segment endpoint, this endpoint is specific to a scan and has a retention time
        of 30 minutes.

        Args:
            scanID (str): Scan ID.
            pointID (int): Point ID to specify a single point in a scan.

        Returns:
            str: Endpoint for scan segments.

        """
        return cls._public_scan_segment.substitute(scanID=scanID, pointID=pointID)

    @classmethod
    def public_scan_baseline(cls, scanID: str) -> str:
        """
        Endpoint for public scan baseline readings. This endpoint is used by the scan bundler
        to publish the scan baseline readings using a BECMessage.ScanBaselineMessage message.
        In contrast to the scan_baseline endpoint, this endpoint is specific to a scan and has
        a retention time of 30 minutes.

        Args:
            scanID (str): Scan ID.

        Returns:
            str: Endpoint for scan baseline readings.
        """
        return cls._public_scan_baseline.substitute(scanID=scanID)

    @classmethod
    def public_file(cls, scanID: str, name: str) -> str:
        """
        Endpoint for public file. This endpoint is used by the file writer to publish the
        status of the file writing using a BECMessage.FileMessage message.

        Args:
            scanID (str): Scan ID.
            name (str): File name.

        Returns:
            str: Endpoint for public files.
        """
        return cls._public_file.substitute(scanID=scanID, name=name)

    @classmethod
    def file_event(cls, name: str) -> str:
        """
        Endpoint for public file_event. This endpoint is used by the file writer to publish the
        status of the file writing using a BECMessage.FileMessage message.

        Args:
            name (str): File name.

        Returns:
            str: Endpoint for public file_events.
        """
        return f"{cls._file_event}/{name}"

    # log
    @classmethod
    def log(cls) -> str:
        """
        Endpoint for log. This endpoint is used by the redis connector to publish logs using
        a BECMessage.LogMessage message.

        Returns:
            str: Endpoint for log.
        """
        return cls._log

    @classmethod
    def alarm(cls) -> str:
        """
        Endpoint for alarms. This endpoint is used by the redis connector to publish alarms
        using a BECMessage.AlarmMessage message.

        Returns:
            str: Endpoint for alarms.
        """
        return cls._alarms

    # service
    @classmethod
    def service_status(cls, service_id: str) -> str:
        """
        Endpoint for service status. This endpoint is used by all BEC services to publish
        their status using a BECMessage.StatusMessage message.
        The status message also contains the service info such as user, host, etc.

        Args:
            service_id (str): Service ID, typically a uuid4 string.
        """
        return f"{cls._services_status}/{service_id}"

    @classmethod
    def metrics(cls, service_id: str) -> str:
        """
        Endpoint for metrics. This endpoint is used by all BEC services to publish their
        performance metrics using a BECMessage.ServiceMetricMessage message.

        Args:
            service_id (str): Service ID, typically a uuid4 string.

        Returns:
            str: Endpoint for metrics.
        """
        return f"{cls._metrics}/{service_id}"

    # misc
    @classmethod
    def global_vars(cls, var_name: str) -> str:
        """
        Endpoint for global variables. This endpoint is used to publish global variables
        using a BECMessage.VariableMessage message.

        Args:
            var_name (str): Variable name.

        Returns:
            str: Endpoint for global variables.
        """
        return f"{cls._public_global_vars}/{var_name}"

    @classmethod
    def observer(cls) -> str:
        """
        Endpoint for observer. This endpoint is used to keep track of observer states.
        This endpoint is currently not used.

        Returns:
            str: Endpoint for observer.
        """
        return cls._observer

    @classmethod
    def progress(cls, var_name) -> str:
        """
        Endpoint for progress. This endpoint is used to publish the current progress
        using a BECMessage.ProgressMessage message.

        Args:
            var_name (str): Variable name.

        Returns:
            str: Endpoint for progress.
        """
        return f"{cls._progress}/{var_name}"

    # logbook
    @classmethod
    def logbook(cls) -> str:
        """
        Endpoint for logbook. This endpoint is used to publish logbook info such as
        url, user and token using a direct msgpack dump of a dictionary.

        Returns:
            str: Endpoint for logbook.
        """
        return cls._logbook

    # experiment
    @classmethod
    def account(cls) -> str:
        """
        Endpoint for account. This endpoint is used to publish the current account.
        The value is set directly as a string.
        """
        return cls._account

    # data processing
    @classmethod
    def processed_data(cls, process_id: str) -> str:
        """
        Endpoint for processed data. This endpoint is used to publish new processed data
        streams using a BECMessage.ProcessedData message.

        Args:
            process_id (str): Process ID, typically a uuid4 string.

        Returns:
            str: Endpoint for processed data.
        """
        return f"{cls._processed_data}/{process_id}"

    @classmethod
    def dap_config(cls) -> str:
        """
        Endpoint for DAP configuration. This endpoint is used to publish the DAP configuration
        using a BECMessage.DAPConfig message.

        Returns:
            str: Endpoint for DAP configuration.
        """
        return cls._dap_config

    @classmethod
    def dap_available_plugins(cls) -> str:
        """
        Endpoint for available DAP plugins. This endpoint is used to publish the available DAP
        plugins using a BECMessage.AvailableResourceMessage message.

        Returns:
            str: Endpoint for available DAP plugins.
        """
        return cls._avilable_dap_plugins
