# Transforms a nested dictionary or iterable into a Pandas DataFrame.

## Tested against Windows / Python 3.11 / Anaconda

## pip install nested2dataframe

```python
	

This function takes a nested dictionary or iterable and converts it into a Pandas DataFrame where each level of nesting
is represented as a separate column. The function is designed to handle dictionaries with varying levels of nesting,
and it can handle missing values, such as NaN or None, and fill them with the specified `tmpnone` value.

Parameters:
- it (dict or iterable): The input nested dictionary or iterable.
- key_prefix (str, optional): The prefix to use for naming the columns representing each level of nesting.
  Defaults to "level_".
- tmpnone (any, optional): The value to replace NaN or None values in the DataFrame. Defaults to "NANVALUE".
- fillna (any, optional): The value to fill NaN values in the final DataFrame. Defaults to pd.NA.
- optimize_dtypes (bool, optional): Whether to optimize the data types of the DataFrame columns. If True,
  it will attempt to reduce memory usage by changing data types where possible. Defaults to True.

Returns:
- pandas.DataFrame: A Pandas DataFrame where each level of nesting is represented as a separate column.

Example:
	from nested2dataframe import nestediter2df
	d7 = {
		"results": [
			{
				"end_time": "2021-01-21",
				"key": "q1",
				"result_type": "multipleChoice",
				"start_time": "2021-01-21",
				"value": ["1"],
			},
			{
				"end_time": "2021-01-21",
				"key": "q2",
				"result_type": "multipleChoice",
				"start_time": "2021-01-21",
				"value": ["False"],
			},
			{
				"end_time": "2021-01-21",
				"key": "q3",
				"result_type": "multipleChoice",
				"start_time": "2021-01-21",
				"value": ["3"],
			},
			{
				"end_time": "2021-01-21",
				"key": "q4",
				"result_type": "multipleChoice",
				"start_time": "2021-01-21",
				"value": ["3"],
			},
		]
	}

	df77 = nestediter2df(d7)
	print(df77.to_string())

	#    level_1  level_2 level_3    end_time key     result_type  start_time      0
	# 0  results        0   value  2021-01-21  q1  multipleChoice  2021-01-21      1
	# 1  results        1   value  2021-01-21  q2  multipleChoice  2021-01-21  False
	# 2  results        2   value  2021-01-21  q3  multipleChoice  2021-01-21      3
	# 3  results        3   value  2021-01-21  q4  multipleChoice  2021-01-21      3




d1 = {
    "level1": {
        "t1": {
            "s1": {"col1": 5, "col2": 4, "col3": 4, "col4": 9},
            "s2": {"col1": 1, "col2": 5, "col3": 4, "col4": 8},
            "s3": {"col1": 11, "col2": 8, "col3": 2, "col4": 9},
            "s4": {"col1": 5, "col2": 4, "col3": 4, "col4": 9},
        },
        "t2": {
            "s1": {"col1": 5, "col2": 4, "col3": 4, "col4": 9},
            "s2": {"col1": 1, "col2": 5, "col3": 4, "col4": 8},
            "s3": {"col1": 11, "col2": 8, "col3": 2, "col4": 9},
            "s4": {"col1": 5, "col2": 4, "col3": 4, "col4": 9},
        },
        "t3": {
            "s1": {"col1": 1, "col2": 2, "col3": 3, "col4": 4},
            "s2": {"col1": 5, "col2": 6, "col3": 7, "col4": 8},
            "s3": {"col1": 9, "col2": 10, "col3": 11, "col4": 12},
            "s4": {"col1": 13, "col2": 14, "col3": 15, "col4": 16},
        },
    },
    "level2": {
        "t1": {
            "s1": {"col1": 5, "col2": 4, "col3": 9, "col4": 9},
            "s2": {"col1": 1, "col2": 5, "col3": 4, "col4": 5},
            "s3": {"col1": 11, "col2": 8, "col3": 2, "col4": 13},
            "s4": {"col1": 5, "col2": 4, "col3": 4, "col4": 20},
        },
        "t2": {
            "s1": {"col1": 5, "col2": 4, "col3": 4, "col4": 9},
            "s2": {"col1": 1, "col2": 5, "col3": 4, "col4": 8},
            "s3": {"col1": 11, "col2": 8, "col3": 2, "col4": 9},
            "s4": {"col1": 5, "col2": 4, "col3": 4, "col4": 9},
        },
        "t3": {
            "s1": {"col1": 1, "col2": 2, "col3": 3, "col4": 4},
            "s2": {"col1": 5, "col2": 6, "col3": 7, "col4": 8},
            "s3": {"col1": 9, "col2": 10, "col3": 11, "col4": 12},
            "s4": {"col1": 13, "col2": 14, "col3": 15, "col4": 16},
        },
    },
}
#    level_1 level_2 level_3  col1  col2  col3  col4
# 0   level1      t1      s1     5     4     4     9
# 1   level1      t1      s2     1     5     4     8
# 2   level1      t1      s3    11     8     2     9
# 3   level1      t1      s4     5     4     4     9
# 4   level1      t2      s1     5     4     4     9
# 5   level1      t2      s2     1     5     4     8
# 6   level1      t2      s3    11     8     2     9
# 7   level1      t2      s4     5     4     4     9
# 8   level1      t3      s1     1     2     3     4
# 9   level1      t3      s2     5     6     7     8
# 10  level1      t3      s3     9    10    11    12
# 11  level1      t3      s4    13    14    15    16
# 12  level2      t1      s1     5     4     9     9
# 13  level2      t1      s2     1     5     4     5
# 14  level2      t1      s3    11     8     2    13
# 15  level2      t1      s4     5     4     4    20
# 16  level2      t2      s1     5     4     4     9
# 17  level2      t2      s2     1     5     4     8
# 18  level2      t2      s3    11     8     2     9
# 19  level2      t2      s4     5     4     4     9
# 20  level2      t3      s1     1     2     3     4
# 21  level2      t3      s2     5     6     7     8
# 22  level2      t3      s3     9    10    11    12
# 23  level2      t3      s4    13    14    15    16


d3 = [
    {
        "cb": ({"ID": 1, "Name": "A", "num": 50}, {"ID": 2, "Name": "A", "num": 68}),
    },
    {
        "cb": ({"ID": 1, "Name": "A", "num": 50}, {"ID": 4, "Name": "A", "num": 67}),
    },
    {
        "cb": (
            {"ID": 1, "Name": "A", "num": 50},
            {"ID": 6, "Name": "A", "num": 67, "bubu": {"bibi": 3}},
        ),
    },
]

#    level_1  level_2    end_time key     result_type  start_time  value
# 0  results        0  2021-01-21  q1  multipleChoice  2021-01-21      1
# 1  results        1  2021-01-21  q2  multipleChoice  2021-01-21  False
# 2  results        2  2021-01-21  q3  multipleChoice  2021-01-21      3
# 3  results        3  2021-01-21  q4  multipleChoice  2021-01-21      x


df33 = nestediter2df(d3)
print(df33.to_string())

#    level_1 level_2  level_3 level_4  ID Name  num  bibi
# 0        0      cb        0     NaN   1    A   50  <NA>
# 1        0      cb        1     NaN   2    A   68  <NA>
# 2        1      cb        0     NaN   1    A   50  <NA>
# 3        1      cb        1     NaN   4    A   67  <NA>
# 4        2      cb        0     NaN   1    A   50  <NA>
# 5        2      cb        1    bubu   6    A   67     3

d4 = {
    "critic_reviews": [
        {"review_critic": "XYZ", "review_score": 90},
        {"review_critic": "ABC", "review_score": 90},
        {"review_critic": "123", "review_score": 90},
    ],
    "genres": ["Sports", "Golf"],
    "score": 85,
    "title": "Golf Simulator",
    "url": "http://example.com/golf-simulator",
}

df44 = nestediter2df(d4)
print(df44.to_string())

#           level_1  level_2 review_critic  review_score       0     1  score           title                                url
# 0  critic_reviews        0           XYZ            90     NaN   NaN   <NA>             NaN                                NaN
# 1  critic_reviews        1           ABC            90     NaN   NaN   <NA>             NaN                                NaN
# 2  critic_reviews        2           123            90     NaN   NaN   <NA>             NaN                                NaN
# 3          genres     <NA>          <NA>          <NA>  Sports  Golf   <NA>             NaN                                NaN
# 4            <NA>     <NA>          <NA>          <NA>     NaN   NaN     85  Golf Simulator  http://example.com/golf-simulator

d5 = {
    "c1": {
        "application_contacts": {"adress": "X", "email": "test@test.com"},
        "application_details": {"email": None, "phone": None},
        "employer": {"Name": "Nom", "email": "bibi@baba.com"},
        "id": "1",
    },
    "c2": {
        "application_contacts": {"adress": "Z", "email": None},
        "application_details": {"email": "testy@test_a.com", "phone": None},
        "employer": {"Name": "Nom", "email": None},
        "id": "2",
    },
    "c3": {
        "application_contacts": {"adress": "Y", "email": None},
        "application_details": {"email": "testy@test_a.com", "phone": None},
        "employer": {"Name": "Nom", "email": None},
        "id": "3",
    },
}

df55 = nestediter2df(d5)
print(df55.to_string())

#    level_1               level_2 adress             email phone Name    id
# 0       c1  application_contacts      X     test@test.com  <NA>  NaN  <NA>
# 1       c1   application_details   <NA>              <NA>  <NA>  NaN  <NA>
# 2       c1              employer   <NA>     bibi@baba.com  <NA>  Nom  <NA>
# 3       c1                  <NA>   <NA>              <NA>  <NA>  NaN     1
# 4       c2  application_contacts      Z              <NA>  <NA>  NaN  <NA>
# 5       c2   application_details   <NA>  testy@test_a.com  <NA>  NaN  <NA>
# 6       c2              employer   <NA>              <NA>  <NA>  Nom  <NA>
# 7       c2                  <NA>   <NA>              <NA>  <NA>  NaN     2
# 8       c3  application_contacts      Y              <NA>  <NA>  NaN  <NA>
# 9       c3   application_details   <NA>  testy@test_a.com  <NA>  NaN  <NA>
# 10      c3              employer   <NA>              <NA>  <NA>  Nom  <NA>
# 11      c3                  <NA>   <NA>              <NA>  <NA>  NaN     3

d6 = {
    "departure": [
        {
            "actual": None,
            "actual_runway": None,
            "airport": "Findel",
            "delay": None,
            "estimated": "2020-07-07T06:30:00+00:00",
            "estimated_runway": None,
            "gate": None,
            "iata": "LUX",
            "icao": "ELLX",
            "scheduled": "2020-07-07T06:30:00+00:00",
            "terminal": None,
            "timezone": "Europe/Luxembourg",
        },
        {
            "actual": None,
            "actual_runway": None,
            "airport": "Findel",
            "delay": None,
            "estimated": "2020-07-07T06:30:00+00:00",
            "estimated_runway": None,
            "gate": None,
            "iata": "LUX",
            "icao": "ELLX",
            "scheduled": "2020-07-07T06:30:00+00:00",
            "terminal": None,
            "timezone": "Europe/Luxembourg",
        },
        {
            "actual": None,
            "actual_runway": None,
            "airport": "Findel",
            "delay": None,
            "estimated": "2020-07-07T06:30:00+00:00",
            "estimated_runway": None,
            "gate": None,
            "iata": "LUX",
            "icao": "ELLX",
            "scheduled": "2020-07-07T06:30:00+00:00",
            "terminal": None,
            "timezone": "Europe/Luxembourg",
        },
    ]
}


df66 = nestediter2df(d6)
print(df66.to_string())

#      level_1  level_2 actual actual_runway airport delay                  estimated estimated_runway  gate iata  icao                  scheduled terminal           timezone
# 0  departure        0   <NA>          <NA>  Findel  <NA>  2020-07-07T06:30:00+00:00             <NA>  <NA>  LUX  ELLX  2020-07-07T06:30:00+00:00     <NA>  Europe/Luxembourg
# 1  departure        1   <NA>          <NA>  Findel  <NA>  2020-07-07T06:30:00+00:00             <NA>  <NA>  LUX  ELLX  2020-07-07T06:30:00+00:00     <NA>  Europe/Luxembourg
# 2  departure        2   <NA>          <NA>  Findel  <NA>  2020-07-07T06:30:00+00:00             <NA>  <NA>  LUX  ELLX  2020-07-07T06:30:00+00:00     <NA>  Europe/Luxembourg

```