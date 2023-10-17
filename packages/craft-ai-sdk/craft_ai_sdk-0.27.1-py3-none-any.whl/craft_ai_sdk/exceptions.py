class SdkException(Exception):
    """General exception while using this package"""

    def __init__(
        self,
        message,
        status_code=None,
        name=None,
        stack_message=None,
        request_id=None,
        additional_data=None,
    ):
        self.message = message
        self.name = name
        self.request_id = request_id
        self.additional_data = additional_data
        self.status_code = status_code

        super().__init__(self.message)

    def __str__(self):
        msg = ""
        if self.name is not None:
            msg += f"[{self.name}] "
        elif self.status_code is not None:
            msg += f"[{self.status_code}] "

        msg += self.message
        if self.additional_data:
            msg += f"\nAdditional data: {self.additional_data}"
        if self.request_id and self.request_id != "NO_REQUEST_ID":
            msg += f"\nRequest id: {self.request_id}"
        return msg
