## Using the API
There is a limit to the number of API calls you can make per minute — if exceeded, your API Key will be banned for an 
hour, and you will be unable to retrieve any data during that period. This is true for all of the APIs (Federal Reserve
Bureau of Economic Analysis, and BLS)

To run all of these scripts at once, and update all of the TAG2 data (excluding CBO, which doesn't provide an API), 
go to pyBEA/update_all/update_all_data.py and run the main function. This will likely take around twenty minutes.
This is because the APIs throttle the rate of requests and the size of responses. 

1. BEA (NIPA) Data
    - Only the annual NIPA data is necessary for the TAG2 model, but this API allows you to get Quarterly or Monthly too 
    - aggregate_nipa_A.csv is equivalent to nipadataA.csv, it has roughly 658,000 lines compared to 551,000 in nipadataA.csv
    - If you want to update this data, go to the file ‘automate_nipa.py’ and call the function update_all_nipa_tag 
      with ‘A’ as the argument
    - i.e update_all_nipa_tag(‘A’)
2. BEA Fixed Asset Account Data
    - aggregate_fa.should be equivalent to fixed_assets.csv in the TAG model
    - aggregate_fa has roughly 530,000 lines vs. fixed_assets with roughly 515,000
    - in pyBEA/pybea/automate_fixed_assets.py, call update_all_fa_tag()
3. Flow of Funds from FED
    - output_fed_merge.csv is equivalent to fed_key_merged.csv in TAG2, it removes a few extraneous columns like 
      variable number, symbol, calculation, fed unique identifier, and file.
    - in pyBEA/federal_reserve/merge_fed_data.py call the main function to collect this data
4. Bureau of Labor Statistics (BLS) data
    - The only BLS data series we actually used appears to be LNU00000000, which is also offered by the Federal Reserve. 
      For simplification purposes (and because the BLS API is not good), we will just get this data from the Fed API from now on.
    - In pyBEA/federal_reserve/labor_data.py call the main function, output goes to labor_data.csv.
5. CBO 
    - There is no API for the CBO data, need to continue downloading it directly from the website.
