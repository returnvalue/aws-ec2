resource "aws_autoscaling_policy" "cpu_tracking" {
  name                   = "CPU-Target-Tracking"
  autoscaling_group_name = var.asg_name
  policy_type            = "TargetTrackingScaling"
  target_tracking_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ASGAverageCPUUtilization"
    }
    target_value = 50.0
  }
}
