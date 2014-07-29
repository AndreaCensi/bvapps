from bootstrapping_olympics.programs.manager.batch.main import (
    batch_process_manager)
from bootstrapping_olympics.programs.manager.meat.data_central import (
    DataCentral)
from conf_tools import GlobalConfig
from quickapp import iterate_context_names
import os



def jobs_comptests(context):
    from comptests import jobs_registrar

    # get testing configuration directory 
    from pkg_resources import resource_filename  # @UnresolvedImport
    rel = resource_filename("bvapps", "configs")
    dirname = os.path.join(rel, '..', '..', '..', 'bdse1')
    
    dirname2 = os.path.join(rel, '..', '..', '..', 'bo_app1') # e.g. r_rf_A
    
    from vehicles import get_vehicles_config
    get_vehicles_config().load('default')
    
    # load into bootstrapping_olympics
    from bootstrapping_olympics import get_boot_config


    for d in [dirname, dirname2]:
        d = os.path.abspath(d)
        if not os.path.exists(d):
            raise ValueError('directory does not exist: %r' % d)
        
        GlobalConfig.global_load_dir(d) 
        
    # Our tests are its tests with our configuration
    from bootstrapping_olympics import unittests
    
    from boot_manager import unittests, get_bootbatch_config
    
    
    jobs_registrar(context, get_boot_config())
    jobs_registrar(context, get_vehicles_config())
    jobs_registrar(context, get_bootbatch_config())


#     
#     which = ["bv1bds2"]
#     for c, id_set in iterate_context_names(context, which, key='set'):
#         root = os.path.join(c.get_output_dir(), 'data_central')
#         if not os.path.exists(root):
#             os.makedirs(root)
#             os.makedirs(os.path.join(root, 'config'))
#         data_central = DataCentral(root)
#         c.comp_config_dynamic(batch_process_manager, data_central, which_sets=id_set)
     
    
