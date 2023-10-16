import qtc.ext.unittest as ut
from qtc.ext.inspect import inspect_caller


class TestInspect(ut.TestCase):
    def test_inspect_caller(self):
        benchmark = {'CLASS': 'TestInspect',
                     'FUNC': 'test_inspect_caller',
                     'LINENO': 11,
                     'MODULE': 'test_inspect'}
        target = inspect_caller(return_info=['MODULE', 'CLASS', 'FUNC', 'LINENO'])
        target['MODULE'] = target['MODULE'].split('.')[-1]
        self.assertEqual(first=benchmark, second=target)


if __name__ == '__main__':
    ut.main()
