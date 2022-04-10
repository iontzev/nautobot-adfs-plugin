from nautobot.extras.plugins import PluginConfig

class NautobotADFSConfig(PluginConfig):
    name = 'nautobot_adfs_plugin'
    verbose_name = 'Nautobot ADSF login'
    description = 'Nautobot plugin for SSO login using ADFS'
    version = '0.0.1'
    author = 'Max Iontzev'
    author_email = 'iontzev@gmail.com'
    base_url = 'sso'
    required_settings = []
    default_settings = {}

config = NautobotADFSConfig
