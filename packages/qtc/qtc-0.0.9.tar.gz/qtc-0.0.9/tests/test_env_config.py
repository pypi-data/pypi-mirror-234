import qtc.ext.unittest as ut
import qtc.env_config as ecfg


class TestEnvConfig(ut.TestCase):
    def test_get_env_config(self):
        self.assertEqual(ecfg.get_env_config().environment,
                         'RESEARCH')
        self.assertEqual(ecfg.get_env_config().get(prop='GMBP-RDS.host'),
                         'rm-rj9e2t4ee6xr208gk6o.mysql.rds.aliyuncs.com')


if __name__ == '__main__':
    ut.main()