
from ciocore.validator import Validator

#TODO: Implement validators here


####################################

# Implement more validators here
####################################


def run(**kwargs):
    errors, warnings, notices = [], [], []

    er, wn, nt = _run_validators(**kwargs)

    errors.extend(er)
    warnings.extend(wn)
    notices.extend(nt)

    return errors, warnings, notices

def _run_validators(**kwargs):

    # takename =  node.name()
    validators = [plugin(**kwargs) for plugin in Validator.plugins()]
    for validator in validators:
        # validator.run(takename)
        pass

    errors = list(set.union(*[validator.errors for validator in validators]))
    warnings = list(set.union(*[validator.warnings for validator in validators]))
    notices = list(set.union(*[validator.notices for validator in validators]))
    return errors, warnings, notices


