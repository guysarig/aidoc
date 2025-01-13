# Infrastructure module
module "infra" {
  source = "./modules/infra"

  resource_prefix    = var.resource_prefix
  order_queue_name   = var.order_queue_name
  product_table_name = var.product_table_name
}

# Services module (depends on infra)
module "services" {
  source     = "./modules/services"
  depends_on = [module.infra]

  resource_prefix                = var.resource_prefix
  queue_url                      = module.infra.queue_url
  queue_arn                      = module.infra.queue_arn
  dynamodb_table_name            = module.infra.dynamodb_table_name
  dynamodb_table_arn             = module.infra.dynamodb_table_arn
  order_verification_lambda_name = var.order_verification_lambda_name
  order_retrieval_lambda_name    = var.order_retrieval_lambda_name
  orders_bucket_name             = var.orders_bucket_name
  lambda_payloads_dir            = var.lambda_payloads_dir
  region                         = var.region
}