import logging
from argparse import ArgumentParser

import mne

from moabb.benchmark import benchmark
from moabb.utils import set_download_dir


log = logging.getLogger(__name__)


def parser_init():
    parser = ArgumentParser(description="Main run script for MOABB")

    parser.add_argument(
        "-mne_p",
        "--mne_data",
        dest="mne_data",
        type=str,
        default=None,
        help="Folder where to save and load the datasets with mne structure.",
    )

    parser.add_argument(
        "-p",
        "--pipelines",
        dest="pipelines",
        type=str,
        default="./pipelines/",
        help="Folder containing the pipelines to evaluates.",
    )
    parser.add_argument(
        "-e",
        "--evaluations",
        dest="evaluations",
        type=list,
        default=None,
        help="Evaluation types to be run. Must be given as a list. "
        'Options - ["WithinSession","CrossSession","CrossSubject"]'
        "By default, all 3 types of evaluations will be done",
    )
    parser.add_argument(
        "-r",
        "--results",
        dest="results",
        type=str,
        default="./results/",
        help="Folder to store the results.",
    )
    parser.add_argument(
        "-f",
        "--force-update",
        dest="force",
        action="store_true",
        default=False,
        help="Force evaluation of cached pipelines.",
    )

    parser.add_argument(
        "-v", "--verbose", dest="verbose", action="store_true", default=False
    )
    parser.add_argument(
        "-d",
        "--debug",
        dest="debug",
        action="store_true",
        default=False,
        help="Print debug level parse statements. Overrides verbose",
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="output",
        type=str,
        default="./",
        help="Folder to put analysis results",
    )
    parser.add_argument(
        "--threads", dest="threads", type=int, default=1, help="Number of threads to run"
    )
    parser.add_argument(
        "--plot",
        dest="plot",
        action="store_true",
        default=False,
        help="Plot results after computing. Defaults false",
    )
    parser.add_argument(
        "-c",
        "--contexts",
        dest="context",
        type=str,
        default=None,
        help="File path to context.yml file that describes context parameters."
        "If none, assumes all defaults. Must contain an entry for all "
        "paradigms described in the pipelines",
    )

    parser.add_argument(
        "-i",
        "--include_datasets",
        dest="include_datasets",
        nargs="*",
        type=str,
        default=None,
        help="List of dataset to be included",
    )

    parser.add_argument(
        "-par",
        "--paradigms",
        dest="paradigms",
        type=list,
        default=None,
        help="List of paradigm to be included",
    )

    return parser


if __name__ == "__main__":
    # FIXME: The verbose and debug params are useless currently
    # set logs
    mne.set_log_level(False)
    # logging.basicConfig(level=logging.WARNING)

    parser = parser_init()
    options = parser.parse_args()

    if options.mne_data is not None:
        set_download_dir(options.mne_data)

    print(options.include_datasets)

    if len(options.include_datasets) > 1:
        list_ = options.include_datasets
        options.include_datasets = []
        options.include_datasets = [list_[0] + " " + list_[1]]
        print(options.include_datasets)

    # call within session benchmark
    df_eval = benchmark(
        pipelines=options.pipelines,
        evaluations=["WithinSession"],
        results=options.results,
        overwrite=options.force,
        output=options.output,
        n_jobs=options.threads,
        plot=options.plot,
        include_datasets=options.include_datasets,
        paradigms=["SSVEP", "FilterBankSSVEP"],
    )

    df_eval.to_csv(f"{options.output}/results.csv")
