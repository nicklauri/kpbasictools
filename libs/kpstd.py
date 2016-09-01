#!/usr/bin/python2

import os, sys

if os.name == 'posix':
    try:
        import colorama
    except ImportError as e:
        print('[-] kpstd: can not import colorama library.')
        print('[-] Exception info: ' + str(e))
        import_failed = True
        class colorama:
            class Style:    
                BRIGHT = RESET_ALL = ''
            class Fore:
                BLUE = GREEN = YELLOW = RED = ''
    else:
        colorama.init()
        import_failed = False

    progname = os.path.split(sys.argv[0])[1]

    def kpout(msg, str_col):
        if not import_failed:
            sys.stdout.write(''.join([str_col, colorama.Style.RESET_ALL, msg]))
            sys.stdout.flush()
        else:
            sys.stdout.write(''.join([str_col, msg]))
            sys.stdout.flush()

    def norm(msg):
        kpout(msg, ''.join([colorama.Style.BRIGHT, colorama.Fore.BLUE, '[*] ']))

    def info(msg):
        kpout(msg, ''.join([colorama.Style.BRIGHT, colorama.Fore.GREEN, '[*] ']))

    def warn(msg):
        kpout(msg, ''.join([colorama.Style.BRIGHT, colorama.Fore.YELLOW, '[-] ']))

    def error(msg):
        kpout(msg, ''.join([colorama.Style.BRIGHT, colorama.Fore.RED, '[-] ']))

################################################################################
elif os.name == 'nt':
    from ctypes import windll

    class color:
	    black	= 0
	    blue	= 1
	    green	= 2
	    cyan	= 3
	    red		= 4
	    pink	= 5
	    yellow	= 6
	    white	= 7
	    gray	= 8
	    class light:    # ~ bright :))
		    blue	= 9
		    green	= 0xA
		    cyan	= 0xB
		    red		= 0xC
		    pink	= 0xD
		    yellow	= 0xE
		    white	= 0xF

    def set_color(color):
	    if type(color) != int:
		    return False;
	    STD_OUTPUT_HANDLE = -11;
	    stdout_handle = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE);
	    windll.kernel32.SetConsoleTextAttribute(stdout_handle, color);
	    return True;

    default_color = color.white;
    def reset_color():
        return set_color(default_color);

    out = lambda msg: sys.stdout.write(msg);
    mod_name = "";
    mod_name_color = color.light.cyan;

    def norm(msg):
        set_color(color.light.cyan);
        out('[*]');
        reset_color();
        if mod_name:
            set_color(mod_name_color);
            out(mod_name); reset_color();
        out(msg);
        return "";

    def info(msg):
        set_color(color.light.green);
        out('[*]');
        reset_color();
        if mod_name:
            set_color(mod_name_color);
            out(mod_name); reset_color();
        out(msg);
        return "";

    def warn(msg):
        set_color(color.light.yellow);
        out('[!]');
        reset_color();
        if mod_name:
            set_color(mod_name_color);
            out(mod_name); reset_color();
        out(msg);
        return "";

    def error(msg):
        set_color(color.light.red);
        out('[-]');
        reset_color();
        if mod_name:
            set_color(mod_name_color);
            out(mod_name); reset_color();
        out(msg);
        return "";

    def exception(msg):
        if True:
            raise Exception(msg);

    def red(msg):
        set_color(color.light.red);
        out(msg);
        reset_color();
        return "";

    def cyan(msg):
        set_color(color.light.cyan);
        out(msg);
        reset_color();
        return " ";

    def yellow(msg):
        set_color(color.light.yellow);
        out(msg);
        reset_color();
        return " ";

    def green(msg):
        set_color(color.light.green);
        out(msg);
        reset_color();
        return " ";

    def white(msg):
        set_color(color.light.white);
        out(msg);
        reset_color();
        return " ";

