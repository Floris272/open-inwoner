from django.conf import settings

from django_setup_configuration.configuration import BaseConfigurationStep

from open_inwoner.configurations.models import SiteConfiguration

from .models import SiteConfigurationSettings


class SiteConfigurationStep(BaseConfigurationStep):
    """
    Set up general configuration ("Algemene configuratie")
    """

    verbose_name = "Site configuration"

    def is_configured(self):
        config = SiteConfiguration.get_solo()
        required_settings = SiteConfigurationSettings.get_required_settings()
        setting_to_config = SiteConfigurationSettings.get_config_mapping()

        for required_setting in required_settings:
            config_field = setting_to_config[required_setting]
            if not getattr(config, config_field, None):
                return False
        return True

    def configure(self):
        config = SiteConfiguration.get_solo()
        setting_to_config = SiteConfigurationSettings.get_config_mapping()

        for key, value in setting_to_config.items():
            setting = getattr(settings, key)
            if setting is not None:
                setattr(config, value, setting)
        config.save()

    def test_configuration(self):
        ...
