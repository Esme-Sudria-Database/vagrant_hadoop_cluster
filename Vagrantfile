# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "bento/ubuntu-16.04"

  config.vm.network "private_network", ip: "192.168.35.10"

  config.vm.provider "virtualbox" do |vb|
      vb.memory = "4096"
      vb.cpus = "2"
  end

  config.vm.provision "shell", inline: <<-SCRIPT
    rsync --archive --exclude='docker/data' /vagrant/ /home/vagrant/ansible/
    chmod -x /home/vagrant/ansible/inventory.ini

    apt-get update
    apt-get install -y python-pip
    apt-get install -y python-dev
    apt-get install -y libffi-dev

    pip install --upgrade setuptools
    pip install cffi
    pip install markupsafe
    pip install ansible

    export PYTHONUNBUFFERED=1
    ansible-playbook -i "/home/vagrant/ansible/inventory.ini" "/home/vagrant/ansible/playbooks/site.yml"
  SCRIPT
end
