resource "aws_security_group" "lab" {
  name        = "vulnerablebank-lab"
  description = "Intentionally insecure lab configuration"
  vpc_id      = "vpc-00000000"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}