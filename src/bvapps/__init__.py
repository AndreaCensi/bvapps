from boot_manager import DataCentral, batch_process_manager
import os


def jobs_comptests(context):
    # get testing configuration directory 
    from pkg_resources import resource_filename  # @UnresolvedImport
    rel = resource_filename("bvapps", "configs")
    dirname = os.path.join(rel, '..', '..', '..', 'bdse1')
    dirname2 = os.path.join(rel, '..', '..', '..', 'bo_app1') # e.g. r_rf_A
    dirs = [
        "bootstrapping_olympics.configs", 
        "vehicles.configs",
        dirname, 
        dirname2,
    ]
    
    from conf_tools import GlobalConfig
    GlobalConfig.global_load_dirs(dirs)
    
    # Our tests are its tests with our configuration
    import bootstrapping_olympics.unittests
    import vehicles.unittests  
    import boot_manager.unittests 

    # Set up tests
    from boot_manager import get_bootbatch_config
    from bootstrapping_olympics import get_boot_config
    from vehicles import get_vehicles_config
    
    from comptests import jobs_registrar
    jobs_registrar(context, get_boot_config())
    jobs_registrar(context, get_vehicles_config())
    jobs_registrar(context, get_bootbatch_config())
