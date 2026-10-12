import json
import sys
from pathlib import Path
import os
from pprint import pprint

class ConfigTest:
    def __init__(self, config=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = config

    def run(self):
        # Resolve path relative to this script's directory to avoid working directory issues

        spider_dir = os.path.dirname(os.path.abspath(__file__))

        config_path = os.path.join(spider_dir, '..', 'configs')


        with open(f"{config_path}/{self.config}", "r", encoding="utf-8") as f:
            file = json.load(f)
            for x,y in file[0].items():
                for url in y["urls"]:
                    print(f"{x}: {url['url']}")

if __name__ == "__main__":
    # Allows passing the filename via command line: python test_config.py OrConfig.json
    
    config_name = sys.argv[1]
    
    tester = ConfigTest(config=config_name)
    tester.run()