import pytest
import torch
from neuromancer.system import Node, System


# Define fixtures
@pytest.fixture
def sample_data():
    # Sample data for testing
    return {
        'input1': torch.tensor([[1.0, 2.0], [3.0, 4.0]]),
        'input2': torch.tensor([[5.0, 6.0], [7.0, 8.0]])
    }


@pytest.fixture
def sample_callable():
    # Sample callable function for testing
    def callable(input1, input2):
        return input1 + input2, input1 - input2

    return callable


# Test cases
def test_node_initialization():
    node = Node(sample_callable, ['input1', 'input2'], ['output1', 'output2'], name='test_node')
    assert node.input_keys == ['input1', 'input2']
    assert node.output_keys == ['output1', 'output2']
    assert node.name == 'test_node'

"""
def test_node_forward(sample_data):
    node = Node(sample_callable, ['input1', 'input2'], ['output1', 'output2'])
    data_dict = sample_data
    result = node.forward(data_dict)

    assert 'output1' in result
    assert 'output2' in result
    assert torch.all(result['output1'] == sample_data['input1'] + sample_data['input2'])
    assert torch.all(result['output2'] == sample_data['input1'] - sample_data['input2'])


def test_node_forward_single_output(sample_data):
    # Test when the callable returns a single tensor (not a tuple)
    def single_output_callable(input1, input2):
        return input1 + input2

    node = Node(single_output_callable, ['input1', 'input2'], ['output1', 'output2'])
    data_dict = sample_data
    result = node.forward(data_dict)

    assert 'output1' in result
    assert 'output2' not in result
    assert torch.all(result['output1'] == sample_data['input1'] + sample_data['input2'])


def test_node_missing_keys(sample_data):
    # Test with missing input keys in the data dictionary
    node = Node(sample_callable, ['missing_input'], ['output1', 'output2'])
    data_dict = sample_data

    with pytest.raises(KeyError):
        node.forward(data_dict)


def test_node_extra_keys(sample_data):
    # Test with extra keys in the data dictionary
    node = Node(sample_callable, ['input1', 'input2', 'extra_input'], ['output1', 'output2'])
    data_dict = sample_data

    with pytest.raises(KeyError):
        node.forward(data_dict)


def test_node_attribute_usage():
    node1 = Node(sample_callable, ['input1'], ['output1'], name='node1')
    node2 = Node(sample_callable, ['input2'], ['output2'], name='node2')

    assert node1.name == 'node1'
    assert node2.name == 'node2'


def test_node_inheritance():
    # Test if Node is an instance of nn.Module
    assert isinstance(Node(sample_callable, ['input1'], ['output1']), torch.nn.Module)
"""