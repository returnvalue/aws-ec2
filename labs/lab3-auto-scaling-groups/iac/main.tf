resource "aws_launch_template" "web_lt" {
  name_prefix   = "WebServersLT"
  image_id      = var.ami_id
  instance_type = "t3.micro"
  vpc_security_group_ids = [var.sg_id]
  user_data = base64encode(<<-EOF
              #!/bin/bash
              echo "Hello from LocalStack Web Server!" > index.html
              python3 -m http.server 80 &
              EOF
  )
}

resource "aws_autoscaling_group" "web_asg" {
  name                = "WebASG"
  vpc_zone_identifier = [var.subnet_1_id, var.subnet_2_id]
  target_group_arns   = [var.tg_arn]
  min_size            = 1
  max_size            = 4
  desired_capacity    = 2

  launch_template {
    id      = aws_launch_template.web_lt.id
    version = "$Latest"
  }
}
