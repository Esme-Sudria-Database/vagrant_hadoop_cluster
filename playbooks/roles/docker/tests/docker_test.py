# coding: utf8

import os
import unittest

import vagrant
import paramiko

class DockerTests(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        script_directory_path = os.path.dirname(os.path.realpath(__file__))
        self.common_vagrant = vagrant.Vagrant(script_directory_path, quiet_stdout=False)
        self.common_vagrant.up(no_provision=True)
        self.common_vagrant.provision()

        vagrant_conf = self.common_vagrant.conf()
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh_client.connect(
            vagrant_conf['HostName'],
            port=int(vagrant_conf['Port']),
            username=vagrant_conf['User'],
            key_filename=vagrant_conf['IdentityFile']
        )

    @classmethod
    def tearDownClass(self):
        self.ssh_client.close()
        self.common_vagrant.destroy()

    def test_vagrant_user_can_use_docker_command(self):
        stdin, stdout, stderr = self.ssh_client.exec_command('docker --version')
        output = stdout.readlines()
        self.assertTrue(output[0].startswith('Docker'))

    def test_vagrant_user_can_pull_docker_image(self):
        stdin, stdout, stderr = self.ssh_client.exec_command('docker pull ubuntu')
        output = stdout.readlines()
        last_line_index = len(output) - 1
        self.assertTrue(
            'ubuntu:latest' in output[last_line_index],
            '[fails] invalid message:' + output[last_line_index]
        )

    def test_vagrant_user_can_pull_and_run_docker_image(self):
        self.ssh_client.exec_command('docker pull ubuntu')
        stdin, stdout, stderr = self.ssh_client.exec_command('docker run ubuntu echo "test"')

        output = stdout.readlines()
        self.assertEquals('test\n', output[0])


if __name__ == '__main__':
    unittest.main()
