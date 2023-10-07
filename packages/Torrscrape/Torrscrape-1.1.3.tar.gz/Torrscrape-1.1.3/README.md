##How to Use 

<h1>Installation</h1>
<h2>pip install Torrscrape</h2>

<h2>1)Install docker</h2> 
  mac:https://docs.docker.com/desktop/install/mac-install/<br>
  win:https://docs.docker.com/desktop/install/windows-install/<br>
  linux:https://docs.docker.com/desktop/install/linux-install/<br>
<h2>2)setup jackett:</h2>

docker run -d \
  --name=jackett \
  -e PUID=1000 \
  -e PGID=1000 \
  -e TZ=Etc/UTC \
  -e AUTO_UPDATE=true `#optional` \
  -e RUN_OPTS= `#optional` \
  -p 9117:9117 \
  -v /path/to/data:/config \
  -v /path/to/blackhole:/downloads \
  --restart unless-stopped \
  lscr.io/linuxserver/jackett:latest

<h2>3)setup qbit web(docker):</h2>

docker run -d \
  --name=qbittorrent \
  -e PUID=1000 \
  -e PGID=1000 \
  -e TZ=Etc/UTC \
  -e WEBUI_PORT=8080 \
  -p 8080:8080 \
  -p 6881:6881 \
  -p 6881:6881/udp \
  -v /path/to/appdata/config:/config \
  -v /path/to/downloads:/downloads \
  --restart unless-stopped \
  lscr.io/linuxserver/qbittorrent:latest

##Usage<br>
<h3>save api key jackett</h3>
<h3>torrscrape --api "jackett_apikey" </h3>
<h1>Search</h1>
<h3>torrscrape --search "search_term" --catagory "catagories"</h3>
<h2>catagories: TV,TV/Anime,Other,Movies,PC/Games</h2>