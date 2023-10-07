"""Machine Current Tango Hardware Object
Example XML:
<device class = "MachCurrent">
  <username>label for users</username>
  <tangoname>orion:10000/fe/id(or d)/xx</tangoname>
  <channel type="tango" name="OperatorMsg" polling="2000">SR_Operator_Mesg</channel>
  <channel type="tango" name="Current" polling="2000">SR_Current</channel>
  <channel type="tango" name="FillingMode" polling="2000">SR_Filling_Mode</channel>
  <channel type="tango" name="RefillCountdown" polling="2000">SR_Refill_Countdown</channel>
</device>
"""

from mxcubecore.HardwareObjects.abstract.AbstractMachineInfo import (
    AbstractMachineInfo,
)

import logging


class MachCurrent(AbstractMachineInfo):
    def __init__(self, name):
        super().__init__(name)
        self.opmsg = ""

    def init(self):
        try:
            chanCurrent = self.get_channel_object("Current")
            chanCurrent.connect_signal("update", self.value_changed)
            self.update_state(self.STATES.READY)
        except Exception as e:
            logging.getLogger("HWR").exception(e)

    def value_changed(self, value):
        mach = value or self.get_current()

        try:
            opmsg = self.get_channel_object("OperatorMsg").get_value()
            fillmode = self.get_channel_object("FillingMode").get_value()
            fillmode = fillmode.strip()

            refill = self.get_channel_object("RefillCountdown").get_value()
        except Exception as e:
            logging.getLogger("HWR").exception(e)
            opmsg, fillmode, value, refill = ("", "", -1, -1)

        if opmsg and opmsg != self.opmsg:
            self.opmsg = opmsg
            logging.getLogger("user_level_log").info(self.opmsg)
        self.emit("valueChanged", (mach, opmsg, fillmode, refill))

    def get_current(self) -> float:
        try:
            value = self.get_channel_object("Current").get_value()
        except Exception as e:
            logging.getLogger("HWR").exception(e)
            value = -1

        return value

    def get_message(self) -> str:
        try:
            msg = self.get_channel_object("OperatorMsg").get_value()
        except Exception as e:
            logging.getLogger("HWR").exception(e)
            msg = ""

        return msg

    def get_fill_mode(self) -> str:
        try:
            fmode = self.get_channel_object("FillingMode").get_value()
        except Exception as e:
            logging.getLogger("HWR").exception(e)
            fmode = ""

        return fmode
