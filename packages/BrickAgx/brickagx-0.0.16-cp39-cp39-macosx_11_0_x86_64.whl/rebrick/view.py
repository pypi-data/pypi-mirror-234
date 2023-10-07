#!/usr/bin/env python3
import agxOSG
import agxSDK
import os
import sys
import signal
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, Action, SUPPRESS
from brickbundles import bundle_path

# Import useful utilities to access the current simulation, graphics root and application
from agxPythonModules.utils.environment import init_app, simulation, application, root

from rebrick import InputSignalListener, OutputSignalListener, load_brickfile, ClickAdapter, __version__, FileChangedListener

class AgxHelpAction(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        start_agx()
        exit(0)

class VersionAction(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        print(__version__)
        exit(0)


def parse_args():
    parser = ArgumentParser(description="View brick models", formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("brickfile", help="the .brick file to load")
    parser.add_argument("[AGX flags ...]", help="any additional AGX flags", default="", nargs="?")
    parser.add_argument("--bundle-path", help="list of path to bundle dependencies if any. Overrides environment variable BRICK_BUNDLE_PATH.", 
                        metavar="<bundle_path>", default=bundle_path())
    parser.add_argument("--click-addr", type=str, help="Address for Click to listen on, e.g. ipc:///tmp/click.ipc", default="tcp://*:5555")
    parser.add_argument("--debug-render-tnc", help="Path to .obj file to use to debug render mate connector frames (tangent, normal, cross)",
                        metavar="<objpath>", default="")
    parser.add_argument("--enable-click", help="Enable sending and receiving signals as Click Messages", action="store_true", default=SUPPRESS)
    parser.add_argument("--loglevel", choices=["trace", "debug", "info", "warn", "error", "critical", "off"], help="Set log level", default="off")
    parser.add_argument("--modelname", help="The model to load (defaults to last model in file)", metavar="<name>", default="")
    parser.add_argument("--reload-on-update", help = "Reload scene automatically when brickfile is updated", action="store_true", default=SUPPRESS)
    parser.add_argument("--usage", help="Show AGX specific help", action=AgxHelpAction, nargs=0, default=SUPPRESS)
    parser.add_argument("--version", help="Show version", action=VersionAction, nargs=0, default=SUPPRESS)
    return parser.parse_known_args()

class AllowCtrlBreakListener(agxOSG.ExampleApplicationListener):
    pass

def buildScene():

    args, extra_args = parse_args()
    ClickAdapter.set_log_level(args.loglevel)
    if extra_args:
        print(f"Passing these args to AGX: {(' ').join(extra_args)}")

    brick_scene, assembly = load_brickfile(simulation(), args.brickfile, args.bundle_path, args.modelname, args.debug_render_tnc)
    simulation().add(assembly.get())
    application().addListener(AllowCtrlBreakListener())


    # Add click listeners unless this is scene-reload, in that case we want to keep our listeners
    # Note that we use globals() since this whole file is reloaded on scene-reload by AGX, so no local globals are kept
    if 'click_listeners_created' not in globals():

        # Add a signal listener so that signals are picked up from inputs
        input_signal_listener = InputSignalListener(assembly)
        output_signal_listener = OutputSignalListener(assembly, brick_scene)

        simulation().add(input_signal_listener, InputSignalListener.RECOMMENDED_PRIO)
        simulation().add(output_signal_listener, OutputSignalListener.RECOMMENDED_PRIO)

        if 'reload_on_update' in args:
            print(f"Will reload scene when {args.brickfile} is updated")
            ClickAdapter.add_file_changed_listener(application(), args.brickfile)

        if 'enable_click' in args:
            ClickAdapter.add_listeners(application(), simulation(), args.click_addr, brick_scene)
            args.enable_click = False
        globals()["click_listeners_created"] = True

    agxOSG.createVisual(assembly.get(), root())

def handler(signum, frame):
    os._exit(0)

def start_agx():
    # Tell AGX to run this file, even if run was called from another file
    sys.argv[0] = __file__
    # Use __main__ otherwise AGX will just skip the init 
    init = init_app(name='__main__',
                    scenes=[(buildScene, '1')],
                    autoStepping=True,  # Default: False
    )


def run():
    signal.signal(signal.SIGINT, handler)
    parse_args()
    start_agx()

if __name__ == '__main__':
    run()
