# ECS Shutdown Scheduler

Shuts down and starts containers for cost saving.

Leverages aws copilot for the infrastructure code and quick deployment.

## Setup
Initialize copilot in your account
```bash
copilot init
```

### Deploy the shutdown container
```bash
copilot job deploy --name ecs-shutdown-scheduler-shutdown
```

### Deploy the start container
```bash
copilot job deploy --name ecs-shutdown-scheduler-start
```

## Local execution
For development purposes you might want to execute the container locally.

```bash
docker build -t ecs-shutdown-scheduler .
docker run -v $HOME/.aws/:/root/.aws/:ro -e AWS_PROFILE=your_profile -e TASK="shutdown" ecs-shutdown-scheduler
```
