#
#  This file is part of Sequana software
#
#  Copyright (c) 2016-2021 - Sequana Development Team
#
#  Distributed under the terms of the 3-clause BSD license.
#  The full license is in the LICENSE file, distributed with this software.
#
#  website: https://github.com/sequana/sequana
#  documentation: http://sequana.readthedocs.io
#
##############################################################################
import sys
import os
import argparse
import subprocess

from sequana_pipetools.options import *
from sequana_pipetools.options import before_pipeline
from sequana_pipetools.misc import Colors
from sequana_pipetools.info import sequana_epilog, sequana_prolog
from sequana_pipetools import SequanaManager

col = Colors()

NAME = "variant_calling"


class Options(argparse.ArgumentParser):
    def __init__(self, prog=NAME, epilog=None):
        usage = col.purple(sequana_prolog.format(**{"name": NAME}))
        super(Options, self).__init__(usage=usage, prog=prog, description="",
            epilog=epilog,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )

        # add a new group of options to the parser
        so = SlurmOptions()
        so.add_options(self)

        # add a snakemake group of options to the parser
        so = SnakemakeOptions(working_directory=NAME)
        so.add_options(self)

        # add a data group of options to the parser
        so = InputOptions()
        so.add_options(self)

        so = GeneralOptions()
        so.add_options(self)

        pipeline_group = self.add_argument_group("pipeline")
        pipeline_group.add_argument(
            "--reference-file",
            dest="reference",
            required=True,
            help="The input reference to mapped reads onto"
        )
        pipeline_group.add_argument(
            "--annotation-file",
            dest="annotation",
            default=None,
            help="The annotation for snpeff"
        )
        pipeline_group.add_argument("--threads", dest="threads", default=4, type=int)
        pipeline_group.add_argument("--do-coverage", dest="do_coverage",
            action="store_true",
            help="perform the coverage analysis using sequana_coverage")
        pipeline_group.add_argument("--do-joint-calling", dest="do_joint_calling",
            action="store_true",
            help="do the joint calling analysise")

        pipeline_group.add_argument("-o", "--circular", action="store_true")
        pipeline_group.add_argument("--freebayes-ploidy", type=int, default=1)

        pipeline_group.add_argument("--create-bigwig", action="store_true",
            help="create the bigwig files from the BAM files" )

        self.add_argument("--run", default=False, action="store_true",
            help="execute the pipeline directly")

    def parse_args(self, *args):
        args_list = list(*args)
        if "--from-project" in args_list:
            if len(args_list)>2:
                msg = "WARNING [sequana]: With --from-project option, " + \
                        "pipeline and data-related options will be ignored."
                print(col.error(msg))
            for action in self._actions:
                if action.required is True:
                    action.required = False
        options = super(Options, self).parse_args(*args)
        return options


def main(args=None):

    if args is None:
        args = sys.argv

    # whatever needs to be called by all pipeline before the options parsing
    before_pipeline(NAME)

    # option parsing including common epilog
    options = Options(NAME, epilog=sequana_epilog).parse_args(args[1:])

    # the real stuff is here
    manager = SequanaManager(options, NAME)

    # create the beginning of the command and the working directory
    manager.setup()

    # fill the config file with input parameters
    if options.from_project is None:
        cfg = manager.config.config
        cfg.input_directory = os.path.abspath(options.input_directory)
        cfg.input_pattern = options.input_pattern
        cfg.input_readtag = options.input_readtag

        if options.annotation:
            cfg.snpeff.do = True
            cfg.annotation_file = os.path.abspath(options.annotation)
            manager.exists(cfg.annotation_file)
            #print("." in cfg.annotation_file,  cfg.annotation_file.split(".")[-1])
            if "." not in cfg.annotation_file or \
                cfg.annotation_file.split(".")[-1] not in ['gbk', 'gff', 'gff3']:
    
                logger.error("The annotation file must end with .gbk or .gff or .gff3. You provided {}".format(cfg.annotation_file))
                sys.exit(1)
            cfg['sequana_coverage']['genbank_file'] = cfg.annotation_file
        else:
            cfg.snpeff.do = False
            cfg['sequana_coverage']['genbank_file'] = ""

        cfg['sequana_coverage']['do'] = options.do_coverage
        cfg['sequana_coverage']["circular"] = options.circular
        cfg['joint_freebayes']['do'] = options.do_joint_calling
        cfg['bwa_mem']['threads'] = options.threads


        cfg['freebayes']['ploidy'] = options.freebayes_ploidy

        cfg.reference_file = os.path.abspath(options.reference)
        manager.exists(cfg.reference_file)

        # Given the reference, let us compute its length and st the index algorithm
        from sequana import FastA
        f = FastA(options.reference)
        N = f.get_stats()['total_length']

        # seems to be a hardcoded values in bwa according to the documentation
        if N >= 2000000000:
            cfg['bwa_mem']['index_algorithm'] = "bwtsw"
        else:
            cfg['bwa_mem']['index_algorithm'] = "is"



    # finalise the command and save it; copy the snakemake. update the config
    # file and save it.
    manager.teardown()

    if options.run:
        subprocess.Popen(["sh", '{}.sh'.format(NAME)], cwd=options.workdir)

if __name__ == "__main__":
    main()
