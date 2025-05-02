from typing import Any

class ServiceBase:
    def validate_request(self, request: Any) -> None:
        try:
            myreq = self.Request()
        except AttributeError:
            raise TypeError(f"{self.__class__.__qualname__} does not have a corresponding Request class.")

        if not isinstance(myreq, request):
            raise TypeError(f"Expected {myreq.__qualname__}, got {type(request).__qualname__} instead.")
            
    