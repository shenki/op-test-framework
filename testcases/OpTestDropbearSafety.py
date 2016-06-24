#!/usr/bin/python
#
# Copyright 2016 IBM Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied. See the License for the specific language governing
# permissions and limitations under the License.

# @package OpTestDropbearSafety
#  Test Dropbear SSH is not present in skiroot
#
# The skiroot (pettiboot environment) firmware contains dropbear for it's ssh
# client functioanlity. We do not want to enable network accessable system in
# the environemnt for security reasons.
#
# This test ensures that the ssh server is not running at boot
#

from common.OpTestIPMI import OpTestIPMI
from common.OpTestError import OpTestError
from common.OpTestSystem import OpTestSystem

class OpTestDropbearSafety():
    ## Initialize this object
    #  @param bmc_ip The IP address of the BMC
    #  @param ipmi_user The userid to issue the BMC IPMI commands with
    #  @param ipmi_password The password of BMC IPMI userid
    #
    def __init__(self, bmc_ip, ipmi_user, ipmi_password):
        self.ipmi = OpTestIPMI(bmc_ip, ipmi_user, ipmi_password,)
        self.system = OpTestSystem(bmc_ip, None, None, ipmi_user,
                ipmi_password)

    ##
    # @brief This function performs below steps
    #        1. Initially connecting to host and ipmi consoles for execution.
    #        2. Check for dropbear running
    #
    # @return BMC_CONST.FW_SUCCESS or raise OpTestError
    #
    def test_dropbear_running(self):
        self.test_init()
        connection = self.system.sys_get_ipmi_console()
        self.ipmi.ipmi_host_login(connection)
        self.ipmi.ipmi_host_set_unique_prompt(connection)

        res = self.ipmi.run_host_cmd_on_ipmi_console("ps")
        if res[-1] == '0':
            print 'ps command worked'
        else:
            raise OpTestError('failed to run ps command')

        for line in res.splitlines():
            if line.count('dropbear'):
                return BMC_CONST.FW_FAILED

        return BMC_CONST.FW_SUCCESS

    ##
    # @brief This is a common function for all the PRD test cases. This will be executed before
    #        any test case starts. Basically this provides below requirements.
    #
    #        1. Validates all required host commands
    #
    # @return BMC_CONST.FW_SUCCESS or raise OpTestError
    #
    def test_init(self):
        self.host.host_get_OS_Level()
        self.host.host_check_command("ps")

        return BMC_CONST.FW_SUCCESS
