for ip in "$@"
do
  ./webrepl_cli.py main.py $ip:/main.py
  ./webrepl_cli.py candle_client.py $ip:/candle_client.py  
done

