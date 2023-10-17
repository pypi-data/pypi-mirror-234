import setuptools

# COMMAND ----------

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read() 
    
setuptools.setup(
    name="dp-ai-data-harmonization",
    version="1.0.2",
    author="Himanshu",
    author_email="himanshu.tomar@decisionpoint.in",
    description="Create data quality rules and apply them to datasets.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    py_modules=['utility'],
    packages=['api','api.mapper','api.mapper.algos'],
     
    classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
    ],
    install_requires=['openai','pandas','fuzzywuzzy','stringmetric','rapidfuzz','IPython','textdistance','django'],
    python_requires='>=3.8',
)