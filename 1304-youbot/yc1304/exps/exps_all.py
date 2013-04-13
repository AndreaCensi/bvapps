from .import CampaignCmd, campaign_sub, QuickApp
from . import Exp01


@campaign_sub
class AllCampaigns(CampaignCmd, QuickApp):
    cmd = 'all-campaigns'
    
    def define_options(self, params):
        pass
    
    def define_jobs_context(self, context):    
        self.call_recursive(context, 'exp01', Exp01, [])
