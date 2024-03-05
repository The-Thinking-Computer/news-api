from scraper import WNEP_scraper,PAHOMEPAGE_scraper
import tools
PAHOMEPAGE.record_articles()
WNEP.record_articles()
tools.write_articles_to_json(all_articles)