import io
import logging
import pandas as pd
from IPython.display import display
from textdistance import jaro_winkler
import pandas as pd

logger = logging.getLogger(__name__)


class Stringmetric:
    header1 = ""
    header2 = ""
    data1 = ""
    data2 = ""

    def invoke(self, df1, df2):
        df1 = self.create_key(df1)
        df2 = self.create_key(df2)

        def map_rows(key):
            match = df2["key"].apply(lambda x: jaro_winkler.normalized_similarity(key, x)).max()


            confidence = match
            # use the Fuzzywuzzy library to find the closest match in Table 2

            # extract the matched SKU_PC and the confidence score
            matched_key = matched_sku = df2[df2["key"].apply(lambda x: jaro_winkler.normalized_similarity(key, x) == match)]["key"].values[0]


            # return a new row with the matched SKU_PC and the confidence score
            return df2.loc[df2.key == matched_key].assign(confidence=confidence).assign(key=key)


        # apply the function to each row in Table 1 and combine the results into a new table
        results = df1.apply(lambda row: map_rows(row["key"]), axis=1)
        df_stacked = pd.concat([r for r in results], ignore_index=True)#.reset_index( inplace=True)
        # result.info()

        result = df1.merge(df_stacked,on="key").reset_index(drop=True)

        ##print(result)
        result.drop_duplicates(inplace=True)
        result.reset_index(drop=True, inplace=True)
        return result.to_json()

    def create_key(self, df):
        '''add to the dataframe passed a new column with all column value concatenated'''
        df["key"] = df.apply(lambda row: " ".join(row.values.astype(str)), axis=1)
        return df
