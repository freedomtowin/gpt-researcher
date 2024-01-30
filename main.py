from researcher.base import Researcher
import asyncio

# It is best to define global constants at the top of your script
QUERY = "What are some Missisipi Pot Roast recipes?"
STORE = "Food Lion"
REPORT_TYPE = "research_report"


# async def fetch_report(query, report_type):
#     """
#     Fetch a research report based on the provided query and report type.
#     """
#     researcher = Researcher(query=query, report_type=report_type, config_path=None)
#     report = await researcher.run()
#     return report

# async def generate_research_report():
#     """
#     This is a sample script that executes an async main function to run a research report.
#     """
#     report = await fetch_report(QUERY, REPORT_TYPE)
#     print(report)

async def fetch_report(store, query, report_type):
    """
    Fetch a research report based on the provided query and report type.
    """
    researcher = Researcher(store=store, query=query, report_type=report_type, source_urls=[], config_path=None)
    report = await researcher.run()
    return report

async def generate_research_report():
    """
    This is a sample script that executes an async main function to run a research report.
    """
    report = await fetch_report(STORE, QUERY, REPORT_TYPE)
    print(report)

if __name__ == "__main__":
    asyncio.run(generate_research_report())