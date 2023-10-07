import sys

from celerabitpipelineintegration.int_main_module import ModuleMain

def run():
    module_main:ModuleMain = ModuleMain()
    module_main.run(sys.argv[1:len(sys.argv)])

run()