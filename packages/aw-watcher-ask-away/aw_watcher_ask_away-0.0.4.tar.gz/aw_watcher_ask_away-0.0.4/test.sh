aw-server --testing &
aw-watcher-afk --testing &
aw-watcher-ask-away --length 0.2 --testing &
$BROWSER http://localhost:5666/#/timeline
