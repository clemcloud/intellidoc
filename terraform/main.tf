variable "aws_region" {
  description = "AWS region to deploy into"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "used as a prefix when naming resources so they're easy to identify"
  type        = string
  default     = "intellidoc"
}
variable "db_password" {
  description = "password for the RDS postgres instance"
  type        = string
  sensitive   = true
}
variable "gemini_api_key" {
  description = "API key for Gemini"
  type        = string
  sensitive   = true
}