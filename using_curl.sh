# https://support.zenoss.com/hc/en-us/articles/202384859-How-To-Create-And-Close-Events-Via-curl-With-The-JSON-API

# create event
curl -u "admin:zenoss" -X POST -H "Content-Type:application/json" -d "{\"action\":\"EventsRouter\", \"method\":\"add_event\", \"data\":[{\"summary\":\"test55\", \"device\":\"test-rhel6.zenoss.loc\", \"component\":\"\", \"severity\":\"Critical\", \"evclasskey\":\"\", \"evclass\":\"/App\"}], \"type\":\"rpc\", \"tid\":1}" "sandbox411.zenoss.loc:8080/zport/dmd/evconsole_router"

# close event
curl -u "admin:zenoss" -X POST -H "Content-Type:application/json" -d '{"action":"EventsRouter","method":"close","data":[{"evids":["0050568a-2045-b48a-11e2-708c5755a8dd"],"params":"{\"severity\":[5,4,3,2,1,0],\"eventState\":[0,1,2]}","limit":1}],"type":"rpc","tid":1}' "sandbox411.zenoss.loc:8080/zport/dmd/evconsole_router"
