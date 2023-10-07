# SEC-API-UTILS
This python package is an unofficial wrapper for the SEC-EDGAR-API. According to the fair-use policy of the API provided 
by the SEC, 10 requests per second can be made (https://www.sec.gov/developer). Limiting the number of requests is automatically fulfilled 
by the data loader of the SEC-API-UTILS package. 
The data loader can be used for retrieving company facts by the use of the ticker name of the company.
Furthermore, the python package provides some utilities for plotting the data retrieved. 
Data can either be retrieved as a dictionary corresponding to the JSON retrieved over the SEC-API or an internal 
representation starting with the SECCompanyInfo class. 
## Data Loader
Loading the data over SEC-EDGAR-API can be performed by using the SECAPILoader to which at least the name and the email 
address must be provided. For being able to use the ticker name as identifier the SECAPILoader loads a 
ticker to CIK (SEC identification number of the stock) mapping into a cache directory once in the current working 
directory.

Following 4 lines show the simple loading of data with the use of the
SECAPILoader. 
```python
from sec_api_utils.data_loading.SECAPILoader import SECAPILoader
from sec_api_utils.data_representation.SECCompanyInfo import SECCompanyInfo
data_loader = SECAPILoader(your_company_name="<your_company_name>", 
                           your_company_email="<your>@<company_email>.com",
                           override_cached_company_tickers=False)
data_msft: SECCompanyInfo = data_loader.get_data_from_ticker(ticker_name="MSFT", as_dict=False)
```
Setting 'override_cached_company_tickers' to False enforces the data loader to use the 
'company_tickers.json' (ticker name to CIK mapping) from the cached directory. 
When set to true the 'company_tickers.json' is overridden in the cache directory 
even if it is already available.
 
When loading the data with 'data_loader.get_data_from_ticker' one can simply choose if he wants the raw data 
as dictionary or in the representation provided by the package by setting flag 'as_dict' to True or False.

## Data Representation (package classes vs. dictionary)
As mentioned in section 'Data Loading' one can choose between representation of the loaded data as a dictionary
or as the provided representation covered by the classes in data_representation.

When choosing the dictionary as representation the retrieved object represents a nested dictionary containing 
the requested data of the given company. The retrieved dictionary will look like the following:
```json
{
	"cik": 789019,
	"entityName": "MICROSOFT CORPORATION",
	"facts": {
		"dei": {
			"EntityCommonStockSharesOutstanding": {
				"label": "Entity Common Stock, Shares Outstanding",
				"description": "Indicate number of shares or other units outstanding of each of registrant's classes of capital or common stock or other ownership interests, if and as stated on cover of related periodic report. Where multiple classes or units exist define each class/interest by adding class of stock items such as Common Class A [Member], Common Class B [Member] or Partnership Interest [Member] onto the Instrument [Domain] of the Entity Listings, Instrument.",
				"units": {
					"shares": [
						{
							"end": "2009-10-19",
							"val": 8879121378,
							"accn": "0001193125-09-212454",
							"fy": 2010,
							"fp": "Q1",
							"form": "10-Q",
							"filed": "2009-10-23",
							"frame": "CY2009Q3I"
						},
						...
					]
				}
			},
			...
		"us-gaap": {
			"AccountsPayableCurrent": {
				"label": "Accounts Payable, Current",
				"description": "Carrying value as of the balance sheet date of liabilities incurred (and for which invoices have typically been received) and payable to vendors for goods and services received that are used in an entity's business. Used to reflect the current portion of the liabilities (due within one year or within the normal operating cycle if longer).",
				"units": {
					"USD": [
						{
							"end": "2009-06-30",
							"val": 3324000000,
							"accn": "0001193125-09-212454",
							"fy": 2010,
							"fp": "Q1",
							"form": "10-Q",
							"filed": "2009-10-23"
						},
                      ...
					]
				}
			},
          ...
		}
	}
}
```

When using the provided classes as representation of the data, the outermost dictionary will be represented by the 
SECCompanyInfo class. Filing information about the company are stored inside the SECFilingInfo class,
which represents the dictionary in the facts section. Each of the members of the SECFilingInfo
like 'us_gaap' is a list of SECBaseMeasures, which contain e.g. label, description and the units. 
The units member of the SECBaseMeasure is a list of SECUnits, which represent one data point in time
to the corresponding SECBaseMeasure. This could be for instance the Goodwill of the company.

SECCompanyInfo provides methods for retrieving the desired information by name in efficient manner.
If one wants to get the yearly goodwill information filed by a company one can simply use the SECCompanyInfo retrieved
as shown below:

```python
from sec_api_utils.data_loading.SECAPILoader import SECAPILoader
from sec_api_utils.data_representation.SECCompanyInfo import SECCompanyInfo
from sec_api_utils.data_representation.SECBaseMeasure import SECBaseMeasure
data_loader = SECAPILoader(your_company_name="<your_company_name>", 
                           your_company_email="<your>@<company_email>.com",
                           override_cached_company_tickers=False)
data_msft: SECCompanyInfo = data_loader.get_data_from_ticker(ticker_name="MSFT", as_dict=False)
goodwill_filings: SECBaseMeasure = data_msft.get_measure_info("Goodwill")
yearly_goodwill = goodwill_filings.get_by_form_type("10-K")
```

## Data Analytics

The data analytics part of the package provides some simple methods for analyzing the data retrieved from the SEC-API or
data from stocks, which were retrieved from other sources. Currently, the data analytics part provides a fair value 
calculator and a monte carlo sampler for the stock price based on a given gaussian distribution.


## Plotting

For fast visualization of the datapoints a simple plotting function, which plots the data
with the help of matplotlib and seaborn is provided.

Continuing the example from above the goodwill can be plotted with the following call

```python
from sec_api_utils.plotting.SECUnitPlotter import NumberFormat, SECUnitPlotter 
SECUnitPlotter().plot_sec_units_base(yearly_goodwill, auto_number_format=False, number_format=NumberFormat.THOUSANDS, title="Goodwill")
```

To the plot_sec_units_base() method the List[SECUnits] is passed, which were retrieved and stored in variable
'yearly_goodwill'. Parameter 'auto_number_format' declares if the number format should be determined automatically, 
which is set to False in this case because we provided a number_format with 'NumberFormat.THOUSANDS'. The passed
number format will show the SECUnits in thousands on the plot. Furthermore, we passed a title
to the plotting method as well. As a result, we get the following plot:

![Goodwill plot](sample_plots/goodwill_yearly.png)

## NOTICE
If you like the package please provide a star on github. If you have any questions or suggestions feel free 
to contact me. If any known issues occur please open an issue on github.
