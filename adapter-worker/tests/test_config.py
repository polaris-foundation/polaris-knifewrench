from dhos_knifewrench_adapter_worker.config import Config


def test_config_defaults(knifewrench_sample_config: Config) -> None:
    """
    Test that the default config sets default values correctly
    """
    config = knifewrench_sample_config

    assert config.RABBITMQ_CONNECTION_STRING is not None
    assert config.RABBITMQ_CONNECTION_STRING.endswith(":5672//")
    assert config.DHOS_KNIFEWRENCH_API == "http://dhos-knifewrench-api"
