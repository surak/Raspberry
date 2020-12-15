IP=$(ip -4 addr show wlan0 | grep -oP '(?<=inet\s)\d+(\.\d+){3}')
TOKEN=$(cat token.secret)
echo url="https://www.duckdns.org/update?domains=surak-bird&token=$TOKEN&ip=$IP" | curl -k -K -
