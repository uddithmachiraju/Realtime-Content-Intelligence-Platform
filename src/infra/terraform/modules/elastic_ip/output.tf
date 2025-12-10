
output "elastic_ip" {
  value       = aws_eip.webhook.public_ip
  description = "Elastic IP address"
}

output "allocation_id" {
  value       = aws_eip.webhook.id
  description = "Elastic IP allocation ID"
}

output "association_id" {
  value       = aws_eip.webhook.association_id
  description = "Elastic IP association ID"
}
