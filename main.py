import requests
import argparse
import random
import logging
from itertools import product
from prettytable import PrettyTable
from multiprocessing import Pool
from requests_html import HTMLSession
from typing import List, NoReturn


logging.basicConfig(
    level=logging.INFO,
    filename="log.log",
    filemode="w",
    format="%(asctime)s %(levelname)s %(message)s",
)

class ConstructorApp:
    __version__ = ''''1.0.0 Beta'''
    
    def __init__(self, processes, hostname):
        self._hostname = hostname
        self._processes = processes
        self.__links = []

    def get_links(self):
        try:
            session = HTMLSession()
            response = session.get(self._hostname)
            for link in response.html.links:
                if link[0] == "/" and len(link) < 120:
                    self.__links.append(link)
            return self.__links
        except Exception as error:
            print(f"OPS! All crashed...! Please, try again!")
            logging.error(f"Error : {error}", exc_info=True)
            exit()

    def create_processes(self):
        try:
            if int(self._processes) == 0 or int(self._processes) < 0:
                self._processes = 10
                return self._processes
            else:
                return self._processes
        except ValueError:
            self._processes = 10
            logging.error("ValueError : parry : continue", exc_info=True)
            return self._processes

def main(processes: int, hostname: str):
    construct_app = ConstructorApp(processes, hostname)
    links = construct_app.get_links()
    proc = construct_app.create_processes()

    logging.info(f"Testing WebSite: {hostname}, processes: {proc}")

    def pool():
        process = Pool(int(proc))
        process.starmap(run_app, product([links], [hostname]))

    return pool()

def run_app(links: List[str], hostname: List[str]) -> NoReturn:
    table = PrettyTable()
    table.field_names: List[str, 4] = ["Requests", "StatusCode", "ResponseTime", "HTTP Method"]
    while True:
        response = requests.get(f"{hostname}{random.choice(links)}")
        logging.info(
            f"Requests: {response.url} : StatusCode : {response.status_code} : ResponseTime : {response.elapsed.total_seconds()} : HTTP Method : GET"
        )
        table.add_row(
            [
                response.url,
                response.status_code,
                response.elapsed.total_seconds(),
                "GET",
            ]
        )
        print(table)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--processes",
        "-p",
        action="store",
        dest="processes",
        help="enter count processes, default=50",
        default=50,
    )
    parser.add_argument(
        "--hostname",
        "-host",
        action="store",
        dest="hostname",
        help="enter hostname, example: https://target.site",
    )
    args = parser.parse_args()
    main(args.processes, args.hostname)
