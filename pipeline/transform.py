'''Transforms AO3 data ready for upload'''
import polars as pl

def clean_column_names(works) -> pl.DataFrame:
    '''Standardises the column names and returns a polars dataframe'''
    clean_df = pl.DataFrame(works)
    clean_df = clean_df.rename({clean_df.columns[0]: "rating",
                                clean_df.columns[1]: "warning",
                                clean_df.columns[2]: "category",
                                clean_df.columns[3]: "fandom",
                                clean_df.columns[4]: "relationship",
                                clean_df.columns[5]: "characters",
                                clean_df.columns[6]: "additional tags",
                                clean_df.columns[7]: "language",
                                clean_df.columns[8]: "stats",
                                clean_df.columns[9]: "published",
                                clean_df.columns[10]: "words",
                                clean_df.columns[11]: "chapters",
                                clean_df.columns[12]: "hits",
                                clean_df.columns[13]: "title",
                                clean_df.columns[14]: "author",})
    return clean_df

def clean_data(works: pl.DataFrame) -> pl.DataFrame:
    '''Returns a data frame with formatted column types'''
    works = works.drop('stats')
    works = works.with_columns(
        pl.col("chapters").str.extract(r"(\d+)$", 1).cast(pl.Int64).alias("chapters"),
        pl.col("words").str.replace(",", "").cast(pl.Int64),
        pl.col("hits").str.replace(",", "").cast(pl.Int64),
        pl.col("published").str.strptime(pl.Date, "%Y-%m-%d").alias("published")
    )
    return works



def transform(works: list[dict]) -> pl.DataFrame:
    '''Orchestrates transformation of scraped works'''
    works_df = clean_column_names(works)
    cleaned_works_df = clean_data(works_df)
    print(cleaned_works_df)

if __name__ == '__main__':
    test = [{'rating:': 'Not Rated', 'archive warning:': 'Creator Chose Not To Use Archive Warnings', 'category:': 'M/M', 'fandom:': ['Badminton RPF'], 'relationship:': ['王昶/梁伟铿'], 'characters:': ['王昶', '梁伟铿'], 'additional tags:': ['昶梁/敞亮/梁王'], 'language:': 'Español', 'stats:': 'Published:2024-11-26Words:2,596Chapters:1/1Hits:0', 'published:': '2024-11-26', 'words:': '2,596', 'chapters:': '1/1', 'hits:': '0', 'title': '[敞亮]绝代双骄', 'author': 'DreamRiverDR'}, {'rating:': 'General Audiences', 'archive warning:': 'No Archive Warnings Apply', 'category:': 'M/M', 'fandom:': ["New Dangan Ronpa V3: Everyone's New Semester of Killing"], 'relationship:': ['Oma Kokichi/Saihara Shuichi'], 'characters:': ['Oma Kokichi', 'Saihara Shuichi', 'Saihara Shuichi Uncle (Mentioned)'], 'additional tags:': ['Married Couple', 'Late Night Writing', 'Overworking', 'Domestic Fluff', 'Fluff', 'Married Life', 'No beta we die like my self esteem when I go ice skating.', 'Oma Kokichi is a sweetheart', 'Oma Kokichi is a housewife'], 'language:': 'English', 'stats:': 'Published:2024-11-26Words:430Chapters:1/1Hits:0', 'published:': '2024-11-26', 'words:': '430', 'chapters:': '1/1', 'hits:': '0', 'title': 'Overworking', 'author': 'JustARandomPersonTryingToSurvive'}]
    transform(test)