from ewokscore.task import Task as EwoksTask


class _TomoobjseriePlaceHolder(
    EwoksTask, input_names=["serie"], output_names=["serie"]
):
    """
    task to define a tomography 'serie'
    """

    def run(self):
        self.outputs.serie = self.inputs.serie
