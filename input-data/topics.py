# Do we need these error regexps?
errorRegexps = [
    {'properties' : ['description'],
     'eventtype' : 'Error',
     'regexp' : r"(\(Service Check Timed Out\))"
    },
    {'properties' : ['description'],
     'eventtype' : 'Error',
     'regexp' : r"(CHECK_NRPE: Error - Could not complete SSL handshake)."
    },
    {'properties' : ['description'],
     'eventtype' : 'Error',
     'regexp' : r"(Connection refused by host)"
    },
    {'properties' : ['description'],
     'eventtype' : 'Error',
     'regexp' : r'(<A HREF="https://hpgloja.ig.com.br:443/" target="_blank">CRITICAL - Socket timeout after 10 seconds)'
    },
]

expressions = {
    'check_tcp': [
        {'labelFilter': 'TCP',
         'eventtype': 'TCP',
         'regexps': [
            {'properties': ['state', 'response_time', 'port'],
             'regexp': r"TCP (OK|WARNING|CRITICAL) - (\d+.\d+) second response time on port (\d+)"
            },
            {'properties': ['state'],
             'regexp': r"TCP (OK|WARNING|CRITICAL) - Invalid"
            }
         ]
        },
        {'labelFilter': None,
         'eventtype': 'TCP',
         'regexps': [
            {'properties': ['state'],
             'regexp': r"(WARNING|CRITICAL) - Socket timeout"
            }
         ]
        }
    ],

    'check_load': [
        {'labelFilter': None,
         'eventtype': 'Load',
         'regexps': [
            {'properties': ['state', 'min1', 'min5', 'min15'],
             'regexp': r"(OK|WARNING|CRITICAL) - load average: ([0-9.]+), ([0-9.]+), ([0-9.]+)"
            }
         ]
        }
    ],

    'check_cpu': [
        {'labelFilter': None,
         'eventtype': 'CPU',
         'regexps': [
            {'properties': ['state', 'min1', 'min5', 'min15'],
             'regexp': r"(OK|WARNING|CRITICAL) - load average: ([0-9.]+), ([0-9.]+), ([0-9.]+)"
            },
            {'properties': ['state', 'percentual', 'type'],
             'regexp': r"(OK|WARNING|CRITICAL) - CPU em (\d+)%, tipo: (.+)"
            },
         ]
        }
    ],

    'check_cpu_snmp': [
        {'labelFilter': None,
         'eventtype': 'CPU',
         'regexps': [
            {'properties': ['state', 'percentual', 'type'],
             'regexp': r"(OK|WARNING|CRITICAL) - CPU em (\d+)%, tipo: (.+)"
            },
         ]
        }
    ],


    'conn': [ #conn = check_fping
        {'labelFilter': 'FPING',
         'eventtype': 'PING',
         'regexps': [
            {'properties': ['state', 'ip', 'loss', 'rta'],
             'regexp': r"FPING (OK|WARNING|CRITICAL) - ([0-9.]+) \(loss=(\d+)%(?:(?:, rta=(\d+\.\d*) ms\)))"
            },
            {'properties': ['state', 'ip', 'loss'],
             'regexp': r"FPING (OK|WARNING|CRITICAL) - ([0-9.]+) \(loss=(\d+)%)"
            }
         ]
        }
    ],

    'check_ping': [
        {'labelFilter': 'PING',
         'eventtype': 'PING',
         'regexps': [
            {'properties': ['state', 'loss', 'rta'],
             'regexp': r"PING (OK|WARNING|CRITICAL) - Packet loss = ([0-9.]+)%, RTA = ([0-9.]+) ms"
            },
            {'properties': ['state', 'loss'],
             'regexp': r"PING (OK|WARNING|CRITICAL) - Packet loss = ([0-9.]+)%"
            }
         ]
        }
    ],

    'dns': [
        {'labelFilter': 'DNS',
         'eventtype': 'DNS',
         'regexps': [
            {'properties': ['state', 'response_time', 'dns_record', 'ip'],
             'regexp': r'DNS (OK|WARNING|CRITICAL): ([0-9.]+) seconds? response time. ([^ ]+) returns ([0-9.]+)'
            }
         ]
        }
    ],

    'ftp': [
        {'labelFilter': 'FTP',
         'eventtype': 'FTP',
         'regexps': [
            {'properties': ['state', 'response_time', 'port'],
             'regexp': r'FTP (OK|WARNING|CRITICAL) - ([0-9.]+) seconds? response time on port ([0-9]+)'
            },
         ]

        }
    ],

    'check_procs': [
        {'labelFilter': None,
         'eventtype': 'Procs',
         'regexps': [
            {'properties': ['state', 'number_of_processes', 'args'],
             'regexp': r'(OK|WARNING|CRITICAL) - ([0-9]+) processes running with args (.+)'
            }
         ]

        }
    ],

    'check_local_procs': [
        {'labelFilter': None,
         'eventtype': 'Procs',
         'regexps': [
            {'properties': ['state', 'number_of_processes', 'state_of_process'],
             'regexp': r'PROCS (OK|WARNING|CRITICAL): ([0-9]+) processes with STATE = (.+)'
            }
         ]
        }
    ],

    'check_many_procs': [
        {'labelFilter': None,
         'eventtype': 'ProcsNotRunning',
         'regexps': [
            {'properties': ['process_not_running'],
             'regexp': r'([^\(]+)'
            }
         ]
        }
    ],
    
    'http_args_follow': [
        {'labelFilter': None,
         'eventtype': 'HTTP',
         'regexps': [
            {'properties': ['url', 'state', 'http_version', 'status_code', 'status_description', 'bytes', 'response_time'],
             'regexp': r'<A HREF="([^"]+)" target="_blank">HTTP (.+): HTTP/([0-9.]+) ([0-9]+) (.+) - ([0-9]+) bytes in ([0-9.]+) second response time </A>'
            }
         ]
        },
        {'labelFilter': None,
         'eventtype': 'HTTP',
         'regexps': [
            {'properties': ['url', 'state', 'status_description'],
             'regexp': r'<A HREF="([^"]+)" target="_blank">HTTP (.+) - (.+)'
            }
         ]
        },
        {'labelFilter': None,
         'eventtype': 'HTTP',
         'regexps': [
            {'properties': ['url', 'status_description'],
             'regexp': r'<A HREF="([^"]+)" target="_blank">(Connection refused)'
            }
         ]
        },
    ],

    'check_disk': [
        {'labelFilter': None,
         'eventtype': 'Disk',
         'regexps': [
            {'properties': ['state', 'free_space', 'usage'],
             'regexp': r'Disk space (OK|WARNING|CRITICAL) - (\d+) kB free \( (\w+) % used\) .*'
            },
            {'properties': ['state', 'f'],
             'regexp': r'DISK (OK|WARNING|CRITICAL) - free space: \/ (\d+) (\w+) \((\d+)% inode=(\d+)%\): \/dev\/shm (\d+) (\w+) \((\d+)% inode=(\d+)%\).*'
            }
         ]
        }
    ],

    'check_http': [
        {'labelFilter': None,
         'eventtype': 'HTTP',
         'regexps': [
            {'properties': ['state', 'status' , 'bytes_returned', 'response_time'],
             'regexp': r'HTTP (OK|WARNING): HTTP\/1.1 (\d{3}) .* - (\d+) bytes in (\d+\.\d+).*'
            }
         ]
        },
	{'labelfilter': None,
	 'eventtype': 'HTTP',
	 'regexps' : [
	   {'properties': ['state'],
	    'regexp': r'(CRITICAL) - Socket timeout after 10 seconds' 
	   }
	]
      }
    ],



    'check_drbd': [
        {'labelFilter': 'DRBD',
         'eventtype': 'DRBD',
         'regexps': [
            {'properties': ['status', 'order', 'connected', 'updated'],
             'regexp': r'DRBD ([^:]+): Device 0 ([^ ]+) ([^ ]+) ([^ ]+)'
            }
         ]
        }
    ],

    'check_local_swap': [
        {'labelFilter': 'SWAP',
         'eventtype': 'SWAP',
         'regexps': [
            {'properties': ['state', 'free_memory'],
             'regexp': r'SWAP (OK|WARNING|CRITICAL) - (\d+)% free .*'
            }
         ]
        }
    ],

    'check_local_users': [
        {'labelFilter': 'USERS',
         'eventtype': 'USERS',
         'regexps': [
            {'properties': ['state', 'users'],
             'regexp': r'USERS (OK|WARNING|CRITICAL) - (\d+) .*'
            }
         ]
        }
    ],


    'check_local_users': [
        {'labelFilter': 'USERS',
         'eventtype': 'USERS',
         'regexps': [
            {'properties': ['state', 'logged_users'],
             'regexp': r'USERS (OK|WARNING|CRITICAL) - (\d+) .*'
            }
         ]
        }
    ],

    'check_ssh': [
        {'labelFilter': 'SSH',
         'eventtype': 'SSH',
         'regexps': [
            {'properties': ['state'],
             'regexp': r'SSH (OK|WARNING|CRITICAL) .*'
            }
         ]
        }
    ],


    'check_smtp': [
        {'labelFilter': 'SMTP',
         'eventtype': 'SMTP',
         'regexps': [
            {'properties': ['state', 'response_time'],
             'regexp': r'SMTP (OK|WARNING|CRITICAL) - (\d+\.\d+) .*'
            }
         ]
        }
    ],



    'check_heartbeat': [
        {'labelFilter': None,
         'eventtype': 'HEARTBEAT',
         'regexps': [
            {'properties': ['status', 'mode'],
             'regexp': r'Heartbeat (OK|WARNING|CRITICAL) - Modo (.+)'
            }
         ]
        }
    ],

    'check_mysql': [
        {'labelFilter': None,
         'eventtype': 'MYSQL',
         'regexps': [
            {'properties': ['uptime', 'threads', 'questions', 'slow_queries', 'opens', 'flush_tables', 'open_tables', 'average_queries_per_second'],
             'regexp': r'Uptime: ([0-9]+)  Threads: ([0-9]+)  Questions: ([0-9]+)  Slow queries: ([0-9]+)  Opens: ([0-9]+)  Flush tables: ([0-9]+)  Open tables: ([0-9]+)  Queries per second avg: ([0-9.]+)'
            }
         ]
        },
    ],

    'check_nt': [
        {'labelFilter': None,
         'eventtype': 'NT',
         'regexps': [
            {'properties': ['state', 'timeout'],
             'regexp': r'(ok|WARNING|CRITICAL) - Socket timeout after ([0-9]+) seconds'
            },
	    {'properties' : [],
	     'regexp': r'Connection refused'
	    },
	    {'properties': [],
             'regexp': r'could not fetch information from server'
	    },
            {'properties': ['load', 'time', 'resolution'],
             'regexp': r'CPU Load (\d+)% \((\d+) (\w+) average\)'
	    },
	    {'properties': ['total', 'total_unit', 'used', 'used_unit', 'used_percentage', 'free', 'free_unit', 'free_percentage'],
             'regexp': r'Memory usage: total:([0-9.]+) (\w{2}) - used: ([0-9.]+) (\w{2}) \(([0-9]+)%\) - free: ([0-9.]+) (\w{2}) \(([0-9]+)%\)'
	    },
	    {'properties': ['total', 'total_unit', 'used', 'used_unit', 'used_percentage', 'free', 'free_unit', 'free_percentage'],
             'regexp': r'c:\\ - total: ([\d.]+) (\w{2}) - used: ([\d.]+) (\w{2}) \((\d+)%\) - free ([\d.]+) (\w{2}) \((\d+)%\)'
	    },
	    {'properties': ['day', 'hour', 'minute'],
             'regexp': r'System Uptime - (\d+) day\(s\) (\d+) hour\(s\) (\d+) minute\(s\)'
	    },
         ]
        }
    ],
    'check_http_solr': [
        {'labelFilter': None,
         'eventtype': 'HTTPSolr',
         'regexps': [
            {'properties': ['state', 'http_version', 'status_code', 'status_description', 'bytes', 'response_time'],
             'regexp': r'HTTP (OK|WARNING|CRITICAL): HTTP\/([0-9.]+) ([0-9]{3}) (.+) - ([0-9]+) bytes in ([0-9.]+) second response time'
            },
	    {'properties' : [],
	     'regexp': r'No route to host'
	    },
         ]
        }
    ],

    'check_webinject': [
        {'labelFilter': None,
         'eventtype': 'WebInject',
         'regexps': [
            {'properties': ['state', 'time'],
             'regexp': r'WebInject (OK|WARNING|CRITICAL) - All tests passed successfully in ([0-9.]+) seconds.*'
            },
	    {'properties': ['state', 'timeout'],
             'regexp': r'WebInject (OK|WARNING|CRITICAL) - All tests passed successfully but global timeout \(([0-9]+) seconds\) has been reached'
            },
	    {'properties': ['state', 'failed'],
             'regexp': r'WebInject (OK|WARNING|CRITICAL) - Test case number \d+ failed'
            },
         ]
        }
    ],
}

expressions['tcp'] = expressions['check_tcp']

expressions['check_local_load'] = expressions['check_load']

expressions['http_args'] = expressions['http_args_follow']
expressions['https'] = expressions['http_args_follow']
expressions['https_args'] = expressions['http_args_follow']
expressions['http_regexp'] = expressions['http_args_follow']

expressions['check_local_disk'] = expressions['check_disk']