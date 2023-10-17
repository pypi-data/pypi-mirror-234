# ver 2.0.1

import numpy as np
from dynamixel_sdk import *

class Dxlfunc:
    class Address:
        ModelNumber         = {'X': 0, 'P': 0}
        ModelInformation    = {'X': 2, 'P': 2}
        VersionOfFirmware   = {'X': 6, 'P': 6}
        ID                  = {'X': 7, 'P': 7}
        BaudRate            = {'X': 8, 'P': 8}
        ReturnDelayTime     = {'X': 9, 'P': 9}
        DriveMode           = {'X': 10, 'P': 10}
        OperatingMode       = {'X': 11, 'P': 11}
        SecondaryShadowID   = {'X': 12, 'P': 12}
        ProtocolVersion     = {'X': 13, 'P': 13}
        HomingOffset        = {'X': 20, 'P': 20}
        MovingThreshold     = {'X': 24, 'P': 24}
        TemperatureLimit    = {'X': 31, 'P': 31}
        MaxVoltageLimit     = {'X': 32, 'P': 32}
        MinVoltageLimit     = {'X': 34, 'P': 34}
        PWMLimit            = {'X': 36, 'P': 36}
        CurrentLimit        = {'X': 38, 'P': 38}
        AccelerationLimit   = {'X': 40, 'P': 40}
        VelocityLimit       = {'X': 44, 'P': 44}
        MaxPositionLimit    = {'X': 48, 'P': 48}
        MinPositionLimit    = {'X': 52, 'P': 52}
        Shutdown            = {'X': 63, 'P': 63}
        TorqueEnable        = {'X': 64, 'P': 512}
        LED                 = {'X': 65, 'P': 513}  # Pシリーズは3色に点灯可能
        StatusReturnLevel   = {'X': 68, 'P': 516}
        RegisteredInstruction = {'X': 69, 'P': 517}
        HardwareErrorStatus = {'X': 70, 'P': 518}
        VelocityIGain       = {'X': 76, 'P': 524}
        VelocityPGain       = {'X': 78, 'P': 526}
        PositionDGain       = {'X': 80, 'P': 528}
        PositionIGain       = {'X': 82, 'P': 530}
        PositionPGain       = {'X': 84, 'P': 532}
        Feedforward2ndGain  = {'X': 88, 'P': 536}
        Feedforward1stGain  = {'X': 90, 'P': 538}
        BusWatchdog         = {'X': 98, 'P': 546}
        GoalPWM             = {'X': 100, 'P': 548}
        GoalCurrent         = {'X': 102, 'P': 550}
        GoalVelocity        = {'X': 104, 'P': 552}
        ProfileAcceleration = {'X': 108, 'P': 556}
        ProfileVelocity     = {'X': 112, 'P': 560}
        GoalPosition        = {'X': 116, 'P': 564}
        RealtimeTick        = {'X': 120, 'P': 568}
        Moving              = {'X': 122, 'P': 570}
        MovingStatus        = {'X': 123, 'P': 571}
        PresentPWM          = {'X': 124, 'P': 572}
        PresentCurrent      = {'X': 126, 'P': 574}
        PresentVelocity     = {'X': 128, 'P': 576}
        PresentPosition     = {'X': 132, 'P': 580}
        VelocityTrajectory  = {'X': 136, 'P': 584}
        PositionTrajectory  = {'X': 140, 'P': 588}
        PresentInputVoltage = {'X': 144, 'P': 592}
        PresentTemperature  = {'X': 146, 'P': 594}

    class operating_mode:
        current_control = 0
        velocity_control = 1
        position_control = 3
        extended_Position_control = 4
        current_base_position_control = 5
        pwm_control = 16

    class _drive_mode_index:
        Torque_on_by_GoalUpdate = 3
        Time_based_Profile = 2
        Reverse_Mode = 0

    class ModelNumber:
        class X_series:
            XC330_M077 = 1190
            XC330_M181 = 1200
            XC330_M288 = 1240
            XC330_T181 = 1210
            XC330_T288 = 1220
            XL430_W250 = 1230
            twoXL430_W250 = 1090
            XC430_W150 = 1070
            XC430_W250 = 1080
            twoXC430_W250 = 1160
            XM430_W210 = 1030
            XH430_W210 = 1010
            XH430_V210 = 1050
            XD430_T210 = 1011
            XM430_W350 = 1020
            XH430_W350 = 1000
            XH430_V350 = 1040
            XD430_T350 = 1001
            XW430_T200 = 1280
            XW430_T333 = 1270
            XM540_W150 = 1130
            XH540_W150 = 1110
            XH540_V150 = 1150
            XM540_W270 = 1120
            XH540_W270 = 1100
            XH540_V270 = 1140
            XW540_T140 = 1180
            XW540_T260 = 1170

        class P_series:
            PH54_200_S500 = 2020
            PH54_100_S500 = 2010
            PH42_020_S300 = 2000
            PM54_060_S250 = 2120
            PM54_040_S250 = 2110
            PM42_010_S260 = 2100

    class br_list:
        br9600 = 9600
        br19200 = 19200
        br38400 = 38400
        br57600 = 57600
        br115200 = 115200
        br230400 = 230400
        br460800 = 460800
        br500000 = 500000
        br576000 = 576000
        br921600 = 921600
        br1000000 = 1000000
        br1152000 = 1152000
        br2000000 = 2000000
        br2500000 = 2500000
        br3000000 = 3000000
        br3500000 = 3500000
        br4000000 = 4000000
        br4500000 = 4500000

    class __initErrorCode:
        USB_disconnect = -3000
        PowerSource_disconnect = -3001

    class DXL_Error(Exception):
        pass

    def __init__(self):
        self._portHandler = None
        self._packetHandler = PacketHandler(2.0)
        self.IDs = []
        self.Present_OperatingMode = []
        self.Present_DriveMode = []
        self.MotorSeries = {}
        self._one_byte_values = [self.Adrress.ID, self.Adrress.BaudRate, self.Adrress.ReturnDelayTime,
                                 self.Adrress.DriveMode, self.Adrress.OperatingMode,
                                 self.Adrress.SecondaryShadowID, self.Adrress.ProtocolVersion,
                                 self.Adrress.TemperatureLimit, self.Adrress.Shutdown,
                                 self.Adrress.TorqueEnable, self.Adrress.LED,
                                 self.Adrress.StatusReturnLevel, self.Adrress.HardwareErrorStatus,
                                 self.Adrress.BusWatchdog, self.Adrress.Moving,
                                 self.Adrress.MovingStatus, self.Adrress.PresentTemperature]
        self._two_byte_values = [self.Adrress.ModelNumber, self.Adrress.MaxVoltageLimit, self.Adrress.MinVoltageLimit,
                                 self.Adrress.PWMLimit, self.Adrress.CurrentLimit,
                                 self.Adrress.VelocityPGain, self.Adrress.VelocityPGain,
                                 self.Adrress.PositionPGain, self.Adrress.PositionIGain,
                                 self.Adrress.PositionDGain, self.Adrress.Feedforward1stGain,
                                 self.Adrress.Feedforward2ndGain, self.Adrress.GoalPWM,
                                 self.Adrress.GoalCurrent, self.Adrress.RealtimeTick,
                                 self.Adrress.PresentPWM, self.Adrress.PresentCurrent,
                                 self.Adrress.PresentInputVoltage]
        self._four_byte_values = [self.Adrress.HomingOffset, self.Adrress.MovingThreshold,
                                 self.Adrress.AccelerationLimit, self.Adrress.VelocityLimit,
                                 self.Adrress.MaxPositionLimit, self.Adrress.MinPositionLimit,
                                 self.Adrress.GoalVelocity, self.Adrress.ProfileAcceleration,
                                 self.Adrress.ProfileVelocity, self.Adrress.GoalPosition,
                                 self.Adrress.PresentPosition, self.Adrress.PresentVelocity,
                                 self.Adrress.VelocityTrajectory, self.Adrress.PositionTrajectory]

    def init(self, com, baudrate=57600):
        self._portHandler = PortHandler(com)
        try:
            if self._portHandler.openPort():
                if baudrate in list(self.br_list.__dict__.values()):
                    self._portHandler.baudrate = baudrate
                    self._portHandler.setupPort(baudrate)
                else:
                    raise self.DXL_Error("Argument baud rate is failure")
                tmp_adrress_id = 7
                self.IDs = [i for i in range(30) if self._packetHandler.read1ByteTxRx(self._portHandler, i, tmp_adrress_id)[1] == 0]
                if len(self.IDs) == 0:
                    for br in list(self.br_list.__dict__.values()):
                        if type(br) != int:
                            continue
                        self._portHandler.setBaudRate(br)
                        self.IDs = [i for i in range(10) if self._packetHandler.read1ByteTxRx(self._portHandler, i, tmp_adrress_id)[1] == 0]
                        if len(self.IDs) > 0:
                            raise self.DXL_Error("Argument baud rate is different from baud rate set in motor")
                if len(self.IDs) > 0:
                    tmp_adrress_model_number = 0
                    for id in self.IDs:
                        motor_series, _, _ = self._packetHandler.read2ByteTxRx(self._portHandler, id, tmp_adrress_model_number)
                        if motor_series in self.ModelNumber.X_series.__dict__.values():
                            self.MotorSeries[id] = 'X'
                        elif motor_series in self.ModelNumber.P_series.__dict__.values():
                            self.MotorSeries[id] = 'P'
                    self.Present_OperatingMode = [self.read(i, self.Adrress.OperatingMode) for i in self.IDs]
                    for i in self.IDs:
                        tmp = list(format(self.read(i, self.Adrress.DriveMode), '04b'))
                        tmp.reverse()
                        self.Present_DriveMode.append(''.join(tmp))
                    return len(self.IDs)
                else:
                    return self.__initErrorCode.PowerSource_disconnect
            else:
                return self.__initErrorCode.USB_disconnect
        except serial.serialutil.SerialException:
            return self.__initErrorCode.USB_disconnect

    def exit(self):
        self.write('ALL', self.Adrress.TorqueEnable, 0)
        self._portHandler.closePort()

    def reboot(self):
        for i in self.IDs:
            if not self.read(i, self.Adrress.HardwareErrorStatus) == 0:
                self._packetHandler.reboot(self._portHandler, i)
                while not self.read(i, self.Adrress.HardwareErrorStatus) == 0:
                    pass

    def write(self, MotorID, INPUT_Adrress, value):
        if MotorID == 'ALL':
            for i in self.IDs:
                if INPUT_Adrress in self._one_byte_values:
                    self._packetHandler.write1ByteTxRx(self._portHandler, i, INPUT_Adrress[self.MotorSeries[i]], value)
                elif INPUT_Adrress in self._two_byte_values:
                    self._packetHandler.write2ByteTxRx(self._portHandler, i, INPUT_Adrress[self.MotorSeries[i]], value)
                elif INPUT_Adrress in self._four_byte_values:
                    self._packetHandler.write4ByteTxRx(self._portHandler, i, INPUT_Adrress[self.MotorSeries[i]], value)
        else:
            if INPUT_Adrress in self._one_byte_values:
                self._packetHandler.write1ByteTxRx(self._portHandler, MotorID, INPUT_Adrress[self.MotorSeries[MotorID]], value)
            elif INPUT_Adrress in self._two_byte_values:
                self._packetHandler.write2ByteTxRx(self._portHandler, MotorID, INPUT_Adrress[self.MotorSeries[MotorID]], value)
            elif INPUT_Adrress in self._four_byte_values:
                self._packetHandler.write4ByteTxRx(self._portHandler, MotorID, INPUT_Adrress[self.MotorSeries[MotorID]], value)

    def read(self, MotorID, INPUT_Adrress):
        ret = 0
        if INPUT_Adrress in self._one_byte_values:
            ret, _, _ = self._packetHandler.read1ByteTxRx(self._portHandler, MotorID, INPUT_Adrress[self.MotorSeries[MotorID]])
            if ret >= np.power(2, 7):
                ret = ret - np.power(2, 8)
        elif INPUT_Adrress in self._two_byte_values:
            ret, _, _ = self._packetHandler.read2ByteTxRx(self._portHandler, MotorID, INPUT_Adrress[self.MotorSeries[MotorID]])
            if ret >= np.power(2, 15):
                ret = ret - np.power(2, 16)
        elif INPUT_Adrress in self._four_byte_values:
            ret, _, _ = self._packetHandler.read4ByteTxRx(self._portHandler, MotorID, INPUT_Adrress[self.MotorSeries[MotorID]])
            if ret >= 2**31:
                ret = ret - 2**32
        return ret

    def readTorque(self, MotorID, LowCurrent=False):
        value2current = 0.00269  # Convert value to current[A]
        current = self.read(MotorID, self.Adrress.PresentCurrent) * value2current
        motorType = self.read(MotorID, self.Adrress.ModelNumber)
        if motorType == self.ModelNumber.XM430_W210:
            if LowCurrent:
                current2torque_p = 0.9221
                current2torque_b = 0
            else:
                current2torque_p = 1.02
                current2torque_b = -0.164
        elif motorType == self.ModelNumber.XM430_W350:
            if LowCurrent:
                current2torque_p = 1.6245
                current2torque_b = 0
            else:
                current2torque_p = 1.73
                current2torque_b = -0.13
        else:
            print('No convertion params for this motor model')
            return 0
        return current2torque_p * current + current2torque_b

    def Change_OperatingMode(self, MotorID, INPUT_OPERATING_MODE):
        if MotorID == 'ALL':
            for i in self.IDs:
                now_frag = self.read(i, self.Adrress.TorqueEnable)
                self.write(i, self.Adrress.TorqueEnable, 0)
                self.write(i, self.Adrress.OperatingMode, INPUT_OPERATING_MODE)
                self.write(i, self.Adrress.TorqueEnable, now_frag)
                self.Present_OperatingMode[self.IDs.index(i)] = INPUT_OPERATING_MODE
        else:
            now_frag = self.read(MotorID, self.Adrress.TorqueEnable)
            self.write(MotorID, self.Adrress.TorqueEnable, 0)
            self.write(MotorID, self.Adrress.OperatingMode, INPUT_OPERATING_MODE)
            self.write(MotorID, self.Adrress.TorqueEnable, now_frag)
            self.Present_OperatingMode[self.IDs.index(MotorID)] = INPUT_OPERATING_MODE

    def Change_DriveMode(self, MotorID, Torque_on_by_GoalUpdate = None, Time_based_Profile = None, Reverse_Mode = None):
        if MotorID == 'ALL':
            for i in self.IDs:
                now_frag = self.read(i, self.Adrress.TorqueEnable)
                self.write(i, self.Adrress.TorqueEnable, 0)
                INPUT_DRIVE_MODE = list(self.Present_DriveMode.copy()[self.IDs.index(i)])
                if Reverse_Mode is not None:
                    INPUT_DRIVE_MODE[self._drive_mode_index.Reverse_Mode] = str(int(Reverse_Mode))
                if Time_based_Profile is not None:
                    INPUT_DRIVE_MODE[self._drive_mode_index.Time_based_Profile] = str(int(Time_based_Profile))
                if Torque_on_by_GoalUpdate is not None:
                    INPUT_DRIVE_MODE[self._drive_mode_index.Torque_on_by_GoalUpdate] = str(int(Torque_on_by_GoalUpdate))
                self.Present_DriveMode[self.IDs.index(i)] = ''.join(INPUT_DRIVE_MODE)
                INPUT_DRIVE_MODE = ''.join(list(reversed(INPUT_DRIVE_MODE)))
                self.write(i, self.Adrress.DriveMode, int(INPUT_DRIVE_MODE, 2))
                self.write(i, self.Adrress.TorqueEnable, now_frag)
        else:
            now_frag = self.read(MotorID, self.Adrress.TorqueEnable)
            self.write(MotorID, self.Adrress.TorqueEnable, 0)
            INPUT_DRIVE_MODE = list(self.Present_DriveMode.copy()[self.IDs.index(MotorID)])
            if Reverse_Mode is not None:
                INPUT_DRIVE_MODE[self._drive_mode_index.Reverse_Mode] = str(int(Reverse_Mode))
            if Time_based_Profile is not None:
                INPUT_DRIVE_MODE[self._drive_mode_index.Time_based_Profile] = str(int(Time_based_Profile))
            if Torque_on_by_GoalUpdate is not None:
                INPUT_DRIVE_MODE[self._drive_mode_index.Torque_on_by_GoalUpdate] = str(int(Torque_on_by_GoalUpdate))
            self.Present_DriveMode[self.IDs.index(MotorID)] = ''.join(INPUT_DRIVE_MODE)
            INPUT_DRIVE_MODE = ''.join(list(reversed(INPUT_DRIVE_MODE)))
            self.write(MotorID, self.Adrress.DriveMode, int(INPUT_DRIVE_MODE,2))
            self.write(MotorID, self.Adrress.TorqueEnable, now_frag)

    def PosCnt_Vbase(self, MotorID, Goal_position, Goal_velocity):
        if Goal_velocity < 0:
            raise self.DXL_Error('Goal velocity should be positive value in PosCnt_Vbase function')
        if self.Present_OperatingMode[self.IDs.index(MotorID)] != self.operating_mode.extended_Position_control:
            self.Change_OperatingMode(MotorID, self.operating_mode.extended_Position_control)
        if self.Present_DriveMode[self.IDs.index(MotorID)][self._drive_mode_index.Time_based_Profile] == '1':
            self.Change_DriveMode(MotorID, None,False,None)
        self.write(MotorID, self.Adrress.ProfileVelocity, Goal_velocity)
        self.write(MotorID, self.Adrress.GoalPosition, Goal_position)
        self.write(MotorID, self.Adrress.ProfileVelocity, 0)

    def PosCnt_Tbase(self, MotorID, Goal_position, Goal_Time):
        if Goal_Time < 0:
            raise self.DXL_Error('Goal time should be positive value in PosCnt_Tbase function')
        if self.Present_OperatingMode[self.IDs.index(MotorID)] != self.operating_mode.extended_Position_control:
            self.Change_OperatingMode(MotorID, self.operating_mode.extended_Position_control)
        if self.Present_DriveMode[self.IDs.index(MotorID)][self._drive_mode_index.Time_based_Profile] == '0':
            self.Change_DriveMode(MotorID, None,True,None)
        self.write(MotorID, self.Adrress.ProfileVelocity, Goal_Time)
        self.write(MotorID, self.Adrress.GoalPosition, Goal_position)
        self.write(MotorID, self.Adrress.ProfileVelocity, 0)

    def CurrentCnt_Vbase(self, MotorID, Goal_current, Goal_velocity):
        if Goal_velocity < 0:
            raise self.DXL_Error('Goal velocity should be positive value in CurrentCnt_Vbase function')
        if self.Present_OperatingMode[self.IDs.index(MotorID)] != self.operating_mode.current_base_position_control:
            self.Change_OperatingMode(MotorID, self.operating_mode.current_base_position_control)
        if self.Present_DriveMode[self.IDs.index(MotorID)][self._drive_mode_index.Time_based_Profile] == '1':
            self.Change_DriveMode(MotorID, None,False,None)
        self.write(MotorID, self.Adrress.ProfileVelocity, Goal_velocity)
        self.write(MotorID, self.Adrress.GoalCurrent, np.abs(Goal_current))
        if Goal_current < 0:
            self.write(MotorID, self.Adrress.GoalPosition, -256*4096+1)
        else:
            self.write(MotorID, self.Adrress.GoalPosition, 256*4096-1)
        self.write(MotorID, self.Adrress.ProfileVelocity, 0)