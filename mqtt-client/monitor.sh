#/bin/bash
# Monitor certain mesages from the loraserver on MQTT
#
# Craig Hesling <craig@hesling.com>
# August 15, 2016
# Updated: November 18, 2016

complete -W "sim gw gwstat gwstats gw* tx rx app apptx apprx app???????????????? app????????????????/???????????????? app/????????????????" monitor

# If we are actually being run and not sourced
if [ "$0" = "$BASH_SOURCE" ]; then

SERVER=openchirp.andrew.cmu.edu
USER=team21
PASS=BobsBurgers5598
#DEBUG=-d

run() {
	local topic_args=(  )
	for arg; do
		topic_args+=( "-t \"$arg\"" )
	done
	eval exec mosquitto_sub -v -h $SERVER --capath /etc/ssl/certs -u $USER -P $PASS $DEBUG ${topic_args[*]}
}

set -x

topics=( )

for arg; do
	case $arg in
		sim)
			topics+=( "simulation/#" )
			;;
		gw)
			topics+=( "gateway/#" )
			;;
		gwstat|gwstats)
			topics+=( "gateway/+/stats" )
			;;
		gw*)
			gatewayid=${arg:2}
			gatewayid_expand=$(printf "%4.4d" "${gatewayid}")
			topics+=( "gateway/d00d8badf00d${gatewayid_expand}/#" )
			;;
		tx)
			topics+=( "gateway/+/tx" )
			;;
		rx)
			topics+=( "gateway/+/rx" )
			;;
		app)
			topics+=( "application/#" )
			;;
		apptx)
			topics+=( "application/+/+/+/tx" )
			;;
		apprx)
			topics+=( "application/+/+/+/rx" )
			;;
		# Match anything in the appended application id
		app????????????????)
			app_id=${arg:4:16}
			topics+=( "application/$app_id/nodes/#" )
			;;
		# Match anything from a the application and device specified
		app????????????????/????????????????)
			app_id=${arg:4:16}
			dev_id=${arg:21:16}
			topics+=( "application/$app_id/nodes/$dev_id/#" )
			;;
		# Match anything from the specified device and default applicaton id 00000000000000
		app/????????????????)
			topics+=( "application/0000000000000000/node/${arg#app/}/#" )
			;;
		*)
			# Allow subscribing to any random topic that is not in the shortcut list
			topics+=( "$arg" )
			;;
	esac
done

# Add default topic if none specified
if [ ${#topics[@]} -eq 0 ]; then
	topics=( "#" )
fi

run ${topics[@]}
fi
