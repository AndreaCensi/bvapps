from bootstrapping_olympics.configuration.master import get_boot_config
from bootstrapping_olympics.programs.manager.meat.data_central import (
    DataCentral)
from quickapp.library.app.quickapp_imp import quickapp_main
from quickapp.library.app_commands.app_with_commands import (QuickMultiCmdApp,
    QuickMultiCmd, add_subcommand)
from rosstream2boot.config.rbconfig import get_rs2b_config
import os
from rosstream2boot.interfaces.ros_log import ExpLogFromYaml


class Campaign(QuickMultiCmdApp):
    cmd = 'yc'
    short = 'Main campaign program'

    boot_root = 'out/boot-root'
    
    def define_multicmd_options(self, params):
        # params.add_flag('dummy', help='workaround for a bug')
        # params.add_string_list('config', help='Configuration directory')
        pass
    
    def get_config_dirs(self):
        from pkg_resources import resource_filename  # @UnresolvedImport
        config_dir = resource_filename("yc1304", "config")
        return [config_dir]

    def get_rs2b_config(self):
        return self.rs2b_config

    def get_boot_config(self):
        return self.boot_config

    def get_data_central(self):
        return self.data_central
    
    def get_boot_root(self):
        return Campaign.boot_root

    def initial_setup(self):
        config_dirs = self.get_config_dirs()
            
        self.rs2b_config = get_rs2b_config()
        self.rs2b_config.load_dirs(config_dirs)
        
        self.boot_config = get_boot_config()
        self.boot_config.load_dirs(config_dirs)
        
        boot_root = self.get_boot_root()
        if not os.path.exists(boot_root):
            os.makedirs(boot_root)
        self.data_central = DataCentral(boot_root)
                  
        
                             
class CampaignCmd(QuickMultiCmd):
    
    def get_config_dirs(self):
        return self.get_parent().get_config_dirs()
    
    def get_rs2b_config(self):
        return self.get_parent().get_rs2b_config()

    def get_boot_config(self):
        return self.get_parent().get_boot_config()

    def get_boot_root(self):
        return self.get_parent().get_boot_root()
    
    def get_data_central(self):
        return self.get_parent().get_data_central()

    def get_log_index(self):
        return self.get_data_central().get_log_index()

    def instance_explog(self, id_explog):
        """ Instances the given explog and checks it is a ExpLogFromYaml """
        rs2b_config = self.get_rs2b_config()
        
        log = rs2b_config.explogs.instance(id_explog)
        if not isinstance(log, ExpLogFromYaml):
            self.info('Skipping log %r because not raw log.' % id_explog)
            return
        return log 
    
def campaign_sub(x):
    add_subcommand(Campaign, x)
    return x


def main():
    quickapp_main(Campaign)
    

