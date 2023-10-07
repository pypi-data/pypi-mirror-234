import pytest


@pytest.fixture
def assert_config_choice():
    def assert_config_choice(choice, value, options, description=None):
        assert choice == value
        assert choice.options == tuple(options)

        cls = type(choice)
        for option in options:
            assert cls(option) == option
            assert cls(option).options == tuple(options)

        options_string = ', '.join(options)
        with pytest.raises(ValueError, match=rf'^Not one of {options_string}: foo$'):
            cls('foo')

        if description is not None:
            assert choice.description == description

    return assert_config_choice


@pytest.fixture
def assert_config_number():
    def assert_config_number(number, value, min, max, description=None):
        assert number == value
        assert number.min == min
        assert number.max == max

        cls = type(number)
        for i in range(min, max + 1):
            assert cls(i) == i
            assert cls(i).min == min
            assert cls(i).max == max

        with pytest.raises(ValueError, match=rf'^Minimum is {min}$'):
            cls(min - 1)

        with pytest.raises(ValueError, match=rf'^Maximum is {max}$'):
            cls(max + 1)

        if description is not None:
            assert number.description == description

    return assert_config_number
