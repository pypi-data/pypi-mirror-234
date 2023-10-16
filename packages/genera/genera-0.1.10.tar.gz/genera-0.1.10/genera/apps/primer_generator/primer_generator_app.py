import genera
from .ui import PrimerGeneratorUI
from .algo import PrimerGeneratorAlgo
from .data import PrimerGeneratorData
from typing import List
from pandas import DataFrame


class PrimerGeneratorApp(genera.classes.App):
    def __init__(self, settings={}, options={}):
        super().__init__()
        self.settings = genera.utils.settings.merge(
            [genera.utils.settings.load(__file__,"app.json"), settings]
        )
        self.options = genera.utils.options.merge([{"UI": "full"}, options])
        self.ui = PrimerGeneratorUI(self.settings)
        self.algo = PrimerGeneratorAlgo(self.settings)
        self.data = PrimerGeneratorData(self.settings)
        self.init_app()

    def primer_generator(
        self,
        fragments: List[str] = None,
        load_file_path: str = None,
        save_file_path: str = None,
    ) -> List[DataFrame]:
        
        # 1. Read fragments from file
        if fragments is None:
            if load_file_path is not None:
                self.data.fragments_file_path = load_file_path
            if self.data.fragments_file_path is not None:
                self.data.load_fragments()
        else:
            self.data.list_to_seq(fragments)
        self.data.reset_primers()

        # 2. Fetch primer parameters from UI or class settings input.
        primer_parameters = self.gather_primer_parameters()

        # 3. Use Primer3 to design primers for each fragment
        for fragment in self.data.fragments:
            primers = self.algo.generate_primers(
                fragment, primer_parameters
            )
            self.data.add_primers(primers)

        # 4. write primers to an XLSX file
        if save_file_path is not None:
            self.data.primers_file_path = save_file_path
        if self.data.primers_file_path is not None:
            self.data.write_primer_xlsx()

        return self.data.primers
    
    def init_app(self):
        if self.options["UI"] == "full":
            self.ui.init_ui()
            self.ui.load_file_path.trace_add("write", self.activate_save_primers)
            self.ui.save_file_path.trace_add("write", self.run_primer_generator)
            self.ui.root.mainloop()

    def activate_save_primers(self, *args):
        file_path = self.ui.load_file_path.get()
        if file_path:
            self.data.fragments_file_path = file_path
            self.ui.elements["save_file_button"].config(state="normal")

    def run_primer_generator(self, *args):
        file_path = self.ui.save_file_path.get()
        if file_path:
            self.data.primers_file_path = file_path
            self.primer_generator()

    def gather_primer_parameters(self):
        primer_parameters = {}
        if self.options["UI"] == "hide":
            for input_tag in self.ui.settings["T_inputs"]:
                primer_parameters[input_tag] = float(self.settings[input_tag])
            for input_tag in self.ui.settings["length_inputs"]:
                primer_parameters[input_tag] = int(self.settings[input_tag])
            primer_parameters["force_GC_end"] = int(self.settings["force_GC_end"])

        elif self.options["UI"] == "full":
            for input_tag in self.ui.settings["T_inputs"]:
                primer_parameters[input_tag] = float(self.ui.elements[f"{input_tag}_input"].get())
            for input_tag in self.ui.settings["length_inputs"]:
                primer_parameters[input_tag] = int(self.ui.elements[f"{input_tag}_input"].get())
            primer_parameters["force_GC_end"] = int(self.ui.force_GC_state.get())
        return primer_parameters


if __name__ == "__main__":
    app = PrimerGeneratorApp()
