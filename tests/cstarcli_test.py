# Copyright 2020 Datastax
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import copy
import unittest

import cstar.args
import cstar.cstarcli


def execute_command(args):
    return

def execute_continue(args):
    return

def execute_cleanup(args):
    return

class CstarcliTest(unittest.TestCase):

    def test_empty(self):

        parser = argparse.ArgumentParser(prog='cstar', formatter_class=argparse.RawDescriptionHelpFormatter)
        cstar.args.add_cstar_arguments(parser, cstar.cstarcli.get_commands(), execute_command, execute_continue, execute_cleanup)
        namespace = parser.parse_args([])

        self.assertEqual(namespace.sub_command, None)

    def test_cleanup_jobs(self):

        parser = argparse.ArgumentParser(prog='cstar', formatter_class=argparse.RawDescriptionHelpFormatter)
        cstar.args.add_cstar_arguments(parser, cstar.cstarcli.get_commands(), execute_command, execute_continue, execute_cleanup)
        namespace = parser.parse_args(["cleanup-jobs"])

        self.assertEqual(namespace.enforced_job_id, None)
        self.assertEqual(namespace.ignore_down_nodes, False)
        self.assertEqual(namespace.jmx_username, None)
        self.assertEqual(namespace.max_job_age, 7)
        self.assertEqual(namespace.output_directory, None)
        self.assertEqual(namespace.ssh_identity_file, None)
        self.assertEqual(namespace.ssh_username, None)
        self.assertEqual(namespace.ssh_password, None)
        self.assertEqual(namespace.stop_after, None)
        self.assertEqual(namespace.sub_command, 'cleanup-jobs')
        self.assertEqual(namespace.verbose, 0)

    def test_run(self):

        parser = argparse.ArgumentParser(prog='cstar', formatter_class=argparse.RawDescriptionHelpFormatter)
        cstar.args.add_cstar_arguments(parser, cstar.cstarcli.get_commands(), execute_command, execute_continue, execute_cleanup)
        namespace = parser.parse_args(["run", "--command", "echo"])

        self.assertEqual(namespace.COMMAND, 'echo')
        self.assertEqual(namespace.command.strategy, 'topology')
        self.assertEqual(namespace.cluster_parallel, None)
        self.assertEqual(namespace.dc_filter, None)
        self.assertEqual(namespace.dc_parallel, None)
        self.assertEqual(namespace.enforced_job_id, None)
        self.assertEqual(namespace.host, None)
        self.assertEqual(namespace.host_file, None)
        self.assertEqual(namespace.ignore_down_nodes, False)
        self.assertEqual(namespace.jmx_username, None)
        self.assertEqual(namespace.key_space, None)
        self.assertEqual(namespace.max_concurrency, None)
        self.assertEqual(namespace.node_done_pause_time, 0.0)
        self.assertEqual(namespace.output_directory, None)
        self.assertEqual(namespace.seed_host, None)
        self.assertEqual(namespace.ssh_identity_file, None)
        self.assertEqual(namespace.ssh_lib, 'paramiko')
        self.assertEqual(namespace.ssh_password, None)
        self.assertEqual(namespace.ssh_pause_time, 0.5)
        self.assertEqual(namespace.ssh_username, None)
        self.assertEqual(namespace.stop_after, None)
        self.assertEqual(namespace.strategy, None)
        self.assertEqual(namespace.strategy_all_per_dc, False)
        self.assertEqual(namespace.strategy_one, False)
        self.assertEqual(namespace.strategy_one_per_dc, False)
        self.assertEqual(namespace.strategy_topology, False)
        self.assertEqual(namespace.strategy_topology_per_dc, False)
        self.assertEqual(namespace.sub_command, 'run')
        self.assertEqual(namespace.timeout, None)
        self.assertEqual(namespace.verbose, 0)

    def test_run_strategy_one(self):

        parser = argparse.ArgumentParser(prog='cstar', formatter_class=argparse.RawDescriptionHelpFormatter)
        cstar.args.add_cstar_arguments(parser, cstar.cstarcli.get_commands(), execute_command, execute_continue, execute_cleanup)
        args = parser.parse_args(["run", "--command", "echo", "--strategy=one"])

        #print(args)
        self.assertEqual(args.COMMAND, 'echo')
        self.assertEqual(args.cluster_parallel, None)
        self.assertEqual(args.dc_filter, None)
        self.assertEqual(args.dc_parallel, None)
        self.assertEqual(args.enforced_job_id, None)
        self.assertEqual(args.host, None)
        self.assertEqual(args.host_file, None)
        self.assertEqual(args.ignore_down_nodes, False)
        self.assertEqual(args.jmx_username, None)
        self.assertEqual(args.key_space, None)
        self.assertEqual(args.max_concurrency, None)
        self.assertEqual(args.node_done_pause_time, 0.0)
        self.assertEqual(args.output_directory, None)
        self.assertEqual(args.seed_host, None)
        self.assertEqual(args.ssh_identity_file, None)
        self.assertEqual(args.ssh_lib, 'paramiko')
        self.assertEqual(args.ssh_password, None)
        self.assertEqual(args.ssh_pause_time, 0.5)
        self.assertEqual(args.ssh_username, None)
        self.assertEqual(args.stop_after, None)
        self.assertEqual(args.strategy, 'one')
        self.assertEqual(args.strategy_all_per_dc, False)
        self.assertEqual(args.strategy_one, False)
        self.assertEqual(args.strategy_one_per_dc, False)
        self.assertEqual(args.strategy_topology, False)
        self.assertEqual(args.strategy_topology_per_dc, False)
        self.assertEqual(args.sub_command, 'run')
        self.assertEqual(args.timeout, None)
        self.assertEqual(args.verbose, 0)

        computed_args = cstar.cstarcli.args_from_strategy_shortcut(copy.deepcopy(args))

        self.assertEqual(computed_args.COMMAND, 'echo')
        self.assertEqual(computed_args.cluster_parallel, None)
        self.assertEqual(computed_args.dc_filter, None)
        self.assertEqual(computed_args.dc_parallel, None)
        self.assertEqual(computed_args.enforced_job_id, None)
        self.assertEqual(computed_args.host, None)
        self.assertEqual(computed_args.host_file, None)
        self.assertEqual(computed_args.ignore_down_nodes, False)
        self.assertEqual(computed_args.jmx_username, None)
        self.assertEqual(computed_args.key_space, None)
        self.assertEqual(computed_args.max_concurrency, None)
        self.assertEqual(computed_args.node_done_pause_time, 0.0)
        self.assertEqual(computed_args.output_directory, None)
        self.assertEqual(computed_args.seed_host, None)
        self.assertEqual(computed_args.ssh_identity_file, None)
        self.assertEqual(computed_args.ssh_lib, 'paramiko')
        self.assertEqual(computed_args.ssh_password, None)
        self.assertEqual(computed_args.ssh_pause_time, 0.5)
        self.assertEqual(computed_args.ssh_username, None)
        self.assertEqual(computed_args.stop_after, None)
        self.assertEqual(computed_args.strategy, 'one')
        self.assertEqual(computed_args.strategy_all_per_dc, False)
        self.assertEqual(computed_args.strategy_one, False)
        self.assertEqual(computed_args.strategy_one_per_dc, False)
        self.assertEqual(computed_args.strategy_topology, False)
        self.assertEqual(computed_args.strategy_topology_per_dc, False)
        self.assertEqual(computed_args.sub_command, 'run')
        self.assertEqual(computed_args.timeout, None)
        self.assertEqual(computed_args.verbose, 0)

        self.assertEqual(
            cstar.strategy.parse(cstar.cstarcli.fallback(computed_args.strategy, args.strategy, "funk")),
            cstar.strategy.Strategy.ONE)


    def test_run_strategy_one__short(self):

        parser = argparse.ArgumentParser(prog='cstar', formatter_class=argparse.RawDescriptionHelpFormatter)
        cstar.args.add_cstar_arguments(parser, cstar.cstarcli.get_commands(), execute_command, execute_continue, execute_cleanup)
        args = parser.parse_args(["run", "--command", "echo", "--one"])

        #print(args)
        self.assertEqual(args.COMMAND, 'echo')
        self.assertEqual(args.cluster_parallel, None)
        self.assertEqual(args.dc_filter, None)
        self.assertEqual(args.dc_parallel, None)
        self.assertEqual(args.enforced_job_id, None)
        self.assertEqual(args.host, None)
        self.assertEqual(args.host_file, None)
        self.assertEqual(args.ignore_down_nodes, False)
        self.assertEqual(args.jmx_username, None)
        self.assertEqual(args.key_space, None)
        self.assertEqual(args.max_concurrency, None)
        self.assertEqual(args.node_done_pause_time, 0.0)
        self.assertEqual(args.output_directory, None)
        self.assertEqual(args.seed_host, None)
        self.assertEqual(args.ssh_identity_file, None)
        self.assertEqual(args.ssh_lib, 'paramiko')
        self.assertEqual(args.ssh_password, None)
        self.assertEqual(args.ssh_pause_time, 0.5)
        self.assertEqual(args.ssh_username, None)
        self.assertEqual(args.stop_after, None)
        self.assertEqual(args.strategy, None)
        self.assertEqual(args.strategy_all_per_dc, False)
        self.assertEqual(args.strategy_one, True)
        self.assertEqual(args.strategy_one_per_dc, False)
        self.assertEqual(args.strategy_topology, False)
        self.assertEqual(args.strategy_topology_per_dc, False)
        self.assertEqual(args.sub_command, 'run')
        self.assertEqual(args.timeout, None)
        self.assertEqual(args.verbose, 0)

        computed_args = cstar.cstarcli.args_from_strategy_shortcut(copy.deepcopy(args))

        #print(computed_args)
        self.assertEqual(computed_args.COMMAND, 'echo')
        self.assertEqual(computed_args.cluster_parallel, None)
        self.assertEqual(computed_args.dc_filter, None)
        self.assertEqual(computed_args.dc_parallel, False)
        self.assertEqual(computed_args.enforced_job_id, None)
        self.assertEqual(computed_args.host, None)
        self.assertEqual(computed_args.host_file, None)
        self.assertEqual(computed_args.ignore_down_nodes, False)
        self.assertEqual(computed_args.jmx_username, None)
        self.assertEqual(computed_args.key_space, None)
        self.assertEqual(computed_args.max_concurrency, None)
        self.assertEqual(computed_args.node_done_pause_time, 0.0)
        self.assertEqual(computed_args.output_directory, None)
        self.assertEqual(computed_args.seed_host, None)
        self.assertEqual(computed_args.ssh_identity_file, None)
        self.assertEqual(computed_args.ssh_lib, 'paramiko')
        self.assertEqual(computed_args.ssh_password, None)
        self.assertEqual(computed_args.ssh_pause_time, 0.5)
        self.assertEqual(computed_args.ssh_username, None)
        self.assertEqual(computed_args.stop_after, None)
        self.assertEqual(computed_args.strategy, 'one')
        self.assertEqual(computed_args.strategy_all_per_dc, False)
        self.assertEqual(computed_args.strategy_one, True)
        self.assertEqual(computed_args.strategy_one_per_dc, False)
        self.assertEqual(computed_args.strategy_topology, False)
        self.assertEqual(computed_args.strategy_topology_per_dc, False)
        self.assertEqual(computed_args.sub_command, 'run')
        self.assertEqual(computed_args.timeout, None)
        self.assertEqual(computed_args.verbose, 0)

        self.assertEqual(
            cstar.strategy.parse(cstar.cstarcli.fallback(computed_args.strategy, args.strategy, "funk")),
            cstar.strategy.Strategy.ONE)


    def test_run_stratgy_one_per_dc(self):

        parser = argparse.ArgumentParser(prog='cstar', formatter_class=argparse.RawDescriptionHelpFormatter)
        cstar.args.add_cstar_arguments(parser, cstar.cstarcli.get_commands(), execute_command, execute_continue, execute_cleanup)
        args = parser.parse_args(["run", "--command", "echo", "--strategy=one", "--dc-parallel"])

        #print(args)
        self.assertEqual(args.COMMAND, 'echo')
        self.assertEqual(args.cluster_parallel, None)
        self.assertEqual(args.dc_filter, None)
        self.assertEqual(args.dc_parallel, True)
        self.assertEqual(args.enforced_job_id, None)
        self.assertEqual(args.host, None)
        self.assertEqual(args.host_file, None)
        self.assertEqual(args.ignore_down_nodes, False)
        self.assertEqual(args.jmx_username, None)
        self.assertEqual(args.key_space, None)
        self.assertEqual(args.max_concurrency, None)
        self.assertEqual(args.node_done_pause_time, 0.0)
        self.assertEqual(args.output_directory, None)
        self.assertEqual(args.seed_host, None)
        self.assertEqual(args.ssh_identity_file, None)
        self.assertEqual(args.ssh_lib, 'paramiko')
        self.assertEqual(args.ssh_password, None)
        self.assertEqual(args.ssh_pause_time, 0.5)
        self.assertEqual(args.ssh_username, None)
        self.assertEqual(args.stop_after, None)
        self.assertEqual(args.strategy, 'one')
        self.assertEqual(args.strategy_all_per_dc, False)
        self.assertEqual(args.strategy_one, False)
        self.assertEqual(args.strategy_one_per_dc, False)
        self.assertEqual(args.strategy_topology, False)
        self.assertEqual(args.strategy_topology_per_dc, False)
        self.assertEqual(args.sub_command, 'run')
        self.assertEqual(args.timeout, None)
        self.assertEqual(args.verbose, 0)

        computed_args = cstar.cstarcli.args_from_strategy_shortcut(copy.deepcopy(args))

        self.assertEqual(computed_args.COMMAND, 'echo')
        self.assertEqual(computed_args.cluster_parallel, None)
        self.assertEqual(computed_args.dc_filter, None)
        self.assertEqual(computed_args.dc_parallel, True)
        self.assertEqual(computed_args.enforced_job_id, None)
        self.assertEqual(computed_args.host, None)
        self.assertEqual(computed_args.host_file, None)
        self.assertEqual(computed_args.ignore_down_nodes, False)
        self.assertEqual(computed_args.jmx_username, None)
        self.assertEqual(computed_args.key_space, None)
        self.assertEqual(computed_args.max_concurrency, None)
        self.assertEqual(computed_args.node_done_pause_time, 0.0)
        self.assertEqual(computed_args.output_directory, None)
        self.assertEqual(computed_args.seed_host, None)
        self.assertEqual(computed_args.ssh_identity_file, None)
        self.assertEqual(computed_args.ssh_lib, 'paramiko')
        self.assertEqual(computed_args.ssh_password, None)
        self.assertEqual(computed_args.ssh_pause_time, 0.5)
        self.assertEqual(computed_args.ssh_username, None)
        self.assertEqual(computed_args.stop_after, None)
        self.assertEqual(computed_args.strategy, 'one')
        self.assertEqual(computed_args.strategy_all_per_dc, False)
        self.assertEqual(computed_args.strategy_one, False)
        self.assertEqual(computed_args.strategy_one_per_dc, False)
        self.assertEqual(computed_args.strategy_topology, False)
        self.assertEqual(computed_args.strategy_topology_per_dc, False)
        self.assertEqual(computed_args.sub_command, 'run')
        self.assertEqual(computed_args.timeout, None)
        self.assertEqual(computed_args.verbose, 0)

        self.assertEqual(
            cstar.strategy.parse(cstar.cstarcli.fallback(computed_args.strategy, args.strategy, "funk")),
            cstar.strategy.Strategy.ONE)


    def test_run_stratgy_one_per_dc__short(self):

        parser = argparse.ArgumentParser(prog='cstar', formatter_class=argparse.RawDescriptionHelpFormatter)
        cstar.args.add_cstar_arguments(parser, cstar.cstarcli.get_commands(), execute_command, execute_continue, execute_cleanup)
        args = parser.parse_args(["run", "--command", "echo", "--one-per-dc"])

        #print(args)
        self.assertEqual(args.COMMAND, 'echo')
        self.assertEqual(args.cluster_parallel, None)
        self.assertEqual(args.dc_filter, None)
        self.assertEqual(args.dc_parallel, None)
        self.assertEqual(args.enforced_job_id, None)
        self.assertEqual(args.host, None)
        self.assertEqual(args.host_file, None)
        self.assertEqual(args.ignore_down_nodes, False)
        self.assertEqual(args.jmx_username, None)
        self.assertEqual(args.key_space, None)
        self.assertEqual(args.max_concurrency, None)
        self.assertEqual(args.node_done_pause_time, 0.0)
        self.assertEqual(args.output_directory, None)
        self.assertEqual(args.seed_host, None)
        self.assertEqual(args.ssh_identity_file, None)
        self.assertEqual(args.ssh_lib, 'paramiko')
        self.assertEqual(args.ssh_password, None)
        self.assertEqual(args.ssh_pause_time, 0.5)
        self.assertEqual(args.ssh_username, None)
        self.assertEqual(args.stop_after, None)
        self.assertEqual(args.strategy, None)
        self.assertEqual(args.strategy_all_per_dc, False)
        self.assertEqual(args.strategy_one, False)
        self.assertEqual(args.strategy_one_per_dc, True)
        self.assertEqual(args.strategy_topology, False)
        self.assertEqual(args.strategy_topology_per_dc, False)
        self.assertEqual(args.sub_command, 'run')
        self.assertEqual(args.timeout, None)
        self.assertEqual(args.verbose, 0)

        computed_args = cstar.cstarcli.args_from_strategy_shortcut(copy.deepcopy(args))

        self.assertEqual(computed_args.COMMAND, 'echo')
        self.assertEqual(computed_args.cluster_parallel, None)
        self.assertEqual(computed_args.dc_filter, None)
        self.assertEqual(computed_args.dc_parallel, True)
        self.assertEqual(computed_args.enforced_job_id, None)
        self.assertEqual(computed_args.host, None)
        self.assertEqual(computed_args.host_file, None)
        self.assertEqual(computed_args.ignore_down_nodes, False)
        self.assertEqual(computed_args.jmx_username, None)
        self.assertEqual(computed_args.key_space, None)
        self.assertEqual(computed_args.max_concurrency, None)
        self.assertEqual(computed_args.node_done_pause_time, 0.0)
        self.assertEqual(computed_args.output_directory, None)
        self.assertEqual(computed_args.seed_host, None)
        self.assertEqual(computed_args.ssh_identity_file, None)
        self.assertEqual(computed_args.ssh_lib, 'paramiko')
        self.assertEqual(computed_args.ssh_password, None)
        self.assertEqual(computed_args.ssh_pause_time, 0.5)
        self.assertEqual(computed_args.ssh_username, None)
        self.assertEqual(computed_args.stop_after, None)
        self.assertEqual(computed_args.strategy, 'one')
        self.assertEqual(computed_args.strategy_all_per_dc, False)
        self.assertEqual(computed_args.strategy_one, False)
        self.assertEqual(computed_args.strategy_one_per_dc, True)
        self.assertEqual(computed_args.strategy_topology, False)
        self.assertEqual(computed_args.strategy_topology_per_dc, False)
        self.assertEqual(computed_args.sub_command, 'run')
        self.assertEqual(computed_args.timeout, None)
        self.assertEqual(computed_args.verbose, 0)

        self.assertEqual(
            cstar.strategy.parse(cstar.cstarcli.fallback(computed_args.strategy, args.strategy, "funk")),
            cstar.strategy.Strategy.ONE)



    def test_continue(self):

        parser = argparse.ArgumentParser(prog='cstar', formatter_class=argparse.RawDescriptionHelpFormatter)
        cstar.args.add_cstar_arguments(parser, cstar.cstarcli.get_commands(), execute_command, execute_continue, execute_cleanup)
        namespace = parser.parse_args(["continue", "1"])
        
        self.assertEqual(namespace.enforced_job_id, None)
        self.assertEqual(namespace.ignore_down_nodes, False)
        self.assertEqual(namespace.jmx_username, None)
        self.assertEqual(namespace.job_id, '1')
        self.assertEqual(namespace.max_job_age, 7)
        self.assertEqual(namespace.output_directory, None)
        self.assertEqual(namespace.ssh_identity_file, None)
        self.assertEqual(namespace.ssh_username, None)
        self.assertEqual(namespace.ssh_password, None)
        self.assertEqual(namespace.stop_after, None)
        self.assertEqual(namespace.sub_command, 'continue')
        self.assertEqual(namespace.verbose, 0)

if __name__ == '__main__':
    unittest.main()
