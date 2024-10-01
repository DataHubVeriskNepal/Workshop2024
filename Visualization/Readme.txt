Requirements: 

PowerBI (Desktop Version) 

 

Instructions: 


Loading Data from Snowflake to Power BI :


Copy the account URL from bottom left account option menu 

Go to Power BI, click on get data, click on more, search for snowflake and hit connect 

Paste the URL in “server” field and remove the `https://` of URL 

Enter “COMPUTE_WH” in Warehouse field 

Enter the credentials and hit ok 

Select a database and go inside public schema and select tables and hit transform 

Follow along the demo for the transformation part 

 

 

DAX Measures: 


Gold Rate in USD = IF( 

    RELATED('Currency_Key_Dimension'[ISO3])="USD", [Native Prices], 

    [Native Prices]*[USD Rate]) 


Max Sell Date = 

    VAR MaxRate = MAXX('Forex_GS_Merged',[Uniform_Sell]) 

    VAR MaxRateDate = CALCULATE( 

            MAX('Date_Dimension'[date]), 

            Filter('Forex_GS_Merged',[Uniform_Sell]=MaxRate) ) 

    RETURN FORMAT(MaxRateDate, "yyyy/mm/dd") 

  

 Max Sell Rate = MAXX('Forex_GS_Merged',[Uniform_Sell]) 

  

Min Buy Date = 

    VAR MinRate = MINX('Forex_GS_Merged',[Uniform_Buy]) 

    VAR MinRateDate = CALCULATE( 

            MIN('Date_Dimension'[date]), 

            Filter('Forex_GS_Merged',[Uniform_Buy]=MinRate)) 

    RETURN FORMAT(MinRateDate, "yyyy/mm/dd") 

  

Min Buy Rate = MINX('Forex_GS_Merged',[Uniform_Buy]) 

 

Avg gold rate(in Thousands)= DIVIDE(AVERAGE('Forex_GS_Merged_Fact'[standard_gold]),1000) 