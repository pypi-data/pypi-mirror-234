from bootstrapping_tools import resample_data


def resample_valid_data(effort_and_capture_data, bootstrapping_number):
    validate_method = validate_samples_to_fit
    return resample_valid_data_by_method(
        effort_and_capture_data, bootstrapping_number, validate_method
    )


def resample_valid_cumulative_data(cumulative_captures_data, bootstrapping_number):
    validate_method = validate_cumulative_samples_to_fit
    return resample_valid_data_by_method(
        cumulative_captures_data, bootstrapping_number, validate_method
    )


def resample_valid_data_by_method(effort_and_capture_data, bootstrapping_number, validate_method):
    blocks_length = 2
    sample = generate_samples(effort_and_capture_data, bootstrapping_number, blocks_length)
    return validate_method(sample)


def generate_samples(cumulative_captures_data, bootstrapping_number, blocks_length):
    return [
        resample_data(cumulative_captures_data, seed, blocks_length)
        for seed in range(bootstrapping_number)
    ]


def validate_samples_to_fit(samples):
    validated = [
        valid_sample
        for valid_sample in samples
        if valid_sample.Capturas.sum() != valid_sample.Capturas[0]
    ]
    return validated


def validate_cumulative_samples_to_fit(samples):
    validated = [
        valid_sample
        for valid_sample in samples
        if len(valid_sample.Cumulative_captures.unique()) > 1
        and len(valid_sample.CPUE.unique()) > 1
    ]
    return validated
