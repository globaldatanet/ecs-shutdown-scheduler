from ecs_shutdown_scheduler.src import schedule_containers, ECSService
from moto import mock_applicationautoscaling

CLUSTER_ID = "test-cluster"
CLUSTER_ARN = "arn:aws:ecs:eu-west-1:123456789012:cluster/test-cluster"
SERVICE_NAME = "test-service"
SERVICE_ARN = "arn:aws:ecs:eu-west-1:123456789012:service/test-cluster/test-service"


def test_whitelist_true(monkeypatch):
    """ given: the service arn includes a whitelisted keyword
        when: the function is called
        then: it returns true
    """
    monkeypatch.setenv("WHITELIST", "test,dev")
    assert schedule_containers.whitelisted(SERVICE_ARN)


def test_whitelist_false(monkeypatch):
    """ given: the service arn doesnt include a whitelisted keyword
        when: the function is called
        then: it returns false
    """
    monkeypatch.setenv("WHITELIST", "test,dev")
    assert not schedule_containers.whitelisted(SERVICE_ARN.replace("test", "prod"))


@mock_applicationautoscaling
def test_constructor_no_autoscaling():
    """ given: the service has no autoscaling configured
        when: the constructor is called
        then: has_autoscaling is set to False
    """
    cluster = ECSService.ECSService(CLUSTER_ARN, SERVICE_ARN)
    assert not cluster.has_autoscaling
