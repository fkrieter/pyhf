import os
import pytest

import pyhf


def test_get_default_schema():
    assert os.path.isfile(pyhf.utils.get_default_schema())


def test_load_default_schema():
    assert pyhf.utils.load_schema(pyhf.utils.get_default_schema())


def test_load_missing_schema():
    with pytest.raises(IOError):
        pyhf.utils.load_schema('a/fake/path/that/should/not/work.json')


def test_load_custom_schema(tmpdir):
    temp = tmpdir.join("custom_schema.json")
    temp.write('{"foo": "bar"}')
    assert pyhf.utils.load_schema(temp.strpath)


@pytest.fixture(scope='module')
def hypotest_args():
    pdf = pyhf.simplemodels.hepdata_like(
        signal_data=[12.0, 11.0], bkg_data=[50.0, 52.0], bkg_uncerts=[3.0, 7.0]
    )
    mu_test = 1.0
    data = [51, 48] + pdf.config.auxdata
    return mu_test, data, pdf


def check_uniform_type(in_list):
    return all(
        [isinstance(item, type(pyhf.tensorlib.astensor(item))) for item in in_list]
    )


def test_hypotest_default(tmpdir, hypotest_args):
    """
    Check that the default return structure of pyhf.utils.hypotest is as expected
    """
    tb = pyhf.tensorlib

    kwargs = {}
    result = pyhf.utils.hypotest(*hypotest_args, **kwargs)
    # CLs_obs
    assert len(list(result)) == 1
    assert isinstance(result, type(tb.astensor(result)))


def test_hypotest_return_tail_probs(tmpdir, hypotest_args):
    """
    Check that the return structure of pyhf.utils.hypotest with the
    return_tail_probs keyword arg is as expected
    """
    tb = pyhf.tensorlib

    kwargs = {'return_tail_probs': True}
    result = pyhf.utils.hypotest(*hypotest_args, **kwargs)
    # CLs_obs, [CL_sb, CL_b]
    assert len(list(result)) == 2
    assert isinstance(result[0], type(tb.astensor(result[0])))
    assert len(result[1]) == 2
    assert check_uniform_type(result[1])


def test_hypotest_return_expected(tmpdir, hypotest_args):
    """
    Check that the return structure of pyhf.utils.hypotest with the
    additon of the return_expected keyword arg is as expected
    """
    tb = pyhf.tensorlib

    kwargs = {'return_tail_probs': True, 'return_expected': True}
    result = pyhf.utils.hypotest(*hypotest_args, **kwargs)
    # CLs_obs, [CLsb, CLb], CLs_exp
    assert len(list(result)) == 3
    assert isinstance(result[0], type(tb.astensor(result[0])))
    assert len(result[1]) == 2
    assert check_uniform_type(result[1])
    assert isinstance(result[2], type(tb.astensor(result[2])))


def test_hypotest_return_expected_set(tmpdir, hypotest_args):
    """
    Check that the return structure of pyhf.utils.hypotest with the
    additon of the return_expected_set keyword arg is as expected
    """
    tb = pyhf.tensorlib

    kwargs = {
        'return_tail_probs': True,
        'return_expected': True,
        'return_expected_set': True,
    }
    result = pyhf.utils.hypotest(*hypotest_args, **kwargs)
    # CLs_obs, [CLsb, CLb], CLs_exp, CLs_exp @[-2, -1, 0, +1, +2]sigma
    assert len(list(result)) == 4
    assert isinstance(result[0], type(tb.astensor(result[0])))
    assert len(result[1]) == 2
    assert check_uniform_type(result[1])
    assert isinstance(result[2], type(tb.astensor(result[2])))
    assert len(result[3]) == 5
    assert check_uniform_type(result[3])


def test_hypotest_return_test_statistics(tmpdir, hypotest_args):
    """
    Check that the return structure of pyhf.utils.hypotest with the
    additon of the return_test_statistics keyword arg is as expected
    """
    tb = pyhf.tensorlib

    kwargs = {
        'return_tail_probs': True,
        'return_expected': True,
        'return_expected_set': True,
        'return_test_statistics': True,
    }
    result = pyhf.utils.hypotest(*hypotest_args, **kwargs)
    # CLs_obs, [CLsb, CLb], CLs_exp, CLs_exp @[-2, -1, 0, +1, +2]sigma, [q_mu, q_mu_Asimov]
    assert len(list(result)) == 5
    assert isinstance(result[0], type(tb.astensor(result[0])))
    assert len(result[1]) == 2
    assert check_uniform_type(result[1])
    assert isinstance(result[2], type(tb.astensor(result[2])))
    assert len(result[3]) == 5
    assert check_uniform_type(result[3])
    assert len(result[4]) == 2
    assert check_uniform_type(result[4])
