// Vertical scale options that vary according to the flavor of PNDA being created

// PNDA mirror Node Variables
variable "pnda_mirror_cpu_count" {
  default     = "4"
  description = "Number of CPUs for the Datanode"
}
variable "pnda_mirror_memory_count" {
  default     = "10240"
  description = "Amount of Memory for the Data Node(s)"
}


// Datanode Node Variables
variable "datanode_count" {
  default = "${DATANODE_COUNT}"
}
variable "datanode_logvolumesize" {
  type        = "string"
  default     = "20"
  description = "Size in GB for the log volume"
}
variable "datanode_data1mountsize" {
  type        = "string"
  default     = "50"
  description = "Size in GB for the data1 directory mount"
}
variable "datanode_data2mountsize" {
  type        = "string"
  default     = "50"
  description = "Size in GB for the data2 directory mount"
}
variable "datanode_cpu_count" {
  default     = "8"
  description = "Number of CPUs for the Datanode"
}
variable "datanode_memory_count" {
  default     = "32000"
  description = "Amount of Memory for the Data Node(s)"
}


// Kafka Node Variables
variable "kafkanode_count" {
  default = "${KAFKA_COUNT}"
}
variable "kafka_logvolumesize" {
  type        = "string"
  default     = "20"
  description = "Size in GB for the log volume"
}
variable "kafka_datamountsize" {
  type        = "string"
  default     = "50"
  description = "Size in GB for the data directory mount"
}
variable "kafka_data2mountsize" {
  type        = "string"
  default     = "50"
  description = "Size in GB for the data directory mount"
}
variable "kafka_cpu_count" {
  default     = "4"
  description = "Number of CPUs for the Kafka Brokers"
}
variable "kafkanode_memory_count" {
  default     = "20000"
  description = "Amount of Memory for the Kafka Node(s)"
}


// Zookeeper Node Variables
variable "zookeeper_count" {
  default     = "${ZK_COUNT}"
  description = "Number of zookeeper nodes"
}
variable "zookeeper_logvolumesize" {
  type        = "string"
  default     = "20"
  description = "Size in GB for the log volume"
}
variable "zookeeper_datamountsize" {
  type        = "string"
  default     = "20"
  description = "Size in GB for the data directory mount"
}
variable "zookeeper_cpu_count" {
  default     = "4"
  description = "Number of CPUs for the Zookeepers"
}
variable "zookeeper_memory_count" {
  default     = "20000"
  description = "Amount of Memory for the Zookeeper Node(s)"
}


// Hadoop Manager Node Variables
variable "manager_count" {
  default     = "5"
  description = "Number of manager nodes including hadoop manager"
}
variable "manager_logvolumesize" {
  type        = "string"
  default     = "20"
  description = "Size in GB for the log volume"
}
variable "manager_datamountsize" {
  type        = "string"
  default     = "20"
  description = "Size in GB for the data directory mount"
}
variable "manager_cpu_count" {
  default     = "8"
  description = "Number of CPUs for the Managers"
}
variable "managernode_memory_count" {
  default     = "32000"
  description = "Amount of Memory for the Manager Node(s)"
}


// Edge node Variables
variable "edge_node_count" {
  default     = "1"
  description = "Number of Edge nodes in the Cluster"
}
variable "edge_node_logvolumesize" {
  type        = "string"
  default     = "20"
  description = "Size in GB for the log volume"
}
variable "edge_node_datamountsize" {
  type        = "string"
  default     = "20"
  description = "Size in GB for the data directory mount"
}
variable "edgenode_cpu_count" {
  default     = "8"
  description = "Number of CPUs for the Edge Node(s)"
}
variable "edgenode_memory_count" {
  default     = "32000"
  description = "Amount of Memory for the Edge Node(s)"
}


// Tools Node variables
variable "tools_node_count" {
  default     = "1"
  description = "Number of tools nodes in the Cluster"
}
variable "tools_node_logvolumesize" {
  type        = "string"
  default     = "20"
  description = "Size in GB for the log volume"
}
variable "tools_node_datamountsize" {
  type        = "string"
  default     = "20"
  description = "Size in GB for the data directory mount"
}
variable "toolsnode_cpu_count" {
  default     = "8"
  description = "Number of CPUs for the Tools Node(s)"
}
variable "toolsnode_memory_count" {
  default     = "20000"
  description = "Amount of Memory for the Tools Node(s)"
}


// OpenTSDB Node variables
variable "opentsdb_node_count" {
  default     = "${OPENTSDB_COUNT}"
  description = "Number of tools nodes in the Cluster"
}
variable "opentsdb_node_logvolumesize" {
  type        = "string"
  default     = "20"
  description = "Size in GB for the log volume"
}
variable "opentsdb_node_datamountsize" {
  type        = "string"
  default     = "20"
  description = "Size in GB for the data directory mount"
}
variable "opentsdbnode_cpu_count" {
  default     = "8"
  description = "Number of CPUs for the OpenTSDB Node(s)"
}
variable "opentsdbnode_memory_count" {
  default     = "20000"
  description = "Amount of Memory for the OpenTSDB Node(s)"
}
