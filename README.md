dataflipper
===========

Often we get csvs/tsvs out of hive or postgres that we want to manually inspect, so we end up manually copying a handful of ids into the address bar or building a spreadsheet with urls that requires lots of clicking.

Instead, use data flipp(e)r

example:

assume you have a csv with headers with 4sq venue ids in the 'id' column. Because 4sq is security conscious, we need to proxy the results with --proxy.

  (-H for headers, -p for url pattern, --proxy for proxy, -f for file input)

  ./create-virtualenv-with-deps.sh
  ./env/bin/python flipper.py -p 'http://foursquare.com/venue/${id}' -H --proxy -f input.csv

If you don't need the proxy, and don't specify --server, it outputs static html to stdout.
