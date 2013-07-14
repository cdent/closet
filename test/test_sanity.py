

def setup_module(module):
    module.our_truth = 1
    module.our_false = 0

def teardown_module(module):
    pass

def test_truth():
    assert our_truth, 'truth is true'

def test_false():
    assert not our_false, 'false is false'

def test_string():
    assert 'hello' == 'hello', 'hello and hello are the same'
