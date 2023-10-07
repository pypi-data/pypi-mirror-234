class RootProcessCmd:
    def __init__(
        self,
        cmd_data: dict,
        cmd_metadata: dict,
    ):
        self.cmd_data = cmd_data
        self.cmd_metadata = cmd_metadata

    def __cmd_post_op__(self) -> dict:
        return self.cmd_metadata["cmd_post_op"]

    def __cmd_pre_op__(self) -> dict:
        return self.cmd_metadata.get("cmd_pre_op", {})

    def __cmd_post_op_enrichment__(self) -> dict:
        return self.__cmd_post_op__().get("enrichment", {})

    def _idempotency_id_(self) -> str:
        return self.cmd_metadata["idempotency_id"]

    def _cmd_post_op_enrichement_map_(self) -> list:
        return self.__cmd_post_op_enrichment__().get("add_property_map", [])

    def _cmd_post_op_store_(self):
        return self.__cmd_post_op__().get("store", {})
