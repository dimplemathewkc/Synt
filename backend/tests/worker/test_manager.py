def test_manager():
    """
    Test manager.
    """
    from app.worker.manager import Manager

    manager = Manager.Instance()
    assert manager is not None
