import time as timeit
from datetime import datetime, time

from bond_data.fixed_rate_bond_data import FixedRateBondData
from plotting import create_single_day_plot_per_institute, create_multi_day_plot
from result_handlers.csv_result_handler import CsvResultHandler
from result_handlers.database_result_handler import DatabaseResultHandler
from result_handlers.result_handler import ResultHandler
from scrapers.scraper import Scraper
from util import print_time_prefixed

from scrapers.scraper_orchestrator import ScraperOrchestrator
from scrapers.jyske_scraper import JyskeScraper
from scrapers.nordea_scraper import NordeaScraper
from scrapers.total_kredit_scraper import TotalKreditScraper
from scrapers.realkredit_danmark_scraper import RealKreditDanmarkScraper


def main():
    # TODO: Remove while-loop when program is executed using pinger/task-scheduler.
    while True:
        start_time = timeit.time()
        now = datetime.utcnow()
        now = datetime(now.year, now.month, now.day, now.hour, now.minute)

        scrapers: list[Scraper] = [
            JyskeScraper(),
            RealKreditDanmarkScraper(),
            NordeaScraper(),
            TotalKreditScraper()
        ]

        result_handler: ResultHandler = DatabaseResultHandler(now)

        scraper_orchestrator = ScraperOrchestrator(scrapers)

        if now.minute % 5 == 0:
            # TODO: Incorporate accounting for Danish banking holidays.
            if time(7, 0) <= now.time() < time(15, 1) and now.isoweekday() <= 5:
                if not result_handler.result_exists():
                    fixed_rate_bond_data: FixedRateBondData = scraper_orchestrator.scrape()
                    result_handler.export_result(fixed_rate_bond_data)
                    # create_single_day_plot_per_institute(now.today())

            if now.hour == 15 and now.minute == 5:
                # create_multi_day_plot()
                # print_time_prefixed("Updated multi day plot")
                timeit.sleep(60)

        timeit.sleep(max(10 - (timeit.time() - start_time), 0))


if __name__ == "__main__":
    main()
