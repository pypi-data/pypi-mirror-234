import ctypes
import functools
import logging
import threading
import time

import dynamixel_sdk as dxl
from serial.tools import list_ports


def get_logger(name):
    logger = logging.getLogger(name)
    if not logger.handlers:
        # Prevent logging from propagating to the root logger
        logger.propagate = 0
        logger.setLevel(("INFO"))
        console = logging.StreamHandler()
        logger.addHandler(console)
        formatter = logging.Formatter(
            "%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s"
            # "%(asctime)s — %(levelname)s — %(message)s"
        )
        console.setFormatter(formatter)
    return logger


def synchronized(lock):
    def decorator(wrapped):
        @functools.wraps(wrapped)
        def wrapper(*args, **kwargs):
            with lock:
                return wrapped(*args, **kwargs)

        return wrapper

    return decorator


# See https://emanual.robotis.com/docs/en/dxl/mx/mx-106-2/ for #
# appropriate control table values at each address #
class DXLControlv2:
    # THESE ARE READ ONLY (FOR STATUS/INFO) #
    DEV_MODEL_NUMBER = 0  # 2 BYTES
    DEV_MODEL_INFO = 2  # 4 BYTES
    DEV_FIRMWARE = 6  # 1 BYTE
    DEV_REG_INSTRUCTION = 69  # 1 BYTE
    DEV_HARDWARE_ERR = 70  # 1 BYTE
    DEV_COUNT_TIME = 120  # 2 BYTES
    DEV_MOVING = 122  # 1 BYTE
    DEV_MOVING_STATUS = 123  # 1 BYTE
    DEV_CURRENT_PWM = 124  # 2 BYTES
    DEV_CURRENT_CURRENT = 126  # 2 BYTES
    DEV_CURRENT_VELOCITY = 128  # 4 BYTES
    DEV_CURRENT_POS = 132  # 4 BYTES
    DEV_CURRENT_VOLTAGE = 144  # 2 BYTES
    DEV_CURRENT_TEMP = 146  # 1 BYTE

    # THESE ARE READ AND WRITE #
    DEV_ID = 7  # 1 BYTE
    DEV_BAUD_RATE = 8  # 1 BYTE
    DEV_DRIVE_MODE = 10  # 1 BYTE
    DEV_OPERATING_MODE = 11  # 1 BYTE
    DEV_PROTOCOL_TYPE = 13  # 1 BYTE
    DEV_SHUTDOWN_ERROR_INFO = 6  # 1 BYTE
    DEV_HOMING_OFFSET = 20  # 4 BYTES
    DEV_RETURN_DELAY_TIME = 9  # 1 BYTE
    DEV_MOVING_THRESHOLD = 24  # 4 BYTES
    LIMIT_TEMP = 31  # 1 BYTE
    LIMIT_MAX_VOLTAGE = 32  # 2 BYTES
    LIMIT_MIN_VOLTAGE = 34  # 2 BYTES
    LIMIT_PWN = 36  # 2 BYTES
    LIMIT_CURRENT = 38  # 2 BYTES
    LIMIT_ACCELERATION = 40  # 4 BYTES
    LIMIT_VELOCITY = 44  # 4 BYTES
    LIMIT_MAX_POS = 48  # 4 BYTES
    LIMIT_MIN_POS = 52  # 4 BYTES
    DEV_ENABLE_TORQUE = 64  # 1 BYTE
    DEV_TOGGLE_LED = 65  # 1 BYTE
    DEV_VELOCITY_P = 78  # 2 BYTES
    DEV_VELOCITY_I = 76  # 2 BYTES
    DEV_VELCOITY_D = 80  # 2 BYTES
    DEV_POS_P = 84  # 2 BYTES
    DEV_POS_I = 82  # 2 BYTES
    BUS_WATCHDOG = 98  # 1 BYTE
    DEV_GOAL_PWM = 100  # 2 BYTES
    DEV_GOAL_CURRENT = 102  # 2 BYTES
    DEV_GOAL_VELOCITY = 104  # 4 BYTES
    ACCELERATION_PROFILE = 108  # 4 BYTES
    VELOCITY_PROFILE = 112  # 4 BYTES
    DEV_GOAL_POSITION = 116  # 4 BYTES
    DEV_DRIVE_MODE = 10  # 1 BYTE
    DEV_MAX_TORQUE = 14  # 2 BYTES

    # These map int to baudrate #
    # should make a dict that goes [baudrate]:[int]
    BAUD_RATE_DICT = {
        9600: 0,
        57600: 1,
        115200: 2,
        1000000: 3,
        2000000: 4,
        3000000: 5,
        4000000: 6,
    }
    BAUD_RATE_DICT_READABLE = {
        0: 9600,
        1: 57600,
        2: 115200,
        3: 1000000,
        4: 2000000,
        5: 3000000,
        6: 4000000,
    }

    # Description of the operating mode #
    OPERATING_MODE = {
        0: "Current control",
        1: "Velocity control",
        3: "Position control (default)",
        4: "Multi-turn",
        5: "Current-based position",
        16: "PWM Control mode",
    }

    MODE_CURRENT_CONTROL = 0
    MODE_VELOCITY_CONTROL = 1
    MODE_POSITION_CONTROL = 3  # DEFAULT
    MODE_MULTITURN = 4
    MODE_CURRENT_BASED_POSITION = 5
    MODE_PWM = 16


class DXLControlv1:
    # THESE ARE READ ONLY (FOR STATUS/INFO) #
    DEV_MODEL_NUMBER = 0  # 2 BYTES
    DEV_FIRMWARE = 2  # 1 BYTE
    DEV_REG_INSTRUCTION = 44  # 1 BYTE
    DEV_COUNT_TIME = 50  # 2 BYTES
    DEV_MOVING = 46  # 1 BYTE
    DEV_CURRENT_VELOCITY = 38  # 4 BYTES
    DEV_CURRENT_POS = 36  # 4 BYTES
    DEV_CURRENT_VOLTAGE = 42  # 2 BYTES
    DEV_CURRENT_TEMP = 43  # 1 BYTE

    # THESE ARE READ AND WRITE #
    DEV_ID = 3  # 1 BYTE
    DEV_BAUD_RATE = 4  # 1 BYTE
    DEV_SHUTDOWN_ERROR_INFO = 18  # 1 BYTE
    DEV_RETURN_DELAY_TIME = 5  # 1 BYTE
    LIMIT_TEMP = 11  # 1 BYTE
    LIMIT_MAX_VOLTAGE = 13  # 2 BYTES
    LIMIT_MIN_VOLTAGE = 12  # 2 BYTES
    DEV_ENABLE_TORQUE = 24  # 1 BYTE
    DEV_CCW_COMPLIANCE_SLOPE = 29  # 1 BYTES
    DEV_CW_COMPLIANCE_SLOPE = 28  # 1 BYTES
    DEV_CCW_COMPLIANCE_MARGIN = 27  # 1 BYTES
    DEV_CW_COMPLIANCE_MARGIN = 26  # 1 BYTES
    DEV_GOAL_VELOCITY = 32  # 2 BYTES
    DEV_GOAL_POSITION = 30  # 4 BYTES
    DEV_DRIVE_MODE = 10  # 1 BYTE
    DEV_CW_ANGLE_LIMIT = 6  # 2 BYTES
    DEV_CCW_ANGLE_LIMIT = 8  # 2 BYTES

    # These map int to baudrate #
    # should make a dict that goes [baudrate]:[int]
    BAUD_RATE_DICT = {
        9600: 207,
        57600: 34,
        115200: 16,
        1000000: 1,
        2000000: 0,
    }
    BAUD_RATE_DICT_READABLE = {
        0: 2000000,
        1: 1000000,
        16: 115200,
        34: 57600,
        207: 9600,
    }

    # Description of the operating mode #
    OPERATING_MODE = {
        0: "Current control",
        1: "Velocity control",
        3: "Position control (default)",
        4: "Multi-turn",
        5: "Current-based position",
        16: "PWM Control mode",
    }

    MODE_CURRENT_CONTROL = 0
    MODE_VELOCITY_CONTROL = 1
    MODE_POSITION_CONTROL = 3  # DEFAULT
    MODE_MULTITURN = 4
    MODE_CURRENT_BASED_POSITION = 5
    MODE_PWM = 16


class DXLDefaults:
    PROTOCOL_VERSION = 2.0
    DEFAULT_BAUDRATE = 1  # maps to 57600

    DXL_MOVING_STATUS_THRESHOLD = 8


class DXLMotorSDK(DXLDefaults):
    lock = threading.RLock()

    def __init__(
        self,
        verbose=False,
        protocol_version=2.0,
        starting_baudrate=57600,
        target_baudrate=57600,
        dev=None
    ):
        if dev is not None:
            self.DEVICENAME = dev
        else:
            devs = list(list_ports.comports())

            try:
                for d in devs:
                    if ("USB" in d.device) or ("usbserial" in d.device):
                        self.DEVICENAME = d.device
            except IndexError:
                raise Exception("No DXL Driver found.")
        self.verbose = verbose
        self.log = get_logger(__name__)

        self.enable_torque = False
        self.starting_baudrate = starting_baudrate
        self.target_baudrate = target_baudrate

        self.PROTOCOL_VERSION = protocol_version
        if self.PROTOCOL_VERSION == 1.0:
            self.control = DXLControlv1
            self.RPM_UNIT = 0.916
        if self.PROTOCOL_VERSION == 2.0:
            self.control = DXLControlv2
            self.RPM_UNIT = 0.229  # / 2.0 #0.229 is from DXL e-manual

        self.connectToDXL()
        self.portHandler.setBaudRate(target_baudrate)
        self.encoder_margin = self.DXL_MOVING_STATUS_THRESHOLD

    @synchronized(lock)
    def connectToDXL(self):
        self.portHandler = dxl.PortHandler(self.DEVICENAME)
        if self.portHandler.openPort():
            if self.verbose:
                self.log.info(
                    "Succeeded to open the port, initializing packetHandler"
                )
            self.packetHandler = dxl.PacketHandler(
                self.PROTOCOL_VERSION
            )
            if self.verbose:
                self.log.info(
                    "Succeeded to initialize the packetHandler"
                )
        else:
            if self.verbose:
                self.log.info(
                    "Failed to open the port, packetHandler not initialized."
                )

    @synchronized(lock)
    def getBaudRate(self, dxl_id):
        (
            dxl_baud_rate,
            dxl_comm_result,
            dxl_error,
        ) = self.packetHandler.read1ByteTxRx(
            self.portHandler, dxl_id, self.control.DEV_BAUD_RATE
        )
        if dxl_comm_result != dxl.COMM_SUCCESS:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getTxRxResult(dxl_comm_result)
                )
            return False
        elif dxl_error != 0:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getRxPacketError(dxl_error)
                )
            return False
        else:
            return self.control.BAUD_RATE_DICT_READABLE[dxl_baud_rate]

    @synchronized(lock)
    def getHardwareError(self, dxl_id):
        (
            dxl_hardware_error,
            dxl_comm_result,
            dxl_error,
        ) = self.packetHandler.read1ByteTxRx(
            self.portHandler, dxl_id, self.control.DEV_HARDWARE_ERR
        )
        if dxl_comm_result != dxl.COMM_SUCCESS:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getTxRxResult(dxl_comm_result)
                )
            return False
        elif dxl_error != 0:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getRxPacketError(dxl_error)
                )
            return False
        else:
            return dxl_hardware_error

    @synchronized(lock)
    def getDriveMode(self, dxl_id):
        (
            dxl_drive_mode,
            dxl_comm_result,
            dxl_error,
        ) = self.packetHandler.read1ByteTxRx(
            self.portHandler, dxl_id, self.control.DEV_DRIVE_MODE
        )
        if dxl_comm_result != dxl.COMM_SUCCESS:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getTxRxResult(dxl_comm_result)
                )
            return False
        elif dxl_error != 0:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getRxPacketError(dxl_error)
                )
            return False
        else:
            return dxl_drive_mode

    @synchronized(lock)
    def getPortBaudRate(self):
        return self.portHandler.getBaudRate()

    @synchronized(lock)
    def getDXLID(self, dxl_id):
        # Read dxl id #
        (
            dxl_id,
            dxl_comm_result,
            dxl_error,
        ) = self.packetHandler.read1ByteTxRx(
            self.portHandler, dxl_id, self.control.DEV_ID
        )
        if dxl_comm_result != dxl.COMM_SUCCESS:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getTxRxResult(dxl_comm_result)
                )
        elif dxl_error != 0:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getRxPacketError(dxl_error)
                )
        else:
            return dxl_id

    @synchronized(lock)
    def setDXLID(self, dxl_id, target_dxl_id):
        # Read dxl id #
        dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(
            self.portHandler,
            dxl_id,
            self.control.DEV_ID,
            int(target_dxl_id),
        )
        if dxl_comm_result != dxl.COMM_SUCCESS:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getTxRxResult(dxl_comm_result)
                )
        elif dxl_error != 0:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getRxPacketError(dxl_error)
                )
        else:
            dxl_id = target_dxl_id
            if self.verbose:
                new_dxl_id = self.getDXLID(dxl_id)
                self.log.info(f"New DXL ID set to: {new_dxl_id}")

    @synchronized(lock)
    def getProtocolVersion(self, dxl_id):
        # Read dxl id #
        (
            dxl_protocol_version,
            dxl_comm_result,
            dxl_error,
        ) = self.packetHandler.read1ByteTxRx(
            self.portHandler, dxl_id, self.control.DEV_PROTOCOL_TYPE
        )
        if dxl_comm_result != dxl.COMM_SUCCESS:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getTxRxResult(dxl_comm_result)
                )
        elif dxl_error != 0:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getRxPacketError(dxl_error)
                )
        else:
            return dxl_protocol_version

    @synchronized(lock)
    def clearMultiTurnInfo(self, dxl_id):
        # Clear Multi-Turn Information #
        dxl_comm_result, dxl_error = self.packetHandler.clearMultiTurn(
            self.portHandler, dxl_id
        )
        if dxl_comm_result != dxl.COMM_SUCCESS:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getTxRxResult(dxl_comm_result)
                )
        elif dxl_error != 0:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getRxPacketError(dxl_error)
                )

    @synchronized(lock)
    def getPosition(self, dxl_id):
        # Read present position #
        if self.PROTOCOL_VERSION == 2.0:
            (
                dxl_present_position,
                dxl_comm_result,
                dxl_error,
            ) = self.packetHandler.read4ByteTxRx(
                self.portHandler, dxl_id, self.control.DEV_CURRENT_POS
            )
        if self.PROTOCOL_VERSION == 1.0:
            (
                dxl_present_position,
                dxl_comm_result,
                dxl_error,
            ) = self.packetHandler.read2ByteTxRx(
                self.portHandler, dxl_id, self.control.DEV_CURRENT_POS
            )
        if dxl_comm_result != dxl.COMM_SUCCESS:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getTxRxResult(dxl_comm_result)
                )
        elif dxl_error != 0:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getRxPacketError(dxl_error)
                )
        else:
            return ctypes.c_int32(dxl_present_position).value

    @synchronized(lock)
    def getMaxTorque(self, dxl_id):
        # Read present max torque #
        if self.PROTOCOL_VERSION == 2.0:
            self.log.info(
                "This method is not yet supported for protocol 2.0!"
            )
            return None
        if self.PROTOCOL_VERSION == 1.0:
            (
                dxl_max_torque,
                dxl_comm_result,
                dxl_error,
            ) = self.packetHandler.read2ByteTxRx(
                self.portHandler, dxl_id, self.control.DEV_MAX_TORQUE
            )
        if dxl_comm_result != dxl.COMM_SUCCESS:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getTxRxResult(dxl_comm_result)
                )
        elif dxl_error != 0:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getRxPacketError(dxl_error)
                )
        else:
            return ctypes.c_int32(dxl_max_torque).value

    @synchronized(lock)
    def getMovingThreshold(self, dxl_id):
        # Read present position #
        (
            dxl_moving_threshold,
            dxl_comm_result,
            dxl_error,
        ) = self.packetHandler.read4ByteTxRx(
            self.portHandler, dxl_id, self.control.DEV_MOVING_THRESHOLD
        )
        if dxl_comm_result != dxl.COMM_SUCCESS:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getTxRxResult(dxl_comm_result)
                )
        elif dxl_error != 0:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getRxPacketError(dxl_error)
                )
        else:
            return self.convertValue2RPM(dxl_moving_threshold)

    @synchronized(lock)
    def getGoalPosition(self, dxl_id):
        # Read present position #
        if self.PROTOCOL_VERSION == 2.0:
            (
                dxl_present_position,
                dxl_comm_result,
                dxl_error,
            ) = self.packetHandler.read4ByteTxRx(
                self.portHandler, dxl_id, self.control.DEV_GOAL_POSITION
            )
        if self.PROTOCOL_VERSION == 1.0:
            (
                dxl_goal_position,
                dxl_comm_result,
                dxl_error,
            ) = self.packetHandler.read2ByteTxRx(
                self.portHandler, dxl_id, self.control.DEV_GOAL_POSITION
            )
        if dxl_comm_result != dxl.COMM_SUCCESS:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getTxRxResult(dxl_comm_result)
                )
        elif dxl_error != 0:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getRxPacketError(dxl_error)
                )
        else:
            return dxl_goal_position

    @synchronized(lock)
    def getVelocity(self, dxl_id):
        # Read present position #
        if self.PROTOCOL_VERSION == 2.0:
            (
                dxl_current_velocity,
                dxl_comm_result,
                dxl_error,
            ) = self.packetHandler.read4ByteTxRx(
                self.portHandler,
                dxl_id,
                self.control.DEV_CURRENT_VELOCITY,
            )
        if self.PROTOCOL_VERSION == 1.0:
            (
                dxl_current_velocity,
                dxl_comm_result,
                dxl_error,
            ) = self.packetHandler.read2ByteTxRx(
                self.portHandler,
                dxl_id,
                self.control.DEV_CURRENT_VELOCITY,
            )
        if dxl_comm_result != dxl.COMM_SUCCESS:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getTxRxResult(dxl_comm_result)
                )
        elif dxl_error != 0:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getRxPacketError(dxl_error)
                )
        else:
            self.log.info(
                f"Velocity value:  {ctypes.c_int32(dxl_current_velocity).value}"
            )
            return self.convertValue2RPM(dxl_current_velocity)

    @synchronized(lock)
    def getGoalVelocity(self, dxl_id):
        # Read present velocity #
        if self.PROTOCOL_VERSION == 2.0:
            (
                dxl_goal_velocity,
                dxl_comm_result,
                dxl_error,
            ) = self.packetHandler.read4ByteTxRx(
                self.portHandler, dxl_id, self.control.DEV_GOAL_VELOCITY
            )
        if self.PROTOCOL_VERSION == 1.0:
            (
                dxl_goal_velocity,
                dxl_comm_result,
                dxl_error,
            ) = self.packetHandler.read2ByteTxRx(
                self.portHandler, dxl_id, self.control.DEV_GOAL_VELOCITY
            )
        if dxl_comm_result != dxl.COMM_SUCCESS:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getTxRxResult(dxl_comm_result)
                )
        elif dxl_error != 0:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getRxPacketError(dxl_error)
                )
        else:
            self.log.info(
                f"Velocity value:  {ctypes.c_int32(dxl_goal_velocity).value}"
            )
            return self.convertValue2RPM(dxl_goal_velocity)

    @synchronized(lock)
    def getVelocityProfile(self, dxl_id):
        # Read velocity profile #
        (
            dxl_velocity_profile,
            dxl_comm_result,
            dxl_error,
        ) = self.packetHandler.read4ByteTxRx(
            self.portHandler, dxl_id, self.control.VELOCITY_PROFILE
        )
        if dxl_comm_result != dxl.COMM_SUCCESS:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getTxRxResult(dxl_comm_result)
                )
        elif dxl_error != 0:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getRxPacketError(dxl_error)
                )
        else:
            return self.convertValue2RPM(dxl_velocity_profile)

    @synchronized(lock)
    def getAccelerationProfile(self, dxl_id):
        # Read velocity profile #
        (
            dxl_acceleration_profile,
            dxl_comm_result,
            dxl_error,
        ) = self.packetHandler.read4ByteTxRx(
            self.portHandler, dxl_id, self.control.ACCELERATION_PROFILE
        )
        if dxl_comm_result != dxl.COMM_SUCCESS:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getTxRxResult(dxl_comm_result)
                )
        elif dxl_error != 0:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getRxPacketError(dxl_error)
                )
        else:
            return ctypes.c_int32(dxl_acceleration_profile).value

    # Ranges from 0-100, scale is degrees Celsius #
    @synchronized(lock)
    def getTemperature(self, dxl_id):
        # Read present position #
        (
            dxl_current_temp,
            dxl_comm_result,
            dxl_error,
        ) = self.packetHandler.read1ByteTxRx(
            self.portHandler, dxl_id, self.control.DEV_CURRENT_TEMP
        )
        if dxl_comm_result != dxl.COMM_SUCCESS:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getTxRxResult(dxl_comm_result)
                )
        elif dxl_error != 0:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getRxPacketError(dxl_error)
                )
        else:
            return dxl_current_temp  # in degrees

    @synchronized(lock)
    def getVoltage(self, dxl_id):
        # Read present position #
        (
            dxl_current_voltage,
            dxl_comm_result,
            dxl_error,
        ) = self.packetHandler.read2ByteTxRx(
            self.portHandler, dxl_id, self.control.DEV_CURRENT_VOLTAGE
        )
        if dxl_comm_result != dxl.COMM_SUCCESS:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getTxRxResult(dxl_comm_result)
                )
        elif dxl_error != 0:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getRxPacketError(dxl_error)
                )
        else:
            return (
                dxl_current_voltage / 10.0
            )  # voltage from 95-160 -> 9.5-16.0V

    @synchronized(lock)
    def getCurrent(self, dxl_id):
        current_unit = 3.36e-3  # A
        # Read present position #
        (
            dxl_current_current,
            dxl_comm_result,
            dxl_error,
        ) = self.packetHandler.read2ByteTxRx(
            self.portHandler, dxl_id, self.control.DEV_CURRENT_CURRENT
        )
        if dxl_comm_result != dxl.COMM_SUCCESS:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getTxRxResult(dxl_comm_result)
                )
        elif dxl_error != 0:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getRxPacketError(dxl_error)
                )
        else:
            return dxl_current_current * current_unit

    @synchronized(lock)
    def getOperatingMode(self, dxl_id):
        # Read operating mode #
        (
            dxl_current_mode,
            dxl_comm_result,
            dxl_error,
        ) = self.packetHandler.read1ByteTxRx(
            self.portHandler, dxl_id, self.control.DEV_OPERATING_MODE
        )
        if dxl_comm_result != dxl.COMM_SUCCESS:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getTxRxResult(dxl_comm_result)
                )
        elif dxl_error != 0:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getRxPacketError(dxl_error)
                )
        else:
            return self.control.OPERATING_MODE[dxl_current_mode]

    @synchronized(lock)
    def getTorqueStatus(self, dxl_id):
        # Read Dynamixel Torque Status #
        (
            torque_status,
            dxl_comm_result,
            dxl_error,
        ) = self.packetHandler.read1ByteTxRx(
            self.portHandler, dxl_id, self.control.DEV_ENABLE_TORQUE
        )
        if dxl_comm_result != dxl.COMM_SUCCESS:
            self.log.info(
                "%s" % self.packetHandler.getTxRxResult(dxl_comm_result)
            )
        elif dxl_error != 0:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getRxPacketError(dxl_error)
                )
        else:
            if self.verbose:
                self.log.info(f"DXL torque status is:{torque_status}")

            return torque_status

    @synchronized(lock)
    def getMovingStatus(self, dxl_id):
        # Read Dynamixel Torque Status #
        (
            moving_status,
            dxl_comm_result,
            dxl_error,
        ) = self.packetHandler.read1ByteTxRx(
            self.portHandler, dxl_id, self.control.DEV_MOVING
        )
        if dxl_comm_result != dxl.COMM_SUCCESS:
            self.log.info(
                "%s" % self.packetHandler.getTxRxResult(dxl_comm_result)
            )
        elif dxl_error != 0:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getRxPacketError(dxl_error)
                )
        # else:
        #     if self.verbose:
        #         self.log.info(f"DXL moving status is:{moving_status}")

        return bool(moving_status)

    @synchronized(lock)
    def getCWAngleLimit(self, dxl_id):
        (
            cw_angle_limit,
            dxl_comm_result,
            dxl_error,
        ) = self.packetHandler.read2ByteTxRx(
            self.portHandler, dxl_id, self.control.DEV_CW_ANGLE_LIMIT
        )
        if dxl_comm_result != dxl.COMM_SUCCESS:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getTxRxResult(dxl_comm_result)
                )
            return False
        elif dxl_error != 0:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getRxPacketError(dxl_error)
                )
            return False
        else:
            return cw_angle_limit

    @synchronized(lock)
    def getCCWAngleLimit(self, dxl_id):
        (
            ccw_angle_limit,
            dxl_comm_result,
            dxl_error,
        ) = self.packetHandler.read2ByteTxRx(
            self.portHandler, dxl_id, self.control.DEV_CCW_ANGLE_LIMIT
        )
        if dxl_comm_result != dxl.COMM_SUCCESS:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getTxRxResult(dxl_comm_result)
                )
            return False
        elif dxl_error != 0:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getRxPacketError(dxl_error)
                )
            return False
        else:
            return ccw_angle_limit

    @synchronized(lock)
    def getVelocityLimit(self, dxl_id):
        (
            dxl_velocity_limit,
            dxl_comm_result,
            dxl_error,
        ) = self.packetHandler.read4ByteTxRx(
            self.portHandler, dxl_id, self.control.LIMIT_VELOCITY
        )

        if dxl_comm_result != dxl.COMM_SUCCESS:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getTxRxResult(dxl_comm_result)
                )
        elif dxl_error != 0:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getRxPacketError(dxl_error)
                )
        else:
            return self.convertValue2RPM(
                ctypes.c_int32(dxl_velocity_limit).value
            )

    @synchronized(lock)
    def getPosition_P(self, dxlid):
        (
            position_p,
            dxl_comm_result,
            dxl_error,
        ) = self.packetHandler.read2ByteTxRx(
            self.portHandler, dxlid, self.control.DEV_POS_P
        )
        if dxl_comm_result != dxl.COMM_SUCCESS:
            self.log.info(
                "%s" % self.packetHandler.getTxRxResult(dxl_comm_result)
            )
        elif dxl_error != 0:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getRxPacketError(dxl_error)
                )
        else:
            if self.verbose:
                self.log.debug(
                    f"Position PID, P = : {ctypes.c_int16(position_p).value}"
                )
        return ctypes.c_int16(position_p).value

    @synchronized(lock)
    def getPosition_I(self, dxlid):
        (
            position_i,
            dxl_comm_result,
            dxl_error,
        ) = self.packetHandler.read2ByteTxRx(
            self.portHandler, dxlid, self.control.DEV_POS_I
        )
        if dxl_comm_result != dxl.COMM_SUCCESS:
            self.log.info(
                "%s" % self.packetHandler.getTxRxResult(dxl_comm_result)
            )
        elif dxl_error != 0:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getRxPacketError(dxl_error)
                )
        else:
            if self.verbose:
                self.log.debug(
                    f"Position PID, I = : {ctypes.c_int16(position_i).value}"
                )
        return ctypes.c_int16(position_i).value

    ############################
    # BEGINNING OF SET METHODS #
    ############################
    @synchronized(lock)
    def setVelocityLimit(self, dxl_id, velocity_limit_rpm):
        # Write goal position #
        velocity_limit_value = self.convertRPM2Value(velocity_limit_rpm)
        dxl_comm_result, dxl_error = self.packetHandler.write4ByteTxRx(
            self.portHandler,
            dxl_id,
            self.control.LIMIT_VELOCITY,
            velocity_limit_value,
        )
        if dxl_comm_result != dxl.COMM_SUCCESS:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getTxRxResult(dxl_comm_result)
                )
        elif dxl_error != 0:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getRxPacketError(dxl_error)
                )
        else:
            if self.verbose:
                self.log.info(
                    f"Velocity limit set to {velocity_limit_rpm}"
                )

    @synchronized(lock)
    def setCWAngleLimit(self, dxl_id, cw_angle_limit):
        dxl_comm_result, dxl_error = self.packetHandler.write2ByteTxRx(
            self.portHandler,
            dxl_id,
            self.control.DEV_CW_ANGLE_LIMIT,
            cw_angle_limit,
        )
        if dxl_comm_result != dxl.COMM_SUCCESS:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getTxRxResult(dxl_comm_result)
                )
            return False
        elif dxl_error != 0:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getRxPacketError(dxl_error)
                )
            return False
        else:
            if self.verbose:
                self.log.info(f"CW angle limit set to {cw_angle_limit}")

    @synchronized(lock)
    def setCCWAngleLimit(self, dxl_id, ccw_angle_limit):
        dxl_comm_result, dxl_error = self.packetHandler.write2ByteTxRx(
            self.portHandler,
            dxl_id,
            self.control.DEV_CCW_ANGLE_LIMIT,
            ccw_angle_limit,
        )
        if dxl_comm_result != dxl.COMM_SUCCESS:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getTxRxResult(dxl_comm_result)
                )
            return False
        elif dxl_error != 0:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getRxPacketError(dxl_error)
                )
            return False
        else:
            if self.verbose:
                self.log.info(
                    f"CCW angle limit set to {ccw_angle_limit}"
                )

    @synchronized(lock)
    def setBaudRate_DXL(
        self,
        dxl_id,
        starting_baudrate=57600,
        target_baudrate=9600,
    ):
        # Set port baudrate #
        if self.portHandler.setBaudRate(starting_baudrate):
            if self.verbose:
                self.log.info(
                    f"Baudrate on PORT set to {starting_baudrate}"
                )

            # Next set baudrate for DXL #
            (
                dxl_comm_result,
                dxl_error,
            ) = self.packetHandler.write1ByteTxRx(
                self.portHandler,
                dxl_id,
                self.control.DEV_BAUD_RATE,
                self.control.BAUD_RATE_DICT[target_baudrate],
            )
            if dxl_comm_result != dxl.COMM_SUCCESS:
                if self.verbose:
                    self.log.info(
                        "%s"
                        % self.packetHandler.getTxRxResult(
                            dxl_comm_result
                        )
                    )
            elif dxl_error != 0:
                if self.verbose:
                    self.log.info(
                        "%s"
                        % self.packetHandler.getRxPacketError(dxl_error)
                    )

            # finally update port baudrate #
            if self.portHandler.setBaudRate(target_baudrate):
                if self.verbose:
                    self.log.info(
                        f"Baudrate set to {target_baudrate} on PORT"
                    )
        else:
            if self.verbose:
                self.log.info("Failed to change the baudrate")

    # default = 0, reversed = 1. for the base tracking drive you want to be in reversed mode
    @synchronized(lock)
    def setDXLDriveMode(self, dxl_id, mode=0):
        # Next set baudrate for DXL #
        dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(
            self.portHandler,
            dxl_id,
            self.control.DEV_DRIVE_MODE,
            mode,
        )
        if dxl_comm_result != dxl.COMM_SUCCESS:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getTxRxResult(dxl_comm_result)
                )
        elif dxl_error != 0:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getRxPacketError(dxl_error)
                )

        if self.verbose:
            self.log.info(f"Drive mode set to {mode}")

    @synchronized(lock)
    def setOperatingMode(self, dxl_id, mode):
        # Set operating mode #
        dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(
            self.portHandler,
            dxl_id,
            self.control.DEV_OPERATING_MODE,
            mode,
        )
        if dxl_comm_result != dxl.COMM_SUCCESS:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getTxRxResult(dxl_comm_result)
                )
        elif dxl_error != 0:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getRxPacketError(dxl_error)
                )
        else:
            if self.verbose:
                self.log.info(
                    f"Operating mode set to: {self.control.OPERATING_MODE[mode]}"
                )

    @synchronized(lock)
    def setEnableTorque(self, dxl_id):
        self.enable_torque = True

        # Enable Dynamixel Torque #
        dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(
            self.portHandler,
            dxl_id,
            self.control.DEV_ENABLE_TORQUE,
            int(self.enable_torque),
        )
        if dxl_comm_result != dxl.COMM_SUCCESS:
            self.log.info(
                "%s" % self.packetHandler.getTxRxResult(dxl_comm_result)
            )
        elif dxl_error != 0:
            if self.verbose:
                self.log.debug(
                    "%s"
                    % self.packetHandler.getRxPacketError(dxl_error)
                )
        else:
            if self.verbose:
                self.log.debug("DXL torque has been enabled")

    @synchronized(lock)
    def setDisableTorque(self, dxl_id):
        self.enable_torque = False

        # Disable Dynamixel Torque
        dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(
            self.portHandler,
            dxl_id,
            self.control.DEV_ENABLE_TORQUE,
            int(self.enable_torque),
        )
        if dxl_comm_result != dxl.COMM_SUCCESS:
            if self.verbose:
                self.log.debug(
                    "%s"
                    % self.packetHandler.getTxRxResult(dxl_comm_result)
                )
        elif dxl_error != 0:
            if self.verbose:
                self.log.debug(
                    "%s"
                    % self.packetHandler.getRxPacketError(dxl_error)
                )
        else:
            if self.verbose:
                self.log.debug("Torque was disabled")

    # goal_pos is an encoder value which is an int
    # range in wheel mode: -1,048,575 -> 1,048,575
    @synchronized(lock)
    def setGoalPosition(self, dxl_id, goal_pos):
        # Write goal position #
        if self.PROTOCOL_VERSION == 2.0:
            (
                dxl_comm_result,
                dxl_error,
            ) = self.packetHandler.write4ByteTxRx(
                self.portHandler,
                dxl_id,
                self.control.DEV_GOAL_POSITION,
                goal_pos,
            )
        if self.PROTOCOL_VERSION == 1.0:
            (
                dxl_comm_result,
                dxl_error,
            ) = self.packetHandler.write2ByteTxRx(
                self.portHandler,
                dxl_id,
                self.control.DEV_GOAL_POSITION,
                goal_pos,
            )
        if dxl_comm_result != dxl.COMM_SUCCESS:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getTxRxResult(dxl_comm_result)
                )
        elif dxl_error != 0:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getRxPacketError(dxl_error)
                )
        # else:
        #     if self.verbose:
        #         self.log.info(f"Goal position set to {goal_pos}")

    # range from 0 -> 1023, linear increase corresponds to %-age of total torque to be used
    @synchronized(lock)
    def setMaxTorque(self, dxl_id, goal_max_torque):
        goal_max_torque = int(goal_max_torque)
        # Write goal position #
        if self.PROTOCOL_VERSION == 2.0:
            self.log.info(
                "This method is not yet supported for protocol 2.0!"
            )
            return None

        if self.PROTOCOL_VERSION == 1.0:
            (
                dxl_comm_result,
                dxl_error,
            ) = self.packetHandler.write2ByteTxRx(
                self.portHandler,
                dxl_id,
                self.control.DEV_MAX_TORQUE,
                goal_max_torque,
            )
        if dxl_comm_result != dxl.COMM_SUCCESS:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getTxRxResult(dxl_comm_result)
                )
        elif dxl_error != 0:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getRxPacketError(dxl_error)
                )
        else:
            if self.verbose:
                self.log.info(f"Goal position set to {goal_max_torque}")

    @synchronized(lock)
    def setMovingThreshold(self, dxl_id, target_moving_threshold_rpm):
        # Write goal position #
        target_moving_threshold_value = self.convertRPM2Value(
            target_moving_threshold_rpm
        )
        dxl_comm_result, dxl_error = self.packetHandler.write4ByteTxRx(
            self.portHandler,
            dxl_id,
            self.control.DEV_MOVING_THRESHOLD,
            target_moving_threshold_value,
        )

        if dxl_comm_result != dxl.COMM_SUCCESS:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getTxRxResult(dxl_comm_result)
                )
        elif dxl_error != 0:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getRxPacketError(dxl_error)
                )
        else:
            if self.verbose:
                self.log.info(
                    f"Moving threshold set to {target_moving_threshold_rpm}"
                )

    @synchronized(lock)
    def setPosition_P(self, dxlid, p_value):
        dxl_comm_result, dxl_error = self.packetHandler.write2ByteTxRx(
            self.portHandler, dxlid, self.control.DEV_POS_P, p_value
        )
        if dxl_comm_result != dxl.COMM_SUCCESS:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getTxRxResult(dxl_comm_result)
                )
        if dxl_error != 0:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getRxPacketError(dxl_error)
                )

    @synchronized(lock)
    def setPosition_I(self, dxlid, i_value):
        dxl_comm_result, dxl_error = self.packetHandler.write2ByteTxRx(
            self.portHandler, dxlid, self.control.DEV_POS_I, i_value
        )
        if dxl_comm_result != dxl.COMM_SUCCESS:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getTxRxResult(dxl_comm_result)
                )
        if dxl_error != 0:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getRxPacketError(dxl_error)
                )

    @synchronized(lock)
    def setVelocity(self, dxl_id, rpm_goal):
        # Write goal velocity #
        GOAL_VELOCITY = self.convertRPM2Value(rpm_goal)
        if self.PROTOCOL_VERSION == 2.0:
            (
                dxl_comm_result,
                dxl_error,
            ) = self.packetHandler.write4ByteTxRx(
                self.portHandler,
                dxl_id,
                self.control.DEV_GOAL_VELOCITY,
                GOAL_VELOCITY,
            )
        if self.PROTOCOL_VERSION == 1.0:
            (
                dxl_comm_result,
                dxl_error,
            ) = self.packetHandler.write2ByteTxRx(
                self.portHandler,
                dxl_id,
                self.control.DEV_GOAL_VELOCITY,
                GOAL_VELOCITY,
            )

        if dxl_comm_result != dxl.COMM_SUCCESS:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getTxRxResult(dxl_comm_result)
                )
        if dxl_error != 0:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getRxPacketError(dxl_error)
                )

    @synchronized(lock)
    def rebootMotor(self, dxl_id):
        dxl_comm_result, dxl_error = self.packetHandler.reboot(
            self.portHandler, dxl_id
        )
        if dxl_comm_result != dxl.COMM_SUCCESS:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getTxRxResult(dxl_comm_result)
                )
            return False
        elif dxl_error != 0:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getRxPacketError(dxl_error)
                )
            return False
        else:
            self.log.info(
                "MotorID:%03d\tsuccesfully rebooted" % (dxl_id)
            )

    @synchronized(lock)
    def getLoad(self, dxl_id):
        # Read Current Load Value #
        (
            current_load,
            dxl_comm_result,
            dxl_error,
        ) = self.packetHandler.read2ByteTxRx(
            self.portHandler, dxl_id, self.control.DEV_CURRENT_CURRENT
        )
        if dxl_comm_result != dxl.COMM_SUCCESS:
            self.log.info(
                "%s" % self.packetHandler.getTxRxResult(dxl_comm_result)
            )
        elif dxl_error != 0:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getRxPacketError(dxl_error)
                )
        else:
            if self.verbose:
                self.log.debug(
                    f"DXL load value is: {abs(ctypes.c_int16(current_load).value/10)}%"
                )
        return ctypes.c_int16(current_load).value / 10

    @synchronized(lock)
    def setVelocityProfile(self, dxl_id, velocity_profile_rpm):
        velocity_profile_value = self.convertRPM2Value(
            velocity_profile_rpm
        )
        # Write goal velocity #
        if self.PROTOCOL_VERSION == 2.0:
            (
                dxl_comm_result,
                dxl_error,
            ) = self.packetHandler.write4ByteTxRx(
                self.portHandler,
                dxl_id,
                self.control.VELOCITY_PROFILE,
                velocity_profile_value,
            )
        if dxl_comm_result != dxl.COMM_SUCCESS:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getTxRxResult(dxl_comm_result)
                )
        if dxl_error != 0:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getRxPacketError(dxl_error)
                )

    @synchronized(lock)
    def setAccelerationProfile(self, dxl_id, acceleration_profile):
        # Write goal velocity #
        if self.PROTOCOL_VERSION == 2.0:
            (
                dxl_comm_result,
                dxl_error,
            ) = self.packetHandler.write4ByteTxRx(
                self.portHandler,
                dxl_id,
                self.control.ACCELERATION_PROFILE,
                acceleration_profile,
            )
        if dxl_comm_result != dxl.COMM_SUCCESS:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getTxRxResult(dxl_comm_result)
                )
        if dxl_error != 0:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getRxPacketError(dxl_error)
                )

    @synchronized(lock)
    def convertRPM2Value(self, rpm):
        # For conversions #
        # RPM2RADPERSEC = 0.104719755  # this is 2pi / 60 seconds
        RPM_UNIT = self.RPM_UNIT

        value = 0

        if rpm == 0:
            value = 0
        elif rpm < 0.0:
            value = rpm / RPM_UNIT
        elif rpm > 0.0:
            # value = (rpm / RPM_UNIT * RPM2RADPERSEC) + 1023
            value = rpm / RPM_UNIT

        return int(value)

    @synchronized(lock)
    def convertValue2RPM(self, value):
        # For conversions #
        # RPM2RADPERSEC = 0.104719755  # this is 2pi / 60 seconds
        RPM_UNIT = 0.229  # 0.229 is from DXL e-manual

        rpm = 0

        if value == 0:
            rpm = 0
        else:
            rpm = value * RPM_UNIT

        return rpm

    # @synchronized(lock)
    def moveDeltaPosition(self, dxl_id, posDelta, speed=2):
        goal_position = self.getPosition(dxl_id) + posDelta
        moving_speed = speed

        if posDelta < 0:
            movingDirection = -1
        else:
            movingDirection = 1

        self.setEnableTorque(dxl_id)
        self.setVelocity(dxl_id, movingDirection * moving_speed)
        # current_position = self.getPosition(dxl_id)
        # max_load_in_move = -1
        while (
            abs(self.getPosition(dxl_id) - goal_position)
            > self.encoder_margin
        ):
            time.sleep(0.0001)
        self.setDisableTorque(dxl_id)
        # self.setVelocity(dxl_id, 0)
        time.sleep(0.1)

        # print(f"\n Max Load: {max_load_in_move}")

    @synchronized(lock)
    def setHomingOffset(self, dxl_id, offset):
        # Write goal velocity #
        dxl_comm_result, dxl_error = self.packetHandler.write4ByteTxRx(
            self.portHandler,
            dxl_id,
            self.control.DEV_HOMING_OFFSET,
            offset,
        )
        if dxl_comm_result != dxl.COMM_SUCCESS:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getTxRxResult(dxl_comm_result)
                )
        if dxl_error != 0:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getRxPacketError(dxl_error)
                )

    @synchronized(lock)
    def setLEDOn(self, dxl_id):
        dxl_comm_result, dxl_error = self.packetHandler.write2ByteTxRx(
            self.portHandler, dxl_id, self.control.DEV_TOGGLE_LED, 1
        )
        if dxl_comm_result != dxl.COMM_SUCCESS:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getTxRxResult(dxl_comm_result)
                )
        if dxl_error != 0:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getRxPacketError(dxl_error)
                )

    @synchronized(lock)
    def setLEDOff(self, dxl_id):
        dxl_comm_result, dxl_error = self.packetHandler.write2ByteTxRx(
            self.portHandler, dxl_id, self.control.DEV_TOGGLE_LED, 0
        )
        if dxl_comm_result != dxl.COMM_SUCCESS:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getTxRxResult(dxl_comm_result)
                )
        if dxl_error != 0:
            if self.verbose:
                self.log.info(
                    "%s"
                    % self.packetHandler.getRxPacketError(dxl_error)
                )

    def moveTurns(self, dxl_id, turns, speed=4):
        delta_encoder_clicks = turns * 4096.0
        self.moveDeltaPosition(
            dxl_id, delta_encoder_clicks, speed=speed
        )
