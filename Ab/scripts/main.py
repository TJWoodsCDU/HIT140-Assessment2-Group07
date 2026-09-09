import os
os.chdir(os.path.dirname(__file__))
 
os.system("python data_wrangling.py")
os.system("python sampling.py")
os.system("python descriptive_stats.py")
os.system("python confidence_interval.py")
os.system("python hypothesis_test.py")
 