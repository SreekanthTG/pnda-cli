#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#   Copyright (c) 2018 Cisco and/or its affiliates.
#   This software is licensed to you under the terms of the Apache License, Version 2.0
#   (the "License").
#   You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#   The code, technical concepts, and all information contained herein, are the property of
#   Cisco Technology, Inc.and/or its affiliated entities, under various laws including copyright,
#   international treaties, patent, and/or contract.
#   Any use of the material herein must be in accordance with the terms of the License.
#   All rights not expressly granted by the License are reserved.
#   Unless required by applicable law or agreed to separately in writing, software distributed
#   under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
#   ANY KIND, either express or implied.
#
#   Purpose: Backend implementation for creating PNDA on vSphere ESX with Terraform

import os
import sys
import json
import string
import time
import traceback
from shutil import copy
from python_terraform import *

from backend_base import BaseBackend
import pnda_cli_utils as utils

utils.init_logging()
CONSOLE = utils.CONSOLE_LOGGER
LOG = utils.FILE_LOGGER
LOG_FILE_NAME = utils.LOG_FILE_NAME

class TerraformBackend(BaseBackend):
    '''
    Deployment specific implementation for TerraformBackend for vSphere ESX
    '''
    def __init__(self, pnda_env, cluster, no_config_check, flavor, keyname, branch, dry_run):
        self._tf_work_dir = 'cli/tf-%s' % cluster
        self._terraform = Terraform(working_dir=self._tf_work_dir)
        self._dry_run = dry_run
        super(TerraformBackend, self).__init__(
            pnda_env, cluster, no_config_check, flavor, self._keyfile_from_keyname(keyname), branch)

    def load_node_config(self):
        '''
        Load a node config descriptor from a config.json file in the terraform flavor specific directory
        '''
        node_config_file = file('terraform/%s/config.json' % self._flavor)
        config = json.load(node_config_file)
        node_config_file.close()
        return config

    def fill_instance_map(self):
        '''
        Use the terraform outputs to generate a list of the target instances
        '''
        CONSOLE.debug('Checking details of created instances')
        instance_map = {}
        if os.path.exists('%s/outputs.tf' % self._tf_work_dir):
            output = self._terraform.output()
            if output:
                for entry in output:
                    instance_map[instance.tags['Name']] = {
                        "bootstrapped": False,
                        "ip_address": None,
                        "private_ip_address": None,
                        "name": 'Name',
                        "node_idx": 'node_idx',
                        "node_type": 'node_type'
                    }
        return instance_map

    def pre_install_pnda(self, node_counts):
        '''
        Use Terraform to launch a stack that PNDA can be installed on
        The ESX stack is defined in tf files in the flavor specific terraform directory
        '''
        self._set_up_terraform_resources(node_counts)
        if self._dry_run:
            return_code, stdout, stderr = self._terraform.plan(capture_output=False)
            CONSOLE.info('Dry run mode completed')
            sys.exit(0)

        CONSOLE.info('Creating ESX stack')
        return_code, stdout, stderr =  self._terraform.apply('-auto-approve', capture_output=False)
        if return_code != 0:
            CONSOLE.error('ESX stack did not come up. Exit code = %s', return_code)
            sys.exit(1)

        self.clear_instance_map_cache()

    def pre_expand_pnda(self, node_counts):
        '''
        Use Terraform to launch a stack that PNDA can be installed on
        The ESX stack is defined in tf files in the flavor specific terraform directory
        '''
        self._set_up_terraform_resources(node_counts)
        if self._dry_run:
            return_code, stdout, stderr =  self._terraform.plan(capture_output=False)
            CONSOLE.info('Dry run mode completed')
            sys.exit(0)

        CONSOLE.info('Updating ESX stack')
        return_code, stdout, stderr = self._terraform.apply('-auto-approve', capture_output=False)
        if return_code != 0:
            CONSOLE.error('ESX stack did not come up. Exit code = %s', return_code)
            sys.exit(1)

        self.clear_instance_map_cache()

    def pre_destroy_pnda(self):
        '''
        Use Terraform to delete the ESX stack that PNDA was installed on
        '''
        CONSOLE.info('Deleting ESX stack')
        if not os.path.exists('%s/tf-vars.tf' % self._tf_work_dir):
            CONSOLE.error("Directory %s from the cluster creation phase is required", self._tf_work_dir)
            sys.exit(1)

        return_code, stdout, stderr = self._terraform.destroy('-auto-approve', capture_output=False)
        if return_code != 0:
            CONSOLE.error('ESX stack was not destroyed. Exit code = %s', return_code)
            sys.exit(1)

        self.clear_instance_map_cache()

    def _set_up_terraform_resources(self, node_counts):
        properties = {}
        properties['PNDA_CLUSTER'] = self._cluster
        if node_counts:
            properties['DATANODE_COUNT'] = node_counts['datanodes']
            properties['OPENTSDB_COUNT'] = node_counts['opentsdb_nodes']
            properties['KAFKA_COUNT'] = node_counts['kafka_nodes']
            properties['ZK_COUNT'] = node_counts['zk_nodes']
        for parameter in self._pnda_env['terraform_parameters']:
            properties[parameter] = self._pnda_env['terraform_parameters'][parameter]
    
        # Make a directory for terraform to use
        if not os.path.exists(self._tf_work_dir):
            os.makedirs(self._tf_work_dir)
        CONSOLE.debug('Creating Terraform directory at %s' % self._tf_work_dir)
        # Copy in deploy.tf and flavor/outputs.tf
        copy('terraform/deploy.tf', self._tf_work_dir)
        copy('terraform/%s/outputs.tf' % self._flavor, self._tf_work_dir)
        # Merge tfvars-common.tf and flavor/tfvars-flavor.tf and expand out properties
        with open('terraform/tfvars-common.tf', 'rb') as vars_common_file:
            vars_common=vars_common_file.read()
        with open('terraform/%s/tfvars-flavor.tf' % self._flavor, 'rb') as vars_flavor_file:
            vars_flavor=vars_flavor_file.read()
        tf_vars = "%s\n%s" % (vars_common, vars_flavor)
        tf_vars = string.Template(tf_vars).safe_substitute(properties)
        with open('%s/tfvars.tf' % self._tf_work_dir, 'wb') as vars_file:
            vars_file.write(tf_vars)
        self._terraform.init()
        CONSOLE.info('Created Terraform directory at %s ' % self._tf_work_dir)