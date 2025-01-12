# Backend configuration
terraform {
  backend "s3" {
    bucket         = "aidoc-devops-cloud-ex-bucket3"
    key            = "tf/wrapper/terraform.tfstate"
    region         = "eu-central-1"
    encrypt        = true
    # dynamodb_table = "terraform-state-lock-table"
  }
}