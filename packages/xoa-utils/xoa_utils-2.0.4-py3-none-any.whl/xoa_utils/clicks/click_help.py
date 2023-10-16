HELP_CONNECT_PORT_LIST = "Specifies the ports on the specified device host, \
default to null. Specify a port using the format slot/port, no spaces between. \
e.g. --port_list 0/0,0/1,0/2,0/3. If used,the context will switch to the first \
port in the list after the connection is established.\n"

HELP_CONNECT_RESET = "Removes all port configurations of the ports in --ports after \
reservation, default to --no-reset."

HELP_CONNECT_FORCE = "Breaks port locks established by another user, aka. \
force reservation, default to --force."


HELP_CONNECT_PWD = "The login password of the tester, default to xena. \
e.g. --password xena"


HELP_CONNECT_TCP_PORT = "The TCP port number on the chassis for the client to \
establish a session, default to 22606."

HELP_CONNECT = """
    Connect to a tester for the current session.

        DEVICE TEXT: Specifies the chassis address for connection. You can specify the IP addresses in IPv4 format, or a host name. e.g. 10.10.10.10, demo.xenanetworks.com\n
        USERNAME TEXT: Specifies the name of the user, e.g. xoa or automation

    """

HELP_PORT_RESET = "Removes all port configurations in --port_list after \
reservation, default to --reset"

HELP_PORT_FORCE = "Breaks port locks established by another user, aka. force \
reservation, default to --force"

HELP_EXIT_RELEASE = "Determines whether the ports should be released before exiting, default to --release"

HELP_PORTS_ALL = "Show all ports of the tester, default to --no-all"

HELP_RECOVERY_ON = "Should xenaserver automatically do link recovery when detecting down signal, default to --on."

HELP_AN_CONFIG_ON = "Enable or disable auto-negotiation on the working port, \
default to --on."

HELP_AN_CONFIG_LOOPBACK = "Should loopback be allowed in auto-negotiation, \
default to --no-loopback."

HELP_LT_CONFIG_MODE = "The mode for link training on the working port, default to --mode auto."

HELP_LT_CONFIG_ON = "Enable or disable link training on the working port, default to --on."

HELP_LT_CONFIG_PRESET0 = "Should the Out-of-Sync use standard values (--preset0 standard) or existing tap values (--preset0 existing), default to --preset0 standard."

HELP_ANLT_LOG_FILENAME = "Filename of the log."

HELP_ANLT_LOG_KEEP = "Specifies what types of log entries to keep, default to keep all.\
Allow values: all | an | lt \
all: keep both AN and LT\
an:  keep AN only\
lt:  keep lt only"

HELP_ANLT_LOG_SERDES = "Specifies which serdes of LT logs to keep. If you don't know how many\
serdes the port has, use 'anlt log', default to all serdes."

HELP_STRICT_ON = "Should enable ANLT strict mode, default to --on."

HELP_LOG_CONTROL_DEBUG_ON = "Debug log out, default to --debug, -D"

HELP_LOG_CONTROL_AN_TRACE_ON = "Auto-negotiation trace output, default to --an-trace, -A"

HELP_LOG_CONTROL_LT_TRACE_ON = "Link training algorithm trace, default to --lt-trace, -L"

HELP_LOG_CONTROL_ALG_TRACE_ON = "Link training algorithm trace output, default to --alg-trace, -G"

HELP_LOG_CONTROL_FSM_PORT_ON = "Port state machine transitions output, default to --no-fsm-port, -p"

HELP_LOG_CONTROL_FSM_AN_ON = "Auto-negotiation state machine transitions, default to --fsm-an, -N"

HELP_LOG_CONTROL_FSM_AN_STIMULI_ON = "Auto-negotiation stimuli state machine transitions, default to --no-fsm-an-stimuli, -m"

HELP_LOG_CONTROL_FSM_LT_ON = "Link training state machine transitions, default to --fsm-lt, -T"

HELP_LOG_CONTROL_FSM_LT_COEFF_ON = "Link training coefficient state machine transitions, default to --no-fsm-lt-coeff, -c"

HELP_LOG_CONTROL_FSM_LT_STIMULI_ON = "Link training stimuli state machine transitions, default to --no-fsm-lt-stimuli, -s"

HELP_LOG_CONTROL_FSM_LT_ALG0_ON = "Link training algorithm 0 state machine transitions, default to --fsm-lt-alg0, -Z"

HELP_LOG_CONTROL_FSM_LT_ALGN1_ON = "Link training algorithm -1 state machine transitions, default to --fsm-lt-algn1, -O"