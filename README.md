usage: main.py [-h] [--dump] [--dry-run] [--client CLIENT]

               [--client-host CLIENT_HOST] [--client-port CLIENT_PORT]
               
               [--torrent-source TORRENT_SOURCE] [--t411-login T411_LOGIN]
               
               [--t411-passwd T411_PASSWD] [--metadata METADATA]
               
               show season episode


Auto-download series and animes


positional arguments:

           show                  Show name to download
           
           season                Season to start download from
           
           episode               Episode to start download from


optional arguments:

         -h, --help            show this help message and exit
         
         --dump                Dump a list for magnet links if possible
         
         --dry-run             Only show what would be done
         
         --client CLIENT       Torrent client for download
         
         --client-host CLIENT_HOST
         
                  Hostname for the torrent client


         --client-port CLIENT_PORT
         
                  Port of the torrent client


         --torrent-source TORRENT_SOURCE
         
                  Source for torrents/magnets

         --t411-login T411_LOGIN
         
                  t411 username

         --t411-passwd T411_PASSWD
         
                  t411 password

         --metadata METADATA   the metadata service to use
