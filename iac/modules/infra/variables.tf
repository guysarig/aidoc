variable "resource_prefix" {
  description = "Prefix to be used for all resource names"
  type        = string
}

variable "order_queue_name" {
  description = "Name suffix for the order processing queue"
  type        = string
}

variable "product_table_name" {
  description = "Name suffix for the product availability table"
  type        = string
} 