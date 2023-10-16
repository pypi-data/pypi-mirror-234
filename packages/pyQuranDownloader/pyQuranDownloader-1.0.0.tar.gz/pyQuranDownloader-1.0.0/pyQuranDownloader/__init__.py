"""
https://github.com/RKDeveloppement
"""

__version__ = "1.0.0"

import os
from time import sleep
from urllib3 import PoolManager
from threading import Thread, active_count

class QuranDownloader:
    
    def __init__(self, *, download: bool, max_threads: int = 10) -> None:
        self.max_threads = max_threads
        if download:
            self.downloadquran()
    
    def downloadquran(self):
        if not os.path.isdir("Quran"):
            os.makedirs("Quran")
        for sheikh_id, sheikh_data in getSheikhs().items():
            sheikh_data = dict(sheikh_data)
            self.createPaths(sheikh_id)
            http = PoolManager()
            base_url = f"https://{sheikh_data.get('downloadServer')}.mp3quran.net/{sheikh_id}/"
            for i in range(1, 115):
                url = base_url + "{:03d}.mp3".format(i)
                a = True
                while a:
                    if active_count() < self.max_threads:
                        Thread(target=self.download, args=(http, url, f"Quran/{sheikh_id}/{url[-7:]}")).start()
                        a = False
                    else:
                        sleep(0.5)
                print(f"Downloading {sheikh_data.get('name')} ({int((i*100)//114)}%)...          ", end="\r")
    
    def download(self, http: PoolManager, url: str, path: str):
        with open(file=path, mode="wb+") as saveQuran:
            response = http.urlopen('GET', url)
            saveQuran.write(response.data)
            
    def createPaths(self, sheikh_id: str):
        if not os.path.isdir(f"Quran/{sheikh_id}"):
            os.makedirs(f"Quran/{sheikh_id}")
            
def getSheikhs() -> dict:
    sheikhsDict = {
        "maher": {
            "name": "Maher Al Muaiqly",
            "riwayat": "Hafs ('Aasim)",
            "biographiy": "Né le 7 janvier 1969 à Médine, il est un imam et prédicateur saoudien connu pour sa récitation du Coran.",
            "img": "https://i.pinimg.com/564x/26/5d/3b/265d3b30f8d48c7acfc92d27d31c72ee.jpg",
            "downloadServer": "server12"
        },
        "shur": {
            "name": "Saoud Al-Shuraim",
            "riwayat": "Hafs ('Aasim)",
            "biographiy": "Né le 19 janvier 1964 à Riyad, il est un célèbre imam et récitateur saoudien, également Imam de la Grande Mosquée de La Mecque",
            "img": "https://s-media-cache-ak0.pinimg.com/564x/41/75/00/4175004b89851b4d92d9ba543deba383.jpg",
            "downloadServer": "server7"
        },
        "yasser": {
            "name": "Yasser Al-Dosari",
            "riwayat": "Hafs ('Aasim)",
            "biographiy": "Né en 1981 à Riyad, il est un célèbre imam et récitateur saoudien, reconnu pour sa psalmodie exceptionnelle du Coran.",
            "img": "https://i.pinimg.com/564x/28/08/6e/28086e4bac69ea06098568974847d672.jpg",
            "downloadServer": "server11"
        },
        "lhdan": {
            "name": "Muhammad Al-Luhaidan",
            "riwayat": "Hafs ('Aasim)",
            "biographiy": "Né en 1965 à Djeddah, est un imam et récitateur saoudien, reconnu pour sa magnifique psalmodie du Coran",
            "img": "https://i.pinimg.com/564x/a4/cd/74/a4cd749ed1726e63e8a62e279e5ea564.jpg",
            "downloadServer": "server8"
        },
        "afs": {
            "name": "Mishary  Al Afasy",
            "riwayat": "Hafs ('Aasim)",
            "biographiy": "Né le 5 septembre 1976 au Koweït il est récitateur et chanteur religieux renommé, reconnu mondialement pour sa voix captivante.",
            "img": "https://i.pinimg.com/564x/93/08/8b/93088be16e324b36b2d98a12748366a6.jpg",
            "downloadServer": "server8"
        },
        "qtm": {
            "name": "Nasser Al Qatami",
            "riwayat": "Hafs ('Aasim)",
            "biographiy": "Né le 18 janvier 1980 au Koweït, est un célèbre récitateur du Coran. Sa voix exceptionnelle et sa précision dans la récitation en ont fait une référence mondiale.",
            "img": "https://i.pinimg.com/564x/6f/2d/35/6f2d3586e913233f1f03ade207398949.jpg",
            "downloadServer": "server6" 
        }
    }

    return sheikhsDict