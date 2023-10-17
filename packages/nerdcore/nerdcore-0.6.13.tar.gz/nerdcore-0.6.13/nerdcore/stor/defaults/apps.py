from nerdcore.defs import import_env_class

ENV = import_env_class()
env = ENV.get()

apps_config = {

    # Barnacle
    'barnacle': {
        'servers': ['barnacle-2a', 'barnacle-2b', 'barnacle-job'],
        'elb': env.BARNACLE_ELB_ARN,
        'dirs': ['barnacle'],
    },

    # LEAD LMS
    'lead': {
        'servers': ['lms-a', 'lms-b'],
        'elb': env.LEAD_ELB_ARN,
        'dirs': [
            "eq", "bpt_staging", "dlu", "fivable", "lms", "nfcym", "universal_rights", "statesville",
            "no_stackable_staging", "lms_demo", "gci", "c3", "c3_sandbox", "ep", "gsa_demo", "lms_staging",
            "statesville-copy", "streetsmart", "schoolofmary", "lead_global"
        ]
    },

    # Stackable
    'stackable': {
        'servers': ['stackable', 'stackable-b'],
        'elb': env.STACKABLE_ELB_ARN,
        'dirs': ['bpt_staging', 'bridgeport.stackable', 'c3_sandbox.stackable', 'c3.stackable', 'dlu',
                 'fivable.stackable', 'fwsb.stackable', 'gsa.stackable', 'lms_staging', 'nfcym.stackable',
                 'omaha.stackable', 'rcan.stackable', 'schoolofmary.stackable', 'sf.stackable', 'stackable_global',
                 'statesville', 'streetsmart.stackable', 'wichita.stackable']
    }
}
