import cyperf_agent_manager.agent_manager as caMgr
agentIPs     = [ '10.36.75.69', '10.36.75.70' ]
controllerIP = '10.36.75.126'
testIface    = 'auto'
debFile      = '/home/pmajumdar/tmp/tiger_x86_64_ixos-8.50_ixstack-raw_release_1.0.0.1815.deb'
agentMgr     = caMgr.CyPerfAgentManager(agentIPs)
agentMgr.InstallBuild (debFile)
agentMgr.ControllerSet (controllerIP)
agentMgr.Reload ()
agentMgr.SetTestInterface (testIface)
