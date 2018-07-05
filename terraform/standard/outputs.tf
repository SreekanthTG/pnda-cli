output "datanode_private_ip" {
   value = "${ vsphere_virtual_machine.datanode.*.default_ip_address }"
}

output "kafkanode_private_ip" {
   value = "${ vsphere_virtual_machine.kafka.*.default_ip_address }"
}

output "managers_private_ip" {
   value = "${ vsphere_virtual_machine.managers.*.default_ip_address }"
}

output "zookeeper_private_ip" {
   value = "${ vsphere_virtual_machine.zookeeper.*.default_ip_address }"
}

output "opentsdb_private_ip" {
   value = "${ vsphere_virtual_machine.opentsdb.*.default_ip_address }"
}

output "edge_private_ip" {
   value = "${ vsphere_virtual_machine.edge.*.default_ip_address }"
}

output "tools_private_ip" {
   value = "${ vsphere_virtual_machine.tools.*.default_ip_address }"
}

output "mirror_private_ip" {
   value = "${ vsphere_virtual_machine.pnda_mirror.*.default_ip_address }"
}