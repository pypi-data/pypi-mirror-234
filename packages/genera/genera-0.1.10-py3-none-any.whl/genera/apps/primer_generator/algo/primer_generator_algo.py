import genera
import primer3
import pandas as pd


class PrimerGeneratorAlgo(genera.classes.Algo):
    def __init__(self, settings={}):
        super().__init__()
        self.settings = genera.utils.settings.merge(
            [genera.utils.settings.load(__file__,"algo.json"), settings]
        )

    def generate_primers(self, template, parameters):
        global_config = {
            **{value: parameters[key] for key, value in self.settings["parameter_inputs"].items()},
            **self.settings["additional_defaults"],
        }
        seq_config = {
            "SEQUENCE_ID": "example",
            "SEQUENCE_TEMPLATE": template,
            "SEQUENCE_INCLUDED_REGION": (0, len(template)),
            "PRIMER_PRODUCT_SIZE_RANGE": (len(template), len(template)),
        }
        results = primer3.bindings.design_primers(global_config, seq_config)

        df = pd.DataFrame(columns=self.settings["output_labels"].values())

        for key in self.settings["output_labels"]:
            if key == "PRIMER_LEFT_{}" or key == "PRIMER_RIGHT_{}":
                df[self.settings["output_labels"][key]] = [results[key.format(i)][1] for i in range(results["PRIMER_PAIR_NUM_RETURNED"])]
            elif key == "PRIMER_LEFT_{}_TM" or key == "PRIMER_RIGHT_{}_TM":
                df[self.settings["output_labels"][key]] = [results[key.format(i)]+self.settings["Tm_offset"] for i in range(results["PRIMER_PAIR_NUM_RETURNED"])]
            else:
                df[self.settings["output_labels"][key]] = [results[key.format(i)] for i in range(results["PRIMER_PAIR_NUM_RETURNED"])]

        return df
