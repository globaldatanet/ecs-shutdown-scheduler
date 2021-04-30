# ECS Shutdown Scheduler

![Linting](https://github.com/globaldatanet/ecs-shutdown-scheduler/workflows/Linting/badge.svg)

Shuts down and starts containers for cost saving in development environments.

Leverages aws SAM for the infrastructure code and quick deployment.

![](assets/ecs-shutdown-scheduler.png)

## Description

ECS Services with or without autoscaling configured can be shutdown using this lambda. Per default they are started at 7:00 AM and stopped at 9:00 PM, which should result in ~40% of cost saving for ECS in dev.

The problem even with autoscaling configured is that the containers dont scale down to 0 on their own. Whether you scale by CPUperTarget, MemoryperTarget or RequestCountperTarget, the minimum amount of tasks needs to be 1. This is because if they were to go down to 0, all these scaling metrics would be 0, so the service wouldnt start up again. This lambda solves this problem: During the day the minimum amount of tasks can be set freely, while during the night the service is shut down.

Services are scheduled based on a whitelist, which defaults to: ["dev", "test"]. This should make sure that only services which run for testing or developing purposes are shutdown. This parameter is of course also customizable in the sam template.

## How to deploy

```bash
sam build
sam deploy --guided
```

## How to contribute

We're open for community contributions!

1) Download the repo
2) Run the tests
3) Make your changes and create a Pull Request