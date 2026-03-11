resource "aws_instance" "spot_server" {
  ami           = var.ami_id
  instance_type = "c5.large"
  subnet_id     = var.subnet_1_id
  instance_market_options {
    market_type = "spot"
  }
  tags = { Name = "BatchProcessorSpot" }
}
