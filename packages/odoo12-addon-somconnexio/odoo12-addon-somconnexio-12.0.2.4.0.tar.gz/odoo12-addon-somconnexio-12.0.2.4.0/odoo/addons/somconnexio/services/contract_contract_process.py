from .contract_process import (
    ADSLContractProcess,
    FiberContractProcess,
    MobileContractProcess,
    Router4GContractProcess,
)


class ErrorUnsuportedTechnology(Exception):
    pass


class ContractContractProcess:
    """
      ContractContractProcess --> ContractProcessFactory

      Refactor to separate the methods of contracts in classes with type as scope.
      We create the ADSLContractProcess, FiberContractProcess,
      MobileContractProcess and Router4GContractProcess classes.

        BaseContractProcess
               |
               |
        ---------------------------
        |                         |
    MobileContractProcess         |
                          BAContractProcess
                                  |
                -------------------------------------
                |                 |                 |
        ADSLContractProcess       |     Router4GContractProcess
                                  |
                           FiberContractProcess
    """

    def __init__(self, env=False):
        self.env = env

    def create(self, **params):
        Contract = None
        service_technology = params["service_technology"]
        if service_technology == "Mobile":
            Contract = MobileContractProcess
        elif service_technology == "ADSL":
            Contract = ADSLContractProcess
        elif service_technology == "Fiber":
            Contract = FiberContractProcess
        elif service_technology == "4G":
            Contract = Router4GContractProcess
        else:
            raise ErrorUnsuportedTechnology()

        return Contract(self.env).create(**params)
