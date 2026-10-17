from src.balance.manage import BalanceServer, Replicator, Replicators

class WatchBalance(BalanceServer):
    def __init__(self, replicas:Replicators|list[Replicator], timeout:int = 60)-> None:
        super().__init__(replicas, timeout)
